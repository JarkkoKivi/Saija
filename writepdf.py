from datetime import datetime
from fpdf import FPDF

class ToPdf(FPDF):
    def __init__(self):
        super().__init__()
        self.add_page()
        self.set_font(family="Arial", size=12)
        
    def headline(self, text):
        self.set_font("Arial", "B", 16)
        self.cell(w=80, txt=text) 
        self.ln(10)
        
    def headline2(self, text):
        self.set_font("Arial", "", 14)
        self.cell(w=80, txt=text) 
        self.ln(15)

    # def header(self):
    #     # Logo
    #     #self.image('logo_pb.png', 10, 8, 33)
    #     # Arial bold 15
    #     self.set_font('Arial', 'B', 15)
    #     # Move to the right
    #     self.cell(80)
    #     # Title
    #     self.cell(30, 10, 'Title', 1, 0, 'C')
    #     # Line break
    #     self.ln(20)
    
    def lasnaolotYht(self, rivi):
        self.set_font('Arial', '', 12)
        self.cell(w=120, txt=rivi)
        self.ln(10)
        
    def tapahtumalistaOtsikot(self, teksti:str):
        self.set_font('Arial', 'B', 12)
        self.cell(w=40, txt=f"{teksti}:")
        self.ln(4)
        
    def tapahtumalista(self, lista:list):
        self.set_font('Arial', '', 12)
        self.multi_cell(w=0, h=5, txt=", ".join(lista))
        self.ln(7)
        
    def divider(self, y):
        self.dashed_line(10, y-5, 210-10, y-5, 3,2)
        

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(75, 10, f"Tulostettu {datetime.today().strftime('%d.%m.%Y')}", 0, 0, 'L')
        self.cell(50, 10, 'Sivu ' + str(self.page_no()), 0, 0, 'C')
    
# if __name__ == "__main__":
#     pdf = ToPdf()
#     pdf.headline("Heippa Maailma!")
#     pdf.output("testi.pdf")