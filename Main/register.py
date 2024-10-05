import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
# from selenium.common.exceptions import ElementClickInterceptedException
from BotBase.BotBase import BotBase
from Data.accounts import AccountsTable
from Utils.utils import create_account, generate_random_string, get_messages, DictAsObject
from colorama import Fore, Style, init as init_colorama


SELECTORS_DICTIONARY = {
    "create_account_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(5)",
    "name_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div:nth-child(1) > label",
    "use_email_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div:nth-child(3)",
    "email_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div:nth-child(2) > label",
    "month_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "day_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(2)",
    "year_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(3)",
    "next_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "cookie_policy": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label > div:nth-child(2) > label",
    "signup_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div",
    "verification_code_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label",
    "step4_next_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "password_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label",
    "step5_next_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div > div",
    "locked_account_text": "body > div.PageContainer > div > div.PageHeader.Edge",
    "skip_for_now_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "username_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label > div > div > div > input",
    "username_modal_skip_for_now": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "continue_authenticate_button": "body > div.PageContainer > div > form > input.Button.EdgeButton.EdgeButton--primary",
    "authenticate_button": "div > div > button",
    "turn_on_notifications_skip_for_now_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div  > div:nth-child(2) > div:nth-child(2)",
    "audio_challange_header": "#root > div > form > h2",
    "start_arkose_challenge_button": "body > div.PageContainer > div > form > input.Button.EdgeButton.EdgeButton--primary",
    "step_header": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div > h2 > span",
    "arkose_authenticate_button": "#root > div > div> button",
    "arkose_info_text": "#root > div > div > div > h2 > span",
    "arkose_submit_button": "#root > div > div > div > button",
}

SELECTORS = DictAsObject(SELECTORS_DICTIONARY)


