
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class InstagramUnfollower:
    def __init__(self, browser_type='chrome'):
        self.browser_type = browser_type.lower()
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        if self.browser_type == 'chrome':
            service = ChromeService(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
        elif self.browser_type == 'edge':
            service = EdgeService(EdgeChromiumDriverManager().install())
            options = webdriver.EdgeOptions()
        else:
            raise ValueError("Tipo de navegador não suportado. Escolha 'chrome' ou 'edge'.")

        options.add_argument("--start-maximized")
        # options.add_argument("--headless") # Descomente para rodar em modo headless
        
        driver = webdriver.Chrome(service=service, options=options) if self.browser_type == 'chrome' else webdriver.Edge(service=service, options=options)
        driver.implicitly_wait(10) # Espera implícita para elementos carregarem
        return driver

    def login(self, username, password):
        logging.info("Navegando para o Instagram...")
        self.driver.get("https://www.instagram.com/")
        time.sleep(2) # Pequena pausa para a página carregar

        try:
            # Aceitar cookies, se houver
            try:
                accept_cookies_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Aceitar todos os cookies']"))
                )
                accept_cookies_button.click()
                logging.info("Cookies aceitos.")
                time.sleep(2)
            except TimeoutException:
                logging.info("Botão de aceitar cookies não encontrado ou já aceito.")

            logging.info("Tentando fazer login...")
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.driver.find_element(By.NAME, "password")

            username_input.send_keys(username)
            password_input.send_keys(password)
            password_input.send_keys(Keys.ENTER)
            logging.info("Credenciais inseridas. Pressionando Enter.")
            time.sleep(5) # Espera para o login ser processado

            # Lidar com pop-ups de 'Salvar informações de login' e 'Ativar Notificações'
            try:
                not_now_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Agora não']"))
                )
                not_now_button.click()
                logging.info("Clicado em 'Agora não' para salvar informações de login.")
                time.sleep(2)
            except TimeoutException:
                logging.info("Botão 'Agora não' para salvar informações de login não encontrado.")

            try:
                not_now_notifications = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[text()='Agora não']"))
                )
                not_now_notifications.click()
                logging.info("Clicado em 'Agora não' para notificações.")
                time.sleep(2)
            except TimeoutException:
                logging.info("Botão 'Agora não' para notificações não encontrado.")

            logging.info("Login bem-sucedido (ou já logado).")

        except Exception as e:
            logging.error(f"Erro durante o login: {e}")
            self.driver.quit()
            return False
        return True

    def get_user_list(self, list_type='followers'):
        # Implementar lógica para coletar seguidores/seguindo
        pass

    def unfollow_users(self, users_to_unfollow):
        # Implementar lógica para deixar de seguir
        pass

    def close(self):
        logging.info("Fechando o navegador.")
        self.driver.quit()

