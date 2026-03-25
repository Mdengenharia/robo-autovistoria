import requests
from bs4 import BeautifulSoup
import pdfplumber

# 🔗 FONTES
urls = [
    "https://www.ioerj.com.br/portal/",
    "https://diariooficial.niteroi.rj.gov.br/"
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

clientes = []

for url in urls:

    print(f"\n🔎 Buscando em: {url}\n")

    try:
        response = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        print("Erro ao acessar:", e)
        continue

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    pdf_link = None

    # 🔍 acha PDF do dia
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
        print("Nenhum PDF encontrado")
        continue

    print("📄 PDF encontrado:", pdf_link)

    # ⬇️ baixa PDF
    try:
        pdf = requests.get(pdf_link, headers=headers, timeout=15)

        if pdf.status_code != 200:
            print("Erro ao baixar PDF")
            continue

        with open("arquivo.pdf", "wb") as f:
            f.write(pdf.content)

    except Exception as e:
        print("Erro no download:", e)
        continue

    # 📖 leitura inteligente
    try:
        with pdfplumber.open("arquivo.pdf") as pdf_file:

            for pagina in pdf_file.pages:
                texto = pagina.extract_text()

                if not texto:
                    continue

                linhas = texto.split("\n")

                for i, linha in enumerate(linhas):

                    linha_lower = linha.lower()

                    # 🎯 FILTRO INTELIGENTE (BASE REAL DO DIÁRIO)
                    if (
                        ("condominio" in linha_lower or "condomínio" in linha_lower or "edificio" in linha_lower or "edifício" in linha_lower)
                        and
                        (
                            "predial" in linha_lower
                            or "manutenção" in linha_lower
                            or "fiscalização" in linha_lower
                            or "fiscalizacao" in linha_lower
                            or "subgerência" in linha_lower
                            or "subgerencia" in linha_lower
                            or "vistoria" in linha_lower
                            or "autovistoria" in linha_lower
                            or "inspeção" in linha_lower
                            or "inspecao" in linha_lower
                            or "laudo" in linha_lower
                            or "exigência" in linha_lower
                            or "exigencia" in linha_lower
                            or "marquise" in linha_lower
                        )
                    ):

                        contexto = linha.strip()

                        # ⬆️ linha anterior
                        if i > 0:
                            contexto = linhas[i-1].strip() + " | " + contexto

                        # ⬇️ linha seguinte
                        if i < len(linhas) - 1:
                            contexto = contexto + " | " + linhas[i+1].strip()

                        clientes.append(contexto)

    except Exception as e:
        print("Erro lendo PDF:", e)
        continue

# 📊 RESULTADO FINAL

print("\n==============================")
print("🔥 CLIENTES ENCONTRADOS")
print("==============================\n")

for c in clientes:
    print(c)

if not clientes:
    print("Nenhuma oportunidade encontrada hoje")
