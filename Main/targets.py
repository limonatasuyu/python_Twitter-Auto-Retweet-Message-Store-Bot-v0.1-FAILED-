import time
from selenium.webdriver.common.action_chains import ActionChains
from Data.targets import TargetsTable
from Utils.utils import DictAsObject
from BotBase.BotBase import BotBase

SELECTORS_DICTIONARY = {
    "homapage_tweet_input": "#react-root > div > div > div > main > div > div > div > div > div > div > div > div > div:nth-child(1) > div > div > div > div > div:nth-child(1) > div > div > div > div > div > div > div > div > div > div > label",
    "userpage_tweet_article": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > div:nth-child(3) > div > div > section > div > div > div:nth-child({x})",
    "explore_button": "#react-root > div > div > div > header > div > div > div > div > div > nav > a:nth-child(2)",
    "search_input": "#react-root > div > div > div > main > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > div > form > div > div > div > div > label",
    "search_page_people_button": "#react-root > div > div > div > main > div > div > div > div > div > div > div > div:nth-child(2) > nav > div > div > div > div:nth-child(3) > a",
    "search_page_username": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > div:nth-child(3) > section > div > div > div:nth-child({x}) > div > div > div > div > div > div > div > div > div > div > a > div > div > span",
    "reposts_and_likes_page_username": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child({x}) > div > div > div > div > div > div > div > div > div > div > a > div > div > span",
    "quotes_page_username": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child({x}) > div > div > article > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div > div > a > div > span",
    "quotes_page_quote_tweet": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child({x}) > div > div > article > div > div > div > div > div:nth-child(2)",
    "quotes_page_current_tweet_link": lambda x: f"#react-root > div > div > div > main > div > div > div > div > div > section > div > div > div:nth-child({x}) > div > div > article > div > div >       div > div:nth-child(2) > div > div > div > div > div > div:nth-child(2) > div > div:nth-child(3) > a",
}

SELECTORS = DictAsObject(SELECTORS_DICTIONARY)


class TargetGatherer(BotBase):

    def __init__(self, tweet_text, base_instance=None, tweet_image=None, target_pages=[]):

        if not type(self).is_logged_in:
            raise Exception("First you need to login.")

        self.target_pages = target_pages
        self.target_tweets = []
        self.target_users = []
        self.tweet_text = tweet_text
        self.tweet_image = tweet_image
        self.targets = TargetsTable()

    def gather_targets(self):
        for page in self.target_pages:
            self.current_target_page = page
            print("current target page: ", self.current_target_page)
            targets = self.__gather_target_users()

        time.sleep(1000)  # TODO: DELETE THIS LINE, ITS FOR DEBUGGING.

        targetsTableInstance = TargetsTable()
        for target in targets:
            targetsTableInstance.add_one(target["tweet_id"], target["action"], target["target_username"], target["target_tweet_id"])

    def __gather_target_users(self):

        # Sometimes if we directly go to target page using the url, twitter logs out automatically.
        current_url = self.get_current_url()
        if current_url == "https://twitter.com/home":
            self.__search_current_target_page()
        else:
            self.go_to(f"https://twitter.com/{self.current_target_page}")

        for i in range(1, 10):
            username_selector = SELECTORS.search_page_username(str(i))
            username = self.find_element_and_get_attribute(username_selector, "innerText", True)
            if username == "@" + self.current_target_page:
                self.find_element_and_click(SELECTORS.search_page_username(str(i)))
                break

        nth_tweet = 1
        self.find_element_and_click(SELECTORS.userpage_tweet_article(nth_tweet), True)

        self.current_tweet_id = self.__extract_current_tweet_id()
        targets = self.__find_targets()

        return targets

    def __search_current_target_page(self, user):
        actionChains = ActionChains(self.driver)
        explore_button = self.wait_for_an_element(SELECTORS.explore_button)
        actionChains.move_to_element(explore_button).click(explore_button).perform()

        time.sleep(1)

        enter_key = '\ue007'
        self.find_element_and_send_keys(SELECTORS.search_input, self.current_target_page + enter_key, True)

        time.sleep(1)

        self.find_element_and_click(SELECTORS.search_page_people_button, True)

    def __find_targets(self, max_target_count_per_action=100):

        quote_targets = self.__extract_targets_from_activity("quotes", max_target_count=max_target_count_per_action)
        retweet_targets = self.__extract_targets_from_activity("retweets", max_target_count=max_target_count_per_action)
        like_targets = self.__extract_targets_from_activity("likes", max_target_count=max_target_count_per_action)

        all_targets = quote_targets + retweet_targets + like_targets
        return all_targets

    def __extract_targets_from_activity(self, activity_type, max_target_count=100):
        if activity_type not in ['retweets', 'quotes', 'likes']:
            raise ValueError("Invalid activity_type. Supported values: 'retweets', 'quotes' or 'likes'.")

        activity_url = f"https://twitter.com/{self.current_target_page}/status/{self.current_tweet_id}/{activity_type}"
        self.driver.get(activity_url)
        targets = []

        if activity_type == 'retweets' or activity_type == "likes":
            username_selector = SELECTORS.reposts_and_likes_page_username
            targets_per_loop = 50
        elif activity_type == 'quotes':
            username_selector = SELECTORS.quotes_page_username
            targets_per_loop = 20

        is_activities_finished = False
        while len(targets) < max_target_count and not is_activities_finished:
            processed_target_count = 0

            for i in range(1, targets_per_loop + 1):
                target_count = targets_per_loop - i
                if len(targets) >= max_target_count:
                    break

                is_activity_exists = self.detect_element_presence(username_selector(target_count))
                if not is_activity_exists:
                    continue

                current_username = self.find_element_and_get_attribute(username_selector(target_count), "innerText", True)[1:]
                processed_target_count += 1

                if current_username in (target["target_username"] for target in targets):
                    if processed_target_count == 1:
                        is_activities_finished = True
                    break

                if activity_type == "quotes":
                    quote_tweet_url = self.find_element_and_get_attribute(SELECTORS.quotes_page_current_tweet_link(target_count), "href")
                    quote_tweet_id = quote_tweet_url.split('/')[-1]
                elif activity_type == "retweets" or activity_type == "likes":
                    quote_tweet_id = None

                targets.append({"tweet_id": self.current_tweet_id, "action": activity_type, "target_username": current_username, "target_tweet_id": quote_tweet_id})

            self.scroll_through_page(700)
            time.sleep(0.5)

        return targets

    def __extract_current_tweet_id(self):

        max_attempts = 60
        tweet_id = None
        for _ in range(max_attempts):
            time.sleep(1)
            current_url = self.get_current_url()
            print(f"Trying to extract tweet ID from current url ({current_url})")
            try:
                tweet_id = current_url.split("/")[5]
                break
            except IndexError:
                print(f"Error: Unable to extract tweet ID. Current URL is {current_url}.")
            except Exception as e:
                raise Exception(e)
        else:
            raise Exception(f"Error: Maximum attempts ({max_attempts}) reached without success.")

        return tweet_id
