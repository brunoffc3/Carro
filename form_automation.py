from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException
import time


# ✅ Configuração do Selenium
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Executa sem abrir o navegador
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--user-data-dir=/tmp/chrome-user-data")  # Diretório único para dados do usuário

# Inicializa o WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL do formulário
form_url = "https://forms.office.com/pages/responsepage.aspx?id=fK7T5Tib3kigh_ZzSih1dGJeHOQK44ZNhPeJ8KFO7HNUOEtLSThYNlFRQllFNERCOU1DUU5MMVBEQi4u"

# 🔹 Acessa a página do formulário
driver.get(form_url)
time.sleep(5)  # Tempo para carregar

# 🔹 CLICAR NO BOTÃO "INICIAR AGORA" SE NECESSÁRIO
try:
    wait = WebDriverWait(driver, 30)

    start_button = None
    for _ in range(3):  # Tenta no máximo 3 vezes caso o botão fique "stale"
        try:
            # Reencontra o botão antes de clicar para evitar referência "stale"
            start_button = driver.execute_script("""
                let buttons = document.querySelectorAll("button");
                for (let btn of buttons) {
                    if (btn.innerText.includes("Iniciar agora")) {
                        return btn;
                    }
                }
                return null;
            """)

            if start_button:
                driver.execute_script("arguments[0].click();", start_button)
                print("✅ Botão 'Iniciar agora' clicado com sucesso!")
                break  # Sai do loop se o clique foi bem-sucedido
        except StaleElementReferenceException:
            print("🔄 Elemento ficou 'stale', tentando novamente...")

    if not start_button:
        print("❌ Erro: O botão 'Iniciar agora' não foi encontrado.")
except Exception as e:
    print(f"❌ Erro inesperado: {e}")

# Aguardar o carregamento dos campos do formulário
time.sleep(5)
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@value='Próximo dia útil']")))

# Preencher as perguntas conforme a ordem

# 1. Acesso para data: Rádio "Próximo dia útil"
acesso_para_data = driver.find_element(By.XPATH, "//input[@value='Próximo dia útil']")
acesso_para_data.click()


# 3. Nome completo: Dropdown
try:
    # Clicar no dropdown usando o atributo aria-describedby correto
    nome_dropdown = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-describedby='r2d0a7e33bd4a42bf8f81296ee31bcb5d_placeholder_content']"))
    )
    nome_dropdown.click()
    print("✅ Dropdown 'Nome completo' clicado")

    # Aguarda as opções aparecerem – assumindo que os itens têm role="option"
    opcoes_nome = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
    )
    opcao_nome_desejada = None
    for opcao in opcoes_nome:
        if "BRUNO FERREIRA COSTA" in opcao.text:  # Altere para o nome correto, se necessário
            opcao_nome_desejada = opcao
            break
    if opcao_nome_desejada:
        opcao_nome_desejada.click()
        print("✅ Opção 'BRUNO FERREIRA COSTA' selecionada no dropdown 'Nome completo'")
    else:
        print("❌ Opção 'BRUNO FERREIRA COSTA' não encontrada no dropdown 'Nome completo'")
except Exception as e:
    print("Erro ao interagir com o dropdown 'Nome completo':", e)

# 4. Horário de entrada: Dropdown
try:
    horario_dropdown = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-describedby='r96856d0890504f9395c004e5e3a9fbcf_placeholder_content']"))
    )
    horario_dropdown.click()
    print("✅ Dropdown 'Horário de entrada' clicado")

    opcoes_horario = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
    )
    opcao_horario_desejada = None
    for opcao in opcoes_horario:
        if "08:00" in opcao.text:  # Altere para o horário desejado
            opcao_horario_desejada = opcao
            break
    if opcao_horario_desejada:
        opcao_horario_desejada.click()
        print("✅ Opção '08:00' selecionada no dropdown 'Horário de entrada'")
    else:
        print("❌ Opção '08:00' não encontrada no dropdown 'Horário de entrada'")
