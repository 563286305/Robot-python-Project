*** Settings ***
Library           RequestsLibrary
Library           DatabaseLibrary
Library           SudsLibrary
Library           Selenium2Library
Library           DateTime
Library           MyLibrary/CreateData.py
Library           MyLibrary/ReadWriteExcel.py
Library           MyLibrary/OperaLib.py
Library           MyLibrary/QuerySQL.py
Library           MyLibrary/CreateData.py
Library           MyLibrary/GenBase.py
Library           MyLibrary/GenInputData.py
Library           MyLibrary/RunCase.py
Library           Collections
Resource          运行环境关键字.txt
Resource          各产品结果校验关键字.txt
Library           MyLibrary/Interface.py
Library           MyLibrary/FtpUpDown.py
Library           Contract/Mylibrary/OperateExcel.py
Library           Contract/Mylibrary/QueryDB_RF.py
Library           Contract/Mylibrary/Contract_RF.py

*** Test Cases ***
进件 - 功能测试
    #基本功能    正常条件    正常进件成功
    ${env}    set variable    1
    ${childlist0}    set variable    403    404
    ${childlist1}    set variable    412    413
    ${childlist2}    set variable    415    416
    ${childlist3}    set variable    430    431
    ${childlist4}    set variable    433    434
    ${childlist5}    set variable    439    440    441
    ${childlist6}    set variable    409    410    #${productidlist}    create_list    137
    ...    # 298    379    380    408    # 411    414
    ...    # 417    432    435    436    # 438    442
    ...    # 448    449    450    451    # 455    456
    ...    # 457    ${childlist0}    ${childlist1}    ${childlist2}    # ${childlist3}    ${childlist4}
    ...    # ${childlist5}    ${childlist6}
    #进件
    ${productidlist}    create_list    403
    #${result}    ${sucessList}    case_normal_input    ${env}    ${productidlist}
    ${result}    ${sucessList}    case_term_risk    ${env}    ${productidlist}
    Set Suite Variable    ${sucessList}
    log    ${sucessList}
    #检测进件成功的appid
    ${len}    Get Length    ${sucessList}
    Run Keyword If    ${len}==0    Fatal Error    没有成功的APPID
    ...    ELSE    No Operation

