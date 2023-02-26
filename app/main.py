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
            <Ftp>
               <FtpParams>
                  <FileName>testfiles</FileName>
                  <Host>192.168.1.64</Host>
                  <User>sammy</User>
                  <Password>password</Password>
                  <StoreDir>/home/sammy/scanned</StoreDir>
                  <PassiveMode>true</PassiveMode>
                  <PortNum>21</PortNum>
               </FtpParams>
            </Ftp>
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

@app.route('/stephasvehicle', methods=['GET', 'POST'])
def getStepHasVehicle():
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
            <Op type="Submit" action="stephasvehiclesteptwo"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">Transfer an Out-of-State Title to Ohio. Please press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')


@app.route('/stephasvehiclesteptwo', methods=['GET', 'POST'])
def getStepHasVehicleStepTwo():
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
            <Op type="Submit" action="stephasvehiclestepthree"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">Enter vehicle VIN number. Please press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/stephasvehiclestepthree', methods=['GET', 'POST'])
def getStepHasVehicleStepThree():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0" >
   <DisplayForm>
      <Script>
         <![CDATA[
             <UiScreen>
            <Operations>
               <Op type="Submit" action="stephasvehiclestepfour">
               </Op>
               <Op type="Back" action="./3.xml">
               </Op>
            </Operations>
            <IoScreen>
               <IoObject>
                  <Title>String Input</Title>
                  <Description>xml TextArea Description</Description>
                  <TextArea id="textarea_id" cpos="Tail">
                     <InitValue>abscefghijklmn</InitValue>
                     <MinLength>1</MinLength>
                     <MaxLength>128</MaxLength>
                     <Mask>false</Mask>
                     <LetterTypes>
                        <LetterType>UpperCase</LetterType>
                        <LetterType>LowerCase</LetterType>
                        <LetterType>Glyph</LetterType>
                     </LetterTypes>
                  </TextArea>
               </IoObject>
            </IoScreen>
         </UiScreen>
         ]]>
      </Script>
   </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/stephasvehiclestepfour', methods=['GET', 'POST'])
def getStepHasVehicleStepFour():
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
               <Description>Does the owner have a loan on the vehicle? Please select "Yes" or "No"</Description>
               <EitherOrControl>
                  <ItemY href="stephasvehiclestepfive">
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



@app.route('/stephasvehiclestepfive', methods=['GET', 'POST'])
def getStepHasVehicleStepFive():
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
            <Op type="Submit" action="stephasvehiclestepsix"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">Enter title info in scanner. Please press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')



@app.route('/stephasvehiclestepsix', methods=['GET', 'POST'])
def getStepHasVehicleStepSix():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
      <IoScanAndSend>
         <TxProfiles>
            <Ftp>
               <FtpParams>
                  <FileName>testfiles</FileName>
                  <Host>192.168.1.64</Host>
                  <User>sammy</User>
                  <Password>password</Password>
                  <StoreDir>/home/sammy/scanned</StoreDir>
                  <PassiveMode>true</PassiveMode>
                  <PortNum>21</PortNum>
               </FtpParams>
            </Ftp>
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





@app.route('/image')
def get_image():
    image_path = '../887e4b80799ebe2f5c8776f40b4a6b71.jpg'
    return send_file(image_path, mimetype='image/jpg')




@app.route('/printimage', methods=['GET', 'POST'])
def getPrintImage():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
  <IoDirectPrint>
  <AuthenticationProfiles>
         <HttpAuth>
            <HttpAuthParams>
               <User>sammy</User>
               <Password>password</Password>
            </HttpAuthParams>
         </HttpAuth>
      </AuthenticationProfiles>
    <FilePath>192.168.1.64/NetworkShare/887e4b80799ebe2f5c8776f40b4a6b71.jpg</FilePath>
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









