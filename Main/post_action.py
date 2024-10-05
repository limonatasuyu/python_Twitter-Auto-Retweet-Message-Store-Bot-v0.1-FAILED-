import time
import pyautogui
from Data.targets import TargetsTable
from BotBase.BotBase import BotBase
from Utils.utils import DictAsObject

SELECTORS_DICTIONARY = {
    "warning_modal": "#layers > div > div > div > div > div > div > div > div > div > div > div > div > div > div > span",
    "warning_modal_skip_button": "#layers > div > div > div > div > div > div > div > div > div > div div > div > div:nth-child(3) > di",
    "retweet_options_button": "#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div:nth-child(3) > div:nth-child(5) > div > div > div:nth-child(2) > div",
    "repost_button": "#layers > div > div > div > div > div > div > div > div > div > div > div",
    "quote_button": "#layers > div > div > div > div > div > div > div > div > div > div > a:nth-child(2)",
    "quote_text_input": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > label",
    "quote_media_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > div > nav > div > div > div > div:nth-child(1) > div > div",
    "quote_submit_button": "#layers > div:nth-child(2) > div > div > div > div > div > div > div > div > div > div > div:nth-child(3) > div > div:nth-child(1) > div > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(4)",
    "like_button": "#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child(1) > div > div > article > div > div > div:nth-child(3) > div:nth-child(5) > div > div > div:nth-child(3) > div",
    "homepage_tweet_input": "#react-root > div > div > div > main > div > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div > div > div > div > div > label",
    "homepage_add_photo_to_tweet_button": "#react-root > div > div > div > main > div > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div:nth-child(2) > div > div > nav > div > div > div > div:nth-child(1) > div > div",
    "homepage_tweet_post_button": "#react-root > div > div > div > main > div > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(4)",
    "tweet_page_reply_input": "#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child(1) > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div > div > div > div > div > label > div > div > div > div > div > div > div:nth-child(2) > div",
    "tweet_page_reply_button": "#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child(1) > div > div > div > div > div > div:nth-child(2) > div > div > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(2)",
    "tweet_page_add_image_button": "#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child(1) > div > div > div > div > div > div:nth-child(2) > div > div > div > div:nth-child(2) > div > div:nth-child(2) > div > div > nav > div > div > div > div:nth-child(1) > div > div",
}

TEXTS_DICTIONARY = {"warning_modal_header": "unlock more on x"}

SELECTORS = DictAsObject(SELECTORS_DICTIONARY)

TEXTS = DictAsObject(TEXTS_DICTIONARY)


class PostActionMaker(BotBase):

    def __init__(self, *args, **kwargs):
        self.targets = TargetsTable()

    def auto_retweet(self, page_name):

        all_targets = self.targets.get_all_with_same_page(page_name)

        for target in all_targets:
            target_tweet_id = target["target_tweet_id"]
            text = self.current_retweet_text
            image = self.current_retweet_image
            self.__retweet(page_name, target_tweet_id, text, image)

    def auto_like(self, page_name=None, tweet_id=None, count=None):
        if page_name is None and tweet_id is None:
            raise ValueError("Either page_name or tweet_id needs to be present.")
        elif tweet_id is None:
            target_tweets = self.targets.get_all_with_same_page(page_name)
        elif page_name is None:
            target_tweets = self.targets.get_all_with_same_tweet_id(tweet_id)
        else:
            target_tweets = self.targets.get_all_with_same_tweet_id_and_page_name(tweet_id=tweet_id, page_name=page_name)

        if count is None:
            count = len(target_tweets)
        for index in range(count):
            current_target = target_tweets[index]
            self.__like(current_target)

    def auto_repost(self, page_name, count=None):
        target_tweets = self.targets.get_all_with_same_page(page_name)
        if count is None:
            count = len(target_tweets)
        for index in range(count):
            current_target = target_tweets[index]
            self.__repost(current_target)

    def __retweet(self, page_name, target_tweet_id, text="", image=None):

        raise NotImplementedError("Needs quote submit button selector")

        if text == "" and image is None:
            raise ValueError("Either text or image needs to be present.")

        url = f"https://twitter.com/{page_name}/status/{target_tweet_id}"
        self.go_to(url)

        self.find_element_and_click(SELECTORS.retweet_options_button, True)
        self.find_element_and_click(SELECTORS.quote_button)
        self.find_element_and_send_keys(SELECTORS.quote_text_input, text, True)
        if image is not None:
            self.find_element_and_click(SELECTORS.quote_media_button)
            pyautogui.write(image)
            pyautogui.press('enter')

        self.find_element_and_click(SELECTORS.quote_submit_button)
        time.sleep(0.4)

    def __like(self, tweet):

        username = tweet["target_username"]
        target_tweet_id = tweet["target_tweet_id"]
        url = f"https://twitter.com/{username}/status/{target_tweet_id}"
        self.go_to(url)

        self.find_element_and_click(SELECTORS.like_button)

    def __repost(self, tweet):
        username = tweet["target_username"]
        target_tweet_id = tweet["target_tweet_id"]
        url = f"https://twitter.com/{username}/status/{target_tweet_id}"
        self.go_to(url)

        self.find_element_and_click(SELECTORS.retweet_options_button)
        self.find_element_and_click(SELECTORS.repost_button)
