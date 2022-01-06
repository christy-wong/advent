import numpy as np

def get_data(file_name = 'day4/bingo.txt'):
  # f = open(file_name)
  f = open('day4/bingo.txt')
  # create list of random numbers
  random_numbers = [int(i) for i in f.readline().rstrip('\n').split(',')]
  # using ravi's code as a guide
  # first get one card per row
  raw_cards = f.read().split("\n\n")
  cards = []
  # then create a list of lists of ints
  for card in raw_cards:
    print(card)
    rows = [int(i) for i in card.split('\n')]
    print(rows)
    cards.append(rows)
    print(cards)
    break
  # print(random_numbers)
  # print(cards)
  return random_numbers, cards


class Board:

  def finding_winner(random_numbers, cards):

    return null

    # we have to find the first instance that a card has 5 in a row

    # horizontal cases

    # vertical cases

## This will execute directly
if __name__ == "__main__":
  get_data()


f = open('day4/bingo.txt')
# create list of random numbers
random_numbers = [int(i) for i in f.readline().rstrip('\n').split(',')]
# using ravi's code as a guide
# first get one card per row
raw_cards = f.read().split("\n\n")
cards = []
# then create a list of lists of ints
for card in raw_cards:
  rows = card.split('\n')
  cards.append(np.array([list(map(int, row.split())) for row in rows]))
  print(cards)
  break

with open('day4/bingo.txt', "r") as f:
  called_numbers = list(map(int, f.readline().rstrip().split(",")))
  next(f)
  raw_grids = f.read().split("\n\n")
boards = []
for raw_grid in raw_grids:
  rows = raw_grid.split("\n")
  boards.append(np.array([list(map(int, row.split())) for row in rows]))
