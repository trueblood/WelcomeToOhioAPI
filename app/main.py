import requests
import app.imageocr as ocr
import app.helper as helper
import app.sftphelper as sftp
from flask import Flask, Response, send_file, request,render_template,render_template_string
from logging.handlers import RotatingFileHandler
import logging
import sys
import io
import os
import app.databasehelper as dbhelper

app = Flask(__name__)
app.config['SECRET_KEY']="hard to guess string"

# Set up logging to Heroku
#if 'DYNO' in os.environ:
#    app.logger.addHandler(logging.StreamHandler(sys.stdout))
#    app.logger.setLevel(logging.INFO)

#handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)
#handler.setLevel(logging.INFO)
#app.logger.addHandler(handler)

@app.route('/', methods=['GET'])
def onGetIndex():
    return render_template('index.html')

@app.route('/getapplicantinfo', methods=['GET', 'POST'])
def getApplicantInfo():
    filename = sftp.sftphelper.get_most_recent_file_name()
    value = sftp.sftphelper.get_file_from_sftp(filename)
    formattedValue = value.replace('\n', ' ')
    info = helper.Helper.find_person_info_from_license(formattedValue)
    return info

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
    #app.logger.info(data)

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

    substring = '<Value>'
    indexOne = str(data).index(substring)
    substringTwo = '</Value>'
    indexTwo = str(data).index(substringTwo)
    value = str(data)[indexOne+7:indexTwo]
    dbhelper.DatabaseHelper.writeToDatabase("4", value)
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
                  <ItemY href="stephasvehiclestepfourandhalf">
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

