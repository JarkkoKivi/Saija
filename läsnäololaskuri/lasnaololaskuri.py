################################################
#                                              #
#           THIS IS THE MAIN FILE              #
#                                              #
################################################


import tkinter as tk
from tkinter import Menu, PhotoImage, Scrollbar, TclError, Toplevel
from tkinter.tix import COLUMN, IMAGE
import ikkunat as win
from tkinter import ttk
import calendar as cal
import datetime as date
from db import Sql
from tkinter import simpledialog as dial
from tkinter import messagebox as msg
from writepdf import ToPdf
from tkinter import filedialog
from tkcalendar import Calendar
import locale

locale.setlocale(locale.LC_TIME, 'fi_FI.UTF-8')
TANAAN = date.datetime.today()
saijaDb = Sql("saijaDb")

#saijaDb.lisaa_tiedostosta("tapahtumat.csv")
def pvmToFi(aika:str):
    uusiAika = date.datetime.strftime(date.datetime.strptime(aika, "%Y-%m-%d"), "%d.%m.%Y")
    return uusiAika

def fiPvmToIso(aika:str):
    uusiAika = date.datetime.strftime(date.datetime.strptime(aika, "%d.%m.%Y"), "%Y-%m-%d")
    return uusiAika

class Application(tk.Tk):            
    def __init__(self, master=None):
        tk.Tk.__init__(self, master)  
        self.grid()                     
        self.createWidgets()

    def createWidgets(self):
        self.quitButton = tk.Button(self, text='Lopeta',
            command=self.quit)           
        self.quitButton.grid(row = 6, column = 2, sticky = "SE", pady=20)
        
    def sendButton(self, name:str, x:int, y:int):
        self.send = tk.Button(self, text = name, command = vietapahtumat)
        self.send.grid(row = x, column = y, pady=10)
        
    def deleteButton(self, name:str, x:int, y:int):
        self.deleteButton = tk.Button(self, text = name, command = poistaTapahtuma)
        self.deleteButton.grid(row = x, column = y, pady=10)
        
    def editButton(self, name:str, x:int, y:int):
        self.editButton = tk.Button(self, text = name, command = muokkaaTapahtuma)
        self.editButton.grid(row = x, column = y, pady=10)
        
    def confirmEditButton(self, name:str, x:int, y:int):
        self.confirmEditButton = tk.Button(self, text = name, command = vahvistaMuokkaus)
        self.confirmEditButton.grid(row = x, column = y, pady=10, sticky = "SE")
        
    def addCustomerButton(self, name:str, x:int, y:int):
        self.addCustomerButton = tk.Button(self, text = name, command = lisaaAsiakas)
        self.addCustomerButton.grid(row = x, column = y, sticky="N")
               
        
        
#
#
#   LÄSNÄOLOTYYPPIEN KÄSITTELY
#
#       
        
def lisaaLasnaTyyppi():
    tyyppi = dial.askstring("Lisää läsnäolotyyppi", "Anna uusi läsnäolotyyppi\t\t\t\t\t\t\t")
    if tyyppi != '':
        saijaDb.lisaa_tapahtumatyyppi(tyyppi)
        app.lasna['values'] = haeLasnaoloTyypit()
        app.lasna.current(0)
        msg.showinfo("info", f"{tyyppi} lisätty", parent=app)
    else:
        msg.showerror('Virhe', 'Syötä läsnäolotyyppi', parent=app)
    app.lasna['values'] = haeLasnaoloTyypit()

