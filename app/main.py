import requests
import app.imageocr as ocr
import app.helper as helper
from flask import Flask, Response
from logging.handlers import RotatingFileHandler
import logging
import sys

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

@app.route('/xml', methods=['POST'])
def getXML():
    xml_data="""


<SerioCommands version="1.2">
      <DisplayForm>
      <Script>
      <![CDATA[
         <UiScreen>
         <Title>'Single Select' (simple)</Title>
         <Operations>
            <Op type="Submit" action="/selected" />
        </Operations>
         <IoScreen>
         <IoObject>
         <Title>Select Fruit</Title>
        <Selection id="fruit" minSelectNum="1" multiple="false">
        <Item selected=false" value="apple">
         <Label>Apple</Label>
         </Item>
          <Item selected=false" value="peach">
         <Label>Peach</Label>
         </Item>
          <Item selected=false" value="pear">
         <Label>Pear</Label>
         </Item>
         </IoObject>
         </IoScreen>
         </UiScreen>
      ]]>
      </Script>
      </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/xml/<data>', methods=['POST'])
def getXML(data):
    xml_data="""


<SerioCommands version="1.0">
      <DisplayForm>
      <Script>
      <![CDATA[
         <UiScreen>
         <IoScreen>
         <IoObject>
         <Title>Example 1</Title>
         <Message>Hello 2nd screen</Message>
         </IoObject>
         </IoScreen>
         </UiScreen>
      ]]>
      </Script>
      </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')