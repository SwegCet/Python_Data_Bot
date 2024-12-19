import pandas as pd

def generateDiffReports(file1Path, file2Path):
    #Load the Excel Files
    df1 = pd.read_excel(file1Path)
    df2 = pd.read_excel(file2Path)
    
    #Merge the two dataframes on "Player ID"
    mergedDf = pd.merge(df1, df2, on="PlayerID", suffixes=('_old', '_new'))

    #Define the column names postfixes
    currentPowerName = "CurrentPower"
    highestPowerName = "HighestPower"
    meritName = "Merits"
    killsName = "Kills"
    victoriesName = "Victories"
    defeatName = "Defeat"
    deadName = "Dead"
    healedName = "Healed"
    oldPostfix = "_old"
    newPostfix = "_new"
    differencePostfix = "_difference"
    
    #Calculate the difference for each player
    mergedDf[f"{currentPowerName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{currentPowerName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{currentPowerName}{oldPostfix}"].str.replace(',', ''))
        
    mergedDf[f"{highestPowerName}{oldPostfix}"] = pd.to_numeric(
        mergedDf[f"{highestPowerName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{highestPowerName}{oldPostfix}"].str.replace(',', ''))
        
    mergedDf[f"{meritName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{meritName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{meritName}{oldPostfix}"].str.replace(',', ''))
    
    mergedDf[f"{victoriesName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{victoriesName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{victoriesName}{oldPostfix}"].str.replace(',', ''))
    
    mergedDf[f"{defeatName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{defeatName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{defeatName}{oldPostfix}"].str.replace(',', ''))
    
    mergedDf[f"{killsName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{killsName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{killsName}{oldPostfix}"].str.replace(',', ''))
    
    mergedDf[f"{deadName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{deadName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{deadName}{oldPostfix}"].str.replace(',', ''))
    
    mergedDf[f"{healedName}{differencePostfix}"] = pd.to_numeric(
        mergedDf[f"{healedName}{newPostfix}"].str.replace(',', '')) - pd.to_numeric(
        mergedDf[f"{healedName}{oldPostfix}"].str.replace(',', ''))
    
    resultDf = mergedDf[["NameNew", "PlayerID",
                         f"{highestPowerName}{differencePostfix}",
                         f"{currentPowerName}{differencePostfix}",
                         f"{meritName}{differencePostfix}",
                         f"{victoriesName}{differencePostfix}",
                         f"{defeatName}{differencePostfix}",
                         f"{killsName}{differencePostfix}",
                         f"{deadName}{differencePostfix}",
                         f"{healedName}{differencePostfix}"
                         ]]
    
    resultDf = resultDf.sort_values(by=f"{meritName}{differencePostfix}", ascending=False)
    
    #save the results to a new excel file
    resultDf.to_excel("differences.xlsx", index=False)
    

def mergeReports(file1Path, file2Path):
    df1 = pd.read_excel(file1Path)
    df2 = pd.read_excel(file2Path)
    
    #merge the two dataframes on a specific column
    mergedDf = pd.concat([df1, df2]).drop_duplicates(subset='PlayerId')
    
    #Save the merged dataframe to a new excel file
    mergedDf.to_excel('new.xlsx', index=False)
    

def savePlayerStats(playerStats, playerStatsFileName):
    #convert the list of objects to a dictionary
    data = {
        "Name": [p.playerName for p in playerStats],
        "PlayerId": [p.playerId for p in playerStats],
        "HighestPower": [p.highestPower for p in playerStats],
        "CurrentPower": [p.currentPower for p in playerStats],
        "Merits": [p.merits for p in playerStats],
        "Victories": [p.victories for p in playerStats],
        "Defeats": [p.defeats for p in playerStats],
        "Kills": [p.unitsKilled for p in playerStats],
        "Dead": [p.unitsDead for p in playerStats],
        "Healed": [p.unitsHealed for p in playerStats]
    }
    
    #Create Data Frame from the dictionary
    df = pd.DataFrame(data)
    
    #Convert Current Power column to numeric type
    df["HighestPower"] = df["HighestPower"].apply(lambda x: "{:,.0f}".format(x))
    df["CurrentPower"] = df["CurrentPower"].apply(lambda x: "{:,.0f}".format(x))
    df["Merits"] = df["Merits"].apply(lambda x: "{:,.0f}".format(x))
    df["Victories"] = df["Victories"].apply(lambda x: "{:,.0f}".format(x))
    df["Defeats"] = df["Defeats"].apply(lambda x: "{:,.0f}".format(x))
    df["Kills"] = df["Kills"].apply(lambda x: "{:,.0f}".format(x))
    df["Dead"] = df["Dead"].apply(lambda x: "{:,.0f}".format(x))
    df["Healed"] = df["Healed"].apply(lambda x: "{:,.0f}".format(x))
    
     # Save the DataFrame to an Excel file
    df.to_excel(f"{playerStatsFileName}.xlsx", index=False)

    print("Player statistics saved to Excel successfully.")