def muutaLasnaTyyppiIkkuna():
    muutaLasnaIkkuna = win.topLevelWindow(app, "Muuta läsnäolotyyppi")
    muutaLasnaIkkuna.firstLabel("Valitse muutettava läsnäolotyyppi")
    
    tyypit = muutaLasnaIkkuna.firstCombo()
    tyypit['values'] = haeLasnaoloTyypit()
    tyypit.set(tyypit['values'][0])
    
    muutaLasnaIkkuna.secondLabel("Anna uusi läsnäolotyyppi:")
    uusityyppi = muutaLasnaIkkuna.secondEntry()
    
    toiminto = muutaLasnaIkkuna.actionButton("Muuta läsnäolotyyppi")
    toiminto.config(command = lambda: muutaLasnaTyyppi(tyypit.get(), uusityyppi.get()))
    
    def muutaLasnaTyyppi(tyyppi, uusityyppi):
        if uusityyppi != '':
            ok = muutaLasnaIkkuna.message("Muuta läsnäolotyyppi", f"Haluatko varmasti muuttaa läsnäolotyypin {tyyppi} tyypiksi {uusityyppi}?")
            if ok == True:
                
                id = saijaDb.hae_lasnatyypin_id(tyyppi)
                saijaDb.paivita_tapahtumatyyppi(id, uusityyppi)
                tyypit['values'] = haeLasnaoloTyypit()
                tyypit.set(tyypit['values'][0])
                nayta_tiedot()
                app.lasna['values'] = haeLasnaoloTyypit()
                muutaLasnaIkkuna.destroy()
        else:
            msg.showerror('Virhe', 'Syötä uusi läsnäolotyyppi', parent=muutaLasnaIkkuna)
        
    muutaLasnaIkkuna.closeButton()        

def poistaLasnaTyyppiIkkuna():
    poistaLasnaIkkuna = win.topLevelWindow(app, "Poista läsnäolotyyppi")
    poistaLasnaIkkuna.firstLabel("Valitse poistettava läsnäolotyyppi")
    
    tyypit = poistaLasnaIkkuna.firstCombo()
    tyypit['values'] = haeLasnaoloTyypit()
    try:
        tyypit.current(0)
    except TclError:
        pass 
    
    toiminto = poistaLasnaIkkuna.actionButton("Poista läsnäolotyyppi")
    toiminto.config(command = lambda: poistaLasnaTyyppi(tyypit.get()))
    
    def poistaLasnaTyyppi(tyyppi):
        ok = poistaLasnaIkkuna.message("Poista läsnäolotyyppi",f"Haluatko varmasti poistaa läsnäolotyypin: {tyyppi}?\n\nToiminto poistaa myös kaikki poistettavan tyypin tapahtumat. Toimintoa ei voi perua!")
        if ok == True:
            saijaDb.poistaLasnaTyyppi(tyyppi)
            app.lasna['values'] = haeLasnaoloTyypit()
            tyypit['values'] = haeLasnaoloTyypit()
            try:
                tyypit.current(0)
                app.lasna.current(0)
            except TclError:
                tyypit.set('')
                app.lasna.set('')
            nayta_tiedot()
            poistaLasnaIkkuna.destroy()
    
    poistaLasnaIkkuna.closeButton()
    
#############################
#                           #
#   HENKILÖIDEN RAPORTIT    #
#                           #
#############################

