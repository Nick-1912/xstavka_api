from configparser import ConfigParser
from os import path
from bin.exceptions import ConfigError, BrowserInitError, CssSelectorError
import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from random import randint
from selenium.webdriver.common.action_chains import ActionChains


class Config:
    def __init__(self) -> None:
        self.config = ConfigParser()
        self.config.read(path.join(path.dirname(path.realpath(__file__)), 'config.ini'))

    def get_value(self, section=None, row=None) -> str:
        if section is None:
            raise ConfigError('Section arg is None')
        if row is None:
            raise ConfigError('Row arg is None')
        return self.config[section][row]


class Browser:
    def __init__(self, undetected=None, fullscreen=None, windowHeight=None, windowWidth=None) -> None:
        if undetected is None:
            raise BrowserInitError('Undetected arg is None')
        if fullscreen is None:
            raise BrowserInitError('Fullscreen arg is None')
        if windowHeight is None:
            raise BrowserInitError('WindowHeight arg is None')
        if windowWidth is None:
            raise BrowserInitError('WindowWidth arg is None')
        
        # not headless because this parameter is not difficult to see, which is why a ban is possible
        self.undetected = undetected
        self.fullscreen = fullscreen
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.config = Config()

    def create_browser_undetected(self, profile_name=None):
        if profile_name is None:
            raise BrowserInitError('Profile name arg is None')
        options = uc.ChromeOptions()
        browser_path = path.join(path.dirname(path.realpath(__file__)), profile_name)
        options.add_argument('--user-data-dir=' + browser_path)
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        if self.fullscreen:
            options.add_argument('--kiosk')
        driver = uc.Chrome(options=options)
        driver.set_window_size(self.windowWidth, self.windowHeight)
        return driver

    def create_browser(self):
        options = Options()
        options.add_argument('--no-sandbox')
        options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
        if self.fullscreen:
            options.add_argument('--kiosk')
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(self.windowWidth, self.windowHeight)
        return driver

    def find_by_CSS(self, css_selector=None):
        if css_selector is None:
            raise CssSelectorError('WindowWidth arg is None')
        return self.driver.find_element(By.CSS_SELECTOR, css_selector)

    def move_to_element(self, element=None):
        if element is None:
            raise CssSelectorError('element arg is None')
        ac = ActionChains(self.driver).move_to_element(element)
        ac.perform()
    
    def click(self, element=None):
        if element is None:
            raise CssSelectorError('element arg is None')
        self.move_to_element(element)
        element.click()

    @staticmethod
    def random_sleep(left=20, right=50):
        sleep(randint(left, right) / 10)

    def send_keys_delay(self, element, keys, delay=0.2):
        if element is None:
            raise CssSelectorError('element arg is None')
        self.move_to_element(element)
        for key in keys:
            element.send_keys(key)
            sleep(delay)
