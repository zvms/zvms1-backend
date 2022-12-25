from flask import Blueprint, request
import json
from deco import *
import oppressor as OP

Notice = Blueprint('notice', __name__)

@Notice.route('/notice/new', methods = ['POST'])
@Deco
def newNotice(json_data, token_data):
	pass

@Notice.route('/notice/query', methods = ['GET'])
@Deco
def queryNotice(json_data, token_data):
	pass

@Notice.route('/notice/modify/<ntcId>', methods = ['POST'])
@Deco
def modifyNotice(ntcId, json_data, token_data):
	pass

'''
GET /notices
urlparams {
	f: int, # 发出者
	t: int, # 接收者(用户)
	c: int, # 接收班级
	s # 学校通知
}
e.g. /notices?f=20220905 # 获取20220905发送的通知
     /notices?s # 获取学校通知
'''