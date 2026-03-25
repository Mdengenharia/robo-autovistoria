from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("🔎 Acessando busca...")
        page.goto("https://doweb.rio.rj.gov.br/buscanova/#/")
        page.wait_for_timeout(5000)

        print("🔎 Pesquisando...")
        page.fill("input", "predial")
        page.keyboard.press("Enter")

        page.wait_for_timeout(6000)

        print("🔎 Pegando resultados...")
        botoes = page.query_selector_all("text=Visualizar")

        resultados = []

        for i, botao in enumerate(botoes[:5]):  # pega só os primeiros pra garantir
            try:
                print(f"➡️ Abrindo resultado {i+1}")

                with page.expect_navigation():
                    botao.click()

                page.wait_for_timeout(4000)

                texto = page.inner_text("body")

                if (
                    "condominio" in texto.lower()
                    or "condomínio" in texto.lower()
                    or "edificio" in texto.lower()
                ):
                    resultados.append(texto[:1000])  # corta pra não ficar gigante

                page.go_back()
                page.wait_for_timeout(4000)

            except:
                print("⚠️ erro ao abrir resultado, pulando...")
                continue

        print("\n==============================")
        print("🔥 RESULTADOS REAIS")
        print("==============================\n")

        for r in resultados:
            print(r)
            print("\n-------------------\n")

        if not resultados:
            print("⚠️ Entrou nas páginas, mas não filtrou ainda")

        browser.close()

run()
