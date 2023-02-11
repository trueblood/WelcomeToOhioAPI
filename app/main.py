import requests
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY']="hard to guess string"

@app.route('/')
def hello_world():
    return "status up"

@app.route('/imagetotext/<filelocation>', methods=['GET'])
def getDataByQuestionJson(website, question):
    url = getFormattedURL(website)
    value = db.DatabaseHelper.findDataByQuestion_Json(question, url)
    return value

