import cv2
from BlackjackAdvisor.BlackjackAdvisor import advisor, labelToCard
from PlayingCardsDetection.infer import detectCards
from camera import camRunning


def main() -> None:
	print("Blackjack Advisor is ready.")

# fix blackjack advisor empty list handling, create new camera function to run camera indefinetly for user, change camera detection to not display images, add diagnostic checks
def run():
	playerSide, dealerSide = camRunning()
	playerCard = detectCards(playerSide)
	dealerCard = detectCards(dealerSide)
	return advisor(playerCard, dealerCard)

running = True


if __name__ == "__main__":
	main()
	while running == True:
		run()

		if cv2.waitKey(1) == ord('q'):
				running = False

