import json
import random
import pyperclip
from tkinter import *
from tkinter import messagebox


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    password_list = []

    [password_list.append(random.choice(letters)) for _ in range(random.randint(8, 10))]
    [password_list.append(random.choice(symbols)) for _ in range(random.randint(2, 4))]
    [password_list.append(random.choice(numbers)) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.delete(0, "end")
    password_input.insert(END, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_credentials = {
        website: {
            "Username": username,
            "Password": password
        }
    }

    if website and username and password:
        try:
            with open("data.json", mode="r") as data_file:
                # Read old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_credentials, data_file, indent=4)
        else:
            # Update data
            data.update(new_credentials)
            with open("data.json", mode="w") as data_file:
                # Save updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, "end")
            password_input.delete(0, "end")
    else:
        messagebox.showerror(title="Oops :(", message="Please make sure you provided all credentials.")


# ---------------------------- SAVE PASSWORD ------------------------------- #
def search_credentials():
    website = website_input.get()
    if website:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Error", message="No Data File Found.")
        else:
            if website in data:
                username = data[website]["Username"]
                password = data[website]["Password"]
                messagebox.showinfo(title=website, message=f"Username: {username}\nPassword: {password}")
            else:
                messagebox.showinfo(title="Error", message=f"No details for {website} exist.")
    else:
        messagebox.showerror(title="Error", message="Please enter a website.")


# ---------------------------- UI SETUP ------------------------------- #
ui = Tk()
ui.title("Password Manager")
ui.minsize(width=450, height=340)
ui.config(padx=20, pady=20)

logo_canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
logo_canvas.create_image(100, 100, image=logo)
logo_canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

username_label = Label(text="Username/Email:")
username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_input = Entry(width=33)
website_input.grid(row=1, column=1, sticky="W")

username_input = Entry(width=35)
username_input.grid(row=2, column=1, columnspan=2, stick="EW")
username_input.insert(END, "my_email@gmail.com")
username_input.focus()

password_input = Entry(width=33)
password_input.grid(row=3, column=1, sticky="W")

# Buttons
search_button = Button(text="Search", width=14, command=search_credentials)
search_button.grid(row=1, column=2, sticky="E")

generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

# Mainloop
ui.mainloop()
