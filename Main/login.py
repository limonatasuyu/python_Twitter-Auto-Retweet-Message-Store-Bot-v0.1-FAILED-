import time
from bs4 import BeautifulSoup
from Data.accounts import AccountsTable
from Utils.utils import get_messages, get_message, delete_all_messages, generate_password, DictAsObject
from BotBase.BotBase import BotBase

SELECTORS_DICTIONARY = {
    "email_input": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label",
    "email_submit_button": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(7)",
    "username_input": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > label",
    "username_submit_button": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "confirmation_modal_next_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2)  > div > div > div > div",
    "modal_header": "#modal-header",
    "modal_header_span": "#modal-header > span > span",
    "modal_text": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > span > span",
    "got_it_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div",
    "find_your_acccount_next_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div > div > div",
    "generic_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label",
    "email_code": "html > body > table > tbody > tr:nth-child(2) > td > table:nth-child(2) > tbody > tr > td:nth-child(2) > table > tbody > tr:nth-child(5) > td > strong",
    "new_password_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > label",
    "new_password_confirm_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(3) > div > label",
    "change_password_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div > div",
    "password_change_reason_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label:nth-child(2) > div > input[type=radio]",
    "password_change_reason_next_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div > div > div > div",
    "account_access_generic_button": "body > div.PageContainer > div > form > input.Button.EdgeButton.EdgeButton--primary",
    "page_header": "div.PageHeader.Edge",
    "continue_to_x_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div",
    "refuse_non_essential_cookies_button": "#layers > div > div > div > div > div > div:nth-child(2) > div:nth-child(2)",
    "cookies_popup_header": "#layers > div > div > div > div > div > div > div > span",
}

TEXTS_DICTIONARY = {
    "change_pass": "enter the email, phone number, or username associated with your account to change your password.",
    "find_x_account": "find your x account",
    "confirmation_code": "where should we send a confirmation code?",
    "confirm_email": "confirm your email",
    "confirm_username": "confirm your username",
    "too_many_attempt": "too many password reset attempts",
    "we_sent_code": "we sent you a code",
    "why_change_password": "why'd you change your password?",
    "new_password": "choose a new password",
    "account_locked": "your account has been locked.",
    "all_set": "you’re all set",
    "cookies_popup_header": "did someone say … cookies?",
}


SELECTORS = DictAsObject(SELECTORS_DICTIONARY)
TEXTS = DictAsObject(TEXTS_DICTIONARY)


