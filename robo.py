import requests
import pdfplumber
import pandas as pd
from bs4 import BeautifulSoup

url = "https://doweb.rio.rj.gov.br/"

page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")

pdf_link = None

for link in soup.find_all("a"):
    href = link.get("href")
    if href and ".pdf" in href:
        pdf_link = href
        break

if pdf_link and
    pdf_link = "https://doweb.rio.rj.gov.br" + pdf_link

pdf = requests.get(pdf_link)

with open("diario.pdf","wb") as f:
    f.write(pdf.content)

enderecos = []

with pdfplumber.open("diario.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()

        if text and "Subgerência de Fiscalização de Manutenção Predial" in text:
            linhas = text.split("\n")

            for linha in linhas:
                if "Rua" in linha or "Av." in linha or "Avenida" in linha:
                    enderecos.append(linha)

df = pd.DataFrame(enderecos, columns=["Endereço"])

df.to_csv("notificacoes.csv", index=False)
