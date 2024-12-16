import customtkinter as ctk
from MagisterPy import MagisterSession
from tkinter import messagebox
class GradesWindow(ctk.CTkToplevel):
    def __init__(self, magister_session:MagisterSession ,*args, fg_color=None, **kwargs):
        super().__init__(*args, fg_color=fg_color, **kwargs)
        
        self.geometry("600x400")
        self.title("Grades")
        self.magister_session = magister_session
        # Initialize a scrollable frame for the grades table
        self.scroll_frame_main = ctk.CTkScrollableFrame(self, height=300)
        self.scroll_frame_main.pack(pady=10, fill="both", expand=True)
        
        self.scroll_frame = ctk.CTkFrame(self.scroll_frame_main)
        self.scroll_frame.pack(pady=10)

        # Create and display the table
        self.grades = self.get_grades_json()
        self.create_grades_table(grades=self.grades)

        self.after(2000,lambda: (self.focus_force()))

    def create_grades_table(self, grades, frame_height=50, padding=10):
        """Create and display the grades table based on provided data."""
        
        # Create headers
        

        # Create table rows
        for i, grade in enumerate(grades):
            col = i % 2  # Alternate between two columns
            row = i // 2

            # Create a styled frame for each grade
            grade_frame = self.create_grade_frame(grade, frame_height, padding)
            grade_frame.grid(row=row + 1, column=col, padx=10, pady=10, sticky="nesw")  # Row offset for headers

    
    def create_grade_frame(self, grade_data, frame_height, padding):
        """Create a styled frame for each grade."""
        frame = ctk.CTkFrame(self.scroll_frame, height=frame_height)
        
        subject_label = ctk.CTkLabel(frame, text=grade_data["subject"], font=("Arial", 15), anchor="w")
        subject_label.pack(padx=padding)

        grade_label = ctk.CTkLabel(frame, text=grade_data["grade"], font=("Arial", 15), anchor="w")
        grade_label.pack(padx=padding)

        return frame
    def get_grades_json(self):
        try:
            grades_json = self.magister_session.get_grades()
            
            grades_json = [{"subject": grade_data["vak"]["omschrijving"],"grade":grade_data["waarde"]} for grade_data in grades_json]
            
            return grades_json
        except Exception as e:
            
            messagebox.showerror("couldn't retrieve grades", "Could not retrieve grades from Magister")
            return {}