def asiakasRaportit():
    asRaportitIkkuna = win.reportWindows(app, "Raportit henkilöittäin")
    asRaportitIkkuna.firstLabel("Valitse asiakas:")
    combo = asRaportitIkkuna.firstCombo()
    combo["values"] = tuoHenkilot()
    try:
        combo.current(0)
    except TclError:
        pass
    #combo.set(combo['values'][0])
    aika = asRaportitIkkuna.aikavali()
    toiminto = asRaportitIkkuna.actionButton("Hae tiedot")
    tulosta = asRaportitIkkuna.tulostaNappi()
    tulosta.config(command=lambda: tulostaAsiakastiedot(combo.get(), (aika[0].get(), aika[1].get())))
    henkilotiedotFrame = asRaportitIkkuna.asiakastiedotFrame()
    toiminto.config(command=lambda: tuoAsiakastiedot(combo.get(), (aika[0].get(), aika[1].get())))
    tietoikkuna = asRaportitIkkuna.tietoIkkuna()
    
    def tuoAsiakastiedot(asiakas:str, aikavali:tuple):
        if asiakas != '':
            aikavali = (fiPvmToIso(aikavali[0]), fiPvmToIso(aikavali[1]))
            tapahtumalistaus = saijaDb.hae_henkilon_tapahtumat(asiakas, aikavali)
            if tapahtumalistaus != None:
                for widgets in henkilotiedotFrame.winfo_children():
                    widgets.destroy()
                tapahtumat = saijaDb.laskeHenkilonLasnaolot(asiakas, aikavali)
                asRaportitIkkuna.frameLabelIkkuna(henkilotiedotFrame, asiakas)
                for lasnaolo in tapahtumat:
                    teksti = f"{lasnaolo}: {tapahtumat[lasnaolo]} kpl"
                    asRaportitIkkuna.frameLabelIkkuna(henkilotiedotFrame, teksti)
                for item in tietoikkuna.get_children():
                    tietoikkuna.delete(item)
                for tapahtuma in tapahtumalistaus:
                    id, pvm, nimi, lasna = tapahtuma
                    pvm = pvmToFi(pvm)
                    tietoikkuna.insert('', 0, text="1", values = (id, pvm, nimi, lasna))
            else:
                msg.showinfo('info', "Asiakkaalla ei tapahtumia", parent=henkilotiedotFrame)
        else:
            msg.showerror('Virhe', 'Lisää ensin asiakas', parent=henkilotiedotFrame)
            
    def tulostaAsiakastiedot(asiakas:str , aikavali:tuple):
        if asiakas != '':
            aikavaliIso = (fiPvmToIso(aikavali[0]), fiPvmToIso(aikavali[1]))
            tallenna = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=[("pdf files", "*.pdf")], title="Tallenna pdf")
            sanakirja = {}
            aika = date.date.today()
            aika = date.datetime.strftime(aika, "%d.%m.%Y")
            pdf = ToPdf()
            pdf.headline(f"{asiakas}")
            pdf.headline2(f"Läsnäolot aikavälillä {aikavali[0]} - {aikavali[1]}")
            tapahtumat = saijaDb.laskeHenkilonLasnaolot(asiakas, aikavaliIso)
            for lasnaolo in tapahtumat:
                sanakirja[lasnaolo]=[]
            tapahtumalistaus = saijaDb.hae_henkilon_tapahtumat(asiakas, aikavaliIso)
            for tapahtuma in tapahtumalistaus:
                pvm = date.datetime.strptime(tapahtuma[1], "%Y-%m-%d")
                pvm = date.datetime.strftime(pvm, "%a %d.%m.%Y")
                sanakirja[tapahtuma[3]].append(pvm)
            for kirja in sorted(sanakirja):
                teksti = f"{kirja}: {len(sanakirja[kirja])} kpl"
                pdf.tapahtumalistaOtsikot(teksti)
                pdf.tapahtumalista(sanakirja[kirja])
            if tallenna.endswith(".pdf"):
                pdf.output(tallenna)
            else:
                pdf.output(f"{tallenna}.pdf")
        else:
            msg.showerror('Virhe', 'Lisää ensin asiakas', parent=henkilotiedotFrame)

    asRaportitIkkuna.closeButton()
    
#############################
#                           #
#   TAPAHTUMA RAPORTIT      #
#                           #
#############################

