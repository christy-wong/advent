
def gamma(lines):
  i = 0
  pos = 0
  string = ''
  count_ones = 0
  count_zeros = 0
  while pos < len(lines[0]):
    while i < len(lines):
      if lines[i][pos] == '0':
        count_zeros += 1
      else:
        count_ones += 1
      i += 1
    if count_ones > count_zeros:
      string = string + '1'
    else:
      string = string + '0'
    pos += 1
    i = 0
    count_ones = 0
    count_zeros = 0
  # return string
  return int(string, 2)


def episilon(lines):
  i = 0
  pos = 0
  string = ''
  count_ones = 0
  count_zeros = 0
  while pos < len(lines[0]):
    while i < len(lines):
      if lines[i][pos] == '0':
        count_zeros += 1
      else:
        count_ones += 1
      i += 1
    if count_ones < count_zeros:
      string = string + '1'
    else:
      string = string + '0'
    pos += 1
    i = 0
    count_ones = 0
    count_zeros = 0
  # return string
  return int(string, 2)



def oxygen_rating(lines):
  i = 0
  pos = 0
  count_ones = 0
  count_zeros = 0
  while len(lines) > 1:
    while i < len(lines):
      if lines[i][pos] == '0':
        count_zeros += 1
      else:
        count_ones += 1
      i += 1
    for item in lines[:]:
      if len(lines) == 1:
        break
      if count_ones >= count_zeros and item[pos] == '0':
        lines.remove(item)
      if count_zeros > count_ones and item[pos] == '1':
        lines.remove(item)
    if len(lines) == 1:
      break
    pos += 1
    i = 0
    count_ones = 0
    count_zeros = 0
  return int(lines[0], 2)

def co2_rating(lines):
  i = 0
  pos = 0
  count_ones = 0
  count_zeros = 0
  while len(lines) > 1:
    while i < len(lines):
      if lines[i][pos] == '0':
        count_zeros += 1
      else:
        count_ones += 1
      i += 1
    for item in lines[:]:
      if len(lines) == 1:
        break
      if count_ones >= count_zeros and item[pos] == '1':
        lines.remove(item)
      if count_zeros > count_ones and item[pos] == '0':
        lines.remove(item)
    if len(lines) == 1:
      break
    pos += 1
    i = 0
    count_ones = 0
    count_zeros = 0
  return int(lines[0], 2)


if __name__ == "__main__":
  f = open('rays.txt')
  lines = [line.rstrip('\n') for line in f]

  print(gamma(lines))
  print(episilon(lines))
  print(gamma(lines)*episilon(lines))
  print(oxygen_rating(lines))
  print(co2_rating(lines))
  print(oxygen_rating(lines)*co2_rating(lines))
