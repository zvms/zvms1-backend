from flask import Blueprint, request
import json
from deco import *
from res import *
import oppressor as OP

Student = Blueprint('student', __name__)

@Student.route('/student/volbook/<int:stuId>', methods = ['GET'])
@Deco
def getVolunteerWork(stuId):
    fl,r=OP.select("volId,volTimeInside,volTimeOutside,volTimeLarge,status","stu_vol","stuId=%s",stuId,
    ["volId","inside","outside","large","status"],only=False)
    if not fl: return r
    for i in r:
        ff,rr=OP.select("volName","volunteer","volId=%s",i["volId"], ["name"])
        if not ff: return rr
        i.update({"name": rr["name"]})
    return {"type":"SUCCESS","message":"获取成功","rec":r}

@Student.route('/student/volcert/', methods = ['POST'])
@Deco
def getVolunteerCertification():
	stuId,volId=json_data()["stuId"],json_data()["volId"]
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