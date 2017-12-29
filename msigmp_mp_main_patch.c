/******************************************************************
* ��Ȩ���� (C) 2006, ����ͨѶ�ɷ����޹�˾��
*
* �ļ����ƣ� msigmp_mp_main.c
* �ļ���ʶ��
* ����ժҪ�� IGMPģ�����ذ�ҵ����ӿ�
* ����˵����
*******************************************************************/

/******************************************************************
 *                           ͷ�ļ�                               *
*******************************************************************/
#include "msctrl_ex.h"
#include "msdatasyn_ex.h"
#include "msmcast_comm.h"
#include "msmcast_msg.h"
#include "msigmp_ctrl.h"

/******************************************************************
 *                           �궨��                               *
*******************************************************************/

/******************************************************************
 *                        ȫ�ֺ�������                            *
*******************************************************************/
extern INT32S MsIgmp_MpSysInit(INT8U *v_MsCtrlMpInitStru);


/******************************************************************
 *                        ��̬��������                            *
*******************************************************************/

/******************************************************************
 *                          ��������                              *
*******************************************************************/

/******************************************************************
 *                          ȫ�ֱ���                              *
*******************************************************************/

/******************************************************************
 *                          ��̬����                              *
*******************************************************************/

/******************************************************************
 *                          ����ʵ��                              *
*******************************************************************/

/******************************************************************
* �������ƣ� MsIgmp_MpSysHandler
* ���������� ҵ��֧�Żص����
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

