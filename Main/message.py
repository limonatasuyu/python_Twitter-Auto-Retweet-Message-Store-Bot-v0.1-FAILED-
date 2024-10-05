import time
import pyautogui
from BotBase.BotBase import BotBase
from Utils.utils import DictAsObject

send_message_with_image = "#react-root > div > div > div > main > div > div > div > section:nth-child(2) > div > div > div > div > div > aside > div > div:nth-child(3)"
send_message_without_image = "#react-root > div > div > div > main > div > div > div > section:nth-child(2) > div > div > div > div > div > aside > div > div:nth-child(2)"

SELECTORS_DICTIONARY = {
    "info_modal_header1": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div > span",
    "info_modal_skip_button1": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(3)",
    "info_modal_header2": "#layers > div:nth-child(3) > div > div > div > div > div > div > div > div > div > div > div > div > div > span",
    "info_modal_skip_button2": "#layers > div:nth-child(3) > div > div > div > div > div > div > div > div > div > div > div > div:nth-child(2) > div",
    "user_page_message_button": "#react-root > div > div > div > main > div > div > div > div > div > div:nth-child(3) > div > div > div > div > div > div:nth-child(2) > div:nth-child(2)",
    "message_text_input": "#react-root > div > div > div > main > div > div > div > section:nth-child(2) > div > div > div > div > div > aside > div > div > div > div > div > div > div > label > div > div > div > div > div > div > div:nth-child(2) > div",
    "send_message_button": lambda with_image: send_message_with_image if with_image else send_message_without_image,
    "message_photo_button": "#react-root > div > div > div > main > div > div > div > section:nth-child(2) > div > div > div > div > div > aside > div > div > div",
    "follower_username": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child({x}) > div > div > div > div > div > div > div > div > div > div > a > div > div > span"
}

TEXTS_DICTIONARY = {"info_modal_header1": "Introducing pinned conversations"}

SELECTORS = DictAsObject(SELECTORS_DICTIONARY)

TEXTS = DictAsObject(TEXTS_DICTIONARY)


class Messager(BotBase):

    def __init__(self, bot_username, *args, **kwargs):
        self.bot_username = bot_username

    def auto_message(self, count):
        messagable_targets = self.__get_messagable_targets(max_target_count=count)
        if len(messagable_targets) < count:
            print(f"WARNING: found {len(messagable_targets)} messagable targets. There are not f{count} targets found.")
            count = len(messagable_targets)

        for index in range(count):
            current_target = messagable_targets[index]
            self.__message_to_target(current_target)

    def __get_messagable_targets(self, max_target_count):
        url = f"https://twitter.com/{self.bot_username}/followers"
        self.go_to(url)

        targets_per_loop = 50
        targets = []
        is_activities_finished = False
        while len(targets) < max_target_count and not is_activities_finished:
            processed_target_count = 0

            for i in range(1, targets_per_loop + 1):
                target_count = targets_per_loop - i
                if len(targets) >= max_target_count:
                    break

                is_activity_exists = self.detect_element_presence(SELECTORS.follower_username(target_count))
                if not is_activity_exists:
                    continue

                current_username = self.find_element_and_get_attribute(SELECTORS.follower_username, "innerText", True)[1:]
                processed_target_count += 1

                if current_username in targets:
                    if processed_target_count == 1:
                        is_activities_finished = True
                    break

                targets.append(current_username)

            self.scroll_through_page(700)
            time.sleep(0.5)

        return targets

    def __message_to_target(self, target_username, text="", image=None):

        if text == "" and image is None:
            raise ValueError("Either text or image needs to be present.")

        url = f"https://twitter.com/{target_username}"
        self.go_to(url)

        self.find_element_and_click(SELECTORS.user_page_message_button, True)
        self.find_element_and_send_keys(SELECTORS.message_text_input, True)
        if image is not None:
            self.find_element_and_click(SELECTORS.message_photo_button)
            pyautogui.write(image)
            pyautogui.press('enter')
