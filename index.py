from flask import Flask
from flask import request
from flask import make_response
from werkzeug import secure_filename
from flask import url_for
from flask import render_template
from flask import send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/Users/qylk/'
app.secret_key = '123456'


@app.route('/')
def index():
    return 'Hello Raspberry!'


@app.errorhandler(404)
def page_not_found(error):
    return 'page_not_found', 404


@app.route('/disk/<command>')
def disk_mount(command):
    if cmp(command, 'mount'):
        output = os.popen('sudo mount /dev/sda1 /media/pi/nas')
    elif cmp(command, 'unmount'):
        output = os.popen('sudo unmount /dev/sda1')
    else:
        return 'command not recognized'
    print output.read()


@app.route('/dlna/<command>')
def dlna(command):
    if cmp(command, 'start'):
        output = os.popen('sudo service minidlna start')
    elif cmp(command, 'stop'):
        output = os.popen('sudo service minidlna stop')
    else:
        return "command not recognized"
    print output.read()


@app.route('/reboot')
def reboot():
    output = os.popen('sudo reboot')
    print output.read()


@app.route('/shutdown')
def shutdown():
    output = os.popen('sudo shutdown -h now')
    print output.read()


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        the_file = request.files['file']
        if the_file:
            filename = secure_filename(the_file.filename)
            the_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'upload success!'
    return render_template('upload.html')


@app.route('/files/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# =============test===========================
@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@app.route('/cookie')
def cookie():
    resp = make_response(render_template('hello.html', name='qylk'))
    resp.set_cookie('username', 'qylk')
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        pass


@app.route('/file')
def file():
    # show the post with the given id, the id is an integer
    return url_for('static', filename='style.css')


@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)
