'''
由于user, student合并, 新版本中不存在Student视图
'''

from flask import Blueprint, request
import json
from deco import *
from res import *
import oppressor as OP

Student = Blueprint('student', __name__)

'''
这个功能被分成了两块
义工时间到了GET /users/<int:id>, 见user.py
义工记录到了GET /volunteers?s=<id>, 见volunteer.py
'''
@Student.route('/student/volbook/<int:stuId>', methods = ['GET'])
@Deco
def getVolunteerWork(stuId, json_data, token_data):
	fl,r=OP.select("volId,volTimeInside,volTimeOutside,volTimeLarge,status","stu_vol","stuId=%s", stuId,
	["volId","inside","outside","large","status"],only=False)
	if not fl:
		if "message" in r and r["message"]==OP.OP_NOT_FOUND:
			return {"type":"ERROR","message":"该学生没有义工记录"}
		return r
	for i in r:
		ff,rr=OP.select("volName","volunteer","volId=%s",i["volId"], ["name"])
		if not ff: return rr
		i.update({"name": rr["name"]})
	return {"type":"SUCCESS","message":"获取成功","rec":r}

'''
现在的义工报酬都只能有一种类型, 你不能在一次义工中既赚校内时间又得校外时间
校内为1, 校外为2, 大型为3, 其他地方也一样
这一部分的数据可以从GET /volunteers, GET /thoughts等api中获取
'''
@Student.route('/student/volcert/', methods = ['POST'])
@Deco
def getVolunteerCertification(json_data, token_data):
	stuId,volId=json_data["stuId"],json_data["volId"]
	f1,r1=OP.select(
		"stuId,volTimeInside,volTimeOutside,volTimeLarge,status,thought",
		"stu_vol","stuId=%s AND volId=%s",(stuId,volId),
		["id","inside","outside","large","status","thought"],only=True
	)
	if not f1: return r1
	f2,r2=OP.select(
		"volId,volName,description,volTime,volDate,volTimeInside,volTimeOutside,volTimeLarge",
		"volunteer","volId=%s",volId,
		["id","name","description","time","date","inside","outside","large"],only=True
	)
	if not f2: return r2
	return {"type":"SUCCESS","message":"获取成功","stu":r1,"vol":r2}
