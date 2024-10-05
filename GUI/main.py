from tkinter import Tk, Button, Entry, Label, StringVar, E as East, W as West
import os
import sys
sys.path.append(os.path.abspath('../'))
from Utils.utils import PositiveInt

window = Tk()
window.title('Twitter Auto Retweet/Message/Store Bot v0.1')

label_description = Label(window, text="")
label_description.grid(row=0, column=3, sticky=West)


def on_hover(event, description):
    label_description.config(text=description)


def on_leave(event):
    label_description.config(text="")


def click_place_holder():
    print("Button clicked!")


class CustomButton:

    def __init__(self, text, description, grid_options, onClick=click_place_holder):
        self = Button(window, text=text, width=20, command=onClick)
        self.bind("<Enter>", lambda event: on_hover(event, description))
        self.bind("<Leave>", on_leave)
        self.grid(**grid_options)


class CustomLabel:

    def __init__(self, text, grid_options):
        self = Label(window, text=text, width=20)
        self.grid(**grid_options)


class CustomEntry(Entry):

    def __init__(self, description, grid_options, default_value="", valueType=str):
        if valueType not in [str, int, float, PositiveInt]:
            raise ValueError("valueType must be type `str`, type `int`, type `float`, or PositiveInt")
        super().__init__(window, textvariable=StringVar())
        self.bind("<Enter>", lambda event: on_hover(event, description))
        self.bind("<Leave>", on_leave)
        self.grid(**grid_options)
        self.value = StringVar()
        self.configure(textvariable=self.value)

        try:
            if valueType != PositiveInt:
                valueType(default_value)
            else:
                PositiveInt(default_value).value
        except ValueError:
            raise ValueError("Default value is not valid according to the specified valueType")

        self.value.set(default_value)
        self.old_value = default_value
        self.value.trace_add("write", self.onChange)
        self.valueType = valueType

    def onChange(self, *args):
        new_value = self.value.get()
        try:
            if new_value == "":
                pass
            elif self.valueType != PositiveInt:
                self.valueType(new_value)
            else:
                PositiveInt(int(new_value)).value
        except ValueError:
            self.value.set(self.old_value)  # Restore the old value
        else:
            self.old_value = new_value
            self.value.set(new_value)  # Setting to new_value instead of str(converted_value)


def main():
    CustomButton(text="Register Multiple", description="Register Multiple Accounts", grid_options={"column": 0, "row": 0, "sticky": East})
    CustomButton(text="Register One", description="Register One Account", grid_options={"column": 0, "row": 1})
    CustomButton(text="Login", description="Login An Account", grid_options={"column": 0, "row": 2})
    CustomButton(text="Gather Targets", description="Start To Gather Targets Automatically", grid_options={"column": 0, "row": 3})
    CustomButton(text="Retweet", description="Start To Retweet Gathered Targets Automatically", grid_options={"column": 0, "row": 4})
    CustomButton(text="Message", description="Start To Message Gathered Targets Automatically", grid_options={"column": 0, "row": 5})
    CustomButton(text="Auto Retweet", description="Start To Gather Targets And Retweet Automatically", grid_options={"column": 1, "row": 4})
    CustomButton(text="Auto Message", description="Start To Gather Targets And Message Automatically", grid_options={"column": 1, "row": 5})

    CustomLabel(text="Account Count", grid_options={"column": 1, "row": 0, "stick": East})
    CustomLabel(text="Target Count", grid_options={"column": 1, "row": 3, "stick": East})

    CustomEntry(description="Account Count", valueType=PositiveInt, default_value=100, grid_options={"column": 2, "row": 0})
    CustomEntry(description="Target Count", valueType=PositiveInt, default_value=100, grid_options={"column": 2, "row": 3})

    window.grid_columnconfigure(0, uniform="group1")
    window.grid_columnconfigure(1, uniform="group1")
    window.grid_columnconfigure(2, uniform="group1")

    window.mainloop()


if __name__ == "__main__":
    main()


'''
acc = {'@context': '/contexts/Account', '@id': '/accounts/655c9e19820d0331fb5bc529', '@type': 'Account', 'id': '655c9e19820d0331fb5bc529', 'address': 'vtrljnkk83@hoanghainam.com', 'quota': 40000000, 'used': 0, 'isDisabled': False, 'isDeleted': False, 'createdAt': '2023-11-21T12:10:01+00:00', 'updatedAt': '2023-11-21T12:10:01+00:00', 'retentionAt': '2023-11-29T20:10:01+00:00', 'password': '9e58E@%jL:dmOJ66z05-9L'}
accounts = AccountsTable()
email_address = acc["address"]
name = "a5lja-3o4x"
username = "A3o4x12797"
email_password = acc["password"]
email_id = acc["id"]
accounts.add_one(email_address, name, email_password, username, email_id)

TARGET_PAGES = []

sys.path.append(os.path.abspath('../'))
'''
