import datetime
import csv
from operator import indexOf
class Customer:
    def __init__(self, name:str):
        self.name = name
        
    def __str__(self):
        return self.name
    
class Events:
    __id = 1
    def __init__(self, pvm:str, customer:Customer, event:int ):
        pvm = pvm.strip()
        d = pvm.rsplit(".")
        self.id = Events.__id
        Events.__id += 1
        self.date = datetime.date(int(d[2]),int(d[1]), int(d[0]))
        self.customer = Customer(customer)
        self.event = event
        
    def __str__(self):
        return f"{self.id}, {self.date.day}.{self.date.month}.{self.date.year}, {self.customer}, {self.event}"
    
    def get_values(self):
        lasna = ''
        if self.event == "1":
            lasna = "Läsnä"
        elif self.event == "2":
            lasna = "Luvaton poissaolo"
        elif self.event == "3":
            lasna = "Selvitetty poissaolo"
        elif self.event == "4":
            lasna = "Sairasloma"  
        return (self.id, self.date, self.customer, lasna)
        
class EventList:
    
    def __init__(self, eventlist:list):
        self.eventlist = eventlist         
        
    def listaus(self):
        for event in self.eventlist:
            print(event)
        # for event in self.eventlist:
        #     for part in event:
        #         print(part.id, part.date, part.customer, part.event )
                
def filereader(file:str):
    eventlist = []
    with open(file, encoding='UTF8',  newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)
        for row in reader:
            event = Events(row[0], row[1], row[2])
            eventlist.append(event)
    return eventlist

def customerreader(file:str):
    lista = []
    with open(file, encoding="UTF8", newline="") as customerlist:
        reader = csv.reader(customerlist, delimiter = ";")
        next(reader)
        for customer in reader:
            lista.append(customer)

    return lista
    
    
if __name__ == "__main__":
    lista = filereader("tapahtumat.csv")
    for event in lista:
        tuple = event.get_values()
        for value in tuple:
            print(value)
            
    customerreader("customers.csv")
    
            
            
        
        
        