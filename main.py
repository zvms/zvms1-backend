from flask import Flask,make_response,request
from flask_cors import CORS
# from flask_script import Manager
import database
from user import User
from _class import Class
from student import Student
from volunteer import Volunteer
from notice import Notice
from report import Report
from res import STATIC_FOLDER

# Flask init
app = Flask(__name__)
#app.debug = True  # 仅在测试环境打开！
app.config["SECRET_KEY"] = "PaSsw0rD@1234!@#$"
app.static_folder = STATIC_FOLDER

CORS(app, supports_credentials=True) # 允许跨域

app.register_blueprint(User)
app.register_blueprint(Class)
app.register_blueprint(Student)
app.register_blueprint(Volunteer)
app.register_blueprint(Notice)
app.register_blueprint(Report)

@app.route('/',methods=['GET', 'POST'])
def main():
   return "连上了"

# manager = Manager(app)
if __name__ == '__main__':
    # manager.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000)
