import pysftp
import io

# Set the SFTP server connection details
sftp_hostname = 'sparkling-water-50295.sftptogo.com'
sftp_username = 'fed873fba5c5afdd136d105b813ae2'
sftp_password = 'rtvxr0u8n7m0o7qnimuleyr1agla41c061jtx7c4'


import pysftp as sftp

remote_file_path = '/Scanned/887e4b80799ebe2f5c8776f40b4a6b71.jpg'
remote_file_path = f'Hello {name}! This is {program}'

cnopts = sftp.CnOpts()
cnopts.hostkeys = None

with sftp.Connection(host=sftp_hostname, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
   print("Connection successfully established ... ")
   sftp.cwd('/Scanned/')  # Switch to a remote directory
   directory_structure = sftp.listdir_attr() # Obtain structure of the remote directory
   with io.BytesIO() as buf:
        sftp.getfo(remote_file_path, buf)
        buf.seek(0)
        file_contents = buf.read()
        print(file_contents)
for attr in directory_structure:
   print(attr.filename, attr)


#import pysftp
#import io

## Set the SFTP server connection details
#sftp_hostname = 'your_sftp_server_hostname'
#sftp_username = 'your_sftp_username'
#sftp_password = 'your_sftp_password'

## Set the remote file path
#remote_file_path = '/path/to/remote/file'

## Connect to the SFTP server
#with pysftp.Connection(sftp_hostname, username=sftp_username, password=sftp_password) as sftp:
 #   # Read the contents of the remote file into memory
  #  with io.BytesIO() as buf:
   #     sftp.getfo(remote_file_path, buf)
    #    buf.seek(0)
     #   file_contents = buf.read()

## Print the contents of the file stored in memory
#print(file_contents)