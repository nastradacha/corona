from selenium import webdriver
from configs.config import chrome_driver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait


# self.chrome_options = webdriver.ChromeOptions()
# self.chrome_options.add_argument("--window-size=1920,1080")
# self.chrome_options.add_argument("--disable-extensions")
# self.chrome_options.add_argument("--proxy-server='direct://'")
# self.chrome_options.add_argument("--proxy-bypass-list=*")
# self.chrome_options.add_argument("--start-maximized")
# self.chrome_options.add_argument('--headless')
# self.chrome_options.add_argument('--disable-gpu')
# self.chrome_options.add_argument('--disable-dev-shm-usage')
# self.chrome_options.add_argument('--no-sandbox')
# self.chrome_options.add_argument('--ignore-certificate-errors')
# self.browser = webdriver.Chrome(options=self.chrome_options)


def browser():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--proxy-server='direct://'")
    chrome_options.add_argument("--proxy-bypass-list=*")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-certificate-errors")
    # chrome_options.add_argument("--headless")
    # initiate Chrome browser
    driver = webdriver.Chrome(executable_path=chrome_driver, options=chrome_options)
    driver.set_window_position(0, 0)
    # browser.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(2)
    return driver


browser = browser()

wait = WebDriverWait(browser, 10)
# options.add_argument('window-size=1200x600')  # optional


def check_exists_by_xpath(css):
    try:
        browser.find_element_by_css_selector(css)
    except NoSuchElementException:
        return False
    return True
