import csv

class CRM():

    def __init__(self, file_path):
        
        self.records = []

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.records.append({
                    'business': row[0],
                    'email': row[1],
                    'name': row[2],
                    'info': row[3],
                    'result':''
                })

    def delete(self,idx):
        del self.records[idx]

    @property
    def length(self):
        return len(self.records)

    def __getitem__(self, index):
        return self.records[index]