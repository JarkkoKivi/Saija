import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as msg
from db import Sql as data
import calendar as cal
from datetime import date
from datetime import timedelta
from datetime import datetime

    
class topLevelWindow(tk.Toplevel):
    def __init__(self, parent, title:str):
        super().__init__(parent)
        self.grab_set() 
        self.title(title)
        self.geometry("400x300")
    
    def firstLabel(self, label:str):
        teksti = tk.Label(self)
        teksti.config(text=label)
        teksti.pack(pady=10)
    
    def firstCombo(self):  
        tyypit = ttk.Combobox(self)
        
        tyypit.pack()
        return tyypit
        
    def secondLabel(self, label:str):  
        uusityyppiLabel = tk.Label(self)
        uusityyppiLabel.config(text=label)
        uusityyppiLabel.pack(pady=10)
    
    def secondEntry(self):    
        uusityyppi = tk.Entry(self)
        uusityyppi.pack()
        return uusityyppi
    
    def message(self,title:str, text:str):
        return msg.askyesno(title, text)

    
    def actionButton(self, text:str):
        removeTypeButton = tk.Button(self, text = text)
        removeTypeButton.pack(pady=10)
        return removeTypeButton
        
    def closeButton(self):   
        closeWindowButton = tk.Button(self, 
                                    text = "Sulje ikkuna", 
                                    command = lambda: self.destroy())
        closeWindowButton.pack(pady=20, side="bottom")
        
