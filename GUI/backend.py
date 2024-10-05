import os
import sys
sys.path.append(os.path.abspath('../'))
from Main.login import TwitterLoginAutomation


def register_multiple(count):
    pass


def register_one():
    pass


def login(BotBaseInstance):
    LoginAutomationInstance = TwitterLoginAutomation(base_instance=BotBaseInstance)
    LoginAutomationInstance.login(passwordCanChange=True)


def gather_targets(count):
    pass


def retweet(BotBasInstance):
    pass


def message():
    pass


def auto_retweet():
    pass


def auto_message():
    pass
