from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto("https://doweb.rio.rj.gov.br/")
        page.wait_for_timeout(6000)

        # 🔥 pega TODOS os links da página
        links = page.eval_on_selector_all("a", "elements => elements.map(el => el.href)")

        html_link = None

        # 🔍 encontra automaticamente link HTML do diário
        for link in links:
            if link and ("html" in link.lower()):
                html_link = link
                break

        if not html_link:
            print("❌ Não encontrou link HTML automaticamente")
            browser.close()
            return

        print("🔗 HTML encontrado:", html_link)

        # 🔥 abre o HTML direto
        page.goto(html_link)
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
        print("🔥 CLIENTES ENCONTRADOS")
        print("==============================\n")

        for r in resultados:
            print(r)

        if not resultados:
            print("⚠️ HTML carregado, mas nenhum padrão encontrado")

        browser.close()

run()