def tapahtumaraportit():
    tapahtumaRaporttiIkkuna = win.reportWindows(app, "Tapahtumaraportti")
    aika = tapahtumaRaporttiIkkuna.aikavali()
    toiminto = tapahtumaRaporttiIkkuna.actionButton("Hae tiedot")
    tulosta = tapahtumaRaporttiIkkuna.tulostaNappi()
    tulosta.config(command=lambda: tulostaTapahtumatiedot( (aika[0].get(), aika[1].get())))
    
    toiminto.config(command=lambda: tuoTapahtumatiedot((aika[0].get(), aika[1].get())))
    def tulostaTapahtumatiedot(aikavali:tuple):
        aikavaliIso = (fiPvmToIso(aikavali[0]), fiPvmToIso(aikavali[1]))
        tallenna = filedialog.asksaveasfilename(confirmoverwrite=True, filetypes=[("Pdf files", "*.pdf")], title="Tallenna pdf")
        aika = date.date.today()
        aika = date.datetime.strftime(aika, "%Y-%m-%d")
        pdf = ToPdf()
        pdf.headline(f"Tapahtumaraportti")
        pdf.headline2(f"Tapahtumat aikavälillä {aikavali[0]} - {aikavali[1]}")
        tapahtumalista = saijaDb.tuo_tapahtuma_raportti(aikavaliIso)
        for tapahtuma in tapahtumalista:
            pdf.divider(pdf.get_y())
            pvm = date.datetime.strptime(tapahtuma, "%Y-%m-%d")
            pvm = date.datetime.strftime(pvm, "%a %d.%m.%Y")
            pdf.headline(pvm)
            for lasna in tapahtumalista[tapahtuma]:
                pdf.tapahtumalistaOtsikot(lasna)
                pdf.tapahtumalista(tapahtumalista[tapahtuma][lasna])
        if tallenna.endswith(".pdf"):
            pdf.output(tallenna)
        else:
            pdf.output(f"{tallenna}.pdf")
                
    def tuoTapahtumatiedot(aikavali:tuple):
        aikavaliIso = (fiPvmToIso(aikavali[0]), fiPvmToIso(aikavali[1]))
        henkilotiedotFrame = tapahtumaRaporttiIkkuna.tapahtumaRaporttiFrame()
        for tieto in henkilotiedotFrame.winfo_children():
            tieto.destroy()
        tapahtumalista = saijaDb.tuo_tapahtuma_raportti(aikavaliIso)
        otsikko = tk.Label(henkilotiedotFrame, text=f"Tapahtumat aikavälillä {aikavali[0]} - {aikavali[1]}" , font=('Arial bold', 14)).grid(row=0, column=0, pady=10, columnspan=2)
        hv = ttk.Separator(henkilotiedotFrame, orient='horizontal')
        hv.grid(row=1, column=0, columnspan=99, sticky='ew', pady=20)
        x=2
        for pv in tapahtumalista:
            pvm = date.datetime.strftime(date.datetime.strptime(pv, "%Y-%m-%d"), "%a %d.%m.%Y")
            label = tk.Label(henkilotiedotFrame)
            label.grid(row=x, column=0)
            label.config(text=pvm)
            x += 1
            for lasna in tapahtumalista[pv]:
                label = tk.Label(henkilotiedotFrame, wraplength=400, justify='left')
                label.grid(row=x, column=1, sticky='w',columnspan=2)
                label.config(text=f"{lasna}:\n{', '.join(tapahtumalista[pv][lasna])}")
                x += 1
            hr = ttk.Separator(henkilotiedotFrame, orient='horizontal')
            hr.grid(row=x, column=0, columnspan=99, sticky='ew', pady=20)
            x += 1
        
    tapahtumaRaporttiIkkuna.closeButton()

    
#############################
#                           #
#   HENKILÖIDEN KÄSITTELY   #
#                           #
#############################
       
def lisaaAsiakas():
    hlo = dial.askstring("Lisää henkilö", "Anna Nimi\t\t\t\t\t\t\t")
    if hlo != None:
        saijaDb.lisaa_henkilo(hlo)
        tuo_asiakkaat()
    msg.showinfo("info", f"{hlo} lisätty", parent=app)
    tuo_asiakkaat()
    
def muokkaaAsiakas():
    muutaAsiakas = win.topLevelWindow(app, "Muuta asiakas")
    muutaAsiakas.firstLabel("Valitse muokattava asiakas")
    boxi = muutaAsiakas.firstCombo()
    boxi['values'] = tuoHenkilot()
    boxi.set(boxi['values'][0])
    
    muutaAsiakas.secondLabel("Anna uusi nimi:")
    uusiNimi = muutaAsiakas.secondEntry()
    toiminto = muutaAsiakas.actionButton("Lähetä")
    toiminto.config(command=lambda: muutaAsiakasDb(boxi.get(), uusiNimi.get()))
    muutaAsiakas.closeButton()
    def muutaAsiakasDb(vanhaNimi, uusiNimi):
        ok = muutaAsiakas.message("Muuta asiakas",f"Haluatko muuttaa asiakkaan {vanhaNimi} nimeksi {uusiNimi}?")
        if ok == True:
            id = saijaDb.hae_henkilo_id(vanhaNimi)
            saijaDb.paivita_henkilo(id, uusiNimi)
            boxi['values'] = tuoHenkilot()
            tuo_asiakkaat()
            nayta_tiedot()
            muutaAsiakas.destroy()
            
