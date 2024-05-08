from ftplib import FTP
import os
import json

def main():

    config = read_config('../config.json')
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']

    # test connection
    # testConnectionToFTPServer(host, port, username, password)

    # # upload file
    # file = './test3.txt' 
    # directory = ''
    # uploadStatus = uploadFile(file, host, port, username, password, directory)
    # print("upload status = {0}".format(uploadStatus))
    # list_directories_remote(host, port, username, password)

    # # download file
    # localPath = "./"
    # ftpFolder = ""
    # filesToDownload = ["test3.txt"]
    # status = downloadFile(host, port, username, password, ftpFolder, localPath, filesToDownload)
    # print("download status = {0}".format(status))

    # list files and directories on server
    # list_directories_remote(host, port, username, password)

    # # rename file
    # oldName = "test3.txt"
    # newName = "modified_test3.txt"
    # rename_file_remote(host, port, username, password, newName, oldName)
    # # test rename
    # list_directories_remote(host, port, username, password)

    # create directory on server
    test_directory = "testdirectory"
    #create_directory_remote(host, port, username, password, test_directory)
    #list_directories_remote(host, port, username, password)
    
    # delete directory on server
    #remove_directory_remote(host, port, username, password, test_directory)
    #list_directories_remote(host, port, username, password)

def testConnectionToFTPServer(host, port, username, password):
    # Connect to the FTP server
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)
    ftp.quit()
    print("User login successful.")

def uploadFile(local, host, port, username, password, remotedir):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)

    uploadStatus = False
    _, targetFilename = os.path.split(local)
    if not (remotedir == None or remotedir.strip() == ""):
        _ = ftp.cwd(remotedir)

    with open(local, "rb") as file:
        retCode = ftp.storbinary(f"STOR {targetFilename}", file, 
    blocksize=1024*1024)
    ftp.quit()

    if retCode.startswith('226'):
        uploadStatus = True
    return uploadStatus

def downloadFile(host, port, username, password, ftpFolder, localPath, filesToDownload):
    DownloadStatus = False
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)
    if not (ftpFolder == None or ftpFolder.strip() == ""):
        _ = ftp.cwd(ftpFolder)
    for i in range(len(filesToDownload)):
        file_name = filesToDownload[i]
        localFilePath = os.path.join(localPath, file_name)  # Corrected line
        print("downloading file {0}".format(file_name))
        # download FTP file using retrbinary function
        with open(localFilePath, "wb") as file:
            retCode = ftp.retrbinary("RETR " + file_name, file.write)
    ftp.quit()
    if retCode.startswith('226'):
        DownloadStatus = True
    return DownloadStatus

def list_directories_remote(host, port, username, password):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)
    try:
        directories = []
        # Redirect the directory listing to the directories list
        ftp.dir("", directories.append)
        for item in directories:
            print(item)
    except FTP.all_errors as e:
        print(f"Error while listing: {str(e)}")
    ftp.quit()

def rename_file_remote(host, port, username, password, newName, oldName):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)
    #try:
    ftp.rename(oldName, newName)
    print(f"Renamed file to {newName}")
    # except FTP.all_errors as e:
    #     print(f"Error while renaming. {str(e)} Current file name: {oldName} ")
    ftp.quit()

def create_directory_remote(host, port, username, password, directory):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)

    try:
        ftp.mkd(directory)
        print(f"Created directory {directory}")
    except FTP.all_errors as e:
        print(f"Error creating directory {directory}: {str(e)}")
    ftp.quit()

def remove_directory_remote(host, port, username, password, directory):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)

    try:
        ftp.rmd(directory)
        print(f"Removed directory {directory}")
    except FTP.all_errors as e:
        print(f"Error removing directory {directory}: {str(e)}")
    ftp.quit()

def read_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

if __name__ == '__main__':
    main()




