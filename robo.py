import requests
from bs4 import BeautifulSoup
import pdfplumber

# 🔗 FONTES (RJ + NITERÓI)
urls = [
    "https://www.ioerj.com.br/portal/",
    "https://diariooficial.niteroi.rj.gov.br/"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

clientes_autovistoria = []
clientes_marquise = []

# 🔁 LOOP NAS FONTES
for url in urls:

    print(f"\n🔎 Buscando em: {url}\n")

    try:
        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            print("Erro ao acessar:", url)
            continue

    except Exception as e:
        print("Erro de conexão:", e)
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    pdf_link = None

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
        print("Nenhum PDF encontrado nessa fonte")
        continue

    print("PDF encontrado:", pdf_link)

    try:
        pdf_response = requests.get(pdf_link, headers=headers, timeout=15)

        if pdf_response.status_code != 200:
            print("Erro ao baixar PDF")
            continue

        with open("arquivo.pdf", "wb") as f:
            f.write(pdf_response.content)

    except Exception as e:
        print("Erro no download:", e)
        continue

    # 🔍 LEITURA INTELIGENTE (VERSÃO QUE FUNCIONA DE VERDADE)
    try:
        with pdfplumber.open("arquivo.pdf") as pdf:
            for pagina in pdf.pages:
                texto = pagina.extract_text()

                if not texto:
                    continue

                linhas = texto.split("\n")

                for linha in linhas:
                    linha_lower = linha.lower()

                    # 🎯 AUTOVISTORIA / INSPEÇÃO (AGORA INTELIGENTE)
                    if (
                        ("condominio" in linha_lower or "condomínio" in linha_lower or "edificio" in linha_lower or "edifício" in linha_lower)
                        and
                        ("laudo" in linha_lower or "vistoria" in linha_lower or "autovistoria" in linha_lower or "inspeção" in linha_lower or "exigência" in linha_lower)
                    ):
                        clientes_autovistoria.append(linha.strip())

                    # 🎯 MARQUISE (DIRETO)
                    if "marquise" in linha_lower:
                        clientes_marquise.append(linha.strip())

    except Exception as e:
        print("Erro lendo PDF:", e)

# 📊 RESULTADO FINAL

print("\n==============================")
print("🏢 CLIENTES - AUTOVISTORIA / INSPEÇÃO")
print("==============================\n")

for c in clientes_autovistoria:
    print(c)

print("\n==============================")
print("🏗️ CLIENTES - MARQUISE")
print("==============================\n")

for c in clientes_marquise:
    print(c)

if not clientes_autovistoria and not clientes_marquise:
    print("\nNenhuma oportunidade encontrada hoje")
