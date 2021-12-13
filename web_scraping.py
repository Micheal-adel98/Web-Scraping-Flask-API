
import requests
from bs4 import BeautifulSoup
import csv
from  itertools import zip_longest
import qrcode
from fpdf import FPDF
import gspread
import shutil
import arabic_reshaper
from bidi.algorithm import get_display




#Declare lists to scarping data
all = []
index_tabel=[]
booknames = []
authors = []
country = []
links_books = []
links_authors = []
links_country = []




qr=qrcode.QRCode(
 version=2, box_size=10,border=5,error_correction=qrcode.constants.ERROR_CORRECT_M,
)



#Scraping Data
result = requests.get("https://ar.wikipedia.org/wiki/%D9%82%D8%A7%D8%A6%D9%85%D8%A9_%D8%A3%D9%81%D8%B6%D9%84_%D9%85%D8%A6%D8%A9_%D8%B1%D9%88%D8%A7%D9%8A%D8%A9_%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9")

src = result.content

soup = BeautifulSoup(src,"lxml")

book_names = soup.find_all("td")

#scrape book page link
for i in range(1,len(book_names),4):
    links_books.append("https://ar.wikipedia.org"+book_names[i].find("a").attrs['href'])

#scrape author page link
for i in range(2,len(book_names),4):
    links_authors.append("https://ar.wikipedia.org"+book_names[i].find("a").attrs['href'])

#scrape country link
for i in range(3,len(book_names),4):
    country.append(book_names[i].find("a").text)
    links_country.append("https://ar.wikipedia.org"+book_names[i].find("a").attrs['href'])

#scrape all data
for i in range(len(book_names)):
    all.append(book_names[i].text)

#scrape id of table
for i in range(0,len(all),4):
    index_tabel.append(all[i].strip("\n"))


#scrape book names
for i in range(1,len(all),4):
    booknames.append(all[i].strip("\n"))
    
#scrape author name
for i in range(2,len(all),4):
    authors.append(all[i].strip("\n"))


#create book CSV file     
file_list = [index_tabel,authors,links_authors,booknames,links_books,country,links_country]
exported = zip_longest(*file_list)
with open("D:/test/python-task-nagwa/books.csv","w",newline="\n",encoding="utf-16") as myfile:
    wr = csv.writer(myfile,delimiter="\t")
    wr.writerow(["id","Author","Authors link","Book Name","Book link","country","country link"])   
    wr.writerows(exported)
myfile.close()


#Generate PDF with QRCOdes
for i in range(len(authors)):
    data = links_books[i]
    qr.clear()
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black' , black_color='white')
    img.save('QRCodes/'+booknames[i]+'.png')
    path = 'QRCodes/'+booknames[i]+'.png'
    pdf =FPDF()
    pdf.add_page()
    pdf.image(path,x=60,y=10,w=90,link=data)
    pdf.add_font('Arial', '','arial.ttf', uni=True)
    pdf.set_font("Arial",size=12)
    pdf.ln(80)
    pdf.cell(90,10,ln=True,align='C')
    bookname =get_display(arabic_reshaper.reshape(booknames[i]))
    name =get_display(arabic_reshaper.reshape(authors[i]))
    pdf.cell(0,10,f"{bookname}",align='C',ln=True,border=20)
    pdf.cell(0,10,f"{name}",align='C',ln=True,border=20)
    pdf.output('PDFS/'+booknames[i]+'.pdf')

#ziping all pdf book covers into pdfs.zip  
shutil.make_archive("pdfs", 'zip', 'PDFS')




#read google sheet file & apen by key
gc = gspread.service_account(filename='keys.json')
sh=gc.open_by_key('################################')
worksheet = sh.get_worksheet(0)

#append data to google sheet note: Please note that the sheet does not contain the entire data because Google Sheet ِ API has a limited requests quota for a free trial
#https://docs.google.com/spreadsheets/d/1MASPnmD9d3xrf9jKLBPzsAv6Cdjva2w9Gnhw_mPwCKU/edit?usp=sharing
uploadsheet=[]
worksheet.append_row(["id","Author","Authors link","Book Name","Book link","country","country link"])
for i in range(len(index_tabel)):
    uploadsheet.append(index_tabel[i])
    uploadsheet.append(authors[i])
    uploadsheet.append(links_authors[i])
    uploadsheet.append(booknames[i])
    uploadsheet.append(links_books[i])
    uploadsheet.append(country[i])
    uploadsheet.append(links_country[i])
    worksheet.append_row(uploadsheet)
    uploadsheet.clear()
