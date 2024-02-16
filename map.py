import re
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

colormap = {
  'N': 'b',
  'E': 'r',
  'W': 'g',
  'S': 'y',
  'NE': 'purple',
  'SE': 'orange',
  'SW': 'greenyellow',
  'NW': 'c'
}

patch = [
  mpatches.Patch(color=colormap['N'], label='North'),
  mpatches.Patch(color=colormap['E'], label='East'),
  mpatches.Patch(color=colormap['W'], label='West'),
  mpatches.Patch(color=colormap['S'], label='South')
]

def standardise_directions(movements):
  result = []
  pattern = r'^([-+]?\d+\.\d+|[-+]?\d+)(.*)$'
  directions = ['N', 'E', 'W', 'S', 'NE', 'SE', 'SW', 'NW']
  for index in range(len(movements)):
    match = re.match(pattern, movements[index][0])
    if match:
      if movements[index][1] in directions:
        dist = float(match.group(1))
        if match.group(2) == 'mm':
          pass
        elif match.group(2) == 'cm':
          dist = dist * 10
        else:
          print(f'Unit not recognised: {match.group(2)}')
          sys.exit()
        result.append((dist, movements[index][1]))
      else:
        print(f'Direction not recognised: {movements[index][1]}')
        sys.exit()
    else:
      print(f'Movement not recognised: {movements[index][0]}')
      sys.exit()
  return result

def plot_movement(start, movements):
  x, y = start
  total_distance = 0
  X = [start[0]]
  Y = [start[1]]

  for distance, direction in movements:
    total_distance += distance
    if direction == 'N':
      y += distance
      X.append(X[-1])
      Y.append(Y[-1] + distance)
    elif direction == 'E':
      x += distance
      X.append(X[-1] + distance)
      Y.append(Y[-1])
    elif direction == 'W':
      x -= distance
      X.append(X[-1] - distance)
      Y.append(Y[-1])
    elif direction == 'S':
      y -= distance
      X.append(X[-1])
      Y.append(Y[-1] - distance)
    elif direction == 'NE':
      x += distance / (2 ** 0.5)
      y += distance / (2 ** 0.5)
      X.append(X[-1] + distance / (2 ** 0.5))
      Y.append(Y[-1] + distance / (2 ** 0.5))
    elif direction == 'SE':
      x += distance / (2 ** 0.5)
      y -= distance / (2 ** 0.5)
      X.append(X[-1] + distance / (2 ** 0.5))
      Y.append(Y[-1] - distance / (2 ** 0.5))
    elif direction == 'SW':
      x -= distance / (2 ** 0.5)
      y -= distance / (2 ** 0.5)
      X.append(X[-1] - distance / (2 ** 0.5))
      Y.append(Y[-1] - distance / (2 ** 0.5))
    else: #elif direction == 'NW':
      x -= distance / (2 ** 0.5)
      y += distance / (2 ** 0.5)
      X.append(X[-1] - distance / (2 ** 0.5))
      Y.append(Y[-1] + distance / (2 ** 0.5))

  for i in range(1, len(X)):
    plt.arrow(
      X[i - 1], Y[i - 1], X[i] - X[i - 1], Y[i] - Y[i - 1],
      length_includes_head=True, head_width=0.125, lw=2,
      color=colormap[movements[i - 1][1]]
    )
  
  if y == start[0]:
    if x > start[0]:
      print('East of S')
    elif x < start[0]:
      print('West of S')
    else:
      print('Same location as S')
  elif y > start[1]:
    if x > start[0]:
      print('North-East of S')
    elif x < start[0]:
      print('North-West of S')
    else:
      print('North of S')
  elif y < start[1]:
    if x > start[0]:
      print('South-East of S')
    elif x < start[0]:
      print('South-West of S')
    else:
      print('South of S')

  print(f'Total distance traveled: {total_distance} units')

  plt.title('Movement Map')
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.grid(True)
  plt.legend(handles=patch)
  plt.show()

if __name__ == "__main__":

  # Sample Input:
  # [('3mm', 'N'), ('4.5mm', 'NW'), ('2mm', 'SE')]

  file_path = 'input.txt'
  with open(file_path, 'r') as file:
    file_content = file.read()
  data = eval(file_content)

  start = (0, 0)
  movements = standardise_directions(data)
  plot_movement(start, movements)