def poistaAsiakas():
    poistaAsiakasIkkuna = win.topLevelWindow(app, "Poista henkilö")
    poistaAsiakasIkkuna.firstLabel("Valitse poistettava henkilö")
    asiakasboxi = poistaAsiakasIkkuna.firstCombo()
    asiakasboxi['values'] = tuoHenkilot()
    asiakasboxi.set(asiakasboxi["values"][0])
    toiminto = poistaAsiakasIkkuna.actionButton("Poista henkilö")
    toiminto.config(command=lambda: poistaAsiakasDb(asiakasboxi.get()))
    def poistaAsiakasDb(asiakas):
        ok = poistaAsiakasIkkuna.message("Poista henkilö", f"Haluatko varmasti poistaa henkilön: {asiakas}?\n\nToiminto poistaa myös kaikki henkilön tapahtumat. Toimintoa ei voi perua!")
        if ok == True:
            id = saijaDb.hae_henkilo_id(asiakas)
            saijaDb.poista_henkilo(id, asiakas)
            asiakasboxi['values'] = tuoHenkilot()
            tuo_asiakkaat()
            nayta_tiedot()
            poistaAsiakasIkkuna.destroy()
    poistaAsiakasIkkuna.closeButton()
    
    


#############################
#                           #
#   TAPAHTUMIEN MUOKKAUS    #
#                           #
#############################
        

def vahvistaMuokkaus():
    print("muutos vahvistettu")

def muokkaaTapahtuma():
    item = app.naytatiedot.selection()
    itemObj = app.naytatiedot.item(item[0])
    itemObj["values"][0]
    app.editEntryId.config(text = itemObj["values"][0])
    app.editEntryPvm.insert(0, itemObj["values"][1])
    app.editEntryName.config(text = itemObj["values"][2])
    app.editEntryLasna.insert(0, itemObj["values"][3])
     
def poistaTapahtuma():
    
    item = app.naytatiedot.selection()
    itemObj = app.naytatiedot.item(item[0])
    tarkista = msg.askokcancel("Poista tapahtuma", f"Haluatko varmasti poistaa tapahtuman id: {itemObj['values'][0]}\n({itemObj['values'][1]} | {itemObj['values'][2]} | {itemObj['values'][3]}) ?")
    id = itemObj["values"][0]
    if tarkista == True:
        saijaDb.poista_tapahtuma(id)
        nayta_tiedot()
        msg.showinfo("Info", "Tapahtuma poistettu")
    else:
        pass

def vietapahtumat():
    asiakkaat = app.listbox.curselection()
    pvm = app.pvm.selection_get()
    lasnaolot = saijaDb.hae_lasnatyypin_id(app.lasna.get())
    p = 0
    if len(asiakkaat) != 0 and lasnaolot != None:
        for asiakas in asiakkaat:      
            hloid = saijaDb.hae_henkilo_id(app.listbox.get(asiakas))
            hlo = app.listbox.get(asiakas)
            if tarkista_tapahtumat((str(pvm), hlo)) == False:
                saijaDb.lisaa_tapahtuma(str(pvm), hloid, lasnaolot)
                p += 1
            else:
                vahvista = msg.askokcancel("Haluatko jatkaa?", f"Asiakkaalla on jo tapahtumatieto tälle päiväykselle. Haluatko päivittää olemassa olevan tapahtuman tiedot --> {str(pvm), hlo, app.lasna.get()}?")
                if vahvista == True:
                    saijaDb.lisaa_tapahtuma(str(pvm), hloid, lasnaolot)
                    p += 1
                else:
                    continue
        nayta_tiedot()
        msg.showinfo("info", f"{p} tapahtumaa lisätty", parent=app)
    else:
        msg.showerror('Virhe', 'Tarkista asiakas ja läsnäolotyyppi!', parent=app)
    
    
    
    
#############################
#                           #
#   TIETOJEN HAKU           #
#                           #
#############################
  