class reportWindows(topLevelWindow):
    def __init__(self, parent, title:str):
        super().__init__(parent, title)
        super().geometry("600x600")
        
    def aikavali(self):
        today = date.today()
        lastday = cal.monthrange(today.year, today.month)[1]
        vuosiPaivina = []
        kalenteri = cal.TextCalendar(0)
        for i in range(1,3):
            vuosi = kalenteri.yeardatescalendar((today.year -2 + i))
            for kuukausi in vuosi:
                for viikko in kuukausi:
                    for pv in viikko:
                        for d in pv:
                            d = datetime.strftime(d, "%d.%m.%Y")
                            if not d in vuosiPaivina:
                                vuosiPaivina.append(d)
            
        aikaLabel = tk.Label(self, text="Anna Aikaväli:")
        aikaLabel.pack()
        alku = ttk.Combobox(self)
        alku["values"] = [pv for pv in vuosiPaivina]
        alku.set(datetime.strftime(today.replace(day=1), "%d.%m.%Y" ))
        loppu = ttk.Combobox(self)
        loppu["values"] = [pv for pv in vuosiPaivina]
        loppu.set(datetime.strftime(today.replace(day=lastday), "%d.%m.%Y"))
        alku.pack()
        loppu.pack()
        return (alku, loppu)
    
    def tapahtumaRaporttiFrame(self):
        atframe = tk.Toplevel(self)
        atframe.geometry('500x600')
        atframe.title('Tapahtumaraportti')
        kanvaasi = tk.Canvas(atframe, relief='sunken', bd=1)
        kanvaasi.pack(side='left', ipady=10, ipadx=10, fill='both', expand=1)
        scbar = ttk.Scrollbar(atframe, orient='vertical', command=kanvaasi.yview)
        scbar.pack(side='right', fill='y')
        kanvaasi.configure(yscrollcommand=scbar.set)
        kanvaasi.bind('<Configure>', lambda e: kanvaasi.configure(scrollregion=(kanvaasi.bbox("all"))))
        tietoFrame = ttk.Frame(kanvaasi, padding=10)
        kanvaasi.create_window((0,0), window=tietoFrame, anchor="nw")
        return tietoFrame
    
    def asiakastiedotFrame(self):
        atframe = tk.LabelFrame(self, border=0)
        atframe.pack(fill='x', expand=1, ipady=10)
        return atframe
    
    # def tapahtumaTreeView(self):
    #     treeFrame = ttk.Frame(self, height=200)
    #     treeFrame.pack(fill='x', expand=1, pady=20, padx=50)
    #     tree = ttk.Treeview(treeFrame, padding=(20), show='tree')
    #     tree.pack(side='left', fill='both', expand=1)
    #     treeboxScbar = ttk.Scrollbar(treeFrame, orient='vertical')
    #     treeboxScbar.pack(side='right', fill='y', expand=1)
    #     tree.configure(yscrollcommand=treeboxScbar.set)
    #     treeboxScbar.configure(command=tree.yview)
    #     return tree
    
    # def updateTreeview(self, tree:ttk.Treeview, sanakirja:dict, aikavali:tuple):
    #     for item in tree.get_children():
    #         # for child in item.get_children():
    #         #     for i in child.get_children():
    #         #         child.delete(i)
    #         #     item.delete(child)
    #         tree.delete(item)
        
    #     i = 0
    #     j = 0
    #     k = 0
    #     for pvm in sanakirja:
    #         tree.insert('', 'end', "pvm" + str(i), text=pvm)
    #         for lasna in sanakirja[pvm]:
    #             tree.insert("pvm" + str(i), 'end', "lasna" + str(j), text=lasna)
    #             tree.move('lasna'+ str(j), 'pvm'+ str(i), 'end')    
    #             for nimi in sorted(sanakirja[pvm][lasna]):
    #                 tree.insert("lasna" + str(j), 'end', 'nimi'+str(k), text=nimi)
    #                 tree.move('nimi'+ str(k), 'lasna' + str(j), 'end')
    #                 k+=1
    #             j += 1
    #         i += 1  
        

    def frameLabel(self, teksti):
        label = tk.Label(self, text = teksti, justify="left" )
        label.pack(fill="x")
        
    def frameLabelIkkuna(self,ikkuna, teksti:str):
        label = tk.Label(ikkuna, text = teksti, justify="left")
        label.pack(fill="x")      
    
    def textiLabel(self, teksti):
        label = tk.Label(self, text = teksti )
        label.pack(expand = True, fill="x")
        
    def tulostaNappi(self):
        nappi = tk.Button(self, text="Tulosta PDF")
        nappi.pack()
        return nappi
    
    def tietoIkkuna(self):
        henkilotietoFrame =  ttk.Frame(self, height=200)
        henkilotietoFrame.pack(fill='x', expand=True)
        naytatiedot = ttk.Treeview(henkilotietoFrame, column=("c1", "c2", "c3", "c4"), show='headings', height=7)
        naytatiedot.column("# 1", anchor="center", minwidth=0, width=50, stretch="no")
        naytatiedot.heading("# 1", text="ID")
        naytatiedot.column("# 2", anchor="w", minwidth=0, width=100, stretch="no")
        naytatiedot.heading("# 2", text="Päivämäärä", anchor="w")
        naytatiedot.column("# 3", anchor="w")
        naytatiedot.heading("# 3", text="Nimi", anchor="w")
        naytatiedot.column("# 4", anchor="w")
        naytatiedot.heading("# 4", text="Läsnäolo", anchor="w")
        naytatiedot.pack(side='left', expand = True, fill='both', padx=10)
        naytatiedotScBar = ttk.Scrollbar(henkilotietoFrame, orient='vertical')
        naytatiedotScBar.pack(side='right', fill='y', expand=True)
        naytatiedot.configure(yscrollcommand=naytatiedotScBar.set)
        naytatiedotScBar.configure(command=naytatiedot.yview)
        return naytatiedot
    
# if __name__ == "__main__":
#     # kalenteri = cal.TextCalendar(0)
#     # vuosi = kalenteri.yeardatescalendar(2022)
#     # for kuukausi in vuosi:
#     #     for viikko in kuukausi:
#     #         for pv in viikko:
#     #             for d in pv:
#     #                 print(d.day, d.month, d.year)
    
#     # kuukausia = kalenteri.itermonthdates(2022, 2)
#     today = date.today()
#     d = cal.monthrange(today.year, today.month)[1]
#     print(d)
    
#     vuosiPaivina = []
#     kalenteri = cal.TextCalendar(0)
#     for i in range(1,3):
#         vuosi = kalenteri.yeardatescalendar((today.year -2 + i))
#         for kuukausi in vuosi:
#             for viikko in kuukausi:
#                 for pv in viikko:
#                     for d in pv:
#                         d = datetime.strftime(d, "%d.%m.%Y")
#                         if not d in vuosiPaivina:
#                             vuosiPaivina.append(d)
#     print(vuosiPaivina)