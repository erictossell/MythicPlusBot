import csv

filename = './top_runs.csv'

def compare_runs(run):
    with open(filename, mode='r') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        data = list(reader)
        for row in data:
            if run.id == row[0]:
                return True
        return False