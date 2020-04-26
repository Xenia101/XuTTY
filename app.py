import paramiko
import time
import re
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

def waitStreams(chan):
    time.sleep(1)
    outdata=errdata = ""
    while chan.recv_ready():
        outdata += str(chan.recv(1024).decode(encoding='UTF-8'))
    while chan.recv_stderr_ready():
        errdata += str(chan.recv_stderr(1024))
    return outdata, errdata

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(request.form['host'], username=request.form['username'], password=request.form['password'], port=22)
            ssh.close()
        except (paramiko.BadHostKeyException, paramiko.AuthenticationException, paramiko.SSHException) as e:
            print(e)
            sys.exit(-1)
        
        session['host'] = request.form['host']
        session['user'] = request.form['username']
        session['pwd'] = request.form['password']
        return redirect(url_for('cmd'))

@app.route('/cmd', methods=['POST', 'GET'])
def cmd():
    global c
    if request.method == 'POST':
        print(c)

        #channel.send(request.form['cmd'])
        c.send("ls\n")
        outdata, errdata = waitStreams(c)
        output = re.compile(r'\x1b[^m]*m').sub('', outdata)
        output = output.split('\n')

        print(output)

        return render_template('home.html')
    else:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(session.get('host'),22, username=session.get('user'), password=session.get('pwd'))

        c = ssh.invoke_shell()
        c.send("")
        outdata, errdata = waitStreams(c)
        output = re.compile(r'\x1b[^m]*m').sub('', outdata)
        output = output.split('\n')

        return render_template('home.html', output=output[:len(output)-1], promt=output[-1])

if __name__ == '__main__':
    app.run(host="localhost", port=5000, debug=True, use_reloader=False)


#while True:
#    command = input()
#    channel.send(command+"\n")
#    outdata, errdata = waitStreams(channel)
#    print(re.compile(r'\x1b[^m]*m').sub('', outdata))

