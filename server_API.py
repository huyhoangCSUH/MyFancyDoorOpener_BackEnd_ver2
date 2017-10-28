import web
import json
from flask import Flask, send_from_directory
app = Flask(__name__)


@app.route('/')
def index():
    return 'Under construction!'


@app.route('/getname')
def get_name():
    with open("server_backend/person_name.txt", "rb") as fin:
        person_name = fin.read()
        # print person_info
        return person_name


@app.route('/getdistance')
def get_distance():
    with open("server_backend/person_distance.txt", "rb") as fin:
        person_distance = fin.read()
        # print person_info
        return person_distance


@app.route('/setauth', methods=['POST'])
def set_auth():
    with open("server_backend/auth_stat.txt", "w") as f:
        f.write("1")
    return "Auth set!"


@app.route('/resetauth', methods=['POST'])
def reset_auth():
    with open("server_backend/auth_stat.txt", "w") as f:
        f.write("0")
    return "Auth reset!"


@app.route('/getimg')
def get_img():
    return send_from_directory('server_backend/video', 'web_cap.jpg')