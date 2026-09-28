from BlackjackAdvisor.BlackjackAdvisor import advisor
from PlayingCardsDetection.infer import detectCards


def main() -> None:
	print("Blackjack Advisor is ready.")

running = True


if __name__ == "__main__":
	main()
	while running == True:
		advisor(0, 0, 0, 0, detectCards(), detectCards())