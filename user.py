from flask import Blueprint
from deco import *
import tokenlib as TK
import res
import traceback
import oppressor as OP
from datetime import date

User = Blueprint('user', __name__)

@User.route('/user/login', methods = ['POST','OPTIONS','GET'])
@Deco
def login_NoToken(json_data, token_data):
    userid = json_data.get("userid")
    password = json_data.get("password")
    version = json_data.get("version")
    if version != res.CURRENT_VERSION:
        return {"type": "ERROR", "message": res.CURRENT_VERSION_ERROR_MESSAGE}
    st, val = OP.userLogin(userid, password)
    ret={}
    if st:
        ret.update({"type":"SUCCESS", "message":"登入成功！"})
        ret.update(OP.user2dict(val))
        ret.update({"token":TK.generateToken({
            "userid": userid,
            "username": ret['username'],
            "class": ret['class'],
            "permission": ret['permission']
        })})
    else:
        ret.update({"type": "ERROR", "message": "用户名或密码错误"})
        traceback.print_exc()
        ret.update(val)
    return ret

@User.route('/user/logout', methods = ['GET','OPTIONS','POST'])
@Deco
def logout_NoToken(json_data, token_data):
    return {'type': 'SUCCESS', 'message': '登出成功！'}
    #最好在这里做点什么吧，比如删除cookie什么的

@User.route('/user/info', methods = ['GET', 'POST'])
@Deco
def info(json_data, token_data):
    return {'type':'SUCCESS', 'message':"获取成功", 'info':token_data}

@User.route('/user/getInfo/<int:userId>', methods=['POST'])
@Deco
def getInfo(userId, json_data, token_data):
    fl,r=OP.select("userName,class,permission","user","userId=%s",userId,["userName","class","permission"])
    if not fl: return r
    r.update({"type":"SUCCESS", "message":"获取成功"})
    return r

@User.route('/user/modPwd', methods = ['POST'])
@Deco
def modifyPassword(json_data, token_data):
    old=json_data.get("oldPwd")
    new=json_data.get("newPwd")
    fl, r = OP.select("userid","user", "userId = %s and password = %s", (token_data.get("userid"), old), ["user"])
    if not fl: return {"type": "ERROR", "message": "密码错误"}
    print(type(token_data.get("userid")))
    OP.update("password=%s","user","userId=%s",(new, token_data.get("userid"),))
    return {"type":"SUCCESS", "message":"修改成功"}

@User.route('/user/notices')
@Deco
def getNotices(json_data, token_data):
    fl, r = OP.select("notices", "user", "userId = %s", token_data.get("userid"), ["notices"])
    if r["notices"] is None: return { "type": "SUCCESS", "data": [] }

    ids = r["notices"].split(",")
    data = []

    year, month, day = [int(i) for i in str(date.today()).split('-')]

    for i in ids:
        _, r = OP.select("noticeTitle, noticeText, deadtime", "user_notice", "noticeId = %s", i, ["title", "text", "deadtime"])

        y, m, d = [int(i) for i in r["deadtime"].split('-')]
        if y < year:
            continue
        elif y > year:
            data.append(r)
        elif m < month:
            continue
        elif m > month:
            data.append(r)
        elif d < day:
            continue
        else:
            data.append(r)

    return {
        "type": "SUCCESS",
        "data": data
    }

@User.route('/user/sendNotice', methods = ['POST'])
@Deco
def sendNotice(json_data, token_data):

    target = json_data.get("target")
    title = json_data.get("title")
    message = json_data.get("message")
    deadtime = json_data.get("deadtime")

    # 不知道为什么有时候会变成None
    if deadtime is None:
        deadtime = str(date.today())

    OP.insert("noticeTitle, noticeText, deadTime", "user_notice", (title, message, deadtime))

    _, r = OP.select("noticeId", "user_notice", "noticeTitle=%s and noticeText=%s and deadtime=%s", (title, message, deadtime), ["noticeId"], False)
    
    noticeId = max(map(lambda x: x["noticeId"], r))
    print(noticeId)

    for i in target:
        _, r = OP.select("notices", "user", "class = %s", i, ["notices"])
        if r["notices"] == None:
            OP.update("notices=%s", "user", "class=%s", (noticeId, i))
        else:
            OP.update("notices=%s", "user", "class=%s", (r["notices"] + ',' + str(noticeId), i))

    return { "type": "SUCCESS", "message": "发送成功！" }
