from tkinter import *
from tkinter import messagebox
import random
import string
import pyperclip
import json


# ---------------------------- Search For Account ------------------------------- #
def search_account():
    website = website_entry.get()
    try:
        with open("data.json", "r") as vault_file:
            data = json.load(vault_file)
    except json.JSONDecodeError:
        messagebox.showinfo(title="Account Not Found!", message="You first need to have accounts!")
    else:
        if website in data:
            acc = data[website]["account"]
            password = data[website]["password"]
            messagebox.showinfo(title="Account Found!", message=f"Website: {website}\nAccount: {acc}\nPassword:"
                                                                f" {password}")
        else:
            messagebox.showinfo(title="Account Not Found!", message="Account Not found!")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    password_entry.delete(0, END)
    characters = list(string.ascii_letters + string.digits + "!@#$%^&*()")
    length = random.randint(8, 13)
    random.shuffle(characters)
    password = [random.choice(characters) for _ in range(length)]
    random.shuffle(password)
    password_entry.insert(0, "".join(password))
    pyperclip.copy("".join(password))


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_pass():
    website = website_entry.get()
    account = account_entry.get()
    password = password_entry.get()

    if not website or not password:
        is_ok = False
        messagebox.showinfo(title="Error Found",
                            message="Please don't leave any of the fields empty")
    else:
        is_ok = messagebox.askokcancel(
            title=website,
            message=f"Account: {account}\nPassword: {password}\nIs it ok to save?")
    if is_ok:
        messagebox.showinfo(title="Success!", message="Your Info is Safe With Us!")
        new_acc = {website: {"account": account, "password": password}}
        try:
            with open("data.json", "r") as vault_file:
                data = json.load(vault_file)
                data.update(new_acc)
            with open("data.json", "w") as vault_file:
                json.dump(data, vault_file, indent=4)
        except json.JSONDecodeError:
            with open("data.json", "w") as vault_file:
                json.dump(new_acc, vault_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
# Canvas
win = Tk()
win.title("Password Manager")
win.config(padx=50, pady=50)
canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
account_label = Label(text="Email/Username:")
account_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()
account_entry = Entry(width=35)
account_entry.grid(column=1, row=2, columnspan=2)
account_entry.insert(0, "israel@gmail.com")
password_entry = Entry(width=18)
password_entry.grid(column=1, row=3, columnspan=1)

# Buttons
search_btn = Button(text="Search", command=search_account)
search_btn.grid(column=2, row=1, columnspan=2)
generate_pass_btn = Button(text="Generate Password", command=gen_pass)
generate_pass_btn.grid(column=2, row=3, columnspan=2)
add_account_btn = Button(text="Add", width=36, command=save_pass)
add_account_btn.grid(column=1, row=4, columnspan=2)

# Window Loop
win.mainloop()
