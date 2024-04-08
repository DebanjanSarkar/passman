"""
Password Manager
--------------------
- This password manager is a GUI-program that is made using tkinter module.
- The Password Manager can be used to organise all your passwords at a single place.
- All the passwords are stored locally in a CSV file(created in a directory isndide current directory by default), and is thus secured.
- The password storage functionality can be extended to store passwords in a database, etc, using functions.

Author - Debanjan Sarkar
"""


import os
import random
import password_utils as utils
import tkinter
import tkinter.messagebox
import pyperclip

# ---------------------------- CONSTANTS ------------------------------- #
BLACK = "#000000"
LIGHT_BLUE = "#41C9E2"


FONT_STYLE = "calibri"
FONT_SIZE_BODY = 12

# This should be the path to the datafile(where data is to be saved), relative to this main Python file.
DATA_FILE_RELATIVE_PATH = "creds/saved_credentials.csv"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    # Randomly selects the length of password between 10 to 20 characters
    password_length = random.randint( 10, 20 )
    # Generates password using password_utils module function
    generated_password = utils.Password.generate_secure_password( n=password_length )

    # Clears the password field(if anything is typed by user)
    password_entry.delete( 0, tkinter.END )

    # Inserts the generated password into the Password Entry field
    password_entry.insert( 0, generated_password )

    # Copies the generated password to clipboard so that after generation, user can directly paste it
    pyperclip.copy( generated_password )
    # tkinter.messagebox.showinfo(title="Password Copied.", message="Password copied to clipboard!")


# ---------------------------- SAVE CREDENTIALS TO FILE ------------------------------- #
# The credentials input by user will be saved in a csv file with following column order:
# website,username,password
def validate_and_save_credentials():
    website = website_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        # If any field is left blank, then this block will run and show error dialogue box
        tkinter.messagebox.showerror(title="Error saving blank fields!", message="You cannot leave any field blank!")
    elif "," in website or "," in username or "," in password:
        # If any field value contains comma(,), this error dialogue box will be shown.
        # We are saving data in csv format, thus no field should have comma"," in it.
        tkinter.messagebox.showerror(title="Comma(,) character cannot be used!", message="You cannot use comma(,) in any of your fields!")
    else:
        creds_ok = tkinter.messagebox.askokcancel( title="Check your credentials.", message=f"The following are the entered credentials: \n\nWebsite:   {website} \nUsername/Email:   {username} \nPassword:   {password} \n\nDo you want to save it?" )
        if creds_ok:
            # If the user presses ok, this block of code will run to save the creds

            # Open the data file in "append" mode to write the credentials
            with open( os.path.join( os.path.dirname(__file__), DATA_FILE_RELATIVE_PATH ), mode="a" ) as data_file:
                data_file.write( f"{website},{username},{password}\n" )

            # Show infobox prompting user that password have been saved successfully.
            tkinter.messagebox.showinfo( title="SUCESS !", message="Credentials Saved Successfully!" )

            # After saving, clear out all the fields
            website_entry.delete( 0, tkinter.END )
            username_entry.delete( 0, tkinter.END )
            password_entry.delete( 0, tkinter.END )



# ---------------------------- UI SETUP ------------------------------- #

window = tkinter.Tk()
window.minsize( width=610, height=490 )
window.title("PASSMAN - Password Manager - made by Debanjan Sarkar")
window.config( padx=50, pady=50 )

# Components:
# ------------

# Creating the canvas to place logo image
canvas_width = 200
canvas_height = 200

canvas = tkinter.Canvas(
    master=window,
    width=canvas_width,
    height=canvas_height,
    background=BLACK
)

# Creating PhotoImage object of the logo to be used inside canvas
logo_img = tkinter.PhotoImage( file=os.path.join( os.path.dirname(__file__), "images/logo.png" ) )

canvas.create_image(
    canvas_width//2,
    canvas_height//2,
    image=logo_img
)

website_label = tkinter.Label(
    master=window,
    text="Website: ",
    font=( FONT_STYLE, FONT_SIZE_BODY )
)

website_entry = tkinter.Entry(
    master=window,
    width=60,
    # highlightbackground=LIGHT_BLUE,   # Highlights before the Entry is clicked and focussed, till it is clicked.
    highlightcolor=LIGHT_BLUE,          # Highlights after the Entry is clicked and focussed
    highlightthickness=3
)

username_label = tkinter.Label(
    master=window,
    text="Email / Username: ",
    font=( FONT_STYLE, FONT_SIZE_BODY )
)

username_entry = tkinter.Entry(
    master=window,
    width=60,
    highlightcolor=LIGHT_BLUE,          # Highlights after the Entry is clicked and focussed
    highlightthickness=3
)

password_label = tkinter.Label(
    master=window,
    text="Password: ",
    font=( FONT_STYLE, FONT_SIZE_BODY )
)

password_entry = tkinter.Entry(
    master=window,
    width=36,
    highlightcolor=LIGHT_BLUE,          # Highlights after the Entry is clicked and focussed
    highlightthickness=3
)

password_generate_button = tkinter.Button(
    master=window,
    text="Generate Password",
    font=( FONT_STYLE, FONT_SIZE_BODY ),
    command=generate_password
)

add_button = tkinter.Button(
    master=window,
    text="Add",
    font=( FONT_STYLE, FONT_SIZE_BODY ),
    width=44,
    command=validate_and_save_credentials
)


# LAYOUT:
# --------
canvas.grid( row=0, column=1 )
website_label.grid( row=1, column=0, pady=5 ),
website_entry.grid( row=1, column=1, columnspan=2, pady=5 )
username_label.grid( row=2, column=0, padx=10 )
username_entry.grid( row=2, column=1, columnspan=2, pady=5 )
password_label.grid( row=3, column=0 )
password_entry.grid( row=3, column=1, pady=5 )
password_generate_button.grid( row=3, column=2, pady=5 )
add_button.grid( row=4, column=1, columnspan=2, pady=10 )


# Setting focus on the Website Entry as soon as the program launches
website_entry.focus_set()

window.mainloop()