@app.route('/stephasvehiclestepfourandhalf', methods=['GET', 'POST'])
def getStepHasVehicleStepFourAndHalf():
    data = request.form # This will capture the data sent in the request body
    dbhelper.DatabaseHelper.writeToDatabase("3", data)
    xml_data="""
<SerioCommands version="v009">
   <DisplayForm>
      <Script>
         <![CDATA[
         <UiScreen>
            <Title>EitherOr Select</Title>
            <LinkScreen>
               <Description>Does the vehicle have multiple owners? Please select "Yes" or "No"</Description>
               <EitherOrControl>
                  <ItemY href="">
                     <Label>Yes</Label>
                  </ItemY>
                  <ItemN href="stephasvehiclestepfive"> 
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




@app.route('/steplicenseone', methods=['GET', 'POST'])
def getStepLicenseOne():
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
            <Op type="Submit" action="steplicensetwo"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">License wizard. Press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/steplicensetwo', methods=['GET', 'POST'])
def getStepLicenseTwo():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1 0">
 <DisplayForm>
  <Script>
   <![CDATA[
    <UiScreen>
     <Title>Layer Select</Title>
     <Operations>
      <Op type="Submit" action="steplicensethree" ></Op>
      <Op type="Back" action="./1.xml" ></Op>
     </Operations>

     <IoScreen>
      <IoObject>
       <Title>Select Item</Title>
       <Selection id="SelectItem" multiple="false">
        <Item value="1" selected="true">
          <Label>18 and older</Label>
        </Item>
        <Item value="2" selected="false">
          <Label>Under 18</Label>
        </Item>
        <Item value="3" selected="false">
          <Label>CDL</Label>
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


@app.route('/steplicensethree', methods=['GET', 'POST'])
def getStepLicenseThree():
    data = request.form # This will capture the data sent in the request body

    substring = '<Value>'
    indexOne = str(data).index(substring)
    substringTwo = '</Value>'
    indexTwo = str(data).index(substringTwo)
    value = str(data)[indexOne+7:indexTwo]
    #dbhelper.DatabaseHelper.writeToDatabase("4", value)
    if (value == "1"):
        xml_data="""
        <SerioCommands version="1.0">
  <DisplayForm>
    <Script>
      <![CDATA[
        <UiScreen>
          <Title>title</Title>
          <Operations>
            <Op type="Submit" action="steplicenseeight"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Information</Title>
              <Message imgsrc="./Sample_A.jpg">We are now going to scan the required documents. Please insert into scanner and click the "OK" button.</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands> """
    elif (value == "2"):
      xml_data="""
<SerioCommands version="1.0">
  <DisplayForm>
    <Script>
      <![CDATA[
        <UiScreen>
          <Title>title</Title>
          <Operations>
            <Op type="Submit" action="steplicensefour"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">Enter first name and then press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    elif (value == "3"):
      xml_data="""

<SerioCommands version="1.0">
  <DisplayForm>
    <Script>
      <![CDATA[
        <UiScreen>
          <Title>title</Title>
          <Operations>
            <Op type="Submit" action="stepthreehalf"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">We are going to print form BMV2159. Please press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')


@app.route('/stepthreehalf', methods=['GET', 'POST'])
def getStepThreeHalf():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
<IoDirectPrint>
<AuthenticationProfiles>
<CifsAuth>
<CifsAuthParams>
<AuthMethod>Auto</AuthMethod>
<User></User>
<Password></Password>
</CifsAuthParams>
</CifsAuth>
</AuthenticationProfiles>
<FilePath>http://192.168.1.64/static/bmv21591024_1.jpg</FilePath>
<ColorMode>Mono</ColorMode>
<PaperSize>Letter</PaperSize>
<FeedTray>Auto</FeedTray>
<JobFinAckUrl>licensestepeighthalf</JobFinAckUrl>
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

@app.route('/steplicensefour', methods=['GET', 'POST'])
def getStepLicenseFour():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0" >
   <DisplayForm>
      <Script>
         <![CDATA[
             <UiScreen>
            <Operations>
               <Op type="Submit" action="steplicensefive">
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

@app.route('/steplicensefive', methods=['GET', 'POST'])
def getStepLicenseFive():
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
            <Op type="Submit" action="steplicensesix"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Message Title</Title>
              <Message imgsrc="./Sample_A.jpg">Enter last name and then press "OK" button</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/steplicensesix', methods=['GET', 'POST'])
def getStepLicenseSix():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0" >
   <DisplayForm>
      <Script>
         <![CDATA[
             <UiScreen>
            <Operations>
               <Op type="Submit" action="steplicenseseven">
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

@app.route('/steplicenseseven', methods=['GET', 'POST'])
def getStepLicenseSeven():
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
            <Op type="Submit" action="steplicenseeight"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Information</Title>
              <Message imgsrc="./Sample_A.jpg">We are now going to scan the required documents. Please insert into scanner and click the "OK" button.</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')

@app.route('/steplicenseeight', methods=['GET', 'POST'])
def getStepLicenseEight():
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
          <JobFinAckUrl>http://192.168.1.64/licensestepnine</JobFinAckUrl>
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

@app.route('/licensestepeighthalf', methods=['GET', 'POST'])
def getLicenseStepEightHalf():
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
               <Description>HAZMAT endorsement? Please select "Yes" or "No"</Description>
               <EitherOrControl>
                  <ItemY href="./8.xml">
                     <Label>Yes</Label>
                  </ItemY>
                  <ItemN href="licensestepten"> 
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



@app.route('/licensestepnine', methods=['GET', 'POST'])
def getLicenseStepNine():
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
            <Op type="Submit" action="printimage"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Information</Title>
              <Message imgsrc="./Sample_A.jpg">We are now going to print form BMV_5750. Please click the "OK" button.</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')


@app.route('/licensestepten', methods=['GET', 'POST'])
def getLicenseStepTen():
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
            <Op type="Submit" action="licensestepeleven"></Op>
            <Op type="Back" action="./back.xml"></Op>
          </Operations>
          <IoScreen>
            <IoObject>
              <Title>Information</Title>
              <Message imgsrc="./Sample_A.jpg">We are now going to scan identity documents. Please click the "OK" button.</Message>
            </IoObject>
          </IoScreen>
        </UiScreen>
      ]]>
    </Script>
  </DisplayForm>
</SerioCommands>
    """
    return Response(xml_data, mimetype='text/xml')


@app.route('/licensestepeleven', methods=['GET', 'POST'])
def getLicenseStepEleven():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
      <IoScanAndSend>
         <TxProfiles>
            <Ftp>
               <FtpParams>
                  <FileName>identitydocuments</FileName>
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
          <JobFinAckUrl>http://192.168.1.64/licensestepnine</JobFinAckUrl>
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

@app.route('/printimage', methods=['GET', 'POST'])
def getPrintImage():
    data = request.form # This will capture the data sent in the request body
    app.logger.info(data)

    xml_data="""
<SerioCommands version="1.0">
<IoDirectPrint>
<AuthenticationProfiles>
<CifsAuth>
<CifsAuthParams>
<AuthMethod>Auto</AuthMethod>
<User></User>
<Password></Password>
</CifsAuthParams>
</CifsAuth>
</AuthenticationProfiles>
<FilePath>http://192.168.1.64/static/testfiles1024_1.jpg</FilePath>
<ColorMode>Mono</ColorMode>
<PaperSize>Letter</PaperSize>
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



