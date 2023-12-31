from flask import Blueprint, request
import tokenlib as tk
import json
import oppressor as OP
from deco import Deco
from res import *

Class = Blueprint('class', __name__)

@Class.route('/class/list', methods = ['GET'])
@Deco
def getClassList(json_data, token_data): # 好了
	# 是不是还要加上特殊情况的判断？
    # fl,r=OP.select("class","user","userId>200000",(),["id"],only=False)
    fl,r=OP.select("class","user","class>200000",(),["id"],only=False)
    print(fl,r)
    if not fl: return r
    classes = []
    for i in r: classes.append(i["id"])
    classes = sorted(set(classes))
    r = []
    for i in classes: r.append({"id": i, "name": OP.classIdToString(i)})
    return {
        "type": "SUCCESS",
        "message": "获取成功",
        "class": r
    }

@Class.route("/class/stulist/<int:classId>", methods = ['GET'])
@Deco
def getStudentList(classId, json_data, token_data): # 好了
    fl,r=OP.select("stuId,stuName,volTimeInside,volTimeOutside,volTimeLarge","student",
        "stuId > %s and stuId < %s",(str(classId*100),str(classId*100+100)),
        ["id","name","inside","outside","large"],only=False)
    if not fl: return r
    return {
        "type": "SUCCESS",
        "message": "获取成功",
        "student": r
    }

@Class.route("/class/volunteer/<int:classId>", methods = ['GET','OPTIONS'])
@Deco
def getClassVolunteer(classId, json_data, token_data): # 还没调
    fl,r=OP.select("volId","class_vol","class=%s",(classId),["id"],only=False)
    if not fl: return r
    ret={"type":"SUCCESS","message":"获取成功","volunteer":[]}
    for i in r:
        ff,rr=OP.select("volId,volName,volDate,volTime,description,status,stuMax",
        "volunteer","volId=%s",(i["id"]),["id","name","date","time","description","status","stuMax"])
        if not ff: return rr
        ret["volunteer"].append(rr)
    return ret

@Class.route('/class/noThought/<int:classId>', methods=['GET'])
@Deco
def getNoThought(classId, json_data, token_data): # 还没调
	fl,r=OP.select("volId,stuId","stu_vol","status=%s or (status = %s and thought='')",(STATUS_RESUBMIT,STATUS_WAITING),["volId","stuId"],only=False)
	if not fl:
		if r["message"]=="数据库信息错误：未查询到相关信息":
			r={"type":"SUCCESS","message":"没有需要填写感想的义工"}
		return r
	rr=[]
	for i in r:
		if i["stuId"]//100==classId: rr+=[i]
	if rr==[]: return {"type":"SUCCESS","message":"没有需要填写感想的义工"}
	return {"type":"SUCCESS","message":"获取成功","result":rr}