流程初始化配置
    #》》》》》》》》》》    运行环境选择    测试环境 == 1    准生产环境 == 2    联调环境 == 3
    ${envir_choice}    set variable    1
    set suite variable    ${envir_choice}
    ${envir_info}    run keyword if    '${envir_choice}'=='1'    测试环境
    ...    ELSE IF    '${envir_choice}'=='2'    准生产环境
    ...    ELSE IF    '${envir_choice}'=='3'    联调环境
    set suite variable    ${envir_info}
    #指定基础数据存放文件名    ↓↓↓文档名需要重新指定
    make_dir    ..//Case
    ${CurrentDate}    Get Time    year,month,day,hour min sec
    ${CurrentDate}    Catenate    SEPARATOR=    @{CurrentDate}[0]    @{CurrentDate}[1]    @{CurrentDate}[2]    @{CurrentDate}[3]
    ...    @{CurrentDate}[4]    @{CurrentDate}[5]
    ${DataFileName}    Catenate    SEPARATOR=_    Process    ${CurrentDate}.xlsx
    ${DataExcelFile}    Catenate    SEPARATOR=    .//Result//    ${DataFileName}
    set suite variable    ${DataExcelFile}
    #指定基础数据存放sheet名
    set suite variable    ${DataExcelSheet}    Sheet
    #指定自动化测试用例导入文档    ↓↓↓文档名需要重新指定
    ${TemplateFile}    set variable    Process_template.xlsx
    ${TemplateFile}    Catenate    SEPARATOR=    .//Template//    ${TemplateFile}
    set suite variable    ${TemplateFile}
    #合同校验模板sheet名
    Set Suite Variable    ${zhsp_result}    zhsp_result
    Set Suite Variable    ${contractresult}    contractresult
    Set Suite Variable    ${seecontractresult}    seecontractresult
    Set Suite Variable    ${signature_result}    signature_result
    Set Suite Variable    ${fee_result}    fee_result
    Set Suite Variable    ${dsfyysh_result}    dsfyysh_result
    #放款校验模板
    Set Suite Variable    ${piliang_result}    piliang_result
    Set Suite Variable    ${danbi_result}    danbi_result
    Set Suite Variable    ${plan_result}    plan_result
    Set Suite Variable    ${zijin}    zijin
    Set Suite Variable    ${tixian_result}    tixian_result
    #放款类型设置
    Set Suite Variable    ${TRUSTEE_TYPE}    B134001    #B134001    B134002
    Set Suite Variable    ${ACCOUNT_TYPE}    B8010    #B8010    B8002
    #创建基础数据存放Excel文档
    create_excel    ${DataExcelFile}    Sheet
    #************    系统参数配置    ************#
    #页面和接口地址
    set suite variable    ${UserCenterURL}    &{envir_info}[UserCenterURL]    #web页面用户中心
    set suite variable    ${RecordLoanURL}    &{envir_info}[RecordLoanURL]    #进件接口地址
    set suite variable    ${LOGIN URL}    &{envir_info}[loginURL]    #web页面地址
    set suite variable    ${BROWSER}    &{envir_info}[BROWSER]    #设置浏览器
    Set Suite Variable    ${url}    &{envir_info}[url]    #提现回盘接口
    Set Suite Variable    ${ip}    &{envir_info}[ip]    #合同接口地址
    Set Suite Variable    ${dainziqianzhang}    &{envir_info}[dainziqianzhang]    #电子签章地址
    #设置数据库信息
    set suite variable    ${user}    &{envir_info}[sql_usr]
    set suite variable    ${password}    &{envir_info}[sql_psw]
    set suite variable    ${sql_port}    &{envir_info}[sql_port]
    set suite variable    ${host}    127.0.0.1
    #SSH配置信息
    set suite variable    ${ssh_host}    &{envir_info}[ssh_host]
    set suite variable    ${ssh_name}    &{envir_info}[ssh_usr]
    set suite variable    ${ssh_psw}    &{envir_info}[ssh_psw]
    set suite variable    ${rds_addr}    &{envir_info}[sql_addr]
    #设置数据库信息
    set suite variable    ${loan_db}    &{envir_info}[loan_db]
    set suite variable    ${base_db}    &{envir_info}[base_db]
    #web帐号
    Set Suite Variable    ${web_user}    &{envir_info}[web_user]
    Set Suite Variable    ${web_password}    &{envir_info}[web_password]

