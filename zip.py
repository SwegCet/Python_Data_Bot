import os
import zipfile

def zipFolder(folderPath, zipPath):
    #Create a zip file to write to
    with zipfile.ZipFile(zipPath, 'w', zipfile.ZIP_DEFLATED) as zipF:
        #Iterate over all files in the folder and subdirectories in the folder
        for root, _, files in os.walk(folderPath):
            for file in files:
                #Add the file to the zip
                filePath = os.path.join(root, file)
                arcname = os.path.relpath(filePath, folderPath)
                zipF.write(filePath, arcname)