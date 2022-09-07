from flask import Blueprint
from deco import *
import tokenlib as TK
import res
import traceback
import oppressor as OP

noticeId = 0

User = Blueprint('user', __name__)

@User.route('/user/login', methods = ['POST','OPTIONS','GET'])
@Deco
def login_NoToken():
    userid = json_data().get("userid")
    password = json_data().get("password")
    version = json_data().get("version")
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
def logout_NoToken():
    return {'type': 'SUCCESS', 'message': '登出成功！'}
    #最好在这里做点什么吧，比如删除cookie什么的

@User.route('/user/info', methods = ['GET', 'POST'])
@Deco
def info():
    return {'type':'SUCCESS', 'message':"获取成功", 'info':tkData()}

@User.route('/user/getInfo/<int:userId>', methods=['POST'])
@Deco
def getInfo(userId):
    fl,r=OP.select("userName,class,permission","user","userId=%s",userId,["userName","class","permission"])
    if not fl: return r
    r.update({"type":"SUCCESS", "message":"获取成功"})
    return r

@User.route('/user/modPwd', methods = ['POST'])
@Deco
def modifyPassword():
    old=json_data().get("oldPwd")
    new=json_data().get("newPwd")
    fl, r = OP.select("userid","user", "userId = %s and password = %s", (tkData().get("userid"), old), ["user"])
    if not fl: return {"type": "ERROR", "message": "密码错误"}
    print(type(tkData().get("userid")))
    OP.update("password=%s","user","userId=%s",(new, tkData().get("userid"),))
    return {"type":"SUCCESS", "message":"修改成功"}

@User.route('/user/notices')
@Deco
def getNotices():
    fl, r = OP.select("notices", "user", "userId = %s", tkData().get("userid"), ["notices"])
    if r["notices"] == None: return { "type": "SUCCESS", "data": [] }

    ids = r["notices"].split(",")
    data = []

    for i in ids:
        fl, r = OP.select("noticeTitle, noticeText, deadtime", "user_notice", "noticeId = %s", i, ["title", "text", "deadtime"])
        data.append(r)
    
    print(data)

    return {
        "type": "SUCCESS",
        "data": data
    }

@User.route('/user/sendNotice', methods = ['POST'])
@Deco
def sendNotice():
    global noticeId

    target = json_data().get("target")
    title = json_data().get("title")
    message = json_data().get("message")

    noticeId += 1
    OP.insert("noticeTitle, noticeText, deadTime, noticeId", "user_notice", (title, message, "", noticeId))

    for i in target:
        fl, r = OP.select("notices", "user", "class = %s", i, ["notices"])
        print("-----", fl, r)
        if r["notices"] == None:
            OP.update("notices=%s", "user", "class=%s", (noticeId, i))
        else:
            OP.update("notices=%s", "user", "class=%s", (r["notices"] + ',' + str(noticeId), i))

    return { "type": "SUCCESS", "message": "发送成功！" }