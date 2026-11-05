import cv2
from BlackjackAdvisor.BlackjackAdvisor import advisor, labelToCard
from PlayingCardsDetection.infer import detectCards
from camera import camRunning


def main() -> None:
	print("Blackjack Advisor is ready.")

# create new camera function to run camera indefinetly for user, change camera detection to not display images, add diagnostic checks
def run():
	playerSide, dealerSide = camRunning()
	playerCard = [labelToCard(label) for label in detectCards(playerSide)]
	dealerCard = [labelToCard(label) for label in detectCards(dealerSide)]
	if not playerCard or not dealerCard:
		return None
	return advisor(playerCard, dealerCard[0])

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

		if cv2.waitKey(1) == ord('q'):
				running = False
