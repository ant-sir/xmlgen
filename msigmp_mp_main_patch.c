/******************************************************************
* 版权所有 (C) 2006, 中兴通讯股份有限公司。
*
* 文件名称： msigmp_mp_main.c
* 文件标识：
* 内容摘要： IGMP模块主控板业务处理接口
* 其它说明：
*******************************************************************/

/******************************************************************
 *                           头文件                               *
*******************************************************************/
#include "msctrl_ex.h"
#include "msdatasyn_ex.h"
#include "msmcast_comm.h"
#include "msmcast_msg.h"
#include "msigmp_ctrl.h"

/******************************************************************
 *                           宏定义                               *
*******************************************************************/

/******************************************************************
 *                        全局函数声明                            *
*******************************************************************/
extern INT32S MsIgmp_MpSysInit(INT8U *v_MsCtrlMpInitStru);


/******************************************************************
 *                        静态函数声明                            *
*******************************************************************/

/******************************************************************
 *                          数据类型                              *
*******************************************************************/

/******************************************************************
 *                          全局变量                              *
*******************************************************************/

/******************************************************************
 *                          静态变量                              *
*******************************************************************/

/******************************************************************
 *                          函数实现                              *
*******************************************************************/

/******************************************************************
* 函数名称： MsIgmp_MpSysHandler
* 功能描述： 业务支撑回调入口
*******************************************************************/
INT32S MsIgmp_MpSysHandler_patch(INT32U vSysEvent, INT8U *vpParaIn)
{
    MCAST_SYSHAND_PARA *ParaIn = NULL;
    UINT32 Len = 0;

    if (MSCTRL_INIT == vSysEvent)
    {
        return MsIgmp_MpSysInit(vpParaIn);
    }

    switch (vSysEvent)
    {
        case MSCTRL_SYS_START:
            {
                Len = sizeof(MCAST_SYSHAND_PARA) + sizeof(MSCTRL_SYS_START_STRU);
                ParaIn = Mcast_MemAlloc(Len, 1, IGMP_PROTOCOL_MODE);
                if (NULL == ParaIn)
                {
                    return MSAN_OK;
                }

                memset(ParaIn, 0, Len);
                memmove(ParaIn->ParaIn, vpParaIn, sizeof(MSCTRL_SYS_START_STRU));
            }
            break;
        case MSCTRL_DEL_CARD:
            {
                Len = sizeof(MCAST_SYSHAND_PARA) + sizeof(MSCTRL_ADD_DEL_CARD_STRU);
                ParaIn = Mcast_MemAlloc(Len, 1, IGMP_PROTOCOL_MODE);
                if (NULL == ParaIn)
                {
                    return MSAN_OK;
                }

                memset(ParaIn, 0, Len);
                memmove(ParaIn->ParaIn, vpParaIn, sizeof(MSCTRL_ADD_DEL_CARD_STRU));
            }
            break;
        case MSCTRL_CARD_DOWN:
            {
                Len = sizeof(MCAST_SYSHAND_PARA) + sizeof(MSCTRL_CARD_DOWN_STRU);
                ParaIn = Mcast_MemAlloc(Len, 1, IGMP_PROTOCOL_MODE);
                if (NULL == ParaIn)
                {
                    return MSAN_OK;
                }

                memset(ParaIn, 0, Len);
                memmove(ParaIn->ParaIn, vpParaIn, sizeof(MSCTRL_CARD_DOWN_STRU));
            }
            break;
        case MSIF_DEL_IF:
        case MSCTRL_ROSNG_DEL_IF:
            {
                Len = sizeof(MCAST_SYSHAND_PARA) + sizeof(UINT32);
                ParaIn = Mcast_MemAlloc(Len, 1, IGMP_PROTOCOL_MODE);
                if (NULL == ParaIn)
                {
                    return MSAN_OK;
                }

                memset(ParaIn, 0, Len);
                memmove(ParaIn->ParaIn, vpParaIn, sizeof(UINT32));
            }
            break;
        case MSCTRL_RESOURCEPRF_APPLY:
            {
                Len = sizeof(MCAST_SYSHAND_PARA) + sizeof(MSCTRL_RESOURCEPRF_INFO);
                ParaIn = Mcast_MemAlloc(Len, 1, IGMP_PROTOCOL_MODE);
                if (NULL == ParaIn)
                {
                    return MSAN_OK;
                }

                memset(ParaIn, 0, Len);
                memmove(ParaIn->ParaIn, vpParaIn, sizeof(MSCTRL_RESOURCEPRF_INFO));
            }
            break;
        case MSCTRL_LACP_MEMBER_ADD:
        case MSCTRL_LACP_MEMBER_DEL:
            {
                Len = sizeof(MCAST_SYSHAND_PARA) + sizeof(MSCTRL_LACP_MEMBER_STRU);
                ParaIn = Mcast_MemAlloc(Len, 1, IGMP_PROTOCOL_MODE);
                if (NULL == ParaIn)
                {
                    return MSAN_OK;
                }

                memset(ParaIn, 0, Len);
                memmove(ParaIn->ParaIn, vpParaIn, sizeof(MSCTRL_LACP_MEMBER_STRU));
            }
            break;
        default:
            return MSAN_OK;
    }

    ParaIn->SysEvent = vSysEvent;
    Comm_PostLocal(MSGID_IGMP_SYSTEM_HANDLER, "McastTask", (UINT8 *)ParaIn, (UINT16)Len);
    Mcast_MemFree(ParaIn, IGMP_PROTOCOL_MODE);

    return MSAN_OK;
}

