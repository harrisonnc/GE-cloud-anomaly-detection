from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/asdf/')
def hello_world1():
    return 'Hello, Goodbye!!'

if __name__ == '__main__':
    app.run()