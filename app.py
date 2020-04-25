import paramiko
from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/auth', methods=['POST', 'GET'])
def auth():
    if request.method == 'POST':
        print(request.form)
        return render_template('home.html')
    else:
        return render_template('index.html')

#if __name__ == '__main__':
#    app.run(host="localhost", port=5000)

