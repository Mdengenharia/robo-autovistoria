from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🔎 Acessando busca pronta...")

        # 🔥 já entra com busca feita
        page.goto("https://doweb.rio.rj.gov.br/buscanova/#/resultado?termo=predial")

        page.wait_for_timeout(6000)

        print("🔎 Pegando resultados...")

        resultados = []

        blocos = page.query_selector_all("text=Diário publicado em")

        for bloco in blocos[:5]:
            try:
                texto = bloco.inner_text()
                resultados.append(texto)
            except:
                continue

        print("\n==============================")
        print("🔥 RESULTADOS ENCONTRADOS")
        print("==============================\n")

        for r in resultados:
            print(r)

        if not resultados:
            print("⚠️ NÃO PEGOU — MAS AGORA NÃO É ERRO, É AJUSTE DE CAPTURA")

        browser.close()

run()
