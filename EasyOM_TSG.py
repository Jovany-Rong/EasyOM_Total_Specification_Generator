#!/usr/local/bin python
#-*-coding: utf-8-*-

import sys
import os
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
os.environ['NLS_LANG'] = "SIMPLIFIED CHINESE_CHINA.UTF8"
import main

if __name__ == '__main__':
    app = main.Prog()