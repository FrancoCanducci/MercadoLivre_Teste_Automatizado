from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string

# Atualize o caminho para o ChromeDriver
chrome_driver_path = "C:\\Users\\franc\\OneDrive\\Área de Trabalho\\chromedriver-win64 (3)\\chromedriver-win64\\chromedriver.exe"

# Caminhos para os arquivos que deseja fazer o upload
file_path_1 = "C:\\Users\\franc\\Downloads\\foto1.jpeg"
file_path_2 = "C:\\Users\\franc\\Downloads\\foto2.jpeg"

# Configurando o serviço do ChromeDriver
service = Service(chrome_driver_path)

# Configurações do navegador
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Iniciar o navegador maximizado
options.add_argument("--disable-notifications")  # Desabilitar notificações

# Função para gerar um email aleatório
def generate_random_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = "example.com"
    return f"{prefix}@{domain}"

# Função para gerar uma senha aleatória forte
def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choices(characters, k=12))
    return password

# Função para calcular o tempo de carregamento da página
def get_page_load_time(driver):
    navigation_start = driver.execute_script("return window.performance.timing.navigationStart")
    load_event_end = driver.execute_script("return window.performance.timing.loadEventEnd")
    return load_event_end - navigation_start

# Função para medir o tempo até um elemento ser clicável
def measure_time_until_clickable(driver, xpath, description):
    try:
        start_time = time.time()
        element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Tempo para {description} aparecer: {elapsed_time:.2f} segundos")
        return element
    except Exception as e:
        print(f"Erro ao esperar o {description}: {e}")
        return None

# Função para verificar se o botão 'Validar' está visível e disponível para clique
def is_validate_button_visible(driver):
    try:
        validate_button = driver.find_element(By.XPATH, "//span[@class='andes-button__text' and text()='Validar']")
        if validate_button.is_displayed():
            return validate_button
        else:
            return None
    except Exception as e:
        print(f"Erro ao procurar o botão 'Validar': {e}")
        return None

# Iniciando o navegador
driver = webdriver.Chrome(service=service, options=options)

# Navegar para a página de criação de conta do Mercado Livre
driver.get("https://www.mercadolivre.com.br/hub/registration?from_landing=true&contextual=unified_normal&redirect_url=https%3A%2F%2Fwww.mercadolivre.com.br%2F&entity=no_apply#nav-header")

