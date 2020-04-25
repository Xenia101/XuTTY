import paramiko
import time
import re
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

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
            ssh.connect(request.form['host'], username=request.form['username'], password=request.form['password'])
        except:
            return render_template('index.html')

        channel = ssh.invoke_shell()
        channel.send("")
        outdata, errdata = waitStreams(channel)
        output = re.compile(r'\x1b[^m]*m').sub('', outdata)
        print(output.split('\n'))

        return render_template('home.html', output=output)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(host="localhost", port=5000)


#while True:
#    command = input()
#    channel.send(command+"\n")
#    outdata, errdata = waitStreams(channel)
#    print(re.compile(r'\x1b[^m]*m').sub('', outdata))

