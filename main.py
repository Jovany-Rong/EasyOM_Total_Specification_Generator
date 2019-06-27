#!/usr/local/bin python
#-*-coding: utf-8-*-

from os import system, path
from configparser import ConfigParser as cp
from libs.report import *
from time import strftime, localtime, time

class Prog(object):
    # variables
    version = "1.0"

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

        print("\t\tLoading file contents ...\n")

        path = "Input/" + file

        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        
        rowList = text.split("\n")

        for row in rowList:
            if " : " in row:
                tList = row.split(" : ")
                dd[tList[0]] = tList[1]
        
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
                    <th style = "background-color: #33CCFF">CPU使用率</th>
                    <th style = "background-color: #33CCFF">内存使用率</th>
                    <th style = "background-color: #33CCFF">进程数</th>
                </tr>
        """

        checkTime = strftime('%Y-%m-%d',localtime(time()))

        checkPerson = input("\t\t---Please Input Checker Name: \n\t\t")
        
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
            </tr>
            """%(str(insCt), dd["ComputerAlias"], dd["Evaluation"], dd["CPUUsed"], dd["MemoryUsed"], dd["ProcessCount"])
        
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

        report.makeRpt()

        print("\tReport generated.\n")

        print("@@@@@@@@\n\n@@@@@@@@\n")

        system("pause")

    def __showEnd(self):
        print("Everything done. Press any key to exit ...\n")
        
        system("pause")