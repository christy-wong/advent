import numpy as np

def get_data(file_name = 'day4/bingo.txt'):

  f = open(file_name)

  # create list of random numbers
  random_numbers = [int(i) for i in f.readline().rstrip('\n').split(',')]

  # using ravi's code as a guide
  # first get one card per row
  raw_cards = f.read().split("\n\n")
  cards = []
  # then create a list of lists of ints
  for card in raw_cards:
    rows = [int(i) for i in card.rstrip('\n').split()]
    cards.append(rows)

  # print(random_numbers)
  # print(cards)
  return random_numbers, cards


class Board:

  def finding_winner(random_numbers, cards):

    # we have to find the first instance that a card has 5 in a row

    # horizontal cases

    # vertical cases

## This will execute directly
if __name__ == "__main__":
  get_data()
