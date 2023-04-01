import csv

filename = './members.csv'

def search_member(name, realm):
    with open(filename, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        data = list(reader)
        for row in data:
            if name == row[0] and realm == row[1]:
                return True
        return False