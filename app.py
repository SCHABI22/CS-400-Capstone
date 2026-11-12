import cv2
from BlackjackAdvisor.BlackjackAdvisor import advisor, labelToCard
from PlayingCardsDetection.infer import detectCards, detectCardsLabeled
from camera import Camera

# create new camera function to run camera indefinetly for user, change camera detection to not display images, add diagnostic checks
def run(frame):
		playerLabels, dealerLabels, labeledFrame = detectCardsLabeled(frame)
		midpoint = frame.shape[1] // 2
		cv2.line(labeledFrame, (midpoint, 0), (midpoint, frame.shape[0]), (255, 255, 255), 1)
		cv2.imshow("Blackjack Advisor", labeledFrame)

		playerCard = [labelToCard(card) for card in playerLabels]
		dealerCard = [labelToCard(card) for card in dealerLabels]

		if playerCard == [] or dealerCard == []:
			return None
		
		return advisor(playerCard, dealerCard[0])

running = True

def main() -> None:
	camera = Camera()
	print("Blackjack Advisor is ready. Press 'q' to quit.")
	lastResult = None
	while True:
		result = run(camera.read())
		if result is not None and result != lastResult:
			total, dealerTotal, move = result
			print(f"Player: {total}  Dealer: {dealerTotal}  Move: {move}")
			lastResult = result

		if cv2.waitKey(1) == ord('q'):
			break

	camera.release()

if __name__ == "__main__":
	main()
	