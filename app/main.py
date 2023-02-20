import requests
import app.imageocr as ocr
import app.helper as helper
import app.sftphelper as sftp
from flask import Flask, Response, send_file, request
from logging.handlers import RotatingFileHandler
import logging
import sys
import io
import os

app = Flask(__name__)
app.config['SECRET_KEY']="hard to guess string"

# Set up logging to Heroku
if 'DYNO' in os.environ:
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

@app.route('/')
def hello_world():
    return "status up"

@app.route('/getapplicantinfo', methods=['GET'])
def getApplicantInfo():
    filename = sftp.sftphelper.get_most_recent_file_name()
    value = sftp.sftphelper.get_file_from_sftp(filename)
    formattedValue = value.replace('\n', ' ')
    info = helper.Helper.find_person_info_from_license(formattedValue)
    return formattedValue

@app.route('/start', methods=['POST'])
def getStart():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""

<SerioCommands version="1.0">
   <DisplayForm>
      <Script>
         <![CDATA[
         <UiScreen>
               <Operations>
                  <Op type="Submit" action="./6.xml">
                  </Op>
                  <Op type="Back" action="./7.xml">
                  </Op>
               </Operations>
               <IoScreen>
                  <IoObject>
                     <Title>Message Title</Title>
                     <Message>Please press "OK" button</Message>
                  </IoObject>
               </IoScreen>
            </UiScreen>
         ]]>
      </Script>
   </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')


@app.route('/xml', methods=['POST'])
def getXML():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""


<SerioCommands version="1.0">
 <DisplayForm>
  <Script>
   <![CDATA[<?xml version="1.0" encoding="UTF-8"?>
    <UiScreen>
      <Operations>
      <Op type="Submit" action="zeroxml" ></Op>
      <Op type="Back" action="./0.xml" ></Op>
    </Operations>
     <IoScreen>
      <IoObject>
       <Title>Select item(Single)</Title>
       <Selection id="selectid test" multiple="false" >
        <Item selected="false" value="FirstItem">
         <Label>First Item</Label>
        </Item>
        <Item selected="false" value="SecondItem">
         <Label>Second Item</Label>
        </Item>
        <Item selected="false" value="ThirdItem">
         <Label>Third Item</Label>
        </Item>
       </Selection>
      </IoObject>
     </IoScreen>
    </UiScreen>
   ]]>
  </Script>
 </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/zeroxml', methods=['POST'])
def getZeroXml():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

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

@app.route('/download', methods=['POST'])
def download_file():
    # Create a BytesIO buffer and write some content to it
    buffer = io.BytesIO()
    buffer.write(b'Hello, world!')

    # Seek to the beginning of the buffer
    buffer.seek(0)

    # Send the buffer as a file download
    return send_file(buffer, as_attachment=True, attachment_filename='example.txt')

@app.route("/download_word_doc", methods=['POST'])
def download_word_doc(): 
    # Assuming you have a Word document named mydoc.docx in a folder named 'static'
    filename = "bmv5745_bmv5750.docx"
    filepath = '/path/to/example.docx'
    return send_file(filepath, attachment_filename=filename, as_attachment=True)


@app.route('/printform745', methods=['POST'])
def getPrintForm745():
    xml_data="""


<SerioCommands version="1.0">
  <IoDirectPrint>
  <AuthenticationProfiles>
         <HttpAuth>
            <HttpAuthParams>
               <User>bsitest</User>
               <Password>bsitest</Password>
            </HttpAuthParams>
         </HttpAuth>
      </AuthenticationProfiles>
    <FilePath>https://pacific-hollows-04361.herokuapp.com/download_word_doc/bmv5745_bmv5750.docx</FilePath>
    <ColorMode>Mono</ColorMode>
    <PaperSize>Letter</PaperSize>
    <NumCopies>3</NumCopies>
    <FeedTray>Auto</FeedTray>
    <JobFinAckUrl>./end.xml</JobFinAckUrl>
  </IoDirectPrint>
  <DisplayInfo>
    <Script><![CDATA[
		<?xml version="1.0" encoding="UTF-8"?>
		<UiScreen>
			<NullScreen></NullScreen>
		</UiScreen>
	]]></Script>
  </DisplayInfo>
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