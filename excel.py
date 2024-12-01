import pandas as pd

def savePlayerStats(playerStats, playerStatsFileName):
    #convert the list of objects to a dictionary
    data = {
        "Name": [p.name for p in playerStats],
        "PlayerId": [p.playerId for p in playerStats],
        "CurrentPower": [p.currentPower for p in playerStats],
        "HighestPower": [p.highestPower for p in playerStats],
        "Merits": [p.merits for p in playerStats],
        "Kills": [p.kills for p in playerStats],
        "Dead": [p.dead for p in playerStats],
        "Healed": [p.healed for p in playerStats]
    }
    
    #Create Data Frame from the dictionary
    df = pd.DataFrame(data)
    
    #Convert Current Power column to numeric type
    df["CurrentPower"] = df["CurrentPower"].apply(lambda x: "{:,.0f}".format(x))
    df["Merits"] = df["Merits"].apply(lambda x: "{:,.0f}".format(x))
    df["HighestPower"] = df["HighestPower"].apply(lambda x: "{:,.0f}".format(x))
    df["Kills"] = df["Kills"].apply(lambda x: "{:,.0f}".format(x))
    df["Dead"] = df["Dead"].apply(lambda x: "{:,.0f}".format(x))
    df["Healed"] = df["Healed"].apply(lambda x: "{:,.0f}".format(x))
    
     # Save the DataFrame to an Excel file
    df.to_excel(f"{playerStatsFileName}.xlsx", index=False)

    print("Player statistics saved to Excel successfully.")