try:
    # Medir o tempo de carregamento da página
    page_load_time = get_page_load_time(driver)
    print(f"Tempo de carregamento da página: {page_load_time / 1000:.2f} segundos")

    # Esperar um pouco para garantir que a página carregue completamente
    time.sleep(4)

    # Medir o tempo para o botão "Adicionar" aparecer
    add_button = measure_time_until_clickable(driver, "//span[@class='andes-button__text' and text()='Adicionar']", "o botão 'Adicionar'")

    if add_button:
        # Clicar no botão "Adicionar"
        add_button.click()
        print("O botão 'Adicionar' foi clicado com sucesso.")

        # Esperar um pouco para garantir que o campo de input de email apareça
        time.sleep(4)

        # Medir o tempo para o campo de input de email aparecer
        email_input_start_time = time.time()
        email_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//input[@id='enter-email-input']")))
        email_input_end_time = time.time()
        email_input_elapsed_time = email_input_end_time - email_input_start_time
        print(f"Tempo para o campo de input de email aparecer: {email_input_elapsed_time:.2f} segundos")

        if email_input.is_displayed():
            # Gerar um email aleatório
            random_email = generate_random_email()
            print(f"Usando email aleatório: {random_email}")

            # Inserir o email no campo de input
            email_input.send_keys(random_email)
            print("O email foi inserido com sucesso.")

            # Esperar alguns segundos para o botão "Continuar" ficar válido
            time.sleep(4)

            # Medir o tempo para o botão "Continuar" aparecer
            continue_button = measure_time_until_clickable(driver, "//span[@class='andes-button__content' and text()='Continuar']", "o botão 'Continuar'")

            if continue_button:
                # Clicar no botão "Continuar"
                continue_button.click()
                print("O botão 'Continuar' foi clicado com sucesso.")

                # Aumentar o tempo de espera para garantir que a nova tela carregue completamente
                time.sleep(10)

                # Medir o tempo para o botão "Escolher" aparecer
                choose_button = measure_time_until_clickable(driver, "//span[@class='andes-button__text' and text()='Escolher']", "o botão 'Escolher'")

                if choose_button:
                    # Clicar no botão "Escolher"
                    choose_button.click()
                    print("O botão 'Escolher' foi clicado com sucesso.")
                else:
                    print("O botão 'Escolher' não está visível.")

                # Esperar 10 segundos após clicar no botão "Escolher"
                time.sleep(15)
                print("Aguardando 15 segundos")

                try:
                    # Procurar o elemento input de arquivo diretamente
                    file_input_1 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))

                    # Enviar o caminho do arquivo para o input
                    file_input_1.send_keys(file_path_1)
                    print("O primeiro arquivo foi selecionado com sucesso.")

                    # Esperar 10 segundos para verificar se o arquivo foi enviado
                    time.sleep(10)

                    # Esperar até o segundo botão de upload esteja presente e visível
                    file_input_2 = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@class='andes-file-uploader__dropzone-input' and @id='input-Lado sem foto']")))

                    # Enviar o caminho do segundo arquivo para o input
                    file_input_2.send_keys(file_path_2)
                    print("O segundo arquivo foi selecionado com sucesso.")

                    # Aguardar até o botão "Continuar" aparecer na tela
                    continue_button_2 = measure_time_until_clickable(driver, "//span[@class='andes-button__content' and text()='Continuar']", "o botão 'Continuar' (após envio dos arquivos)")

                    if continue_button_2:
                        # Clicar no botão "Continuar"
                        continue_button_2.click()
                        print("O botão 'Continuar' foi clicado com sucesso (após envio dos arquivos).")

                        # Esperar alguns segundos para garantir que a nova tela carregue completamente
                        time.sleep(10)

                        # Verificar a visibilidade do botão "Validar" com tentativas escalonadas
                        for attempt in range(3):
                            validate_button = is_validate_button_visible(driver)
                            if validate_button:
                                # Esperar 10 segundos adicionais antes de clicar
                                time.sleep(10)
                                # Clicar no botão "Validar"
                                validate_button.click()
                                print("O botão 'Validar' foi clicado com sucesso.")
                                break
                            else:
                                if attempt == 0:
                                    print("O botão 'Validar' não está visível. Tentando novamente em 40 segundos...")
                                    time.sleep(40)
                                else:
                                    print(f"Tentativa {attempt + 1}: O botão 'Validar' não está visível. Tentando novamente em 6 segundos...")
                                    time.sleep(6)
                        else:
                            print("O botão 'Validar' não está visível após múltiplas tentativas.")
                        
                        # Esperar alguns segundos para garantir que a nova tela carregue completamente
                        time.sleep(10)

                        # Aguardar até o campo de input de telefone aparecer
                        phone_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//input[@type='tel' and @id=':R1ot1:']")))

                        # Inserir o número de telefone no campo de input
                        phone_input.send_keys("16999941794")
                        print("O número de telefone foi inserido com sucesso.")

                        # Esperar 10 segundos após inserir o número de telefone
                        print("Esperando 10 segundos após inserir o número de telefone...")
                        time.sleep(10)

                        # Verificar se o botão "Enviar código por WhatsApp" está visível
                        print("Verificando se o botão 'Enviar código por WhatsApp' está visível...")
                        whatsapp_button_xpath = "//span[@class='andes-button__content' and text()='Enviar código por WhatsApp']"
                        whatsapp_button = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, whatsapp_button_xpath)))

                        if whatsapp_button.is_displayed():
                            print("O botão 'Enviar código por WhatsApp' está visível. Tentando clicar...")
                            whatsapp_button.click()

                            # Esperar 5 segundos após clicar no botão
                            print("Esperando 5 segundos após clicar no botão 'Enviar código por WhatsApp'...")
                            time.sleep(5)

                            # Verificar novamente se o botão "Enviar código por WhatsApp" ainda está visível
                            print("Verificando novamente se o botão 'Enviar código por WhatsApp' ainda está visível...")
                            whatsapp_button_still_visible = WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, whatsapp_button_xpath)))

                            if whatsapp_button_still_visible:
                                print("O botão 'Enviar código por WhatsApp' ainda está visível.")
                            else:
                                print("O botão 'Enviar código por WhatsApp' não está mais visível. Prosseguindo com o próximo passo...")

                        else:
                            print("O botão 'Enviar código por WhatsApp' não está visível.")

                        # Continuar com os próximos passos aqui

                    else:
                        print("O botão 'Continuar' não está visível após o envio dos arquivos.")
                except Exception as e:
                    print(f"Erro ao selecionar os arquivos: {e}")
            else:
                print("O botão 'Continuar' não está visível após a inserção do email.")
        else:
            print("O campo de input de email não está visível.")
    else:
        print("O botão 'Adicionar' não está visível.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Fechar o navegador após a execução
    time.sleep(60)
    driver.quit()
