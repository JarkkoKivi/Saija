import sqlite3
import datahandlers as data
from datetime import date, datetime
class Sql:
    def __init__(self, db:str):
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()
        self.__create_tables()
        
    def __create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS henkilot (id INTEGER PRIMARY KEY,
                                                             name text UNIQUE NOT NULL, 
                                                             liittynyt text)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS lasnatyypit (id INTEGER PRIMARY KEY,
                                                                    tyyppi TEXT UNIQUE)""")
        self.cur.execute("""CREATE TABLE IF NOT EXISTS tapahtumat (id INTEGER PRIMARY KEY,
                                                                    date TEXT, 
                                                                    hloid INT, 
                                                                    lasna INTEGER,
                                                                    FOREIGN KEY (hloid) REFERENCES henkilot (id) ON UPDATE CASCADE ON DELETE CASCADE,
                                                                    FOREIGN KEY (lasna) REFERENCES lasnatyypit(id) ON UPDATE CASCADE ON DELETE CASCADE)""")
        
        self.con.commit()
        # self.cur.execute("""INSERT OR IGNORE INTO lasnatyypit(tyyppi) VALUES ("Läsnä"), ("Luvaton poissaolo"), ("Selvitetty Poissolo"), ("Sairasloma")""")
        # self.con.commit()
        
    def lisaa_tiedostosta(self, tiedosto: str):
        tiedot = data.filereader(tiedosto)
        for tieto in tiedot:
            id, pvm, nimi, lasna = tieto.get_values()
            pvmstr = f"{pvm.year}-{pvm.month}-{pvm.day}"
            lasnaNo = self.__lasna_numeroiksi(lasna)
            tanaan = date.today()
            tanaan = tanaan.isoformat()
            self.cur.execute("""INSERT OR IGNORE INTO henkilot(name, liittynyt) VALUES (?,?)""",(str(nimi), str(tanaan)))
            self.con.commit()
            
            self.cur.execute("Select id from henkilot where name ='"+str(nimi)+"'")
            self.con.commit()
            hloid = self.cur.fetchone()
            self.cur.execute("INSERT INTO tapahtumat(date, hloid, lasna) VALUES(?,?,?)",(str(pvmstr), int(hloid[0]), int(lasnaNo)))
            self.con.commit()
    
    def hae_henkilo_id(self, kohde:str):
        if kohde != '':
            sql= "SELECT id FROM henkilot WHERE name = ?"
            self.cur.execute(sql, (kohde,))
            self.con.commit()
            id = self.cur.fetchone()
            return int(id[0])
        else:
            pass
    
    def hae_lasnatyypin_id(self, kohde:str):
        if kohde != "":
            sql= "SELECT id FROM lasnatyypit WHERE tyyppi = ?"
            self.cur.execute(sql, (kohde,))
            self.con.commit()
            id = self.cur.fetchone()
            return int(id[0])
        else:
            return None
    
    def poistaLasnaTyyppi(self, type):
        sql = """DELETE FROM lasnatyypit WHERE tyyppi = ?""" 
        self.cur.execute(sql, (type,))
        self.con.commit()
        
    
    def lisaa_henkilo(self, nimi:str):
        tanaan = date.today()
        tanaan = tanaan.isoformat()
        self.cur.execute("""INSERT OR IGNORE INTO henkilot(name, liittynyt) VALUES (?,?)""",(str(nimi), str(tanaan)))
        self.con.commit()
    
    def poista_henkilo(self, id:int, nimi:str):
        sql = """DELETE FROM henkilot WHERE id = ? AND name = ?""" 
        self.cur.execute(sql, (id, nimi))
        self.con.commit()
    
        
    def lisaa_tapahtuma(self, pvm:str, hloid:int, lasnaid:int):
        etsi = """SELECT * FROM tapahtumat WHERE date = ? AND hloid = ?"""
        self.cur.execute(etsi, (pvm, hloid))
        self.con.commit()
        tulos = self.cur.fetchone()
        if tulos != None:
            paivita = """REPLACE INTO tapahtumat(id, date, hloid, lasna) VALUES (?, ?, ?, ?)"""
            self.cur.execute(paivita, (tulos[0], pvm, hloid, lasnaid))
            self.con.commit()
        else:
            sql = """INSERT INTO tapahtumat(date, hloid, lasna) VALUES (?, ?, ?)"""
            self.cur.execute(sql, (pvm, hloid, lasnaid))
            self.con.commit()
            
    def paivita_henkilo(self,id:int, nimi:str):
        sql = """REPLACE INTO henkilot(id, name) VALUES (?,?)"""
        self.cur.execute(sql, (id, nimi))
        self.con.commit()
        
    def paivita_tapahtuma(self, id:int, pvm:str, hloid:int, lasnaid:int):
        sql = """REPLACE INTO tapahtumat(id, date, hloid, lasna) VALUES (?,?,?,?)"""
        self.cur.execute(sql, (id, pvm, hloid, lasnaid))
        self.con.commit()
    
    def poista_tapahtuma(self, id:int):
        sql = """DELETE FROM tapahtumat WHERE id = ?"""
        self.cur.execute(sql, (id,))
        self.con.commit()
        
    def hae_tapahtumatyypit(self):
        sql = """SELECT * FROM lasnatyypit"""
        self.cur.execute(sql)
        self.con.commit()
        lista = self.cur.fetchall()
        return lista
        
    def lisaa_tapahtumatyyppi(self, tyyppi:str):
        sql = """INSERT OR IGNORE INTO lasnatyypit(tyyppi) VALUES (?) """
        self.cur.execute(sql, (tyyppi,))
        self.con.commit()
        
    def paivita_tapahtumatyyppi(self, vanhaid:int, uusityyppi:str):
        sql = """REPLACE INTO lasnatyypit(id, tyyppi) VALUES (?,?)"""
        self.cur.execute(sql, (vanhaid, uusityyppi))
        self.con.commit()
            
    def hae_henkilot(self, tiedot:tuple):
        henkiloLista = []
        if tiedot[0] == 'all':
            self.cur.execute("SELECT * FROM henkilot ORDER BY name ASC")
            self.con.commit()
            henkilot = self.cur.fetchall()
            for henkilo in henkilot:
                henkiloLista.append(henkilo)
        return henkiloLista
    
    def hae_tapahtumat(self, tiedot:tuple):
        tapahtumaLista = []
        if tiedot[0] == 'all':
            self.cur.execute("""SELECT * FROM tapahtumat""")
            self.con.commit()
            lista = self.cur.fetchall()
            for item in lista:
                tapahtumaLista.append(item)
        return tapahtumaLista
    
    def hae_henkilon_tapahtumat(self, nimi:str, aikavali:tuple):
        tapahtumalista = []
        sql = """SELECT tapahtumat.id, tapahtumat.date, henkilot.name, lasnatyypit.tyyppi FROM tapahtumat
        LEFT JOIN henkilot, lasnatyypit
        WHERE tapahtumat.hloid = henkilot.id AND tapahtumat.lasna = lasnatyypit.id AND henkilot.name = ?
        ORDER BY date(tapahtumat.date)"""
        self.cur.execute(sql, (nimi, ))
        self.con.commit()
        tapahtumat = self.cur.fetchall()
        if len(tapahtumat) != 0:
            for tapahtuma in tapahtumat:
                if datetime.strptime(aikavali[0], "%Y-%m-%d") <= datetime.strptime(tapahtuma[1], "%Y-%m-%d") <= datetime.strptime(aikavali[1], "%Y-%m-%d"):
                    tapahtumalista.append(tapahtuma)
            return tapahtumalista
        else:
            return None
    
    def tuo_kaikki_tapahtumatiedot(self):
        tapahtumatiedot =[]
        sql = """SELECT tapahtumat.id, tapahtumat.date, henkilot.name, lasnatyypit.tyyppi FROM tapahtumat
        LEFT JOIN henkilot, lasnatyypit
        WHERE tapahtumat.hloid = henkilot.id AND tapahtumat.lasna = lasnatyypit.id"""
        self.cur.execute(sql)
        self.con.commit()
        tapahtumat = self.cur.fetchall()
        for tapahtuma in tapahtumat:
            tapahtumatiedot.append(tapahtuma)
        return (tapahtumatiedot)
    
    def tuo_tapahtuma_raportti(self, aikavali:tuple):
        tapahtumat_ajalla = []
        sanakirja = {}
        sql = """SELECT tapahtumat.date, henkilot.name, lasnatyypit.tyyppi FROM tapahtumat
        LEFT JOIN henkilot, lasnatyypit
        WHERE tapahtumat.hloid = henkilot.id AND tapahtumat.lasna = lasnatyypit.id
        ORDER BY date(tapahtumat.date) ASC"""
        self.cur.execute(sql)
        self.con.commit()
        tapahtumat = self.cur.fetchall()
        for tapahtuma in tapahtumat:
            if datetime.strptime(aikavali[0], "%Y-%m-%d") <= datetime.strptime(tapahtuma[0], "%Y-%m-%d") <= datetime.strptime(aikavali[1], "%Y-%m-%d"):
                tapahtumat_ajalla.append(tapahtuma)
        for pvm, nimi, lasna in tapahtumat_ajalla:
            if not pvm in sanakirja:
                sanakirja[pvm] = {}
            if not lasna in sanakirja[pvm]:
                sanakirja[pvm][lasna]=[]
            sanakirja[pvm][lasna].append(nimi)    
        return sanakirja
        
    
    def laskeHenkilonLasnaolot(self, nimi:str, aikavali:tuple):
        sanakirja = {}
        if nimi != '':
            id = self.hae_henkilo_id(nimi)
            sql = """SELECT lasnatyypit.tyyppi, tapahtumat.date FROM tapahtumat LEFT JOIN lasnatyypit WHERE hloid = ? AND tapahtumat.lasna = lasnatyypit.id """
            self.cur.execute(sql, (id,))
            self.con.commit()
            tapahtumat = self.cur.fetchall()
            for lasna, pvm in tapahtumat:
                if datetime.strptime(aikavali[0], "%Y-%m-%d") <= datetime.strptime(pvm, "%Y-%m-%d") <= datetime.strptime(aikavali[1], "%Y-%m-%d"):
                    if not lasna in sanakirja:
                        sanakirja[lasna] = 1
                    else:
                        sanakirja[lasna] += 1
            return sanakirja
        else:
            pass
        
    
    def __del__(self):
        self.con.close()
    
    def __lasna_numeroiksi(self, arvo:str):
        lasnanro = None
        if arvo == "Läsnä":
            lasnanro = 1
        elif arvo == "Luvaton poissaolo":
            lasnanro = 2
        elif arvo == "Selvitetty poissaolo":
            lasnanro = 3
        elif arvo == "Sairasloma":
            lasnanro = 4
        return lasnanro
    

# if __name__ == "__main__":
#     saijaSql = Sql("saijaDb")

#     dd = saijaSql.tuo_tapahtuma_raportti(('2022-01-01', '2022-04-30'))
#     for d in dd:
#         print(dd[d])

        
        
        
    

