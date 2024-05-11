from ftplib import FTP
import os
import json

def main():

    config = read_config('../config.json')
    host = config['host']
    port = config['port']
    username = config['username']
    password = config['password']


    while True:
        
        printMenu()

        choice = input("Enter your choice: ")

        if choice == '1':
            # test connection
            testConnectionToFTPServer(host, port, username, password)
        elif choice == '2':
            # upload file
            uploadFileUI(host, port, username, password)
            list_directories_remote(host, port, username, password)
        elif choice == '3':
            # download file
            downloadFileUI(host, port, username, password)
        elif choice == '4':
            # list files and directories on server
            list_directories_remote(host, port, username, password)
        elif choice == '5':
            # list files and directories on local
            list_directories_local()
        elif choice == '6':
            # rename file
            renameFileUI(host, port, username, password)
            # test rename
            list_directories_remote(host, port, username, password)
            pass
        elif choice == '7':
            # create directory on server
            directory = input("Enter the directory name to be created on the server: ")
            create_directory_remote(host, port, username, password, directory)
            list_directories_remote(host, port, username, password)
        elif choice == '8':
            # delete directory on server
            directory = input("Enter the directory name to be deleted from the server: ")
            remove_directory_remote(host, port, username, password, directory)
            list_directories_remote(host, port, username, password)
        elif choice == '9':
            file_name = input("Enter the file name to be deleted from the server: ")
            remove_file_remote(host, port, username, password, file_name)
            list_directories_remote(host, port, username, password)
        elif choice == "10":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


def uploadFileUI(host, port, username, password):
    file = input("Enter file path to be uploaded: ")
    if not os.path.isfile(file):
        print("File not found.")
        return
    directory = input("Enter the remote directory (leave blank for root): ")
    uploadStatus = uploadFile(file, host, port, username, password, directory)
    print("Upload status =", uploadStatus)
    if uploadStatus:
        print("File uploaded successfully.")
    else:
        print("Upload failed.")

def downloadFileUI(host, port, username, password):
    list_directories_remote(host, port, username, password)
    file_to_download = input("Enter the name of the file to download: ")
    local_path = input("Enter the local directory to save the file: ")
    ftp_folder = input("Enter the remote directory containing the file (leave blank for root): ")
    status = downloadFile(host, port, username, password, ftp_folder, local_path, [file_to_download])
    print("Download status =", status)
    if status:
        print("File downloaded successfully.")
    else:
        print("Download failed.")

def renameFileUI(host, port, username, password):
    old_name = input("Enter the current name of the file: ")
    new_name = input("Enter the new name for the file: ")
    rename_file_remote(host, port, username, password, new_name, old_name)

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
        localFilePath = os.path.join(localPath, file_name)  
        print("downloading file {0}".format(file_name))
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

def list_directories_local():
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        print(file)
    
def rename_file_remote(host, port, username, password, newName, oldName):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)
    try:
        ftp.rename(oldName, newName)
        print(f"Renamed file to {newName}")
    except FTP.all_errors as e:
        print(f"Error while renaming. {str(e)} Current file name: {oldName} ")
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
    except AttributeError as e:
        print(f"Error removing directory {directory}: {str(e)}")
    ftp.quit()

def remove_file_remote(host, port, username, password, file_name):
    ftp = FTP(timeout=30)
    ftp.connect(host, port)
    ftp.login(username, password)

    try:
        ftp.delete(file_name)
        print(f"Removed file {file_name} from the server")
    except AttributeError as e:
        print(f"Error removing file {file_name} from the server: {str(e)}")
    ftp.quit()

def read_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

def printMenu():
    print("\nMenu:")
    print("1. Test connection to FTP server")
    print("2. Upload file to FTP server")
    print("3. Download file from FTP server")
    print("4. List directories on FTP server")
    print("5. List directories in local")
    print("6. Rename file on FTP server")
    print("7. Create directory on FTP server")
    print("8. Remove directory from FTP server")
    print("9. Remove file from FTP server")
    print("10. Exit")

if __name__ == '__main__':
    main()




