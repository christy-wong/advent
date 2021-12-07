
def count_increases(lines):
  count = 0
  increase = 0
  while count < len(lines) - 1:
    if lines[count + 1] > lines[count]:
      increase += 1
      count += 1
    else:
      count += 1
  return increase

def count_moving_increases(lines):
  i = 0
  increase = 0
  while i < len(lines) - 3:
    sum1 = lines[i] + lines[i+1] + lines[i+2]
    sum2 = lines[i+1] + lines[i+2] + lines[i+3]
    if sum2 > sum1:
      increase += 1
      i += 1
    else:
      i += 1
  return increase

if __name__ == "__main__":
    f = open('depths.txt')
    lines = [int(i) for i in f.readlines()]

    print(count_increases(lines))
    print(count_moving_increases(lines))
