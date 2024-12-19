#Defines 2d coordinates
class Point: 
    def __init__(self, x ,y):
        self.x = x
        self.y = y
    
class ImageBounds:
    def __init__(self, pivot, width, height):
        self.x = pivot.x
        self.y = pivot.y
        self.width = width
        self.height = height
    
# Class for objects that will be tracked
class PlayersStats:
    def __init__(self, playerId, playerName, highestPower, currentPower, merits, victories, defeats, unitsKilled, unitsDead, unitsHealed):
        self.playerId = playerId
        self.playerName = playerName
        self.currentPower = currentPower
        self.highestPower = highestPower
        self.merits = merits
        self.victories = victories
        self.defeats = defeats
        self.unitsKilled = unitsKilled
        self.unitsDead = unitsDead
        self.unitsHealed = unitsHealed