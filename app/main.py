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


<SerioCommands version="1 0">
 <DisplayForm>
  <Script>
   <![CDATA[
    <UiScreen>
     <Title>Layer Select</Title>
     <Operations>
      <Op type="Submit" action="./3.xml" ></Op>
      <Op type="Back" action="./1.xml" ></Op>
     </Operations>

     <IoScreen>
      <IoObject>
       <Title>Select Item</Title>
       <Selection id="SelectItem" multiple="false">
        <Item value="1" selected="true">
          <Label>Item 1</Label>
        </Item>
        <Item value="2" selected="false">
          <Label>Item 2</Label>
        </Item>
        <Item value="3" selected="false">
          <Label>Item 3</Label>
        </Item>
       </Selection>
      </IoObject>

      <IoObject>
       <Title>Text Input</Title>
       <TextArea id="textArea" cpos="Tail" priorInput="LowerCase">
        <InitValue>example text</InitValue>
        <MinLength>1</MinLength>
        <MaxLength>32</MaxLength>
        <Mask>false</Mask>
        <LetterTypes>
          <LetterType>UpperCase</LetterType>
          <LetterType>LowerCase</LetterType>
          <LetterType>Numeric</LetterType>
          <LetterType>Glyph</LetterType>
        </LetterTypes>
       </TextArea>
      </IoObject>

      <IoObject>
       <Title>Num Input</Title>
       <NumericalArea id="numericalArea" cpos="Tail">
        <InitValue>123</InitValue>
        <MinValue>1</MinValue>
        <MaxValue>65535</MaxValue>
       </NumericalArea>
      </IoObject>

     </IoScreen>
    </UiScreen>
   ]]>
  </Script>
 </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/xml/test/<data>', methods=['POST'])
def getXMLPage(data):
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