except Exception as e:
    print("Erro ao interagir com o dropdown 'Horário de entrada':", e)

# 5. Masp: Campo de texto
try:
    masp_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@aria-label='Texto de linha única' and contains(@placeholder, 'número')]"))
    )
    masp_input.send_keys('7523079')
    print("✅ Campo 'Masp' preenchido")
except Exception as e:
    print("Erro ao preencher o campo 'Masp':", e)

#time.sleep(3)
#WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@aria-describedby='r174b4cc3b2994ce283a6798c35daab45_placeholder_content']")))

# 6. Órgão: Dropdown
try:
    orgao_dropdown = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-describedby='r174b4cc3b2994ce283a6798c35daab45_placeholder_content']"))
    )
    orgao_dropdown.click()
    print("✅ Dropdown 'Órgão' clicado")

    opcoes_orgao = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
    )
    opcao_orgao_desejada = None
    for opcao in opcoes_orgao:
        if "SEGOV" in opcao.text:  # Ajuste conforme o texto correto da opção desejada
            opcao_orgao_desejada = opcao
            break
    if opcao_orgao_desejada:
        opcao_orgao_desejada.click()
        print("✅ Opção 'SEGOV' selecionada no dropdown 'Órgão'")
    else:
        print("❌ Opção 'SEGOV' não encontrada no dropdown 'Órgão'")
except Exception as e:
    print("Erro ao interagir com o dropdown 'Órgão':", e)

# 7. Cargo: Dropdown
try:
    cargo_dropdown = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@aria-describedby='r9323056dff104eec8423ef20ddbd15ee_placeholder_content']"))
    )
    cargo_dropdown.click()
    print("✅ Dropdown 'Cargo' clicado")

    opcoes_cargo = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@role='option']"))
    )
    opcao_cargo_desejada = None
    for opcao in opcoes_cargo:
        if "Superintendente" in opcao.text:  # Ajuste conforme necessário
            opcao_cargo_desejada = opcao
            break
    if opcao_cargo_desejada:
        opcao_cargo_desejada.click()
        print("✅ Opção 'Superintendente' selecionada no dropdown 'Cargo'")
    else:
        print("❌ Opção 'Superintendente' não encontrada no dropdown 'Cargo'")
except Exception as e:
    print("Erro ao interagir com o dropdown 'Cargo':", e)

# 8. Modelo do Veículo: Campo de texto
try:
    # Supondo que o primeiro campo de texto (entre os inputs com mesmo aria-label) seja o Modelo do Veículo
    modelo_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "(//input[@aria-label='Texto de linha única'])[2]"))
    )
    modelo_input.send_keys('Audi a3')
    print("✅ Campo 'Modelo do Veículo' preenchido")
except Exception as e:
    print("Erro ao preencher o campo 'Modelo do Veículo':", e)

# 9. Placa do Veículo: Campo de texto
try:
    placa_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "(//input[@aria-label='Texto de linha única'])[3]"))
    )
    placa_input.send_keys('owz7j12')
    print("✅ Campo 'Placa do Veículo' preenchido")
except Exception as e:
    print("Erro ao preencher o campo 'Placa do Veículo':", e)

# 10. E-mail institucional: Campo de texto
try:
    email_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "(//input[@aria-label='Texto de linha única'])[4]"))
    )
    email_input.send_keys('bruno.costa@governo.mg.gov.br')
    print("✅ Campo 'E-mail institucional' preenchido")
except Exception as e:
    print("Erro ao preencher o campo 'E-mail institucional':", e)

# Enviar o formulário
try:
    submit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Enviar')]"))
    )
    submit_button.click()
    print("✅ Formulário enviado com sucesso!")
except Exception as e:
    print("Erro ao enviar o formulário:", e)

time.sleep(2)
driver.quit()

#"Adiciona script de automação"
