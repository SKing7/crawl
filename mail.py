#!/bin/env python
# -*- encoding:utf-8 -*-
import subprocess
def send_mail(From, To, Cc, Subject, content) :
    """发送邮件"""
    msg = '''From: %s
To: %s
Cc: %s
Subject: %s
Mime-Version: 1.0
Content-Type: text/html; charset="utf-8"
<html>
    <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
      <style>
            body {font:normal 18px/1.5 Tahoma, Helvetica, arial, sans-serif; color:#000;}
            #standard-table { table-layout:fixed; width:80%%; margin-top:5px; border:1px solid #E8E8E8; border-collapse:collapse; border-spacing:0; font-size:14px; color:#222; text-align:center; background-color:#FFF; margin:auto;}
             #standard-table th { padding:4px 5px; text-align:center; border-bottom:1px solid #E8E8E8; background-color:rgb(33, 224, 224); }
            #standard-table td { padding:4px 5px; border-bottom:1px dotted #DCDCDC; border-right:1px dotted #DCDCDC; word-break:break-all; word-wrap:break-word; }
            #standard-table tr.alt td { background-color:#EEE; }
     </style>
    </head>
    <body>
        %s
    </body>
</html>''' % (From, To, Cc, Subject, content)
    print msg
    popj = subprocess.Popen(['/usr/sbin/sendmail','-t'], stdin=subprocess.PIPE)
    popj.communicate(msg)
    return popj.returncode == 0
#print send_mail("liying@meituan.com", "lishipeng@meituan.com", "", "test","你好!")
