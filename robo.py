import requests
from bs4 import BeautifulSoup

url = "https://www.ioerj.com.br/portal/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 🔐 CONEXÃO SEGURA
try:
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        print("Erro ao acessar o site:", response.status_code)
        exit()

except Exception as e:
    print("Erro de conexão:", e)
    exit()

# 🔎 PARSE HTML
try:
    soup = BeautifulSoup(response.text, "html.parser")
except Exception as e:
    print("Erro ao ler HTML:", e)
    exit()

links = soup.find_all("a")

pdf_link = None

# 🔍 BUSCAR PDF
for link in links:
    href = link.get("href")

    if href and ".pdf" in href.lower():
        # 🔧 Corrigir link relativo
        if href.startswith("/"):
            pdf_link = "https://www.ioerj.com.br" + href
        else:
            pdf_link = href
        break

# 🚨 SE NÃO ENCONTRAR
if not pdf_link:
    print("Nenhum PDF encontrado no site")
    exit()

# 🚨 VALIDAR LINK
if not pdf_link.startswith("http"):
    print("Link inválido:", pdf_link)
    exit()

print("PDF encontrado:", pdf_link)

# 📥 DOWNLOAD SEGURO
try:
    pdf = requests.get(pdf_link, headers=headers, timeout=15)

    if pdf.status_code != 200:
        print("Erro ao baixar PDF:", pdf.status_code)
        exit()

    # 🔐 Garantir que tem conteúdo
    if not pdf.content:
        print("PDF vazio")
        exit()

    with open("arquivo.pdf", "wb") as f:
        f.write(pdf.content)

    print("PDF salvo com sucesso")

except Exception as e:
    print("Erro no download:", e)
