from gevent.wsgi import WSGIServer
from flask import Flask, send_from_directory, Response
import faceRec_API as fr

app = Flask(__name__)


path_for_files = "/home/huy/MyFancyDoorOpener_BackEnd_ver2/server_backend"
@app.route('/')
def index():
    return 'Under construction!'


@app.route('/getname')
def get_name():
    person_name = fr.recognize(path_for_files + '/video/web_cap.jpg')
    # with open(path_for_files + "/person_name.txt", 'w') as f:
    #     f.write(person_name)
    #
    # with open(path_for_files + "/person_name.txt", "r") as fin:
    #     person_name = fin.read()
    #     # print person_info
    #     return person_name
    return person_name


@app.route('/getdistance')
def get_distance():
    with open(path_for_files + "/person_distance.txt", "r") as fin:
        person_distance = fin.read()
        # print person_info
        return person_distance


@app.route('/setauth', methods=['GET', 'POST'])
def set_auth():
    with open(path_for_files + "/auth_stat.txt", "w") as f:
        f.write("1")
    return "Auth set!"


@app.route('/resetauth', methods=['GET', 'POST'])
def reset_auth():
    with open(path_for_files + "/auth_stat.txt", "w") as f:
        f.write("0")
    return "Auth reset!"


def load_photo():
    while True:
        frame = open(path_for_files + '/video/web_cap.jpg').read()
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(load_photo(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, threaded=True)

http_server = WSGIServer(('', 8000), app)
http_server.serve_forever()
