import pandas as pd

class Database:
  def __init__(self):
    self.df = pd.DataFrame(columns=[
      'First Name',
      'Last Name',
      'Roll Number',
      'Course Name',
      'Semester',
      'Exam Type',
      'Total Marks',
      'Scored Marks'
      ]
    )
  
  def get_attributes(self):
    return self.df.columns
  
  def import_csv(self, file_path):
    try:
      self.df = pd.read_csv(file_path)
      print('Entries loaded successfully from CSV.')
    except FileNotFoundError:
      print('File not found. No entries loaded.')

  def export_csv(self, file_path):
    try:
      self.df.to_csv(file_path, index=False)
      print('Entries save successfully to CSV.')
    except Exception as e:
      print(f'Error: {e}')

  def display(self):
    if not self.df.empty:
      print(self.df.to_string(index=False))
    else:
      print('No entries found.')

  def insert_row(self, row):
    self.df = pd.concat([self.df, pd.DataFrame([row])], ignore_index=True)
    print('Entry added successfully.')

  def delete_row(self, index):
    if 0 <= index and index < self.df.shape[0]:
      self.df = self.df.drop(index)
      print('Entry removed successfully.')
    else:
      print('Index out of bound. No entry was removed.')

  def update(self, index, attribute, new_value):
    if 0 <= index and index < self.df.shape[0]:
      if attribute in self.get_attributes():
        self.df.at[index, attribute] = new_value
        print('Entry updated successfully.')
      else:
        print('Attribute not found. No entry was updated.')
    else:
      print('Index out of bound. No entry was updated.')

  def search(self, attribute, value):
    if attribute in self.get_attributes():
      results = self.df[self.df[attribute] == value]
      if not results.empty:
        print(results.to_string(index=False))
      else:
        print('No such entry found.')
    else:
      print('Attribute not found. No entry was updated.')

directory = Database()
print('Welcome to Marks Directory!')
print('Note: All indices are assumed to start from zero.')

while True:
  print('\nSupported Operations:')
  print('1. Load entries from CSV')
  print('2. Save entries to CSV')
  print('3. Display all entries')
  print('4. Add new entry')
  print('5. Remove entry')
  print('6. Update entry')
  print('7. Search entries')
  print('8. Exit')

  choice = input('Enter your choice (1-8): ')
  
  if choice == '1':
    file_path = input('Enter CSV file path: ')
    directory.import_csv(file_path)

  elif choice == '2':
    file_path = input('Enter CSV file path: ')
    directory.export_csv(file_path)

  elif choice == '3':
    directory.display()

  elif choice == '4':
    row = {}
    for attr in directory.get_attributes():
      row[attr] = input(f'Enter {attr}: ')
    directory.insert_row(row)

  elif choice == '5':
    index = int(input('Enter the index of the entry to remove: '))
    directory.delete_row(index)

  elif choice == '6':
    index = int(input('Enter the index of the entry to update: '))
    attr = input('Enter the attribute to update: ')
    val = input('Enter the new value: ')
    directory.update(index, attr, val)

  elif choice == '7':
    attr = input('Enter the attribute for search: ')
    val = input('Enter the value to search: ')
    directory.search(attr, val)

  elif choice == '8':
    break

  else:
    print('Please enter a number between 1 and 8.')
