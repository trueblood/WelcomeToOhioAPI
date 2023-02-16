import requests
import app.imageocr as ocr
import app.helper as helper
from flask import Flask, Response
from logging.handlers import RotatingFileHandler
import logging

app = Flask(__name__)
app.config['SECRET_KEY']="hard to guess string"


handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/')
def hello_world():
    return "status up"

@app.route('/getapplicantinfo/<filename>', methods=['GET'])
def getApplicantInfo(filename):
    filename = '887e4b80799ebe2f5c8776f40b4a6b71.jpg'
    value = ocr.ImageOCR.get_Text_From_Image(filename)
    formattedValue = value.replace('\n', ' ')
    info = helper.Helper.find_person_info_from_license(formattedValue)
    return info

@app.route('/xml')
def getXML():
    print("My message", file=sys.stdout)
    xml_data="""
<SerioCommands version="1.0">
      <DisplayForm>
      <Script>
      <![CDATA[
         <UiScreen>
         <IoScreen>
         <IoObject>
         <Title>Example 1</Title>
         <Message>Example 2</Message>
         </IoObject>
         </IoScreen>
         </UiScreen>
      ]]>
      </Script>
      </DisplayForm>
</SerioCommands>


    """
    return Response(xml_data, mimetype='text/xml')