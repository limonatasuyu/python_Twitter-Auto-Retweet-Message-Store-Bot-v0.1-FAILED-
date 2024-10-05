from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from MITMProxy.MITMProxy import MITMProxy


class BotBaseMeta(type):

    def __call__(cls, *args, **kwargs):
        if cls == BotBase:
            return super().__call__(*args, **kwargs)
        else:
            if 'base_instance' in kwargs:
                base_instance = kwargs['base_instance']
            if cls.__base__ == BotBase:
                instance = super().__call__(*args, **kwargs)
                instance.__dict__.update(base_instance.__dict__)
                return instance
            else:
                raise ValueError(
                    "Provided base_instance must be an instance of BotBase.")


class BotBase(metaclass=BotBaseMeta):
    is_logged_in = False
    is_captcha_configured = False

    @classmethod
    def change_to_logged_in(cls):
        cls.is_logged_in = True

    def __init__(self, *args, **kwargs):
        self.mitm_proxy = MITMProxy()
        self.mitm_proxy.start_proxy()
        self.mitm_proxy_port = self.mitm_proxy.proxy_port
        self.initialize_driver()

    def initialize_driver(self):
        if hasattr(self, "driver"):
            self.driver.quit()

        options = webdriver.ChromeOptions()
        options.add_argument('--start-minimized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        options.add_argument("--window-size=1920x1080")
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0"
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("sec-ch-ua-platform=Windows")

        self.driver = webdriver.Chrome(options=options)

        mitm_proxy_address = f'http://localhost:{self.mitm_proxy_port}'
        print("mitm proxy: ", mitm_proxy_address)
        self.driver.proxy = {"http": mitm_proxy_address,
                             "https": mitm_proxy_address}
        self.wait_short = WebDriverWait(self.driver, 10)
        self.wait_long = WebDriverWait(self.driver, 300)

    def go_to(self, url):
        self.driver.get(url)

    def get_current_url(self):
        return self.driver.current_url

    def detect_element_presence(self, selector):
        return bool(self.driver.find_elements(By.CSS_SELECTOR, selector))

    def detect_home_page(self):
        pass

    def find_element_and_send_keys(self, selector, keys, wait=False, wait_type="short"):
        if not wait:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
        elif wait_type == "long":
            element = self.wait_long.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
        elif wait_type == "short":
            element = self.wait_short.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
            )
        else:
            raise Exception("wait_type or wait paramater is not compatible")

        element.send_keys(keys)

    def find_element_and_click(self, selector, wait=False, wait_type="short"):
        if not wait:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
        elif wait_type == "long":
            element = self.wait_long.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        elif wait_type == "short":
            element = self.wait_short.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        else:
            raise Exception("wait_type or wait paramater is not ...")
        element.click()

    def find_element_and_get_attribute(self, selector, attribute_name, wait=False, wait_type="short"):

        element = None
        if not wait:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
        elif wait_type == "long":
            element = self.wait_long.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        elif wait_type == "short":
            element = self.wait_short.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        else:
            raise ValueError(
                "Invalid wait_type. It should be 'short' or 'long'.")

        return element.get_attribute(attribute_name)

    def wait_for_an_element(self, selector, wait_type="short"):
        if wait_type not in ["short", "long"]:
            raise ValueError(
                "Invalid wait_type. It should be 'short' or 'long'.")

        wait = self.wait_short
        if wait_type == "long":
            wait = self.wait_long

        element = wait.until(EC.visibility_of_element_located(
            (By.CSS_SELECTOR, selector)))
        return element

    def wait_for_any_element(self, selectors, wait_type="short"):
        if wait_type not in ["short", "long"]:
            raise ValueError(
                "Invalid wait_type. It should be 'short' or 'long'.")

        conditions = [EC.visibility_of_element_located(
            (By.CSS_SELECTOR, selector)) for selector in selectors]

        wait = self.wait_short
        if wait_type == "long":
            wait = self.wait_long

        index = None

        try:
            for i, condition in enumerate(conditions):
                try:
                    wait.until(EC.any_of(condition))
                    index = i
                    break
                except Exception:
                    pass

            return index

        except Exception as err:
            print("Error: ", err)
            return None

    def is_page_scrolled(self):
        script = "return (window.pageYOffset !== undefined) ? window.pageYOffset : (document.documentElement || document.body.parentNode || document.body).scrollTop;"
        scroll_position = self.driver.execute_script(script)
        return scroll_position

    def scroll_through_page(self, value=None):
        if value is None:
            script = "window.scrollTo(0, document.body.scrollHeight);"
        elif isinstance(value, int) and value >= 0:
            script = f"window.scrollTo(0, {value} + window.scrollY);"
        else:
            raise ValueError("Value must be a non-negative integer or None")
        self.driver.execute_script(script)

    def print_logs(self):
        logs = self.driver.get_log('browser')
        for log_entry in logs:
            print(log_entry)
