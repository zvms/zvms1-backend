from flask import Blueprint, request
import json
from deco import *
import oppressor as OP

Volunteer = Blueprint('volunteer', __name__)

@Volunteer.route('/volunteer/list', methods = ['POST'])
@Deco
def getVolunteerList():
    respdata = {'type': 'ERROR', 'message': '未知错误'}
    st, val = OP.volunteerList()
    if st:
        respdata['type'] = 'SUCCESS'
        respdata['message'] = '获取成功'
        respdata['volunteer'] = []
        for i in val:
            respdata['volunteer'].append(
                {'id': i[0], 'name': i[1], 'description': i[2], 'time': i[3], 'status': i[4], 'stuMax': i[5]})
    return respdata

@Volunteer.route('/volunteer/fetch/<int:volId>', methods = ['POST'])
@Deco
def getVolunteer(volId):
    respdata = {'type': 'ERROR', 'message': '未知错误'}
    st, val = OP.getVolunteerInfo(volId)
    if st:
        # version 1
        st1, val1 = OP.listToDict_volunteer(val)
        if st1:
            respdata['type'] = 'SUCCESS'
            respdata['message'] = '获取成功'
        respdata.update(val1)
        # version 2
        # respdata['type'] = 'SUCCESS'
        # respdata['message'] = '获取成功'
        # respdata.update(OP.listToDict_volunteer_faultless(val))
    else:
        respdata.update(val)
    return respdata

@Volunteer.route('/volunteer/signup/<int:volId>', methods = ['POST'])
@Deco
def signupVolunteer(volId):
    user_class = tkdata.get("class")
    for i in json_data['stulst']:
        if i < user_class * 100 or i >= user_class * 100 + 100:
            return {"type": "ERROR", "message": "学生列表错误"}
    st, r = OP.select("stuMax, nowStuCount","volunteer","volId=%d",volId,[])
    if not st: return r
    if len(json_data['stulst']) > r["stuMax"] - r["nowStuCount"]:
        return {"type":"ERROR", "message":"人数超限"}
    # 先到这
    DB.execute(
        "SELECT stuMax FROM class_vol WHERE volId = %d AND classId = %d", volId, user_class)
    # 这里不对，应该在class_vol表里存这个班已经报名了多少人，不然多次报名可以突破班级人数限制
    r = DB.fetchall()
    if len(r) != 1:
        respdata['message'] = "数据库信息错误"
    else:
        if len(json_data['stulst']) > r[0][0]:
            respdata['message'] = "人数超限"
        else:
            for i in json_data['stulst']:
                # 代码来不及写了，写一下思路
                # class_vol表里修改一下这个班的报名人数
                # stu_vol表里加一条未审核的记录
                # volunteer表里修改nowStuCount
            respdata['type'] = "SUCCESS"
            respdata['message'] = "添加成功"
    return respdata

@Volunteer.route('volunteer/create', methods = ['POST'])
@Deco
def createVolunteer():
    respdata = {'type': 'error', 'message': '未知错误'}
    json_data = json.loads(request.get_data().decode("utf-8"))
    # if session["permisson"]>1

@Volunteer.route('volunteer/signerList/<int:volId>', methods = ['POST'])
def getSignerList(volId):
    pass

@Volunteer.route('volunteer/choose/<int:volId>', methods = ['POST'])
def chooseVolunteer(volId):
    pass

@Volunteer.route('volunteer/joinerList/<int:volId>', methods = ['POST'])
def getJoinerList(volId):
    pass

@Volunteer.route('volunteer/thought/<int:volId>', methods = ['POST'])
def submitThought(volId):
    pass

@Volunteer.route('volunteer/randomThought', methods=['POST','GET'])
def randthought():
    respdata = {'type':'SUCCESS', 'stuName':'用户名', 'stuId': 20200101, 'content':'这是感想内容'}
    return json.dumps(respdata)