import cv2
from BlackjackAdvisor.BlackjackAdvisor import advisor, labelToCard
from PlayingCardsDetection.infer import detectCards, detectCardsLabeled
from camera import camRunning, liveFeed


def main() -> None:
	print("Blackjack Advisor is ready.")

# create new camera function to run camera indefinetly for user, change camera detection to not display images, add diagnostic checks
def run():
		playerSide, dealerSide = camRunning()
		print("Player Side Cards Detected: ", detectCards(playerSide))

		playerCard = []
		for card in detectCards(playerSide):
			playerCard.append(labelToCard(card))
		print("Player Side Card Values: ", playerCard)

		dealerCard = []
		for card in detectCards(dealerSide):
			dealerCard.append(labelToCard(card))
		print("Dealer Side Card Values: ", dealerCard)

		if playerCard == [] or dealerCard == []:
			print("Error: No cards detected on one or both sides. Please ensure the cards are clearly visible and try again.")
			return
		return advisor(playerCard, dealerCard)

running = True


if __name__ == "__main__":
	main()
	lastResult = None
	while running == True:
		result = run()
		if result is not None and result != lastResult:
			total, dealerTotal, move = result
			print(f"Player: {total}  Dealer: {dealerTotal}  Move: {move}")
			lastResult = result
