from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from models.sorteo import Sorteo
import time

class SorteoController:
    def __init__(self):
        self.modelSorteo = Sorteo()
    
    def setup(self):
        self.__WHATSAPP_USER = self.modelSorteo.WHATSAPP_USER
        self.__WORD_SEARCH = self.modelSorteo.WORD_SEARCH

        self.chrome_options = Options()
        self.xpath = By.XPATH
        self.chrome_options.add_argument("--user-data-dir=chrome-data")
        self.driver = webdriver.Chrome('chromedriver', options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 20)
        self.actions = ActionChains(self.driver)
        self.driver.get('https://web.whatsapp.com/')

    def execute(self):
        self.setup()
        chats_list = self.get_chat_list()

        time.sleep(6)
        for chat_list in chats_list:
            self.move_to_element(chat_list)
            contacto = chat_list.find_element(self.xpath, './/span[@dir="auto"]').text
            panel_messages = chat_list.find_elements(self.xpath, '//div[@data-testid="conversation-panel-messages"]')
            time.sleep(4)
            for panel_message in panel_messages:
                elements_chats = panel_message.find_elements(self.xpath, '//span[@class="i0jNr selectable-text copyable-text"]')

                for element_chat in elements_chats:
                    move_path_chat = element_chat.find_element(self.xpath,'./../../..')

                    try:
                        data_chat = move_path_chat.find_element(self.xpath,'.//div[@class="copyable-text"]').get_attribute("data-pre-plain-text")
                        data_chat.index(self.__WHATSAPP_USER)
                    except NoSuchElementException:
                        continue
                    except ValueError:
                        data_chat = data_chat.translate(str.maketrans('', '', '[],'))
                        if self.__WORD_SEARCH in element_chat.text.lower():

                            fecha = data_chat.split(' ')[1]+' '+data_chat.split(' ')[0]
                            if not self.modelSorteo.checkSavedMessage(contacto, element_chat.text, fecha):
                                self.modelSorteo.insertMensaje(contacto, element_chat.text, fecha)

        self.close()
    
    def get_draw(self, fecha_desde, fecha_hasta):
        return self.modelSorteo.generateDraw(fecha_desde, fecha_hasta)

    def close(self):
        self.driver.close()

    def get_chat_list(self):
        self.wait.until(EC.presence_of_element_located((self.xpath, '//div[@data-testid="chat-list"]')))
        return self.driver.find_elements(self.xpath, '//div[@data-testid="chat-list"]/div/div')

    def move_to_element(self, element):
        self.actions.move_to_element(element).click().perform()