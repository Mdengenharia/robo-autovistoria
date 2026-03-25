from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        url = "https://doweb.rio.rj.gov.br/buscanova/#/p=1&q=predial"

        page.goto(url)

        page.wait_for_timeout(6000)

        texto = page.inner_text("body")

        linhas = texto.split("\n")

        resultados = []

        for i, linha in enumerate(linhas):
            linha_lower = linha.lower()

            if (
                ("condominio" in linha_lower or "condomínio" in linha_lower or "edificio" in linha_lower or "edifício" in linha_lower)
                and
                (
                    "predial" in linha_lower
                    or "manutenção" in linha_lower
                    or "fiscalização" in linha_lower
                    or "fiscalizacao" in linha_lower
                    or "laudo" in linha_lower
                    or "vistoria" in linha_lower
                    or "autovistoria" in linha_lower
                    or "inspeção" in linha_lower
                    or "inspecao" in linha_lower
                    or "exigência" in linha_lower
                    or "exigencia" in linha_lower
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
        print("🔥 RESULTADOS ENCONTRADOS")
        print("==============================\n")

        for r in resultados:
            print(r)

        if not resultados:
            print("Nenhum resultado encontrado")

        browser.close()

run()
