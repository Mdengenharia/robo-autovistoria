import requests
from bs4 import BeautifulSoup

# URL do Diário Oficial (exemplo – depois ajustamos melhor)
url = "https://www.ioerj.com.br/portal/"

response = requests.get(url)

if response.status_code != 200:
    print("Erro ao acessar o site")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Procurar links de PDF (ajustável depois)
links = soup.find_all("a")

pdf_link = None

for link in links:
    href = link.get("href")
    
    if href and ".pdf" in href:
        pdf_link = href
        break

# 🔥 BLOCO SEGURO (ESSENCIAL)
if pdf_link and pdf_link.startswith("http"):
    print("PDF encontrado:", pdf_link)

    try:
        pdf = requests.get(pdf_link)

        if pdf.status_code == 200:
            with open("arquivo.pdf", "wb") as f:
                f.write(pdf.content)
            print("PDF salvo com sucesso")
        else:
            print("Erro ao baixar PDF")

    except Exception as e:
        print("Erro no download:", e)

else:
    print("Nenhum link válido encontrado")
