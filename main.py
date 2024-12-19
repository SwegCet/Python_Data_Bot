import logging
import os
import shutil
import time
from datetime import datetime
import tkinter as tk
import pytz

from parser import collectPlayerStats
from excel import savePlayerStats
from memberScreenBot import processRanks
from mouse import moveClickTarget
from config import member_screen_coordinates
from googledrive import uploadFile, createFolder
from zip import zipFolder

parentFolderId = "1ty4CfIdRfnTw9fFuOPdpFTOz4DNZIRBN"

def parseScreenshots(directoryName, destinationDirectoryName):
    results = {}
    skipCount = 0
    
    #Traverse the main directory
    for root, dirs, files in os.walk(directoryName):
        for directory in dirs:
            dir_path = os.path.join(root, directory)
            
            #Check if detailed_profile.png and profile_summary.png exists in the directory
            if 'detailed_profile.png' in os.listdir(dir_path) and 'profile_summary.png' in os.listdir(dir_path):
                detailedProfilePath = os.path.join(dir_path, 'detailed_profile.png')
                profileSummaryPath = os.path.join(dir_path, 'profile_summary.png')
                
                playerStats = collectPlayerStats(detailedProfilePath, profileSummaryPath)
                
                if playerStats.playerId in results:
                    skipCount += 1
                    print(f"Skipping, already processed {playerStats.playerId}")
                    continue
                
                moveToDirectory(dir_path, 'detailed_profile.png', os.path.join(destinationDirectoryName, "ss"), f"{playerStats.playerId}_detailed_profile.png")
                moveToDirectory(dir_path, 'profile_summary.png', os.path.join(destinationDirectoryName, "ss"), f"{playerStats.playerId}_profile_summary.png")
                
                results[playerStats.playerId] = playerStats
        
        print(f"Skipped {skipCount} players")
        print(f"Total unique players: {len(results)}")
        zipFolder(os.path.join(destinationDirectoryName, "ss"), os.path.join(destinationDirectoryName,"ss.zip"))
        #recursively remove the directory and its contents
        shutil.rmtree(os.path.join(destinationDirectoryName, "ss"))
        return results, destinationDirectoryName.replace("outputs/", "")
        
                               
def moveToDirectory(sourceDirectoryName, sourceFile, destinationDirectoryName, destinationFile):
    if not os.path.exists(destinationDirectoryName):
        os.makedirs(destinationDirectoryName)
    
    sourcePath = os.path.join(sourceDirectoryName, sourceFile)
    destination_path = os.path.join(destinationDirectoryName, destinationFile)
    
    shutil.copy(sourcePath, destination_path)    
    

def main():
    #Get current time in UTC timezone
    currentTime = datetime.now(pytz.utc)
    
    #Format the current time as a string in desired format
    timestampString = currentTime.strftime("%Y-%m-%d %H-%M")
    
    destination_directory_names = []
    
    # Don't like the predetermined values, this is a test so far
    directoryName = f"outputs/ECHO_{timestampString}" # CHANGE ALLIANCE NAME HERE
    os.makedirs(directoryName)
    print("Processing alliance ECHO") # CHANGE ALLIANCE NAME HERE
    processRanks(directoryName)
    # ----------------------------- GetScreenshots -----------------------------
    print("Processing alliance ECHO finished. Parsing screenshots") # CHANGE ALLIANCE NAME HERE
   
    # ----------------------------- Parse Screenshots -----------------------------
    result_path = os.path.join(directoryName)
    results, destination_directory_name = parseScreenshots(os.path.join(directoryName), result_path)
    destination_directory_names.append(destination_directory_name)
    print(f"Parsed {len(results)} screenshots")
    savePlayerStats(results.values(), os.path.join(result_path,"player_statistics"))
    # ----------------------------- Parse Screenshots -----------------------------
    
    
    # ----------------------------- Clear Directories -----------------------------
    # Get a list of all directories in the parent directory
    allDirectories = [d for d in os.listdir(directoryName) if os.path.isdir(os.path.join(directoryName, d))]

    # Delete directories except for the one specified
    for directory in allDirectories:
        if directory != 'result':
            directory_path = os.path.join(directoryName, directory)
            print(f"Deleting directory: {directory_path}")
            shutil.rmtree(directory_path)
    # ----------------------------- Clear Directories -----------------------------
    
    moveClickTarget(member_screen_coordinates["back_button_location"])
    moveClickTarget(member_screen_coordinates["back_button_location"])
    time.sleep(1)

    # Here is where putting files into googledrive will be 
    for directoryName in destination_directory_names:
        upload_count = 1
        #Traverse the main directory
        for root, dirs, files in os.walk(os.path.join("outputs/", directoryName)):
            folderId = createFolder(parentFolderId, directoryName)
            for file in files:
                file_path = os.path.join("outputs/", directoryName, file)
                uploadFile(folderId, file_path, os.path.basename(file_path))
                logging.info(f"Uploaded {file_path}, Count: {upload_count}")
                upload_count += 1

if __name__ == "__main__":
    main()