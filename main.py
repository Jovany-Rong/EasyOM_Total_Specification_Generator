#!/usr/local/bin python
#-*-coding: utf-8-*-

from os import system, path
from configparser import ConfigParser as cp
from libs.report import *
from time import strftime, localtime, time
import base64
import cx_Oracle as ora

class Prog(object):
    # variables
    version = "1.1"

    author = "Chenfei Jovany Rong"

    configCheck = 0

    ddList = []

    def __init__(self):
        self.__showHead()

        self.__showTutorial()

        self.__configCheck()

        self.__doGenerate()

    def __showHead(self):
        print("EasyOM Total Specification Generator\n")

        print("Version: %s\t\tAuthor: %s\n" % (self.version, self.author))

        print("Powered by Summer Moon Talk Studio, TQM, SEC, GTMAP.\n")

        print("EasyOM Official Site: https://rongchenfei.com/EasyOM/\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")
        
        system("pause")

    def __showTutorial(self):
        print("***Tutorial***\n")

        print("\t1. Check configs in conf/tsg.conf .\n")

        print("\t2. Put all your EasyOM Specification Part files (*.esp) into Input directory.\n")

        print("\t3. Press any key to generate the Total Specification and it will be in Output directory.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __configCheck(self):
        print("***Config Check***\n")

        try:
            conf = cp()

            conf.read("conf/tsg.conf", encoding="utf-8-sig")

            self.configCheck = 1

            self.rptTitle = conf.get("Format", "title")

            self.rptHeader = conf.get("Format", "header")

            self.rptFooter = conf.get("Format", "footer")

            self.province = conf.get("Basic", "province")

            self.city = conf.get("Basic", "city")

            self.district = conf.get("Basic", "district")

            self.person = conf.get("Basic", "person")

            self.tns = conf.get("Database", "tns")

        except Exception:
            self.configCheck = 2

        if self.configCheck == 1:
            print("\tOK.\n")
        else:
            print("\tError.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __doGenerate(self):
        if self.configCheck != 1:
            print("Press any key to EXIT ...")
        else:
            d = self.__checkDir()

            if d:
                d = self.__detectESPs()
                self.__genRpt()
                self.__genOmx()
                self.__genOmz()

                self.__showEnd()


    def __checkDir(self):
        print("***Checking Input Directory***\n")

        if path.exists("Input/"):
            print("\tOK.\n")

            print("@@@@@@@@\n\n@@@@@@@@\n")

            system("pause")

            return True
        
        else:
            print("\tError.\n")

            print("@@@@@@@@\n\n@@@@@@@@\n")

            system("pause")

            return False
        
    def __detectESPs(self):
        ct = 0

        print("***Detecting ESP Files***\n")

        for root, dirs, files in os.walk("Input/"):
            del root
            del dirs

            for file in files:
                if file.endswith(".esp"):
                    ct += 1
                    print("\tESP file %s: %s\n"%(str(ct), file))
                    
                    self.__loadESP(file)
            
            break

        #print(self.ddList)

        print("\tTotally %s ESP file(s) is(are) found.\n"%str(ct))
        
        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __loadESP(self, file):
        dd = dict()

        dd["TotalScore"] = None
        dd["SysScore"] = None
        dd["DbScore"] = None
        dd["TomcatScore"] = None

        print("\t\tLoading file contents ...\n")

        path = "Input/" + file

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        rowList = text.split("\n")

        for row in rowList:
            if " : " in row:
                tList = row.split(" : ")
                dd[tList[0]] = tList[1]

        if dd["TotalScore"] != None:
            if int(float(dd["TotalScore"])) >= 85:
                dd["Evaluation"] = "运行良好"
            elif int(float(dd["TotalScore"])) >= 70:
                dd["Evaluation"] = "运行正常"
            elif int(float(dd["TotalScore"])) >= 50:
                dd["Evaluation"] = "运行基本正常"
            else:
                dd["Evaluation"] = "运行异常"
        else:
            dStatus = input("\t\t---Please choose Status for '%s': (1 for EXCELLENT[Default], 2 for GOOD, 3 for NOT BAD, 4 for TERRIBLE)\n\t\t"%dd["ComputerAlias"])
        
            if dStatus == "2":
                dd["Evaluation"] = "运行正常"
            elif dStatus == "3":
                dd["Evaluation"] = "运行基本正常"
            elif dStatus == "4":
                dd["Evaluation"] = "运行异常"
            else:
                dd["Evaluation"] = "运行良好"

        self.ddList.append(dd)

        print("\n\t\tDone.\n")
    
    def __genRpt(self):
        print("***Generating Total Specification***\n")

        print("\tLoading configurations ...\n")
        report = Report()

        report.changeStarter("title", self.rptTitle)
        report.changeStarter("header", self.rptHeader)

        report.changeFooter("footer", self.rptFooter)

        print("\tDone.\n")

        print("\tLoading Check Result ...\n")
        
        tmp = """
            <table border = "1" style = "text-align: center">        
                <tr>
                    <th style = "background-color: #33CCFF">巡查人</th>
                    <td><< checkPerson >></td>
                    <th style = "background-color: #33CCFF">巡查时间</th>
                    <td><< checkTime >></td>
                </tr>
            </table>
            <table border = "1" style = "text-align: center">        
                <tr>
                    <th style = "background-color: #33CCFF">序号</th>
                    <th style = "background-color: #33CCFF">巡检内容</th>
                    <th style = "background-color: #33CCFF">运行态势</th>
                    <th style = "background-color: #33CCFF">运维评分</th>
                    <th style = "background-color: #33CCFF">CPU使用率</th>
                    <th style = "background-color: #33CCFF">内存使用率</th>
                    <th style = "background-color: #33CCFF">进程数</th>
                </tr>
        """

        checkTime = strftime('%Y-%m-%d',localtime(time()))

        checkPerson = self.person
        
        tmp = tmp.replace("<< checkPerson >>", checkPerson)
        tmp = tmp.replace("<< checkTime >>", checkTime)

        print("\n\t\tDone.\n")

        insCt = 0
        for dd in self.ddList:
            insCt += 1

            tmp = tmp + """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
            </tr>
            """%(str(insCt), dd["ComputerAlias"], dd["Evaluation"], dd["TotalScore"], dd["CPUUsed"], dd["MemoryUsed"], dd["ProcessCount"])
        
        tmp = tmp + """
        </table>
        """

        report.appendHTML(tmp)

        print("\tDone.\n")

        print("\tLoading ESP information ...\n")
        
        report.appendH2("服务器运行情况")

        for dd in self.ddList:
            print("\t\tWriting information of %s ...\n"%(dd["ComputerAlias"]))
            report.appendH3(dd["ComputerAlias"])

            report.appendH4("操作系统信息")
            table = Table()
            table.addHead("架构", "系统版本")
            table.addRow(dd["SystemArchitecture"], dd["OSVersion"])
            report.appendHTML(table.makeTable("操作系统"))
            del table

            report.appendH4("CPU及内存信息")
            table = Table()
            table.addHead("CPU型号", "CPU核数", "CPU核数建议值", "CPU使用率", "CPU使用率建议值", "物理内存", "物理内存建议值", "内存使用率", "内存使用率建议值")
            table.addRow(dd["CPU"], dd["CPUCore"], "大于等于4", dd["CPUUsed"], "低于80%", dd["Memory"], "不低于16384M", dd["MemoryUsed"], "低于80%")
            report.appendHTML(table.makeTable("CPU及内存"))
            del table

            report.appendH4("磁盘空间信息")
            report.appendHTML(dd["hTable_Disk"])

            report.appendH4("软件环境信息")

            table = Table()
            table.addHead("Java", "Python", ".NET")
            table.addRow(dd["JavaEnvironment"], dd["PythonEnvironment"], dd["DotNetEnvironment"])
            report.appendHTML(table.makeTable("开发环境"))
            del table

            table = Table()
            table.addHead("Oracle", "MySQL", "SQL Server")
            table.addRow(dd["OracleEnvironment"], dd["MySQLEnvironment"], dd["SQLServerEnvironment"])
            report.appendHTML(table.makeTable("数据库环境"))
            del table

            table = Table()
            table.addHead("Desktop", "ArcSDE", "Server")
            table.addRow(dd["ArcGISDesktopEnvironment"], dd["ArcSDEEnvironment"], dd["ArcGISServerEnvironment"])
            report.appendHTML(table.makeTable("ArcGIS环境"))
            del table

            report.appendH4("进程信息")
            report.appendParagraph("该计算机共包含%s个进程。"%dd["ProcessCount"])

            report.appendH4("问题与建议")
            if dd["Advice"] != "":
                advice = dd["Advice"].rstrip(";")
                advice = advice + "。"
            else:
                advice = "无。"

            report.appendParagraph(advice)

            print("\t\tDone.\n")
        
        report.appendH2("数据库运行情况")

        print("\t\tWriting information of database(s) ...\n")

        for dd in self.ddList:
            try:
                if dd["DatabaseConnectionStatus"] == "Success":
                    report.appendH3(dd["DatabaseConnection"])

                    report.appendH4("基本信息")
                    report.appendParagraph(dd["DatabaseVersion"])

                    report.appendH4("实例信息")
                    report.appendHTML(dd["hTable_DatabaseInstance"])
                    report.appendParagraph("数据库共包含%s个实例。"%dd["DatabaseInstanceCount"])

                    report.appendH4("日志信息")
                    report.appendHTML(dd["hTable_DatabaseLog"])
                    report.appendParagraph("数据库共包含%s个日志。"%dd["DatabaseLogCount"])

                    report.appendH4("表空间信息")
                    report.appendHTML(dd["hTable_DatabaseTablespace"])
                    report.appendParagraph("数据库共包含%s个表空间。"%dd["DatabaseTablespaceCount"])

                    report.appendH4("表空间使用信息")
                    report.appendHTML(dd["hTable_DatabaseTablespaceUtilization"])

                    report.appendH4("数据文件自扩展信息")
                    report.appendHTML(dd["hTable_DatabaseFileAutoExtension"])

                    report.appendH4("无效对象信息")
                    report.appendHTML(dd["hTable_DatabaseInvalidObject"])
                    report.appendParagraph("数据库共包含%s个无效对象。"%dd["DatabaseInvalidObjectCount"])

                    report.appendH4("资源限制信息")
                    report.appendHTML(dd["hTable_DatabaseResourceLimit"])
                    report.appendParagraph("数据库共包含%s个资源限制。"%dd["DatabaseResourceLimitCount"])

                    report.appendH4("会话信息")
                    report.appendHTML(dd["hTable_DatabaseSession"])
                    report.appendParagraph("数据库共包含%s个会话。"%dd["DatabaseSessionCount"])
                
                    report.appendH4("异常扩展信息")
                    if dd["DatabaseAbnormalExtensionCount"] != "0":
                        report.appendHTML(dd["hTable_DatabaseAbnormalExtension"])
                    report.appendParagraph("数据库共包含%s个异常扩展。"%dd["DatabaseAbnormalExtensionCount"])

                    report.appendH4("SYSTEM表空间对象所有者异常信息")
                    if dd["DatabaseAbnormalObjectOwnerCount"] != "0":
                        report.appendHTML(dd["hTable_DatabaseAbnormalObjectOwner"])
                    report.appendParagraph("数据库共包含%s个SYSTEM表空间对象所有者异常。"%dd["DatabaseAbnormalObjectOwnerCount"])

                    report.appendH4("长时间执行SQL信息")
                    if dd["DatabaseLongExecutedSQLCount"] != "0":
                        report.appendHTML(dd["hTable_DatabaseLongExecutedSQL"])
                    report.appendParagraph("数据库共包含%s个长时间执行SQL。"%dd["DatabaseLongExecutedSQLCount"])
            except:
                pass

        print("\t\tDone.\n")

        report.appendH2("Tomcat运行情况")

        print("\t\tWriting information of Tomcat(s) ...\n")

        for dd in self.ddList:
            try:
                if dd["TomcatConnectionStatus"] == "Success":
                    report.appendH3(dd["TomcatConnection"])

                    report.appendH4("应用信息")
                    report.appendHTML(dd["hTable_Application"])
                    report.appendParagraph("Tomcat共包含%s个应用。" % dd["ApplicationCount"])

                    report.appendH4("JVM信息")
                    report.appendHTML(dd["hTable_JVMMemory"])

                    report.appendH4("响应时间")
                    report.appendParagraph("Tomcat连接响应时间为%s秒。" % dd["ResponseTime"])
            except:
                pass

        report.makeRpt("%s_%s_%s" % (self.province, self.city, self.district))

        try:
            sql = ""
            for dd in self.ddList:
                #print(dd)
                alias = dd["ComputerAlias"]
                chkTime = dd["CheckFinishTime"]
                architecture = dd["SystemArchitecture"]
                os_version = dd["OSVersion"]
                cpu = dd["CPU"]
                memory = dd["Memory"]
                ipv4 = dd["IPv4"]
                mac = dd["MacAddress"]
                disk_count = dd["DiskCount"]
                java = dd["JavaEnvironment"]
                python = dd["PythonEnvironment"]
                dot_net = dd["DotNetEnvironment"]
                oracle = dd["OracleEnvironment"]
                mysql = dd["MySQLEnvironment"]
                sql_server = dd["SQLServerEnvironment"]
                desktop = dd["ArcGISDesktopEnvironment"]
                sde = dd["ArcSDEEnvironment"]
                gis_server = dd["ArcGISServerEnvironment"]
                proc_count = dd["ProcessCount"]

                try:
                    sql = """
                    insert into om_jbxx
                    values (
                        '%s', to_date('%s', 'yyyy-mm-dd hh24:mi:ss'), to_date('%s', 'yyyy-mm-dd hh24:mi:ss'), 
                        '%s', '%s', '%s', '%s', '%s', 
                        '%s', %s, '%s', '%s', '%s', 
                        '%s', '%s', '%s', '%s', '%s', '%s', 
                        %s
                    )
                    """ % (
                        alias, chkTime, chkTime, 
                        architecture, os_version, cpu, memory, ipv4, 
                        mac, disk_count, java, python, dot_net, 
                        oracle, mysql, sql_server, desktop, sde, gis_server, 
                        proc_count
                    )
                    
                    print(sql)
                    db = ora.connect(self.tns)
                    cr = db.cursor()
                    cr.execute(sql)
                    db.commit()
                    cr.close()
                    db.close()
                except:
                    sql = """
                    update om_jbxx
                    set update_time = to_date('%s', 'yyyy-mm-dd hh24:mi:ss'), 
                    architecture = '%s', 
                    os_version = '%s', 
                    cpu = '%s', 
                    memory = '%s', 
                    ipv4 = '%s', 
                    mac = '%s', 
                    disk_count = %s, 
                    java = '%s', 
                    python = '%s', 
                    dot_net = '%s', 
                    oracle = '%s', 
                    mysql = '%s', 
                    sql_server = '%s', 
                    desktop = '%s', 
                    sde = '%s', 
                    gis_server = '%s', 
                    proc_count = %s
                    where alias = '%s'
                    """ % (
                        chkTime, architecture, os_version, cpu, memory, ipv4, 
                        mac, disk_count, java, python, dot_net, 
                        oracle, mysql, sql_server, desktop, sde, gis_server, 
                        proc_count, alias
                    )
                    print(sql)
                    db = ora.connect(self.tns)
                    cr = db.cursor()
                    cr.execute(sql)
                    db.commit()
                    cr.close()
                    db.close()

            
            print("\tCommit success.\n")

        except Exception as e:
            print("\tCommit failed. Error: %s\nSQL: %s\n" % (str(e), sql))

        try:
            sql = ""
            for dd in self.ddList:
                tns = dd["DatabaseConnection"]
                chkTime = dd["CheckFinishTime"]
                version = dd["DatabaseVersion"]
                instance_count = dd["DatabaseInstanceCount"]
                log_count = dd["DatabaseLogCount"]
                tablespace_count = dd["DatabaseTablespaceCount"]
                dbf_count = dd["DatabaseFileCount"]
                rbs_count = dd["DatabaseRollbackSegmentCount"]
                resource_limit_count = dd["DatabaseResourceLimitCount"]
                session_count = dd["DatabaseSessionCount"]
                abnormal_ext_count = dd["DatabaseAbnormalExtensionCount"]
                abnormal_owner_count = dd["DatabaseAbnormalObjectOwnerCount"]
                long_sql_count = dd["DatabaseLongExecutedSQLCount"]
                invalid_index_count = dd["DatabaseInvalidIndexCount"]
                invalid_constraint_count = dd["DatabaseInvalidConstraintCount"]
                invalid_trigger_count = dd["DatabaseInvalidTriggerCount"]
                invalid_object_count = dd["DatabaseInvalidObjectCount"]

                try:
                    sql = """
                    insert into om_dbxx
                    values (
                        '%s', to_date('%s', 'yyyy-mm-dd hh24:mi:ss'), to_date('%s', 'yyyy-mm-dd hh24:mi:ss'), 
                        '%s', %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s, 
                        %s, %s, %s, %s, %s
                    )
                    """ % (
                        tns, chkTime, chkTime, 
                        version, instance_count, log_count, tablespace_count, dbf_count, 
                        rbs_count, resource_limit_count, session_count, abnormal_ext_count, abnormal_owner_count, 
                        long_sql_count, invalid_index_count, invalid_constraint_count, invalid_trigger_count, invalid_object_count
                    )
                    print(sql)
                    db = ora.connect(self.tns)
                    cr = db.cursor()
                    cr.execute(sql)
                    db.commit()
                    cr.close()
                    db.close()
                except:
                    sql = """
                    update om_dbxx
                    set update_time = to_date('%s', 'yyyy-mm-dd hh24:mi:ss'), 
                    version = '%s', 
                    instance_count = %s, 
                    log_count = %s, 
                    tablespace_count = %s, 
                    dbf_count = %s, 
                    rbs_count = %s, 
                    resource_limit_count = %s, 
                    session_count = %s, 
                    abnormal_ext_count = %s, 
                    abnormal_owner_count = %s, 
                    long_sql_count = %s, 
                    invalid_index_count = %s, 
                    invalid_constraint_count = %s, 
                    invalid_trigger_count = %s, 
                    invalid_object_count = %s
                    where tns = '%s'
                    """ % (
                        chkTime, 
                        version, instance_count, log_count, tablespace_count, dbf_count, 
                        rbs_count, resource_limit_count, session_count, abnormal_ext_count, abnormal_owner_count, 
                        long_sql_count, invalid_index_count, invalid_constraint_count, invalid_trigger_count, invalid_object_count, 
                        tns
                    )
                    print(sql)
                    db = ora.connect(self.tns)
                    cr = db.cursor()
                    cr.execute(sql)
                    db.commit()
                    cr.close()
                    db.close()
            
            print("\tCommit success.\n")

        except Exception as e:
            print("\tCommit failed. Error: %s\nSQL: %s\n" % (str(e), sql))


        print("\tReport generated.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __genOmx(self):
        print("***Generating OMX file***\n")

        temp = ""

        rptTime = localtime(time())
        now = strftime('%Y-%m-%d',rptTime)

        province = self.province

        city = self.city

        district = self.district

        score = 0
        scoreT = 0
        ct = 0

        scoreSys = 0
        scoreSysT = 0
        ctSys = 0

        scoreDb = 0
        scoreDbT = 0
        ctDb = 0

        scoreTomcat = 0
        scoreTomcatT = 0
        ctTomcat = 0

        for dd in self.ddList:
            this = dd["TotalScore"]
            scoreT += int(float(this))
            ct += 1

            this = dd["SysScore"]
            scoreSysT += int(float(this))
            ctSys += 1

            this = dd["DbScore"]
            if this != None:
                scoreDbT += int(float(this))
                ctDb += 1

            this = dd["TomcatScore"]
            if this != None:
                scoreTomcatT += int(float(this))
                ctTomcat += 1

        score = int(scoreT / ct)
        scoreSys = int(scoreSysT / ctSys)
        if ctDb > 0:
            scoreDb = int(scoreDbT / ctDb)
        if ctTomcat > 0:
            scoreTomcat = int(scoreTomcatT / ctTomcat)

        temp = """
        date : %s
        province : %s
        city : %s
        district : %s
        score : %s
        sys_score : %s
        db_score : %s
        tomcat_score : %s
        """ % (now, province, city, district, score, scoreSys, scoreDb, scoreTomcat)

        encTemp = base64.b64encode(temp.encode("utf-8")).decode("utf-8")

        if not os.path.isdir("Output"):
            os.makedirs("Output")

        fileName = "%s_%s_%s_%s.omx" % (province, city, district, now)

        with open("Output/" + fileName, "w+", encoding='utf-8') as f:
            f.write(encTemp)

        print("\tOmx generated.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __genOmz(self):
        print("***Generating OMZ file***\n")

        temp = ""

        rptTime = localtime(time())
        now = strftime('%Y-%m-%d',rptTime)

        province = self.province

        city = self.city

        district = self.district

        temp = """
        date : %s
        province : %s
        city : %s
        district : %s
        ========
        """ % (now, province, city, district)

        sql = """
        select ''''||alias||''', to_date('''||to_char(init_time, 'yyyy-mm-dd hh24:mi:ss')||''', ''yyyy-mm-dd hh24:mi:ss''), to_date('''||
to_char(init_time, 'yyyy-mm-dd hh24:mi:ss')||''', ''yyyy-mm-dd hh24:mi:ss''), '''||architecture||''', '''||os_version||
''', '''||cpu||''', '''||memory||''', '''||ipv4||''', '''||mac||''', '||disk_count||', '''||java||''', '''||python||
''', '''||dot_net||''', '''||oracle||''', '''||mysql||''', '''||sql_server||''', '''||desktop||''', '''||sde||''', '''||
gis_server||''', '||proc_count
from om_jbxx
        """

        try:
            db = ora.connect(self.tns)
            cr = db.cursor()
            cr.execute(sql)
            rows = cr.fetchall()
            cr.close()
            db.close()
            for row in rows:
                temp = temp + str(row[0]) + "\n"
        except Exception as e:
            print(e)
            print(sql)

        temp = temp + """
        ========
        """

        sql = """
        select ''''||warn_level||''', '''||warn_info||''', '''||warn_type||''', '''||warn_host||
''', to_date('''||to_char(warn_time, 'yyyy-mm-dd hh24:mi:ss')||''', ''yyyy-mm-dd hh24:mi:ss'')'
from om_warning
        """

        try:
            db = ora.connect(self.tns)
            cr = db.cursor()
            cr.execute(sql)
            rows = cr.fetchall()
            cr.close()
            db.close()
            for row in rows:
                temp = temp + str(row[0]) + "\n"
        except Exception as e:
            print(e)
            print(sql)

        temp = temp + """
        ========
        """
        
        sql = """
        select to_char(check_time, 'yyyy-mm-dd') rq, alias, 
max(cpu_used) max_cpu, round(avg(cpu_used), 2) avg_cpu, 
max(memory_used) max_memory, round(avg(memory_used), 2) avg_memory, 
max(disk_used) max_disk, round(avg(disk_used), 2) avg_disk
from OM_JKXX_SERVER t group by alias, to_char(check_time, 'yyyy-mm-dd')
        """

        try:
            db = ora.connect(self.tns)
            cr = db.cursor()
            cr.execute(sql)
            rows = cr.fetchall()
            cr.close()
            db.close()
            ins = ["check_date", "alias", "max_cpu", "avg_cpu", "max_memory", 
            "avg_memory", "max_disk", "avg_disk"]
            for row in rows:
                #temp = temp + str(row[0]) + "\n"
                ctFld = 0
                for fld in row:
                    ttt = "%s : %s\n" % (ins[ctFld], str(fld))
                    temp = temp + ttt
                    ctFld += 1
                temp = temp + "----\n"

        except Exception as e:
            print(e)
            print(sql)

        temp = temp + """
        ========
        """

        sql = """
        select to_char(check_time, 'yyyy-mm-dd') rq, ip_port, 
max(req_count) max_req, round(avg(req_count), 2) avg_req, 
max(jvm_memory_used) max_memory, round(avg(jvm_memory_used), 2) avg_memory
from Om_Jkxx_Middleware t 
where t.req_count >= 0
group by ip_port, to_char(check_time, 'yyyy-mm-dd')
        """
        try:
            db = ora.connect(self.tns)
            cr = db.cursor()
            cr.execute(sql)
            rows = cr.fetchall()
            cr.close()
            db.close()
            ins = ["check_date", "ip_port", "max_req", "avg_req", "max_memory", 
            "avg_memory"]
            for row in rows:
                ctFld = 0
                #temp = temp + str(row[0]) + "\n"
                for fld in row:
                    ttt = "%s : %s\n" % (ins[ctFld], str(fld))
                    temp = temp + ttt
                    ctFld += 1
                temp = temp + "----\n"

        except Exception as e:
            print(e)
            print(sql)

        temp = temp + """
        ========
        """

        print(temp)

        encTemp = base64.b64encode(temp.encode("utf-8")).decode("utf-8")

        if not os.path.isdir("Output"):
            os.makedirs("Output")

        fileName = "%s_%s_%s_%s.omz" % (province, city, district, now)

        with open("Output/" + fileName, "w+", encoding='utf-8') as f:
            f.write(encTemp)

        print("\tOmz generated.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __showEnd(self):
        print("Everything done. Press any key to exit ...\n")
        
        system("pause")