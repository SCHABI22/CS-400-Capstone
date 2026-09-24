# Players & dealers cards, input by YOLO card detection
playerCards = []
dealerCards = []

# The value of all player & dealer cards
playerValue = 0
dealerValue = 0

# Extra player & dealer value. Used when player has an Ace which has value of 1 or 11
playerLowAce = 0 
dealerLowAce = 0

# List of all cards the player & dealer has doubles of 
playerDoubles = []
dealerDoubles = []

# Function for adding up all player & dealer cards 
def returnValues(playerCards, dealerCards):
    for p in playerCards:
        if p <= 10:
            playerValue += p
        else:
            if p < 14:
                playerValue += 10
            if p == 14:
                playerLowAce += playerValue + 1
                playerValue += 11

    for d in dealerCards:
        if p <= 10:
            dealerValue += d
        else:
            if d < 14:
                dealerValue += 10
            if p == 14:
                dealerLowAce += dealerValue + 1
                dealerValue += 11

    return playerCards, dealerCards

# Function to detect a player or dealer bust, return -1 player bust, return -2 dealer bust, return 1 no bust
def detectBust(playerValue, dealerValue):
    if playerValue > 21:
        playerValue = 0
        if playerLowAce == 0:
            return -1
        if playerLowAce > 21:
            playerLowAce = 0
            return -1

    if dealerValue > 21:
        dealerValue = 0
        if dealerLowAce == 0:
            return -2
        if dealerLowAce > 21:
            dealerLowAce = 0
            return -2

    return 1

# Used to find doubles that can be split by the player. Returns a list of all doubles the player has
def detectDoubles(playerCards):
    for i in playerCards:
        for z in playerCards:
            if (i == z) and (playerCards.index(i) != playerCards.index(z)):
                playerDoubles.append(i)
    return playerDoubles

# Main advisor function, returns player and dealer values, and players best move
def advisor(playerValue, dealerValue, playerLowAce, dealerLowAce, playerCards, dealerCards):
    returnValues(playerCards, dealerCards)
    detectBust(playerValue, dealerValue)
    detectDoubles(playerCards)

    if playerValue == 21:
        return playerValue, dealerValue, "Blackjack!"
    if playerLowAce == 21:
        return playerValue, dealerValue, "Blackjack!"
    if playerValue > 21:
        return playerValue, dealerValue, "Bust!"
    if playerLowAce > 21:
        return playerValue, dealerValue, "Bust!"

    if (playerValue >= 17) and (dealerValue <= 6):
        return playerValue, dealerValue, "Stand"
    if (playerLowAce >= 17) and (dealerLowAce <= 6):
        return playerValue, dealerValue, "Stand"
    if (playerValue >= 12) and (dealerValue <= 3):
        return playerValue, dealerValue, "Stand"
    if (playerLowAce >= 12) and (dealerLowAce <= 3):
        return playerValue, dealerValue, "Stand"

    if (playerDoubles != []) and (dealerValue <= 7):
        return playerValue, dealerValue, "Split"
    
    if (playerDoubles != []) and (dealerLowAce <= 7):
        return playerValue, dealerValue, "Split"

    if (playerDoubles != []) and (dealerLowAce == 8):
        return playerValue, dealerValue, "Split"

    if (playerDoubles != []) and (dealerLowAce == 9):
        return playerValue, dealerValue, "Split"

    if (playerDoubles != []) and (dealerLowAce == 10):
        return playerValue, dealerValue, "Split"

    else:
        return playerValue, dealerValue, "Hit"
    
    