def tarkista_tapahtumat(tiedot:tuple):
    check = False
    tapahtumalistaus = saijaDb.tuo_kaikki_tapahtumatiedot()
    for tapahtuma in tapahtumalistaus:
        if tiedot[0] == tapahtuma[1] and tiedot[1] == tapahtuma[2]:
            check = True 
    return check
    
# HAKEE TAPAHTUMALISTAUKSEN 


def nayta_tiedot():
    for item in app.naytatiedot.get_children():
        app.naytatiedot.delete(item)
    tapahtumalistaus = saijaDb.tuo_kaikki_tapahtumatiedot()
    for tapahtuma in tapahtumalistaus:
        id, pvm, nimi, lasna = tapahtuma
        pvm = pvmToFi(pvm)
        app.naytatiedot.insert('', 0, text="1", values = (id, pvm, nimi, lasna))

def tuoHenkilot():
    lista = []
    asiakkaat = saijaDb.hae_henkilot(('all',))
    for asiakas in asiakkaat:
        lista.append(asiakas[1])
    return lista

def tuo_asiakkaat():
    app.listbox.delete(0, "end")
    asiakkaat = saijaDb.hae_henkilot(("all",))
    for asiakas in asiakkaat:
        app.listbox.insert("end", asiakas[1])
        
def tuo_henkilot(values:ttk.Combobox):
    lista = []
    asiakkaat = saijaDb.hae_henkilot(("all",))
    for asiakas in asiakkaat:
        lista.append(asiakas[1])
    values['values']=lista
    

def tuo_paivat():
    paivaykset = []
    kalenteri = cal.Calendar(1)
    vuosikalenteri = kalenteri.yeardatescalendar(year = 2022)
    for vuosi in vuosikalenteri:
        for kuukausi in vuosi:
            for viikko in kuukausi:
                for paiva in viikko: 
                    paivaykset.append(date.datetime.strftime(paiva, "%d.%m.%Y"))
    app.paivat['values'] = paivaykset
    app.paivat.set(date.date.today().strftime("%d.%m.%Y"))

def haeLasnaoloTyypit():
    return [f"{y}" for x, y in saijaDb.hae_tapahtumatyypit()]



#############################
#                           #
#   MAIN APPLICATION        #
#                           #
#############################
app = Application()



#############################
#                           #
#   MENUBAR                 #
#                           #
#############################

# create a menubar
menubar = Menu(app)
app.config(menu=menubar)

# create a menu
henkilot_menu = Menu(menubar, tearoff=False)
lasnaolot_menu = Menu(menubar, tearoff=False)
raportit_menu = Menu(menubar,tearoff=False)

# add a menu item to the menu

#
#
#   HENKILÖT MENU
#
#

henkilot_menu.add_command(
    label='Lisää Henkilö',
    command=lisaaAsiakas
)

henkilot_menu.add_command(
    label='Muokkaa Henkilöä',
    command=muokkaaAsiakas
)

henkilot_menu.add_command(
    label='Poista Henkilö',
    command=poistaAsiakas
)

#
#
#   LÄSNÄOLOTYYPIT MENU
#
#

lasnaolot_menu.add_command(
    label='Lisää Läsnäolotyyppi',
    command=lisaaLasnaTyyppi
)

lasnaolot_menu.add_command(
    label='Muokkaa Läsnäolotyyppiä',
    command=muutaLasnaTyyppiIkkuna
)

lasnaolot_menu.add_command(
    label='Poista Läsnäolotyyppi',
    command=poistaLasnaTyyppiIkkuna
)

#
#
#   RAPORTIT MENU
#
#

raportit_menu.add_command(
    label='Henkilöt',
    command= asiakasRaportit
)

raportit_menu.add_command(
    label='Tapahtumat',
    command = tapahtumaraportit
)


#
#
#   PÄÄMENUT (MENUBAR)
#
#

# add the File menu to the menubar
menubar.add_cascade(
    label="Henkilöt",
    menu=henkilot_menu
)
menubar.add_cascade(
    label="Läsnätyyppi",
    menu=lasnaolot_menu
)
menubar.add_cascade(
    label="Raportit",
    menu=raportit_menu
)


app.paiva = tk.Label(app)
app.paiva.config(text = "Päiväys")
app.paiva.grid(row = 0, column = 0)

