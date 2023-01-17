import os
import threading
import time

from models.sorteo import Sorteo
from selenium import webdriver
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
)
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SorteoController:
    def __init__(self):
        self.modelSorteo = Sorteo()

    def setup(self):
        self.__WHATSAPP_USER = self.modelSorteo.WHATSAPP_USER
        self.__WORD_SEARCH = self.modelSorteo.WORD_SEARCH

        self.chrome_options = Options()
        self.xpath = By.XPATH
        self.chrome_options.add_argument("--user-data-dir=chrome-data")

        os.path.exists("chrome-data") and self.chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome("chromedriver", options=self.chrome_options)
        self.wait = WebDriverWait(
            self.driver,
            80,
            ignored_exceptions=(StaleElementReferenceException, NoSuchElementException),
        )
        self.actions = ActionChains(self.driver)
        self.driver.get("https://web.whatsapp.com/")

    def execute(self):
        self.setup()
        chats_list = self.get_chat_list()

        for chat_list in chats_list:

            try:
                self.actions.move_to_element(chat_list).click().perform()
                time.sleep(4)

                contact = chat_list.find_element(
                    self.xpath, './/span[@dir="auto"]'
                ).text
                panel_messages = chat_list.find_elements(
                    self.xpath, '//div[@data-testid="conversation-panel-messages"]'
                )
            except:
                continue

            for panel_message in panel_messages:
                chats = panel_message.find_elements(
                    self.xpath, '//div[@class="copyable-text"]'
                )

                for chat in chats:
                    data_plain_text = chat.get_attribute("data-pre-plain-text")

                    try:

                        message = chat.find_element(self.xpath, "./div/span/span").text

                        if (
                            data_plain_text.find(self.__WHATSAPP_USER) == -1
                            and self.__WORD_SEARCH in message.lower()
                        ):
                            data_plain_text = data_plain_text.translate(
                                str.maketrans("", "", "[],")
                            )

                            message_date = (
                                data_plain_text.split(" ")[1]
                                + " "
                                + data_plain_text.split(" ")[0]
                            )

                            if not self.modelSorteo.checkSavedMessage(
                                contact, message, message_date
                            ):

                                self.modelSorteo.insertMensaje(
                                    contact, message, message_date
                                )
                    except:
                        continue

        self.close()

    def run_time(self, seconds):
        while True:
            self.execute()
            time.sleep(seconds)
            continue

    def init_thread(self):
        time_interval = self.modelSorteo.NUMBER_HOURS_THREAD * 3600
        thread = threading.Thread(target=self.run_time, args=(time_interval,))
        thread.start()

    def get_draw(self, date_from, date_to):
        return self.modelSorteo.generateDraw(date_from, date_to)

    def close(self):
        self.driver.close()

    def get_chat_list(self):
        self.wait.until(
            EC.presence_of_element_located(
                (self.xpath, '//div[@data-testid="chat-list"]')
            )
        )

        time.sleep(4)

        return self.driver.find_elements(
            self.xpath, '//div[@data-testid="chat-list"]/div/div'
        )
