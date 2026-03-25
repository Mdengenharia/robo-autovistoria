import requests
from datetime import datetime
from bs4 import BeautifulSoup

# 📅 data de hoje
hoje = datetime.now().strftime("%Y%m%d")

# 🔗 URL direta (padrão do site)
url = f"https://doweb.rio.rj.gov.br/portal/edicoes/download/{hoje}"

headers = {
    "User-Agent": "Mozilla/5.0"
}

try:
    response = requests.get(url, headers=headers, timeout=15)

    if response.status_code != 200:
        print("❌ Não conseguiu acessar edição direta")
        exit()

except Exception as e:
    print("Erro:", e)
    exit()

# 🔥 LÊ HTML MESMO (mesmo que venha “disfarçado”)
soup = BeautifulSoup(response.text, "html.parser")

texto = soup.get_text()

linhas = texto.split("\n")

resultados = []

for i, linha in enumerate(linhas):
    linha_lower = linha.lower()

    if (
        ("condominio" in linha_lower or "condomínio" in linha_lower or "edificio" in linha_lower)
        and
        (
            "predial" in linha_lower
            or "manutenção" in linha_lower
            or "fiscalização" in linha_lower
            or "laudo" in linha_lower
            or "vistoria" in linha_lower
            or "exigência" in linha_lower
            or "marquise" in linha_lower
        )
    ):
        contexto = linha.strip()

        if i > 0:
            contexto = linhas[i-1].strip() + " | " + contexto

        if i < len(linhas) - 1:
            contexto = contexto + " | " + linhas[i+1].strip()

        resultados.append(contexto)

print("\n==============================")
print("🔥 RESULTADOS REAIS DO DIÁRIO")
print("==============================\n")

for r in resultados:
    print(r)

if not resultados:
    print("⚠️ Conteúdo carregado, mas filtro não capturou — ajustar palavras")