if __name__ == "__main__":
    # Exemplo de uso:
    # unfollower = InstagramUnfollower(browser_type='chrome')
    # unfollower.login("seu_usuario", "sua_senha")
    # unfollower.close()
    logging.info("Script iniciado. Por favor, preencha as credenciais e a lógica de coleta/unfollow.")
    logging.info("Este script é um esqueleto. As funções get_user_list e unfollow_users precisam ser implementadas.")





    def get_user_list(self, list_type=\'followers\', username=None):
        logging.info(f"Coletando lista de {list_type}...")
        if username is None:
            # Navegar para o próprio perfil se o username não for fornecido
            self.driver.get("https://www.instagram.com/accounts/edit/") # Uma página que geralmente redireciona para o perfil
            time.sleep(3)
            # Obter o nome de usuário da URL atual ou de um elemento na página
            current_url = self.driver.current_url
            parts = current_url.split(\'/\')
            # A URL do perfil geralmente é instagram.com/username/
            if len(parts) >= 4 and parts[2] == \'www.instagram.com\':
                username = parts[3]
            else:
                logging.error("Não foi possível determinar o nome de usuário a partir da URL. Por favor, forneça o nome de usuário manualmente ou verifique se está logado.")
                return []
        
        self.driver.get(f"https://www.instagram.com/{username}/")
        time.sleep(3)

        if list_type == \'followers\':
            xpath = "//a[contains(@href, \'/followers/\')]"
        elif list_type == \'following\':
            xpath = "//a[contains(@href, \'/following/\')]"
        else:
            logging.error("Tipo de lista inválido. Use \'followers\' ou \'following\'.")
            return []

        try:
            list_link = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            list_link.click()
            time.sleep(3)

            # Esperar o modal carregar
            dialog = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role=\'dialog\']//div[@class=\'_aano\']"))
            )

            users = set()
            last_height = self.driver.execute_script("return arguments[0].scrollHeight", dialog)

            while True:
                # Encontrar todos os elementos de nome de usuário visíveis
                # Usando um seletor mais robusto para os nomes de usuário dentro do modal
                # O Instagram frequentemente muda as classes, então XPATHs baseados em texto ou atributos são mais estáveis
                user_elements = dialog.find_elements(By.XPATH, ".//a[contains(@href, \'/\') and @role=\'link\']")
                for element in user_elements:
                    try:
                        # Extrair o nome de usuário da URL do link
                        href = element.get_attribute(\'href\')
                        if href and \'instagram.com/\' in href:
                            user_name = href.split(\'instagram.com/\')[1].strip(\'/\')
                            if user_name and user_name != username: # Evitar adicionar o próprio usuário
                                users.add(user_name)
                    except Exception as e:
                        logging.warning(f"Não foi possível extrair nome de usuário de um elemento: {e}")

                # Rolar para baixo
                self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
                time.sleep(2) # Pequena pausa para carregar novos elementos

                new_height = self.driver.execute_script("return arguments[0].scrollHeight", dialog)
                if new_height == last_height:
                    break # Chegou ao final da lista
                last_height = new_height
                logging.info(f"Rolando para carregar mais {list_type}... Total de usuários encontrados até agora: {len(users)}")

            logging.info(f"Total de {list_type} coletados: {len(users)}")
            return list(users)

        except Exception as e:
            logging.error(f"Erro ao coletar lista de {list_type}: {e}")
            return []

    def unfollow_users(self, users_to_unfollow):
        logging.info(f"Iniciando processo de deixar de seguir {len(users_to_unfollow)} usuários...")
        for user in users_to_unfollow:
            try:
                logging.info(f"Navegando para o perfil de {user}...")
                self.driver.get(f"https://www.instagram.com/{user}/")
                time.sleep(3) # Esperar o perfil carregar

                # Tentar encontrar o botão 'Seguindo' ou 'Deixar de Seguir'
                # XPath para o botão 'Seguindo' (que se torna 'Deixar de Seguir' ao clicar)
                unfollow_button_xpath = "//button[contains(., \'Seguindo\') or contains(., \'Following\')]"
                unfollow_confirm_xpath = "//button[contains(., \'Deixar de Seguir\') or contains(., \'Unfollow\')]"

                unfollow_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, unfollow_button_xpath))
                )
                logging.info(f"Clicando no botão 'Seguindo' para {user}...")
                unfollow_button.click()
                time.sleep(1) # Pequena pausa para o modal de confirmação aparecer

                confirm_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, unfollow_confirm_xpath))
                )
                logging.info(f"Confirmando 'Deixar de Seguir' para {user}...")
                confirm_button.click()
                logging.info(f"Deixou de seguir: {user}")
                time.sleep(random.uniform(5, 10)) # Simular comportamento humano

            except TimeoutException:
                logging.warning(f"Não foi possível encontrar o botão de 'Seguindo' ou 'Deixar de Seguir' para {user}. Talvez já tenha deixado de seguir ou o elemento mudou.")
            except ElementClickInterceptedException:
                logging.warning(f"Clique interceptado para {user}. Tentando novamente ou pulando.")
                # Pode ser um pop-up. Tentar fechar pop-ups genéricos se necessário.
                time.sleep(2)
            except Exception as e:
                logging.error(f"Erro ao deixar de seguir {user}: {e}")
            
        logging.info("Processo de deixar de seguir concluído.")


if __name__ == "__main__":
    # Exemplo de uso:
    # Adicione um arquivo .env com INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD
    from dotenv import load_dotenv
    import os
    import random

    load_dotenv()
    USERNAME = os.getenv("INSTAGRAM_USERNAME")
    PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

    if not USERNAME or not PASSWORD:
        logging.error("Por favor, defina as variáveis de ambiente INSTAGRAM_USERNAME e INSTAGRAM_PASSWORD no arquivo .env")
    else:
        unfollower = InstagramUnfollower(browser_type=\'chrome\') # ou \'edge\'
        if unfollower.login(USERNAME, PASSWORD):
            logging.info("Login bem-sucedido. Coletando listas...")
            # É importante passar o nome de usuário para get_user_list para garantir que a navegação seja para o perfil correto
            # Você pode obter o nome de usuário logado após o login, ou passá-lo diretamente
            # Para simplificar, vamos assumir que o USERNAME fornecido é o nome de usuário do perfil.
            my_followers = unfollower.get_user_list(list_type=\'followers\', username=USERNAME)
            my_following = unfollower.get_user_list(list_type=\'following\', username=USERNAME)

            if my_followers and my_following:
                not_following_back = [user for user in my_following if user not in my_followers]
                logging.info(f"Usuários que você segue mas não te seguem de volta: {len(not_following_back)}")
                for user in not_following_back:
                    logging.info(f" - {user}")
                
                if not_following_back:
                    # Descomente a linha abaixo para realmente deixar de seguir
                    # unfollower.unfollow_users(not_following_back)
                    logging.info("Para realmente deixar de seguir, descomente a linha 'unfollower.unfollow_users(not_following_back)' no script.")
                else:
                    logging.info("Nenhum usuário encontrado para deixar de seguir.")
            else:
                logging.warning("Não foi possível coletar ambas as listas de usuários. Verifique o log para erros.")
        else:
            logging.error("Falha no login. Verifique suas credenciais.")
        
        unfollower.close()





# Refinamentos e tratamento de erros adicionais podem ser incluídos aqui.
# Por exemplo, tentar novamente em caso de falha de clique, ou lidar com diferentes pop-ups.
# A lógica de logging já está configurada no início do script.


