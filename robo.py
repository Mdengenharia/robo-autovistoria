import requests
from bs4 import BeautifulSoup
import pdfplumber

# 🔗 FONTES (pode expandir depois)
urls = [
    "https://www.ioerj.com.br/portal/",
    "https://diariooficial.niteroi.rj.gov.br/"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

# 🧠 PALAVRAS-CHAVE (CÉREBRO DO ROBÔ)
palavras_condominio = [
    "condominio", "condomínio", "edificio", "edifício"
]

palavras_problema = [
    "predial",
    "manutenção", "manutencao",
    "fiscalização", "fiscalizacao",
    "vistoria", "autovistoria",
    "inspeção", "inspecao",
    "laudo",
    "exigência", "exigencia",
    "regularização", "regularizacao",
    "marquise"
]

clientes = []

for url in urls:

    print(f"\n🔎 Buscando em: {url}\n")

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except:
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    pdf_link = None

    # 🔍 acha PDF
    for link in links:
        href = link.get("href")

        if href and ".pdf" in href.lower():
            if href.startswith("/"):
                base = url.split("/")[0] + "//" + url.split("/")[2]
                pdf_link = base + href
            else:
                pdf_link = href
            break

    if not pdf_link:
        continue

    print("📄 PDF:", pdf_link)

    try:
        pdf = requests.get(pdf_link, headers=headers, timeout=15)

        with open("arquivo.pdf", "wb") as f:
            f.write(pdf.content)

    except:
        continue

    try:
        with pdfplumber.open("arquivo.pdf") as pdf_file:

            for pagina in pdf_file.pages:
                texto = pagina.extract_text()

                if not texto:
                    continue

                linhas = texto.split("\n")

                for i, linha in enumerate(linhas):

                    linha_lower = linha.lower()

                    # 🎯 REGRA INTELIGENTE
                    if any(p in linha_lower for p in palavras_condominio):

                        if any(p in linha_lower for p in palavras_problema):

                            contexto = linha.strip()

                            # linha antes
                            if i > 0:
                                contexto = linhas[i-1].strip() + " | " + contexto

                            # linha depois
                            if i < len(linhas) - 1:
                                contexto = contexto + " | " + linhas[i+1].strip()

                            clientes.append(contexto)

    except:
        continue

# 📊 RESULTADO

print("\n==============================")
print("🔥 CLIENTES ENCONTRADOS")
print("==============================\n")

for c in clientes:
    print(c)

if not clientes:
    print("Nenhuma oportunidade encontrada hoje")
