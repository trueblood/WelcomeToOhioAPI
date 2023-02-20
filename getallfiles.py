import pysftp

sftp_hostname = 'sparkling-water-50295.sftptogo.com'
sftp_username = 'fed873fba5c5afdd136d105b813ae2'
sftp_password = 'rtvxr0u8n7m0o7qnimuleyr1agla41c061jtx7c4'
# Set up the SFTP connection
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# Connect to the SFTP server
with pysftp.Connection(sftp_hostname, username=sftp_username, password=sftp_password, cnopts=cnopts) as sftp:
    # Change to the directory you want to download from
    sftp.cwd('/Scanned')

    # Get a list of all files in the directory
    file_list = sftp.listdir_attr()

    file_list_sorted = sorted(file_list, key=lambda x: x.st_atime) 

    first_file = file_list_sorted[0].filename
    return first_file
    # Download each file in the list
    for file in file_list_sorted:
        created_time = file.st_atime #
        print(file.filename, created_time)