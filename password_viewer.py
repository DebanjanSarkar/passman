import os
import csv
import tkinter
import pyperclip

# ---------------------------- CONSTANTS --------------------------------------- #
BLACK = "#000000"
GREEN = "#408140"

FONT_STYLE = "calibri"
FONT_SIZE_BODY = 12

# This should be the path to the datafile(where data is to be saved), relative to this main Python file.
DATA_FILE_RELATIVE_PATH = "creds/saved_credentials.csv"


# ---------------------------- LOAD SAVED CREDENTIALS ------------------------------- #
# Here, we load all the saved credentials from the data file, to appropriate Python data structures
try:
    with open( os.path.join( os.path.dirname(__file__), DATA_FILE_RELATIVE_PATH ) ) as data_file:
        creds_data = csv.reader( data_file )
        # websites_list will be a Python list, that will contain all the websites in ascending order.
        websites_list = []

        # credentials_dict will contain user's credentials as a Python dictionary, with following structure:
        # {
        #     website1: { "username": username1, "password": password1 },
        #     website2: { "username": username2, "password": password2 },...
        # }
        credentials_dict = dict()
        
        for row in creds_data:
            if len(row) == 3:
                # Each row must contain 3 values, else the row will be assumed to be corrupted, thus not added to search datastruture
                websites_list.append( row[0] )
                credentials_dict[ row[0] ] = {
                    "username": row[1],
                    "password": row[2]
                }

        # Sorting the websites in ascending order
        websites_list.sort()

except FileNotFoundError:
    # If user launches password viewer before storing any credentials
    print("No credentials found! Store your credentials first...")
    websites_list=["-- no credentials --"]
    credentials_dict={None: None}


# ---------------------------- SEARCH BUTTON FNCTIONALITY ------------------------- #
def website_creds_search():
    selected_website = selected_website_var.get()

    if selected_website != "-- SELECT --" and selected_website != "-- no credentials --":
        # When any website is selected from dropdown and then Search is clicked, this code block will run
        username = credentials_dict[selected_website]["username"]
        password = credentials_dict[selected_website]["password"]
        
        website_result_label.config( text=selected_website )
        username_result_label.config( text=username )
        password_result_label.config( text=password )

        website_copy_button.config( state="normal" )
        username_copy_button.config( state="normal" )
        password_copy_button.config( state="normal" )


# ---------------------------- COPY BUTTON FNCTIONALITY ------------------------- #
def reset_copied_to_clipboard_msg():
    copied_to_clipboard_msg_label.config( text="  " )

def copy_website():
    # .cget() method takes the name of configuration/property name as parameter.
    # .cget() returns the property value of that particular tkinter widget
    website = website_result_label.cget("text")
    pyperclip.copy( website )

    # After copying to clipboard, this message will be displayed, and cleared after 1 sec
    copied_to_clipboard_msg_label.config( text="Website copied to clipboard!" )
    window.after( 1000, reset_copied_to_clipboard_msg )

def copy_username():
    username = username_result_label.cget("text")
    pyperclip.copy( username )

    # After copying to clipboard, this message will be displayed, and cleared after 1 sec
    copied_to_clipboard_msg_label.config( text="Username/Email copied to clipboard!" )
    window.after( 1000, reset_copied_to_clipboard_msg )

def copy_password():
    password = password_result_label.cget("text")
    pyperclip.copy( password )

    # After copying to clipboard, this message will be displayed, and cleared after 1.5 sec
    copied_to_clipboard_msg_label.config( text="Password copied to clipboard!" )
    window.after( 1500, reset_copied_to_clipboard_msg )



# ---------------------------- UI SETUP ---------------------------------------- #

window = tkinter.Tk()
window.minsize( width=610, height=490 )
window.title("PASSMAN - Password Viewer - made by Debanjan Sarkar")
window.config( padx=50, pady=50 )

# Components:
# -------------------------------------------
# -------------------------------------------

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

website_search_label = tkinter.Label(
    master=window,
    text="Select Website: ",
    font=( FONT_STYLE, FONT_SIZE_BODY )
)

  
# datatype of menu text 
selected_website_var = tkinter.StringVar() 
# initial menu text 
selected_website_var.set( "-- SELECT --" ) 
  
# Create Dropdown menu 
# As the last parameter, we unpack the values of a List, to pass it to 
# VARIABLE LENGTH POSITIONAL ARGUMENT of the "OptionMenu" __init__() method.
website_select_dropdown = tkinter.OptionMenu( window , selected_website_var , *websites_list )
website_select_dropdown.config( width=40, pady=4 )

search_button = tkinter.Button(
    master=window,
    text="Search",
    width=20,
    pady=4,
    command=website_creds_search
)

website_title_label = tkinter.Label(
    master=window,
    text="Website: ",
    font=(FONT_STYLE,FONT_SIZE_BODY)
)
website_result_label = tkinter.Label(
    master=window,
    text=" ----- ",
    width=40,
    font=(FONT_STYLE,FONT_SIZE_BODY, "bold")
)
website_copy_button = tkinter.Button(
    master=window,
    text="Copy",
    state="disabled",
    width=20,
    pady=2,
    command=copy_website
)

username_title_label = tkinter.Label(
    master=window,
    text="Username/Email: ",
    font=(FONT_STYLE,FONT_SIZE_BODY)
)
username_result_label = tkinter.Label(
    master=window,
    text=" ----- ",
    width=40,
    font=(FONT_STYLE,FONT_SIZE_BODY, "bold")
)
username_copy_button = tkinter.Button(
    master=window,
    text="Copy",
    state="disabled",
    width=20,
    pady=2,
    command=copy_username
)

password_title_label = tkinter.Label(
    master=window,
    text="Password: ",
    font=(FONT_STYLE,FONT_SIZE_BODY)
)
password_result_label = tkinter.Label(
    master=window,
    text=" ----- ",
    width=40,
    font=(FONT_STYLE,FONT_SIZE_BODY, "bold")
)
password_copy_button = tkinter.Button(
    master=window,
    text="Copy",
    state="disabled",
    width=20,
    pady=2,
    command=copy_password
)


copied_to_clipboard_msg_label = tkinter.Label(
    master=window,
    text="  ",
    font=(FONT_STYLE,FONT_SIZE_BODY),
    foreground=GREEN,
    width=30
)

# LAYOUT:
# -------------------------------------------
# -------------------------------------------

canvas.grid( row=0, column=1 )

website_search_label.grid( row=1, column=0, pady=15 ),
website_select_dropdown.grid( row=1, column=1, pady=15 )
search_button.grid( row=1, column=2, pady=15 )

website_title_label.grid( row=3, column=0, pady=5 )
website_result_label.grid( row=3, column=1, pady=5 )
website_copy_button.grid( row=3, column=2, pady=5 )

username_title_label.grid( row=4, column=0, pady=5 )
username_result_label.grid( row=4, column=1, pady=5 )
username_copy_button.grid( row=4, column=2, pady=5 )

password_title_label.grid( row=5, column=0, pady=5 )
password_result_label.grid( row=5, column=1, pady=5 )
password_copy_button.grid( row=5, column=2, pady=5 )

copied_to_clipboard_msg_label.grid( row=6, column=0, columnspan=3, pady=7 )

window.mainloop()