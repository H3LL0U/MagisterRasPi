import customtkinter as ctk
import datetime
import get_time
import lessongetter
import credentials
from tkinter import messagebox
from gradeswindow import GradesWindow
# Initialize CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class TimetableApp(ctk.CTk):
    def __init__(self,magister_session = None):
        super().__init__()
        self.lesson_getter = lessongetter.LessonGetter()
        
        self.session = magister_session
        self.title("Magister")
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self._geometry = f"{self.screen_width}x{self.screen_height}"
        self.geometry(self._geometry)
        self.lesson_frames = []
        self.scroll_frame = None
        self.fullscreen = False
        self.current_time = get_time.get_ntp_time()
        self.selected_time = self.current_time
        self.grades_window = None
        self.lessons = self.lesson_getter.extract_lessons_from_date(self.session,self.current_time)
        self.bind("<Escape>", self.toggle_fullscreen)
        self._logged_out = False
    
        full_screen_button_frame = ctk.CTkFrame(self)
        full_screen_button_frame.pack(fill="x", pady=10)

        #clock

        self.clock = ctk.CTkLabel(full_screen_button_frame,text = self.current_time[:-8],font=("Arial", 14))
        self.clock.pack(side = "right",padx = 30)

        # Dropdown Menu
        self.options = ["Fullscreen", "Logout", "Grades"]  # Dropdown options
        self.dropdown = ctk.CTkOptionMenu(
            full_screen_button_frame, 
            values=self.options,
            command=self.handle_dropdown_selection,
            
        )
        self.dropdown.pack(side="left", padx=20)
        self.dropdown.set("Options")
        self.create_top_bar()
        self.create_timetable(lessons=self.lessons)



        self.set_current_date()
    def handle_dropdown_selection(self, selected_option):
        """Handle the dropdown menu selection."""
        self.dropdown.set("Options")
        if selected_option == "Fullscreen":
            self.toggle_fullscreen()
        elif selected_option == "Logout":
            self.logout()
        elif selected_option == "Grades":
            self.get_grades()
    def logout(self):
        if messagebox.askyesno("Logout?","Are you sure you want to logout?"):

            credentials.clear_saved_credentials()
            self._logged_out = True
            self.destroy()
    def get_grades(self):
        """Open the Grades window if not already open."""
        if not hasattr(self, 'grades_window') or self.grades_window is None or not self.grades_window.winfo_exists():
            
            
            self.grades_window = GradesWindow(self.session)  
        else:
            
            
            self.grades_window.lift()
            self.grades_window.focus_force()
        

    def toggle_fullscreen(self,event=None):
            
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.wm_attributes("-fullscreen", True)
            self.state("zoomed")  # Set window to full screen
        else:
            self.wm_attributes("-fullscreen", False)
            self.state("zoomed")
            self.geometry(self._geometry)  # Restore to initial window size
    def create_top_bar(self):
        """Create the top bar with navigation buttons and the date label."""
        self.top_bar_frame = ctk.CTkFrame(self)
        self.top_bar_frame.pack(pady=10)

        # Left button
        self.left_button = ctk.CTkButton(self.top_bar_frame, text="<", command=self.left_button_action, width=20)
        self.left_button.grid(row=0, column=0, sticky="w", padx=(10, 10), pady=(10, 5))

        # Date label in the center
        today_date = self.selected_time
        self.date_label = ctk.CTkLabel(self.top_bar_frame, text=today_date, font=("Arial", 14))
        self.date_label.grid(row=0, column=1, pady=(10, 5))
        
        # Right button
        self.right_button = ctk.CTkButton(self.top_bar_frame, text=">", command=self.right_button_action, width=20)
        self.right_button.grid(row=0, column=2, sticky="e", padx=(10, 10), pady=(10, 5))

        # Column configuration for centering
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)  # Center column for date
        self.grid_columnconfigure(2, weight=1)
    def set_current_date(self):
        self.current_time = get_time.get_ntp_time()
        self.clock.configure(text=self.current_time[:-8])
        self.after(60000,self.set_current_date)

    def clear_timetable(self):
        for frame in self.lesson_frames:
            frame.grid_forget()
    def create_timetable(self, lessons, frame_height=80, padding=15):
        
        """Create and display the timetable based on lesson data."""
        self.clear_timetable()
        if not self.scroll_frame:
            self.scroll_frame_main = ctk.CTkScrollableFrame(self, height=self.screen_height*0.65)
            
            
            self.scroll_frame_main.pack(pady=10, fill="both")
            self.scroll_frame = ctk.CTkFrame(self.scroll_frame_main,)
            self.scroll_frame.pack()
        for i, lesson in enumerate(lessons):
            col = i%2
            # Create and configure a frame for each lesson
            lesson_frame = self.create_lesson_frame(lesson, frame_height, padding)
            self.lesson_frames.append(lesson_frame)
            lesson_frame.grid(pady=10,padx= 10, column = col, row = i//2,sticky = "nesw")  # Add margin between frames

    def create_lesson_frame(self, lesson, frame_height, padding):
        """Create a frame for a single lesson."""
        lesson_frame = ctk.CTkFrame(self.scroll_frame, height=frame_height, corner_radius=8, 
                                    border_width=2, border_color="gray",)  # Added border

        # Lesson name label
        lesson_label = ctk.CTkLabel(lesson_frame, text=lesson["lesson"], font=("Arial", 14, "bold"))
        lesson_label.pack(pady=(padding, 5))  # Add padding between name and other content

        # Time label
        time_label = ctk.CTkLabel(lesson_frame, text=lesson["time"], font=("Arial", 12))
        time_label.pack(pady=5)  # Padding between time and location

        # Location label
        location_label = ctk.CTkLabel(lesson_frame, text=lesson["location"], font=("Arial", 12))
        location_label.pack(pady=(5, padding))  # Padding between location and bottom border

        return lesson_frame


    def increment_selected_date(self,days:int):
        self.selected_time = get_time.add_day_to_date(self.selected_time,days=days)
        self.date_label.configure(text=self.selected_time)
        self.lessons = self.lesson_getter.extract_lessons_from_date(self.session,self.selected_time)
        self.create_timetable(self.lessons)

    def left_button_action(self):
        self.increment_selected_date(-1)
    def right_button_action(self):
        self.increment_selected_date(1)
    

'''# Sample data
lessons = [
    {"lesson": "Math", "location": "Room 101", "time": "9:00 - 10:00"},
    {"lesson": "History", "location": "Room 102", "time": "10:00 - 11:00"},
    {"lesson": "Science", "location": "Lab 201", "time": "11:00 - 12:00"},
    {"lesson": "English", "location": "Room 103", "time": "1:00 - 2:00"},
    {"lesson": "Art", "location": "Studio 104", "time": "2:00 - 3:00"},
    {"lesson": "Physical Ed", "location": "Gym", "time": "3:00 - 4:00"},
    # Add more lessons as needed to test scrolling
]
'''
'''lessons = []
# Run the application
app = TimetableApp(lessons)
app.mainloop()'''
