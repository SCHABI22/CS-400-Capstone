# Cards are ints: 2-10, J=11, Q=12, K=13, A=14
# If Ace return 11, otherwise return the card value capped at 10

def cardValue(card):
    if card == 14:
        return 11
    return min(card, 10)


def labelToCard(label):
    rank = label[:-1]
    if rank == "A":
        return 14
    elif rank == "J":
        return 11
    elif rank == "Q":
        return 12
    elif rank == "K":
        return 13
    else:
        return int(rank)

# Calculates the total value of the hand
# If bust, cards over 21, looks for Ace, 
# and subtracts 10 for each Ace until total is 21 or less
def handTotal(cards):
    total = sum(cardValue(card) for card in cards)
    aces = cards.count(14)
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total, aces > 0


# Function to detect a player or dealer bust
def detectBust(cards):
    return handTotal(cards)[0] > 21

# Used to find doubles that can be split by the player
def detectDoubles(cards):
    return (len(cards) == 2) and (cardValue(cards[0]) == cardValue(cards[1]))

# Main advisor function, returns player and dealer values, and players best move
def advisor(playerCards, dealerUpCard):

    # Check if lists are empty, if so rise exception
    if playerCards == [] or dealerUpCard == []:
        raise ValueError("Player cards or dealer up card list is empty")

    total, soft = handTotal(playerCards)
    pair = cardValue(playerCards[0])
    dealerTotal = cardValue(dealerUpCard)
    move = None

    # Detects player cards over 21
    if detectBust(playerCards):
        return total, dealerTotal, "Bust!"

    # Detect Blackjack
    if total == 21 and len(playerCards) == 2:
        return total, dealerTotal, "Blackjack!"

    # Logic for doubles
    if detectDoubles(playerCards) and pair != 5:
        if (pair == 11) or (pair == 8):
            move = "Split"
        
        elif pair == 10:
            move = "Stand"

        elif pair == 9:
            if dealerTotal in [2, 3, 4, 5, 6, 8, 9]:
                move = "Split"
            else: move = "Stand"

        elif pair in [2, 3, 7]:
            if dealerTotal in [2, 3, 4, 5, 6, 7]:
                move = "Split"
            else: move = "Hit"

        elif pair == 6:
            if dealerTotal in [2, 3, 4, 5, 6]:
                move = "Split"
            else: move = "Hit"

        elif pair == 4:
            if dealerTotal in [5, 6]:
                move = "Split"
            else: move = "Hit"          



    # Logic for soft totals
    elif soft:
        if total >= 19: move = "Stand"

        elif total == 18:
            if dealerTotal in [3, 4, 5, 6]:
                move = "Double Down"
            elif dealerTotal in [2, 7, 8]:
                move = "Stand"
            elif dealerTotal in [9, 10, 11]:
                move = "Hit"

        elif total == 17: 
            if dealerTotal in [3, 4, 5, 6]:
                move = "Double Down"
            else: move = "Hit"

        elif total >= 15 and total <= 16: 
            if dealerTotal in [4, 5, 6]:
                move = "Double Down"
            else: move = "Hit"

        elif total >=13 and total <= 14:
            if dealerTotal in [5, 6]:
                move = "Double Down"
            else: move = "Hit"



    # Logic for hard totals
    else:
        if total >= 17: move = "Stand"

        elif total >= 13 and total <= 16:
            if dealerTotal in [2, 3, 4, 5, 6]:
                move = "Stand"
            else: move = "Hit"

        elif total == 12: 
            if dealerTotal in [4, 5, 6]:
                move = "Stand"
            else: move = "Hit"
            
        elif total == 11:
            if dealerTotal == 11:
                move = "Hit"
            else: move = "Double Down"
            
        elif total == 10:
            if dealerTotal in [2, 3, 4, 5, 6, 7, 8, 9]:
                move = "Double Down"
            else: move = "Hit"
            
        elif total == 9:
            if dealerTotal in [3, 4, 5, 6]:
                move = "Double Down"
            else: move = "Hit"

        elif total <= 8:
            move = "Hit"

    if move == "Double Down" and len(playerCards) > 2:
        move = "Stand" if (soft and total == 18) else "Hit"

    return total, dealerTotal, move
        
    



