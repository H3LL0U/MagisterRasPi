#import tkinter as tk
from tkinter import messagebox
#from MagisterPy import MagisterSession
import customtkinter as tk
from entry_widgets import *
# Predefined user credentials and school
from MagisterPy import *


class LoginPage():
    def __init__(self):
        self.SCHOOL_NAME =None
        self.USERNAME = None
        
        self.PASSWORD = None
        
        session = MagisterSession()
        # Function to toggle full-screen mode
        self.session = session
                
        root = tk.CTk()
        root.title("Login Page")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        geometry = f"{screen_width}x{screen_height}"
        root.geometry(geometry)

        # Variable to track full-screen state
        fullscreen = False

        def toggle_fullscreen(event=None):
            nonlocal fullscreen
            fullscreen = not fullscreen
            if fullscreen:
                root.wm_attributes("-fullscreen", True)
                root.state("zoomed")  # Set window to full screen
            else:
                root.wm_attributes("-fullscreen", False)
                root.state("zoomed")
                root.geometry(geometry)  # Restore to initial window size
        root.bind("<Escape>", toggle_fullscreen)

        # Fullscreen toggle button in the top right corner
        full_screen_button_frame = tk.CTkFrame(root)
        full_screen_button_frame.pack(fill="x")
        fullscreen_button = tk.CTkButton(full_screen_button_frame, text="full", command=toggle_fullscreen)
        fullscreen_button.pack(side="left")


        def submit_school():
            try:
                school_submit.submit_button.configure(state = "disabled")
                school_submit.entry.configure(state = "disabled")
                typed_school = school_submit.str_var.get()
                response = session.input_school(typed_school)
                
                if response and response.status_code == 200:
                    
                    display_name = response.json()["tenantname"]
                    school_submit.str_var.set(display_name)
                    school_submit.submit_button.grid_forget()
                    self.SCHOOL_NAME = typed_school
                    username_submit.pack()
                else:
                    school_submit.submit_button.configure(state = "enabled")
                    school_submit.entry.configure(state = "normal")
                    messagebox.showerror("No school found",f"No school {typed_school} found")
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except Exception as e:
                school_submit.submit_button.configure(state = "enabled")
                school_submit.entry.configure(state = "normal")
                raise e

        school_submit = EntryWithButton(root,submit_command=submit_school,label_text="School")
        school_submit.pack()

        # Username label and entry
        def submit_username():
            try:
                username_submit.submit_button.configure(state = "disabled")
                username_submit.entry.configure(state = "disabled")
                typed_username = username_submit.str_var.get()
                response = session.input_username(typed_username)
                
                if response and response.status_code == 200:
                    
                    
                    username_submit.str_var.set(typed_username)
                    username_submit.submit_button.grid_forget()
                    self.USERNAME = typed_username
                    password_submit.pack()
                else:
                    username_submit.submit_button.configure(state = "enabled")
                    username_submit.entry.configure(state = "normal")
                    messagebox.showerror("No username found",f"No username {typed_username} found")
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except Exception as e:
                
                school_submit.submit_button.configure(state = "enabled")
                school_submit.entry.configure(state = "normal")
                raise(e)

        username_submit = EntryWithButton(root,submit_command=submit_username,label_text="Username")

        def submit_password():
            try:
                password_submit.submit_button.configure(state = "disabled")
                password_submit.entry.configure(state = "disabled")
                typed_password = password_submit.str_var.get()
                response = session.input_password(typed_password)
                
                if response and response.status_code == 200:
                    
                    
                    password_submit.str_var.set(typed_password)
                    password_submit.submit_button.grid_forget()
                    self.PASSWORD = typed_password
                    password_submit.pack()
                    messagebox.showinfo("Logged in","Login succesful")
                    root.destroy()


                else:
                    password_submit.submit_button.configure(state = "enabled")
                    password_submit.entry.configure(state = "normal")
                    messagebox.showerror("Password isn't right",f"The password is not right or user on cooldown")
            except KeyboardInterrupt:
                raise KeyboardInterrupt()
            except Exception as e:
                
                school_submit.submit_button.configure(state = "enabled")
                school_submit.entry.configure(state = "normal")
                raise(e)



        password_submit = EntryWithButton(root,submit_command=submit_password,label_text="Password")


        root.mainloop()
