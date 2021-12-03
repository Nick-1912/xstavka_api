from selenium.webdriver.common.keys import Keys
from bin.browser import Browser
from selenium.common.exceptions import NoSuchElementException
from bin.exceptions import XstavkaError, CssSelectorError


class Xstavka(Browser):
    def __init__(self, undetected=None, fullscreen=None, windowHeight=None, windowWidth=None) -> None:
        super().__init__(undetected, fullscreen, windowHeight, windowWidth)
        self.driver = self.create_browser_undetected(profile_name='xstavka') if self.undetected else self.create_browser()

    def open_page(self, url=None) -> None:
        if url is None:
            raise XstavkaError('Url arg is None')
        self.driver.get(url)

    def login(self) -> bool:
        try:
            self.click(self.find_by_CSS(self.config['ButtonsCSS_login']['enter_login_panel']))
            self.random_sleep()
        except NoSuchElementException:
            raise CssSelectorError('Cant find login button')

        self.send_keys_delay(self.find_by_CSS(self.config['ButtonsCSS_login']['login_input']), self.config['UserData']['login'])
        self.random_sleep()

        self.send_keys_delay(self.find_by_CSS(self.config['ButtonsCSS_login']['password_input']), self.config['UserData']['password'])
        self.random_sleep()

        self.click(self.find_by_CSS(self.config['ButtonsCSS_login']['enter_button']))
        self.random_sleep(50, 100)

        if self.is_second_auth():
            for i in range(3):
                self.second_auth()
                if self.is_second_auth_done():
                    print('Authed')
                    break
                print(f'{i + 1} try was unsuccessful')
            else:
                raise XstavkaError('Many attempts at 2FA were unsuccessful')

    def is_second_auth(self) -> bool:
        try:
            self.find_by_CSS(self.config['ButtonsCSS_login']['second_auth_check1'])
            return True
        except NoSuchElementException:
            return False

    def second_auth(self, code) -> None:
        code = input('type second auth code: ')
        self.send_keys_delay(self.find_by_CSS(self.config['ButtonsCSS_login']['second_auth_input']), code + Keys.ENTER)
        self.random_sleep(50, 100)

    def is_second_auth_done(self) -> bool:
        try:
            self.find_by_CSS(self.config['ButtonsCSS_login']['second_auth_check2'])
            return True
        except NoSuchElementException:
            return False

    def check_balance(self) -> float:
        try:
            self.click(self.find_by_CSS(self.config['ButtonsCSS_main']['balance']))
        except NoSuchElementException:
            raise XstavkaError('Cant check balance')
        self.random_sleep()
        return float(self.find_by_CSS(self.config['ButtonsCSS_main']['balance']).get_attribute('innerText'))