class TwitterSignupAutomation(BotBase):
    def __init__(self, base_instance=None):
        init_colorama()

    def __detect_arkose(self):
        time.sleep(2)
        print("\n\n\n---======----\nDETECTING ARKOSE\n---======----\n\n\n")
        if bool(self.driver.find_elements(By.ID, "arkoseFrame")):
            self.__handle_arkose("arkoseFrame")
        elif bool(self.driver.find_elements(By.ID, "arkose_iframe")):
            self.__handle_arkose("arkose_iframe")

    def __handle_arkose(self, arkose_id):

        print(f"{Fore.GREEN}\n\n\n---======----\nARKOSE DETECTED\n---======----\n\n\n{Style.RESET_ALL}")
        return

        self.wait_long.until(EC.visibility_of_element_located((By.ID, arkose_id)))
        self.driver.switch_to.frame(arkose_id)
        self.wait_long.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))
        self.driver.switch_to.frame(0)
        self.wait_long.until(EC.visibility_of_element_located((By.TAG_NAME, "iframe")))  # "game-core-frame")))
        self.driver.switch_to.frame(0)

        # try:
        #    self.find_element_and_click(SELECTORS.arkose_authenticate_button, True, "long")
        # except ElementClickInterceptedException as e:
        #    print(f"Error happened while clicking to button: {e}")
        self.driver.switch_to.default_content()
        print("\n\n\n---=======================---\nARKOSE CHALLENGE HAPPENING\n---====================---\n\n\n")
        return
        arkose_info_text = self.find_element_and_get_attribute(SELECTORS.arkose_info_text, 'innerText', True)
        substring_inside_parentheses = arkose_info_text.split('(')[-1]
        count_str = substring_inside_parentheses[:-1].split('of')[-1]
        challenge_count = int(count_str)
        for _ in range(challenge_count):
            self.wait_short.until(EC.visibility_of_element_located((By.CSS_SELECTOR, SELECTORS.arkose_submit_button)))
            self.find_element_and_click(SELECTORS.arkose_submit_button, True)
            time.sleep(5)

        self.driver.switch_to.default_content()

    def __execute_step_one(self, name, email_address):
        print("---=========\nEXECUTING STEP 1\n=============---")
        self.find_element_and_click(SELECTORS.create_account_button, True, "long")
        self.find_element_and_send_keys(SELECTORS.name_input, name, True)
        self.find_element_and_click(SELECTORS.use_email_button)
        self.find_element_and_send_keys(SELECTORS.email_input, email_address)

        month_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS.month_input)
        day_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS.day_input)
        year_input = self.driver.find_element(By.CSS_SELECTOR, SELECTORS.year_input)

        ActionChains(self.driver).click(month_input).send_keys("\ue015").send_keys("\ue007").perform()
        ActionChains(self.driver).click(day_input).send_keys("\ue015").send_keys("\ue007").perform()
        ActionChains(self.driver).click(year_input).send_keys("\ue015" * 22).send_keys("\ue007").perform()

        time.sleep(0.5)
        self.find_element_and_click(SELECTORS.next_button)

    def __execute_step_two(self):
        print("---=========\nEXECUTING STEP 2\n=============---")
        # self.find_element_and_click(SELECTORS.cookie_policy, True)
        self.find_element_and_click(SELECTORS.next_button, True)

    def __execute_step_three(self):
        print("---=========\nEXECUTING STEP 3\n=============---")
        self.find_element_and_click(SELECTORS.signup_button)

    def __execute_step_four(self, email_address, email_password):
        print("---=========\nEXECUTING STEP 4\n=============---")
        self.wait_for_an_element(SELECTORS.verification_code_input)
        verification_code = ""
        for i in range(10):
            time.sleep(1)
            print("=========\nTRYING TO RECEIVE VERIFICATION CODE\n=============")
            messages = get_messages(email_address, email_password)
            if len(messages["hydra:member"]) > 0 and messages["hydra:member"][0]["from"]["address"] == "info@x.com":
                verification_code = int(messages["hydra:member"][0]["subject"].split(" ")[0])
                print(f"====\nverification_code:  {verification_code}\n===")
                # print("===\nFIRST ATTEMPT\n===")
                self.find_element_and_send_keys(SELECTORS.verification_code_input, verification_code, True)
                self.find_element_and_click(SELECTORS.step4_next_button)
                time.sleep(2)
                # print("===\nSECOND ATTEMPT\n===")
                # self.find_element_and_send_keys(SELECTORS.verification_code_input, verification_code, True)
                # self.find_element_and_click(SELECTORS.step4_next_button)
                # time.sleep(2)
                return
                # current_step_text = self.find_element_and_get_attribute(SELECTORS.step_header, "innerText", True)
                # if current_step_text == "Step 5 of 5":
                #   return

        # raise Exception("Error While Executinh Step 4")

    def __execute_step_five(self, email_password):
        print("---=========\nEXECUTING STEP 5\n=============---")
        time.sleep(1)
        self.__detect_arkose()
        self.find_element_and_send_keys(SELECTORS.password_input, email_password, True, "long")
        time.sleep(1.5)
        self.find_element_and_click(SELECTORS.step5_next_button)

    def signup(self):
        account = create_account()
        email_address = account["address"]
        email_id = account["id"]
        email_password = account["password"]
        name = generate_random_string()

        self.go_to("https://twitter.com/signup")

        self.__execute_step_one(name, email_address)
        self.__detect_arkose()

        self.__execute_step_two()
        self.__detect_arkose()

        # self.print_logs()

        self.__execute_step_three()
        self.__detect_arkose()

        self.__execute_step_four(email_address, email_password)
        self.__detect_arkose()

        self.__execute_step_five(email_password)
        self.__detect_arkose()

        print("account is: ", account)
        print("gonna wait till end of time (1000 seconds actually)")
        time.sleep(1000)

        username = self.find_element_and_get__attribute(SELECTORS.username, "value", True)
        accounts = AccountsTable()
        accounts.add_one(email_address, name, email_password, username, email_id)

        self.driver.quit()


if __name__ == "__main__":
    instance = BotBase()
    twitter_signup_automation = TwitterSignupAutomation(base_instance=instance)
    twitter_signup_automation.signup()