class TwitterLoginAutomation(BotBase):

    def __init__(self, *args, **kwargs):
        print("child class initialized")
        print("self from child: ", self)
        self.account_index = 0

    def __get_verification_code(self, doc):
        soup = BeautifulSoup(str(doc), 'html.parser')
        elements = soup.select(SELECTORS.email_code)
        text = elements[0].text
        return text

    def __handle_confirmation(self):

        verification_code = ""

        for i in range(10):
            time.sleep(1)
            messages = get_messages(self.email, self.password)
            if len(messages["hydra:member"]) == 0:
                continue
            for message in messages["hydra:member"]:
                if message["subject"].strip() == "Password reset request":
                    full_message = get_message(self.email, self.password, message["downloadUrl"])
                    verification_code = self.__get_verification_code(full_message)
                else:
                    continue
                self.find_element_and_send_keys(SELECTORS.generic_input, verification_code, True)
                time.sleep(1.5)
                self.find_element_and_click(SELECTORS.confirmation_modal_next_button)
                break
            break
        delete_all_messages(self.email, self.password)
        return True

    def __handle_modals(self, password_inputs_filled, passwordCanChange):

        modal_header_string = self.find_element_and_get_attribute(SELECTORS.modal_header_span, "innerText", True, "long")
        modal_header_string = modal_header_string.strip()

        print("Modal Header String: ", modal_header_string)

        if modal_header_string.lower() == TEXTS.find_x_account:
            modal_text = self.find_element_and_get_attribute(SELECTORS.modal_text, "innerText", True)
            if modal_text.lower() == TEXTS.change_pass and not passwordCanChange:
                self.account_index += 1
                self.login()
                return
            elif modal_text.lower() == TEXTS.change_pass and passwordCanChange:

                self.find_element_and_send_keys(SELECTORS.generic_input, self.email)
                time.sleep(1.5)
                self.find_element_and_click(SELECTORS.find_your_acccount_next_button)
            else:
                print("An unexpected condition occured, program will closed in 100 seconds")
                time.sleep(100)
                return

        if modal_header_string.lower() == TEXTS.confirmation_code:
            self.find_element_and_click(SELECTORS.confirmation_modal_next_button)
            self.__handle_confirmation()
        elif modal_header_string.lower() == TEXTS.confirm_email:
            self.find_element_and_send_keys(SELECTORS.generic_input, self.email, True)
            time.sleep(1.5)
            self.find_element_and_click(SELECTORS.find_your_acccount_next_button)
        elif modal_header_string.lower() == TEXTS.confirm_username:
            self.find_element_and_send_keys(SELECTORS.generic_input, self.username, True)
            time.sleep(1.5)
            self.find_element_and_click(SELECTORS.find_your_acccount_next_button)
        elif modal_header_string.lower() == TEXTS.we_sent_code:
            self.__handle_confirmation()
        elif modal_header_string.lower() == TEXTS.new_password:
            if not password_inputs_filled:
                new_password = generate_password()
                print("new_password: ", new_password)
                self.find_element_and_send_keys(SELECTORS.new_password_input, new_password, True)
                self.find_element_and_send_keys(SELECTORS.new_password_confirm_input, new_password, True)
                password_inputs_filled = True
                time.sleep(1.5)
                self.find_element_and_click(SELECTORS.change_password_button, True)
        elif modal_header_string.lower() == TEXTS.why_change_password:
            self.find_element_and_click(SELECTORS.password_change_reason_input)
            self.find_element_and_click(SELECTORS.password_change_reason_next_button)
        elif modal_header_string.lower() == TEXTS.all_set:
            self.find_element_and_click(SELECTORS.continue_to_x_button)
        elif modal_header_string.lower() == TEXTS.too_many_attempt:
            print("An unexpected condition occured, program will closed in 100")
            for i in range(99):
                time.sleep(1)
                print(99 - i)
            return

    def login(self, passwordCanChange=False):
        accounts = AccountsTable()
        account = accounts.get_random_account()
        self.username = account[4]
        self.password = account[3]
        self.email = account[1]

        self.driver.get("https://twitter.com/login")

        delete_all_messages(self.email, self.password)

        self.find_element_and_send_keys(SELECTORS.email_input, self.email, True)
        self.find_element_and_click(SELECTORS.email_submit_button)

        password_inputs_filled = False
        while True:

            if self.get_current_url() == "https://twitter.com/account/access":
                page_header_exists = self.detect_element_presence(SELECTORS.page_header)
                if page_header_exists:
                    self.find_element_and_click(SELECTORS.account_access_generic_button)
            elif self.get_current_url() == "https://twitter.com/home":
                break

            self.__handle_modals(password_inputs_filled=password_inputs_filled, passwordCanChange=passwordCanChange)

            time.sleep(1)

        cookies_popup_exists = self.detect_element_presence(SELECTORS.cookies_popup_header)
        if cookies_popup_exists:
            cookies_popup_header_string = self.find_element_and_get_attribute(SELECTORS.cookies_popup_header, "innerText")
            if cookies_popup_header_string.lower() == TEXTS.cookies_popup_header:
                self.find_element_and_click(SELECTORS.refuse_non_essential_cookies_button)

        self.__class__.change_to_logged_in()


if __name__ == "__main__":
    twitter_automation = TwitterLoginAutomation()
    twitter_automation.login(passwordCanChange=True)
