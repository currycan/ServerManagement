from flask import request,render_template,redirect,url_for,session
import time
from index import app,sql
import json
import os
import base64
import traceback
from .login import cklogin
@app.route('/linkButton',methods=['GET','POST'])
def linkButton():
    if request.method == 'GET':
        #返回HTML网页
        return render_template('linkButton.html')
    else:
        #返回全部已设定的按钮数据
        allLinkButton = sql.selectLinkButton()
        return json.dumps({'resultCode':0,'result':allLinkButton})

@app.route('/linkButton/Shell',methods=['GET','POST'])
@cklogin()
def getShell():
    if request.method == 'GET':
        #根据ID号单独获取按钮的SHELL,估计用不到这里
        BTID = request.values.get('BTID')
        result = sql.selectShellForLinkButton(BTID)
        try:
            result = result[0][0]
        except:
            result = '查询的按钮ID不存在'
        return json.dumps({'resultCode':0,'result':result})
    else:
        BTID = request.values.get('BTID')
        SHELL = request.values.get('SHELL')
        result = sql.updateLinkButton(BTID,SHELL)
        if result[0]:
            return json.dumps({'resultCode':0})
        else:
            return json.dumps({'resultCode':1,'result':str(result[1])})
@app.route('/linkButton/Create',methods=['POST'])
@cklogin()
def CreateLinkButton():
    LinkButtonDict = {
        'BUTTONNAME' : request.values.get('BUTTONNAME','按钮')[:5].ljust(5,'`').replace('`','&#8195;'),
        'TYPE' : request.values.get('TYPE'),
        'NOTE' : request.values.get('NOTE'),
        'SHELL' : request.values.get('SHELL')
    }
    sqlResult = sql.createLinkButton(LinkButtonDict)
    if sqlResult[0]:
        return json.dumps({'resultCode':0})
    else:
        return json.dumps({'resultCode':1,'result':str(result[1])})   
@app.route('/linkButton/Delete',methods=['POST'])
@cklogin()
def DeleteLinkButton():
    BTID = request.values.get('BTID')
    if BTID:
        sql.deleteLinkButton(BTID)
        return json.dumps({'resultCode':0})
    else:
        return json.dumps({'resultCode':1,'result':'???'})   
@app.route('/linkButton/Run',methods=['POST'])
@cklogin()
def RunLinkButton():
    BTID = request.values.get('BTID')
    SHELL = request.values.get('SHELL')
    if not BTID:
        return json.dumps({'resultCode':1,'result':'???'}) 
    SearchShell = sql.selectShellForLinkButton(BTID)[0][0]
    if SearchShell != SHELL:
        result = sql.updateLinkButton(BTID,SHELL)
    import subprocess
    subprocess.Popen(SHELL,shell=True)
    return json.dumps({'resultCode':0})
