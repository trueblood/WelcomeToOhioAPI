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

@app.route('/start', methods=['POST', 'GET'])
def getStart():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
  <DisplayForm>
    <Script>
      <![CDATA[
        <UiScreen>
          <Title>title</Title>
          <Operations>
            <Op type="Submit" action="steptwo"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Welcome To Ohio</Title>
              <Message imgsrc="./Sample_A.jpg">Welcome To Ohio New Resident Wizard. Please press "OK" button to continue.</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
  </SerioCommands>

    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/steptwo', methods=['GET', 'POST'])
def getStepTwo():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="v009">
   <DisplayForm>
      <Script>
         <![CDATA[
         <UiScreen>
            <Title>EitherOr Select</Title>
            <LinkScreen>
               <Description>Does applicant have license present?"</Description>
               <EitherOrControl>
                  <ItemY href="stepthree">
                     <Label>Yes</Label>
                  </ItemY>
                  <ItemN href="./0.xml"> 
                     <Label>No</Label>
                  </ItemN>
               </EitherOrControl>
            </LinkScreen>
         </UiScreen>
         ]]>
      </Script>
   </DisplayForm>
</SerioCommands>

    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/stepthree', methods=['GET', 'POST'])
def getStepThree():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
  <DisplayForm>
    <Script>
      <![CDATA[
        <UiScreen>
          <Title>title</Title>
          <Operations>
            <Op type="Submit" action="stepfour"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Information</Title>
              <Message imgsrc="./Sample_A.jpg">We are now going to scan the license. Please insert into scanner and click the "OK" button.</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>

    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/stepfour', methods=['GET', 'POST'])
def getStepFour():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""

<SerioCommands version="1.0">
      <IoScanAndSend>
         <TxProfiles>
			<Media>
				<MediaParams>
					<FileName>scan2usb</FileName>
				</MediaParams>
			</Media>
         </TxProfiles>
         <ScanTray>ADF</ScanTray>
         <ColorMode>Color</ColorMode>
         <Resolution>Normal</Resolution>
         <FileType>PDF</FileType>
         <FileNameFixed>true</FileNameFixed>
         <JobFinAckUrl>http://example.bsi.com/jobfin</JobFinAckUrl>
      </IoScanAndSend>
   <DisplayInfo>
      <Script>
         <![CDATA[<?xml version="1.0" encoding="UTF-8"?>
         <UiScreen >
                    <NullScreen></NullScreen>
         </UiScreen>
         ]]>
      </Script> 
   </DisplayInfo>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')


























