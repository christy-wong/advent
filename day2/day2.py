f = open('moves.txt')
# lines = [i for i in f.readlines()]
lines = [line.rstrip('\n') for line in f]

hor = 0
dep = 0
i = 0
while i < len(lines):
      word = lines[i][0:lines[i].find(' ')]
      number = int(lines[i][lines[i].find(' ')+1:len(lines[i])])
      if word == 'forward':
        hor += number
        i += 1
      elif word == 'down':
        dep += number
        i += 1
      else:
        dep -= number
        i += 1

hor = 0
dep = 0
aim = 0
i = 0
while i < len(lines):
      word = lines[i][0:lines[i].find(' ')]
      number = int(lines[i][lines[i].find(' ')+1:len(lines[i])])
      if word == 'down':
        i += 1
        aim += number
      elif word == 'up':
        i += 1
        aim -= number
      else:
        hor += number
        i += 1
        dep += number * aim

