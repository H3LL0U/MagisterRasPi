import customtkinter as tk

# Define the SchoolFrame class
class EntryWithButton(tk.CTkFrame):
    def __init__(self, parent, submit_command, label_text, **kwargs):
        super().__init__(parent, **kwargs)  # Initialize the parent CTkFrame
        self.label_text = label_text
        self.submit_command = submit_command  # Store the command for the button

        # Create a StringVar to hold the typed school value
        self.str_var = tk.StringVar()

        # Create the label for "School"
        self.label = tk.CTkLabel(parent, text=label_text)
        

        # Create the entry field for the school name
        self.entry = tk.CTkEntry(self, textvariable=self.str_var)
        self.entry.grid(column=0, row=0)

        # Create the submit button with the provided command
        self.submit_button = tk.CTkButton(self, text="->", command=self.submit_command,width=50)
        self.submit_button.grid(column=1,row=0)
    def pack(self):
        
        self.label.pack(pady=5)
        super().pack()
