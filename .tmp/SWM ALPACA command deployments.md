spxlaucms0001:~ # grep "HANA BACKUP FILE" /opt/PMS/scr/type_5/*
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:# @version      1.2 2023-07-27 changed HANA BACKUP FILE to HANA BACKUP FILE DAILY for uniqness
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:# HANA BACKUP FILE DAILY
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:func_check_cmd "HANA BACKUP FILE DAILY" && $CMD -c COMMAND_CREATE -SYS_NAME ${SID} -CMD_DESCR "BKP: HANA db dump file backint"\
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh: -INFO_TXT "HANA BACKUP FILE DAILY" -AGENT_DESCR localhost -PARAM "-s ${SID} -d <BKP_DATA_DEST1> -r - -b $LOCAL_FILE_RET\
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:# HANA BACKUP FILE MONTHLY
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:func_check_cmd "HANA BACKUP FILE MONTHLY" && $CMD -c COMMAND_CREATE -SYS_NAME ${SID} -CMD_DESCR "BKP: HANA db dump file backint"\
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh: -INFO_TXT "HANA BACKUP FILE MONTHLY" -AGENT_DESCR localhost -PARAM "-s ${SID} -d <BKP_DATA_DEST1_MONTHLY> -r -\
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:# HANA BACKUP FILE YEARLY
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh:func_check_cmd "HANA BACKUP FILE YEARLY" && $CMD -c COMMAND_CREATE -SYS_NAME ${SID} -CMD_DESCR "BKP: HANA db dump file backint"\
/opt/PMS/scr/type_5/PMS_cz_prep_hana_nw.sh: -INFO_TXT "HANA BACKUP FILE YEARLY" -AGENT_DESCR localhost -PARAM "-s ${SID} -d <BKP_DATA_DEST1_YEARLY> -r -\


func_set_values()
{
case $SLA in
        1)
        LOCAL_FILE_RET="<CZ_LOCAL_FILE_RET_CLASS_1>"
        LOCAL_SNAP_RET="<CZ_LOCAL_SNAP_RET_CLASS_1>"
        LOCAL_LOG_RET="<CZ_LOCAL_LOG_RET_CLASS_1>"
        BLOB_LOG_RET="<CZ_BLOB_LOG_RET_CLASS_1>"
        BLOB_FILE_RET="<CZ_BLOB_FILE_RET_CLASS_1>"
        BLOB_FILE_RET_MONTHLY="<CZ_BLOB_FILE_RET_MONTHLY_CLASS_1>"
        BLOB_FILE_RET_YEARLY="<CZ_BLOB_FILE_RET_YEARLY_CLASS_1>"
        ;;
        2)
        LOCAL_FILE_RET="<CZ_LOCAL_FILE_RET_CLASS_2>"
        LOCAL_SNAP_RET="<CZ_LOCAL_SNAP_RET_CLASS_2>"
        LOCAL_LOG_RET="<CZ_LOCAL_LOG_RET_CLASS_2>"
        BLOB_LOG_RET="<CZ_BLOB_LOG_RET_CLASS_2>"
        BLOB_FILE_RET="<CZ_BLOB_FILE_RET_CLASS_2>"
        BLOB_FILE_RET_MONTHLY="<CZ_BLOB_FILE_RET_MONTHLY_CLASS_2>"
        BLOB_FILE_RET_YEARLY="<CZ_BLOB_FILE_RET_YEARLY_CLASS_2>"
        ;;
        3)
        LOCAL_FILE_RET="<CZ_LOCAL_FILE_RET_CLASS_3>"
        LOCAL_SNAP_RET="<CZ_LOCAL_SNAP_RET_CLASS_3>"
        LOCAL_LOG_RET="<CZ_LOCAL_LOG_RET_CLASS_3>"
        BLOB_LOG_RET="<CZ_BLOB_LOG_RET_CLASS_3>"
        BLOB_FILE_RET="<CZ_BLOB_FILE_RET_CLASS_3>"
        BLOB_FILE_RET_MONTHLY="<CZ_BLOB_FILE_RET_MONTHLY_CLASS_3>"
        BLOB_FILE_RET_YEARLY="<CZ_BLOB_FILE_RET_YEARLY_CLASS_3>"
        ;;
        4)
        LOCAL_FILE_RET="<CZ_LOCAL_FILE_RET_CLASS_4>"
        LOCAL_SNAP_RET="<CZ_LOCAL_SNAP_RET_CLASS_4>"
        LOCAL_LOG_RET="<CZ_LOCAL_LOG_RET_CLASS_4>"
        BLOB_LOG_RET="<CZ_BLOB_LOG_RET_CLASS_4>"
        BLOB_FILE_RET="<CZ_BLOB_FILE_RET_CLASS_4>"
        BLOB_FILE_RET_MONTHLY="<CZ_BLOB_FILE_RET_MONTHLY_CLASS_4>"
        BLOB_FILE_RET_YEARLY="<CZ_BLOB_FILE_RET_YEARLY_CLASS_4>"
        ;;
        *)
        func_print_comment "Available SLA CLASS 1 | 2 | 3 | 4"
        func_print_usage
        ;;
esac
