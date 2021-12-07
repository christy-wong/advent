
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

if __name__ == "__main__":
  f = open('rays.txt')
  lines = [line.rstrip('\n') for line in f]

  print(gamma(lines))
  print(episilon(lines))
  print(gamma(lines)*episilon(lines))