综合审批
    #读取APPID
    ${statussuccess}    Create List
    ${zhsp_success}    Create List
    ${zhsp_fail}    Create List
    ${plus}    set variable    1
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${zhsp_result}    ${zhsp_result}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0206    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS"    Append To List    ${statussuccess}    ${APPID}
    : FOR    ${APPID}    IN    @{statussuccess}
    \    ${result}    Run Keyword And Continue On Failure    信审综审判断    ${loan_db}    ${APPID}
    \    Run Keyword If    '''${result}'''=='''True''' or '''${result}'''=='''wu'''    Append To List    ${zhsp_success}    ${APPID}
    \    ...    ELSE    Append To List    ${zhsp_fail}    ${APPID}
    \    Continue For Loop If    '''${result}'''=='''wu'''
    \    ${jieguo}    Set Variable If    '''${result}'''=='''True'''    PASS    FAIL
    \    @{finally_result}    Create List    ${APPID}    ${jieguo}
    \    ${plus}    plusPlus    ${plus}
    \    List Add Excel    ${DataExcelFile}    ${zhsp_result}    ${plus}    1    @{finally_result}
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${zhsp_fail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${zhsp_success}
    log    ${zhsp_success}

生成合同
    #读取APPID
    #@{sucessList}    Create List    926656508
    ${plus}    set variable    1
    ${generatesuccess}    Create List
    ${generate_fail}    Create List
    ${statussuccess}    Create List
    #链接base和loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[base_db]
    ${server2}    ${con}    ${port2}    connectdb    ${envir_info}
    connDB    ${base_db}    ${user}    ${password}    ${host}    ${port2}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${contractresult}    ${contractresult}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #如果是测试环境需要更改工单状态
    \    Run Keyword If    "${envir_choice}"=="1"    inf_channel    ${APPID}    ${ProductIDAssign}
    \    sleep    3
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0220    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS"    Append To List    ${statussuccess}    ${APPID}
    #遍历appid，走流程
    : FOR    ${APPID}    IN    @{statussuccess}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #生成合同
    \    ${returnCode}    ${returnMsg}    Run Keyword And Continue On Failure    生成合同    ${APPID}
    \    ${resultCode}    Set Variable If    '''${returnCode}'''=='''000'''    PASS    FAIL
    \    @{resultlist}    Run Keyword If    '''${returnCode}'''=='''000'''    Run Keyword And Continue On Failure    生成合同结果校验    ${base_db}
    \    ...    ${loan_db}    ${ProductIDAssign}    ${APPID}
    \    Run Keyword If    '''${returnCode}'''=='''000'''    Append To List    ${generatesuccess}    ${APPID}
    \    ...    ELSE    Append To List    ${generate_fail}    ${APPID}
    \    @{result}    Create List    ${APPID}    ${returnCode}    ${returnMsg}    ${resultCode}
    \    ...    @{resultlist}
    \    ${plus}    plusPlus    ${plus}
    \    listAddExcel    ${DataExcelFile}    ${contractresult}    ${plus}    1    @{result}
    stopssh    ${server1}
    stopssh    ${server2}
    Disconnect From Database
    ${len}    Get Length    ${generate_fail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${generatesuccess}
    log    ${generatesuccess}

查看合同
    ${plus}    set variable    1
    ${seesuccess}    Create List
    ${seefail}    Create List
    ${statussuccess}    Create List
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${seecontractresult}    ${seecontractresult}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0222    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS"    Append To List    ${statussuccess}    ${APPID}
    #遍历appid，走流程
    : FOR    ${APPID}    IN    @{statussuccess}
    \    ${returnCode}    ${returnMsg}    Run Keyword And Continue On Failure    查看合同    ${APPID}
    \    ${resultCode}    Set Variable If    '''${returnCode}'''=='''000'''    PASS    FAIL
    \    ${app_status}    ${result_app_status}    Run Keyword If    '''${returnCode}'''=='''000'''    工单状态_APP_STATUS    ${APPID}
    \    ...    F0223    ${loan_db}
    \    Run Keyword If    '''${returnCode}'''=='''000'''    Append To List    ${seesuccess}    ${APPID}
    \    ...    ELSE    Append To List    ${seefail}    ${APPID}
    \    @{result}    Create List    ${APPID}    ${returnCode}    ${returnMsg}    ${resultCode}
    \    ...    ${app_status}    ${result_app_status}
    \    ${plus}    plusPlus    ${plus}
    \    List Add Excel    ${DataExcelFile}    ${seecontractresult}    ${plus}    1    @{result}
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${seefail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${seesuccess}
    log    ${seesuccess}

电子签章
    #@{sucessList}    Create List    926655169
    ${plus}    set variable    1
    ${signaturesuccess}    Create List
    ${statussuccess}    Create List
    ${signaturefail}    Create List
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${signature_result}    ${signature_result}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0223    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS"    Append To List    ${statussuccess}    ${APPID}
    #遍历appid，走流程
    : FOR    ${APPID}    IN    @{statussuccess}
    \    log    ${APPID}
    \    log    ${dainziqianzhang}
    \    ${returnCode}    ${returnMsg}    Run Keyword And Continue On Failure    电子签章    ${dainziqianzhang}    ${APPID}
    \    ${resultCode}    Set Variable If    '''${returnCode}'''=='''000000'''    PASS    FAIL
    \    Run Keyword If    '''${returnCode}'''=='''000000'''    Append To List    ${signaturesuccess}    ${APPID}
    \    ...    ELSE    Append To List    ${signaturefail}    ${APPID}
    \    #检测签章后状态，F0230或者F0225都可以
    \    sleep    5
    \    ${app_status}    ${result_app_status}    工单状态_APP_STATUS    ${APPID}    F0230    ${loan_db}
    \    Log Many    ${app_status}    ${result_app_status}
    \    ${app_status}    ${result_app_status}    Run Keyword If    "${result_app_status}"=="FAIL"    工单状态_APP_STATUS    ${APPID}
    \    ...    F0225    ${loan_db}
    \    ...    ELSE    Set Variable    ${app_status}    ${result_app_status}
    \    Log Many    ${app_status}    ${result_app_status}
    \    #@{check_result}    Run Keyword If    '''${returnCode}'''=='''000000'''    Run Keyword And Continue On Failure    电子签章结果校验    ${loan_db}
    \    ...    # ${APPID}
    \    @{result}    Create List    ${APPID}    ${returnCode}    ${returnMsg}    ${resultCode}
    \    ...    ${app_status}    ${result_app_status}
    \    ${plus}    plusPlus    ${plus}
    \    List Add Excel    ${DataExcelFile}    ${signature_result}    ${plus}    1    @{result}
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${signaturefail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${signaturesuccess}
    log    ${signaturesuccess}

第三方运营审核
    ${dsfyysh_success}    Create List
    ${plus}    set variable    1
    #${sucessList}    Create List    926671083    926671084
    ${statussuccess}    Create List
    ${dsfyysh_fail}    Create List
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${dsfyysh_result}    ${dsfyysh_result}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0225    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS"    Append To List    ${statussuccess}    ${APPID}
    log    ${statussuccess}
    登录    ${web_user}    ${web_password}
    #选择菜单    span520    span520032
    选择菜单    span521    span521004
    #遍历appid，走流程
    : FOR    ${APPID}    IN    @{statussuccess}
    \    ${result}    Run Keyword And Continue On Failure    第三方运营审核新    ${APPID}
    \    选择二级菜单    span521004
    \    Run Keyword If    '''${result}'''=='''True'''    Append To List    ${dsfyysh_success}    ${APPID}
    \    ...    ELSE    Append To List    ${dsfyysh_fail}    ${APPID}
    \    ${jieguo}    Set Variable If    '''${result}'''=='''True'''    PASS    FAIL
    \    ${app_status}    ${result_app_status}    Run Keyword If    '''${result}'''=='''True'''    工单状态_APP_STATUS    ${APPID}
    \    ...    F0230    ${loan_db}
    \    @{finally_result}    Create List    ${APPID}    ${jieguo}    ${app_status}    ${result_app_status}
    \    ${plus}    plusPlus    ${plus}
    \    List Add Excel    ${DataExcelFile}    ${dsfyysh_result}    ${plus}    1    @{finally_result}
    关闭浏览器
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${dsfyysh_fail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${dsfyysh_success}
    log    ${dsfyysh_success}

债匹
    @{fangkuan}    Set Variable    ${signaturesuccess}
    ${statussuccess}    Create List
    ${zhaipisuccess}    Create List
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0230    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS"    Append To List    ${statussuccess}    ${APPID}
    #遍历appid，走流程
    : FOR    ${APPID}    IN    @{statussuccess}
    \    Run Keyword And Continue On Failure    更新工单状态    ${loan_db}    ${APPID}    ${TRUSTEE_TYPE}    ${ACCOUNT_TYPE}
    \    Append To List    ${zhaipisuccess}    ${APPID}
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${zhaipisuccess}
    Run Keyword If    ${len}==0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${zhaipisuccess}
    log    ${zhaipisuccess}

存管批量放款
    ${loan_success}    Create List
    ${statussuccess}    Create List
    ${loan_fail}    Create List    #@{sucessList}    Create List    926670826    926670827    926670828
    ...    # 926670829    926670830    # 926670831
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0240    ${loan_db}
    \    Run Keyword If    "${c}"=="PASS" and "${TRUSTEE_TYPE}"=="B134001"    Append To List    ${statussuccess}    ${APPID}
    登录    ${web_user}    ${web_password}
    选择菜单    span521    span521006
    : FOR    ${APPID}    IN    @{statussuccess}
    \    ${result}    Run Keyword And Continue On Failure    批量放款    ${APPID}    ${ACCOUNT_TYPE}
    \    Run Keyword If    '''${result}'''=='''True'''    Append To List    ${loan_success}    ${APPID}
    \    ...    ELSE    Append To List    ${loan_fail}    ${APPID}
    关闭浏览器
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${loan_fail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${loan_success}
    log    ${loan_success}

存管批量回盘
    ${huipan_success}    Create List
    ${huipan_fail}    Create List
    ${plus}    set variable    1
    #@{loan_success}    Create List    926656563
    @{fangkuan}    Set Variable    ${loan_success}
    #链接loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${piliang_result}    ${piliang_result}
    #造回盘文件
    : FOR    ${APPID}    IN    @{fangkuan}
    \    Run Keyword And Continue On Failure    查询放款报盘文件    ${loan_db}    ${APPID}
    #回盘
    登录    ${web_user}    ${web_password}
    选择菜单    span521    span521009
    : FOR    ${APPID}    IN    @{fangkuan}
    \    ${BATCH_SEQ}    查询放款批次号    ${loan_db}    ${APPID}
    \    ${result}    Run Keyword And Continue On Failure    放款回盘    ${BATCH_SEQ}
    \    Run Keyword If    '''${result}'''=='''True'''    Append To List    ${huipan_success}    ${APPID}
    \    ...    ELSE    Append To List    ${huipan_fail}    ${APPID}
    \    ${a}    Set Variable If    '''${result}'''=='''True'''    PASS    FAIL
    \    @{check_result}    Run Keyword If    '''${result}'''=='''True'''    Run Keyword And Continue On Failure    放款结果校验    ${loan_db}
    \    ...    ${APPID}
    \    @{batch_result}    Run Keyword If    '''${result}'''=='''True'''    Run Keyword And Continue On Failure    批次表信息核对    ${loan_db}
    \    ...    ${APPID}
    \    @{finally_result}    Run Keyword If    '''${result}'''=='''True'''    Create List    ${APPID}    ${a}
    \    ...    @{check_result}    @{batch_result}
    \    ...    ELSE    Create List    ${APPID}    ${a}
    \    ${plus}    plusPlus    ${plus}
    \    listAddExcel    ${DataExcelFile}    ${piliang_result}    ${plus}    1    @{finally_result}
    关闭浏览器
    stopssh    ${server1}
    Disconnect From Database
    ${len}    Get Length    ${huipan_fail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
    Set Suite Variable    ${huipan_success}
    log    ${huipan_success}

合同生成器
    #说明    env_1--测试环境    env_2--准生产环境    env_3--联调环境
    log    ${loan_success}
    @{fangkuan}    Set Variable    ${loan_success}
    Contract_Check    env_1    @{fangkuan}

放款资金流校验
    ${row_number}    set variable    2
    @{zjin_check}    Set Variable    ${huipan_success}
    #@{zjin_check}    Create List    926648738    926645286    926648718
    #链接base和loan库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[base_db]
    ${server2}    ${con}    ${port2}    connectdb    ${envir_info}
    connDB    ${base_db}    ${user}    ${password}    ${host}    ${port2}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${zijin}    ${zijin}
    : FOR    ${APPID}    IN    @{zjin_check}
    \    Run Keyword And Continue On Failure    资金流校验    ${base_db}    ${loan_db}    ${APPID}    ${DataExcelFile}
    \    ...    ${zijin}    ${row_number}
    \    ${number}    查询配置条数    ${base_db}    ${loan_db}    ${APPID}
    \    ${row_number}    Evaluate    ${row_number}+${number}
    stopssh    ${server1}
    stopssh    ${server2}
    Disconnect From Database
    log    ${zjin_check}

提现
    ${tixian_success}    Create List
    ${tixian2_success}    Create List
    ${tixian2_fail}    Create List
    ${statussuccess}    Create List
    ${plus}    set variable    1
    #链接loan,base库
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[loan_db]
    ${server1}    ${con}    ${port1}    connectdb    ${envir_info}
    connDB    ${loan_db}    ${user}    ${password}    ${host}    ${port1}
    Set To Dictionary    ${envir_info}    dbname=&{envir_info}[base_db]
    ${server2}    ${con}    ${port2}    connectdb    ${envir_info}
    connDB    ${base_db}    ${user}    ${password}    ${host}    ${port2}
    #拷贝结果excel
    copysheet    ${TemplateFile}    ${DataExcelFile}    ${tixian_result}    ${tixian_result}
    #遍历appid,过滤符合条件的工单
    : FOR    ${APPID}    IN    @{sucessList}
    \    #根据appid获取productid
    \    ${a}    Query    SELECT PRODUCT_ID FROM ${loan_db}.t_lon_application WHERE APP_ID=${APPID}
    \    ${ProductIDAssign}    Set Variable    ${a[0][0]}
    \    #判断工单状态
    \    ${b}    ${c}    工单状态_APP_STATUS    ${APPID}    F0243    ${loan_db}
    \    #判断是否提现
    \    ${e}    Query    SELECT LOAN_TYPE FROM ${base_db}.t_prd_loan_withdraw WHERE PRODUCT_ID=${ProductIDAssign}
    \    log    ${e}
    \    ${loan_type}    Run Keyword If    "${e}"!="()"    Set Variable    ${e[0][0]}
    \    ...    ELSE    Set Variable    ${e}
    \    log    ${loan_type}
    \    Run Keyword If    "${c}"=="PASS" and "${TRUSTEE_TYPE}"=="B134001" and "${loan_type}"=="B134001"    Append To List    ${statussuccess}    ${APPID}
    登录    ${web_user}    ${web_password}
    选择菜单    span521    span521018
    定时器触发    创建放款成功后的任务    46
    选择二级菜单    span521019
    : FOR    ${APPID}    IN    @{statussuccess}
    \    ${result}    Run Keyword And Continue On Failure    提现    ${APPID}
    \    Run Keyword If    '''${result}'''=='''True'''    Append To List    ${tixian_success}    ${APPID}
    @{tixian1_success}    Set Variable    ${tixian_success}
    : FOR    ${APPID}    IN    @{tixian1_success}
    \    ${TRANS_NO}    查询提现流水号    ${loan_db}    ${APPID}
    \    ${result1}    Run Keyword And Continue On Failure    提现回盘    ${url}    ${TRANS_NO}
    \    Run Keyword If    '''${result1}'''=='''True'''    Append To List    ${tixian2_success}    ${APPID}
    \    ...    ELSE    Append To List    ${tixian2_fail}    ${APPID}
    选择二级菜单    span521018
    定时器触发    执行存管单笔任务    59
    关闭浏览器
    sleep    2
    @{tixian3_success}    Set Variable    ${tixian2_success}
    : FOR    ${APPID}    IN    @{statussuccess}
    \    ${status_result}    Run Keyword And Continue On Failure    查询提现交易状态    ${loan_db}    ${APPID}
    \    ${jieguo}    Set Variable If    '''${status_result}'''=='''S'''    PASS    FAIL
    \    @{check_result}    Run Keyword If    '''${status_result}'''=='''S'''    Run Keyword And Continue On Failure    提现结果校验    ${base_db}
    \    ...    ${loan_db}    ${APPID}
    \    @{finally_result}    Run Keyword If    '''${status_result}'''=='''S'''    Create List    ${APPID}    ${jieguo}
    \    ...    @{check_result}
    \    ...    ELSE    Create List    ${APPID}    ${jieguo}
    \    ${plus}    plusPlus    ${plus}
    \    listAddExcel    ${DataExcelFile}    ${tixian_result}    ${plus}    1    @{finally_result}
    stopssh    ${server2}
    stopssh    ${server1}
    Disconnect From Database
    log    ${tixian3_success}
    ${len}    Get Length    ${tixian2_fail}
    Run Keyword If    ${len}!=0    FAIL    没有成功的APPID
    ...    ELSE    No Operation
