#!/usr/local/bin python
# -*- coding: utf-8 -*-

import time
import os
import webbrowser

class Report(object):
    title = ""

    __starter = """
    <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            <title><< title >></title>
            <link href="../css/bootstrap.min.css" rel="stylesheet">
            <style type="text/css" media="screen">
                body  { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px;}
            </style>
        </head>
        <body>
        <header>
            <p style = "text-align:right; color: #CCCCCC"><< header >></p>
        </header>
        <div id = "statement">
            <h1 style = "text-align: center"><< title >></h2>
        </div>
        <h2>前言</h2>
        <p>
            1、本报告主要就与不动产登记信息系统相关的各项运维工作，包括操作系统、网络系统、数据库系统、应用系统、其它事项说明、附件等七个部分进行记录、分析、汇总和报告，以保障信息安全，实现不动产登记信息系统的安全、稳定、高效运行，支持日常业务、管理及各项工作的开展。
            <br/>
            <br/>
            2、本报告为月度报告，报告周期为每月一次，在出现重大事件时，实时提交《重大事件报告》。
            <br/>
            <br/>
            运行态势类别及说明（请选择其中之一）：
            <table border = "1" style = "text-align: center">        
                <tr>
                    <th style = "background-color: #33CCFF">运行态势类别</th>
                    <th style = "background-color: #33CCFF">说明</th>
                </tr>
                <tr>
                    <td>运行良好</td>
                    <td>无故障</td>
                </tr>
                <tr>
                    <td>运行正常</td>
                    <td>无故障、性能和资源已经处于或接近临界状态</td>
                </tr>
                <tr>
                    <td>运行基本正常</td>
                    <td>有轻微故障，本月度非正常停机次数少于3次且每次非正常停机不超过5分钟</td>
                </tr>
                <tr>
                    <td>运行异常</td>
                    <td>有严重故障，本月度非正常停机次数高于3次或单次非正常停机超过5分钟</td>
                </tr>        
            </table>
        </p>
        <h2>总体概述</h2>
        <p>
            本文档中内容为南京国图信息产业有限公司进行不动产登记项目软件实施运维安全管理的阶段性服务报告。通过本报告能够反映该段时间的整体维护工作、系统运行状况统计、故障统计与分析、技术协助及部署工作汇总、补丁管理总结等几个方面的内容。
            <br/>
            <br/>
            此报告为阶段性总结报告，旨在对本阶段的运维工作及故障情况进行总结与趋势分析，对于具体问题和故障处理的详细信息，可查询月度维护记录汇总。
            <br/>
            <br/>
            经巡查，本阶段软件系统及其运行环境的巡查情况如下：
        </p>
    """

    __finisher = """
        <footer>
            <p style = "text-align:right; color: #CCCCCC"><< footer >></p>
        </footer>
        </body>
        </html>"""

    body = """
        """

    def makeRpt(self):
        rptTime = time.localtime(time.time())
        now = time.strftime('%Y-%m-%d_%H-%M-%S',rptTime)
        rptFile = r"Output/EasyOM_Total_Specification_" + now + r".html"
        #encFile = r"rep/EasyOM_Report_" + now + r".eom"

        report = self.__starter + self.body + self.__finisher

        if not os.path.isdir("Output"):
            os.makedirs("Output")

        with open(rptFile, "w+", encoding='utf-8') as f:
            f.write(report)

        try:
            webbrowser.open("file://" + os.path.realpath(rptFile))
        except:
            pass

    def appendParagraph(self, str):
        text = """
        <p>%s</p>
        """ % (str)

        self.body = self.body + text

    def appendHTML(self, str):
        self.body = self.body + str

    def appendH1(self, str):
        text = """
        <h1>%s</h1>
        """ % (str)

        self.body = self.body + text

    def appendH2(self, str):
        text = """
        <h2>%s</h2>
        """ % (str)

        self.body = self.body + text

    def appendH3(self, str):
        text = """
        <h3>%s</h3>
        """ % (str)

        self.body = self.body + text

    def appendH4(self, str):
        text = """
        <h4>%s</h4>
        """ % (str)

        self.body = self.body + text

    def appendH5(self, str):
        text = """
        <h5>%s</h5>
        """ % (str)

        self.body = self.body + text

    def appendH6(self, str):
        text = """
        <h6>%s</h6>
        """ % (str)

        self.body = self.body + text

    def init(self):
        self.body = """
        """

    def changeStarter(self, para, val):
        self.__starter = self.__starter.replace("<< %s >>"%para, val)

    def changeFooter(self, para, val):
        self.__finisher = self.__finisher.replace("<< %s >>"%para, val)

class Table(object):
    __starter = """
    <table border = "1" style = "text-align: center">
    """

    __finisher = """
    </table>
    """

    cap = """
    <caption></caption>
    """

    body = ""

    def makeTable(self, str):
        cap = """
        <caption>%s</caption>
        <br />
        """ % (str)

        self.cap = cap

        return self.__starter + self.cap + self.body + self.__finisher

    def addHead(self, *str):
        text = """
        <tr>
        """
        for i in str:
            text = text + """<th style = "background-color: #33CCFF">%s</th>\n""" % (i)
        
        text = text + """
        </tr>
        """

        self.body = self.body + text

    def addRow(self, *str):
        text = """
        <tr>
        """
        for i in str:
            text = text + "<td>%s</td>\n" % (i)
        
        text = text + """
        </tr>
        """

        self.body = self.body + text