app.asiakas = tk.Label(app)
app.asiakas.config(text = "Asiakas")
app.asiakas.grid(row = 0, column = 2) 

app.lasnalabel = tk.Label(app)
app.lasnalabel.config(text = "Läsnäolotyyppi")
app.lasnalabel.grid(row = 0, column = 1)

#
#
#   PÄÄIKKUNAN NAPIT
#
#
                  
app.title('Saija')
photo = PhotoImage(file="saija logo.png")
app.iconphoto(True, photo)
app.geometry('700x700')
app.sendButton("Lisää tapahtuma(t)", 2, 2)
app.deleteButton("Poista", 5, 2)
#app.editButton("Muokkaa", 5, 1)
#app.confirmEditButton("Lähetä", 5, 3)

#
#
#   PÄÄIKKUNAN ASIAKASLISTA
#
#

app.listbox = tk.Listbox(app, selectmode="multiple")
tuo_asiakkaat()
app.listbox.grid(row = 1, column = 2, padx=20, sticky="nsw")
lstboxScbar = Scrollbar(app, orient='vertical')
lstboxScbar.grid(row = 1, column = 2, sticky="nse")
app.listbox.configure(yscrollcommand=lstboxScbar.set)
lstboxScbar.configure(command=app.listbox.yview)


#
#
#   PÄÄIKKUNAN PÄIVÄYKSET
#
#

# app.paivat = ttk.Combobox(app)
# tuo_paivat() 
# app.paivat.grid(row = 1, column = 0, sticky = "N", padx=20)

app.pvm = Calendar(app, year=TANAAN.year, month=TANAAN.month, day=TANAAN.day, locale='fi_FI')
app.pvm.grid(row = 1, column = 0, sticky = "N", padx=20)

#
#
#   PÄÄIKKUNAN LÄSNÄOLOTYYPIT
#
#

app.lasna = ttk.Combobox(app)
app.lasna['values'] = haeLasnaoloTyypit()
try:
   app.lasna.current(0)
except TclError:
    pass
haeLasnaoloTyypit()
app.lasna.grid(row = 1, column = 1, sticky = "N", padx=10)

########## POISTETTAVA??? ##########

# app.editEntryId = tk.Label(app)
# app.editEntryPvm = tk.Entry(app)
# app.editEntryName = tk.Label(app)
# app.editEntryLasna = tk.Entry(app)
# app.editEntryId.grid(row = 6, column = 0, pady = 10)
# app.editEntryPvm.grid(row = 6, column = 1, pady = 10)
# app.editEntryName.grid(row = 6, column = 2, pady = 10)
# app.editEntryLasna.grid(row = 6, column = 3, pady = 10)

#
#
#   PÄÄIKKUNAN TAPAHTUMALISTAUS (TREEVIEW)
#
#
tapahtumalabel = tk.Label(app, text="Kaikki tapahtumat", font=('Arial bold', 14))
tapahtumalabel.grid(row=3, column=0, sticky='sw', padx=30)

app.naytatiedot = ttk.Treeview(app, column=("c1", "c2", "c3", "c4"), show='headings', height=10)
app.naytatiedot.column("# 1", anchor="center", minwidth=0, width=50, stretch="no")
app.naytatiedot.heading("# 1", text="ID")
app.naytatiedot.column("# 2", anchor="w", minwidth=0, width=100, stretch="no")
app.naytatiedot.heading("# 2", text="Päivämäärä", anchor="w")
app.naytatiedot.column("# 3", anchor="w")
app.naytatiedot.heading("# 3", text="Nimi", anchor="w")
app.naytatiedot.column("# 4", anchor="w")
app.naytatiedot.heading("# 4", text="Läsnäolo", anchor="w")
app.naytatiedot.grid(row=4, column=0, columnspan = 3, padx=10, pady=10)
nayta_tiedot()
fpEventsScbar = Scrollbar(app, orient='vertical')
fpEventsScbar.grid(row = 4, column = 2, sticky="nse")
app.naytatiedot.configure(yscrollcommand=fpEventsScbar.set)
fpEventsScbar.configure(command=app.naytatiedot.yview)


app.mainloop()    