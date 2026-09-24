from BlackjackAdvisor.BlackjackAdvisor import advisor
from PlayingCardsDetection.infer import detectCards


def main() -> None:
	print("Blackjack Advisor is ready.")


if __name__ == "__main__":
	main()
	advisor(0, 0, 0, 0, detectCards(), detectCards())