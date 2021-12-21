if __name__ == "__main__":
  f = open('bingo.txt')
  random_numbers = f.readline()
  cards = [line.rstrip('\n') for line in f]
  print(cards)
