import tkinter as tk
from tkinter import messagebox, Toplevel, PhotoImage
import sqlite3


# --- Global Variable ---
logged_in_user = None  # To store the student ID of the logged-in user

# --- Database Initialization ---
def initialize_database():
    connection = sqlite3.connect("database.db")
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        student_id TEXT PRIMARY KEY,
                        password TEXT NOT NULL,
                        year_section TEXT,
                        goal TEXT,
                        total_grade REAL
                      )''')
    connection.commit()
    connection.close()

initialize_database()

# --- Functions ---
def show_frame(frame):
    frame.tkraise()
    if frame == profile_frame:
        load_profile()  # Load profile when navigating to profile frame

def on_login():
    global logged_in_user
    student_id = email_entry.get().strip()
    password = password_entry.get().strip()
    if check_credentials(student_id, password):
        logged_in_user = student_id
        messagebox.showinfo("Login", "Login successful!")
        # Check if the user has already completed setup
        if user_has_completed_setup(student_id):
            show_frame(profile_frame)  # Navigate to profile page
        else:
            show_frame(program_selection_frame)  # Continue setup
    else:
        messagebox.showerror("Login Failed", "Invalid Student ID or Password! Please try again or sign up.")

def user_has_completed_setup(student_id):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('SELECT year_section, goal FROM users WHERE student_id = ?', (student_id,))
        row = cursor.fetchone()
        connection.close()
        return row and row[0] and row[1]  # Ensure both year_section and goal are set
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False

def on_signup():
    student_id = email_entry.get().strip()
    password = password_entry.get().strip()
    if not student_id or not password:
        messagebox.showerror("Input Error", "Please fill in all fields to sign up.")
        return

    if register_user(student_id, password):
        messagebox.showinfo("Sign Up Successful", "You have successfully signed up! Please log in.")
    else:
        messagebox.showerror("Sign Up Failed", "Sign up failed. Please try again.")

def check_credentials(student_id, password):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE student_id = ? AND password = ?', (student_id, password))
        row = cursor.fetchone()
        connection.close()
        return row is not None
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False

def register_user(student_id, password):
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (student_id, password) VALUES (?, ?)', (student_id, password))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Sign Up Error", "Student ID already exists!")
        return False
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False
    
def register_user(student_id, password):
    """Register a new user."""
    import re
    if not re.fullmatch(r"\d{4}-\d{5}-PQ-0", student_id):
        messagebox.showerror("Invalid Student ID", "Student ID must be in the format YR-XXXXX-PQ-0, e.g., 2024-00274-PQ-0.")
        return False

    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('INSERT INTO users (student_id, password) VALUES (?, ?)', (student_id, password))
        connection.commit()
        connection.close()
        return True
    except sqlite3.IntegrityError:
        messagebox.showerror("Sign Up Error", "Student ID already exists!")
        return False
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return False

def load_profile():
    global logged_in_user
    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE student_id = ?', (logged_in_user,))
        user_data = cursor.fetchone()
        connection.close()
        if user_data:
            user_info_label.config(
                text=f"Student ID: {user_data[0]}\nYear & Section: {user_data[2]}\nGoal: {user_data[3]}\nTotal Grade: {user_data[4]}"
            )
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def edit_information():
    show_frame(program_selection_frame)  # Redirect to Program Selection for editing

def save_goal(goal):
    global logged_in_user
    if not logged_in_user:
        messagebox.showerror("Error", "No user is logged in!")
        return

    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET goal = ? WHERE student_id = ?', (goal, logged_in_user))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", f"Goal '{goal}' saved successfully!")
        show_frame(grade_input_frame)
    except Exception as e:
        messagebox.showerror("Database Error", f"Error: {e}")

def save_year_section(year_section):
    global logged_in_user
    if not logged_in_user:
        messagebox.showerror("Error", "No user is logged in!")
        return

    try:
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute('UPDATE users SET year_section = ? WHERE student_id = ?', (year_section, logged_in_user))
        connection.commit()
        connection.close()
        messagebox.showinfo("Success", f"Year and Section '{year_section}' saved successfully!")
        show_frame(goal_selection_frame)
    except Exception as e:
        messagebox.showerror("Database Errop0l", f"Error: {e}")

# The remaining code structure remains as-is, with SQLite used consistently throughout


def add_quiz_inputs():
    row = quiz_frame.grid_size()[1]  # Get the current number of rows in quiz_frame
    new_score_entry = tk.Entry(quiz_frame, font=("Times New Roman", 14))
    new_score_entry.grid(row=row, column=0, pady=5)
    quiz_score_entries.append(new_score_entry)
    
    new_total_entry = tk.Entry(quiz_frame, font=("Times New Roman", 14))
    new_total_entry.grid(row=row, column=1, pady=5)
    quiz_total_entries.append(new_total_entry)
    remove_button = tk.Button(quiz_frame, text="Remove", command=lambda: remove_quiz_input(new_score_entry, new_total_entry, remove_button))
    remove_button.grid(row=row, column=2, pady=5)

def add_project_inputs():
    row = project_frame.grid_size()[1]  # Get the current number of rows in project_frame
    new_score_entry = tk.Entry(project_frame, font=("Times New Roman", 14))
    new_score_entry.grid(row=row, column=0, pady=5)
    project_score_entries.append(new_score_entry)
    
    new_total_entry = tk.Entry(project_frame, font=("Times New Roman", 14))
    new_total_entry.grid(row=row, column=1, pady=5)
    project_total_entries.append(new_total_entry)
    remove_button = tk.Button(project_frame, text="Remove", command=lambda: remove_project_input(new_score_entry, new_total_entry, remove_button))
    remove_button.grid(row=row, column=2, pady=5)

def clear_inputs():
    # Clear all quiz input fields
    for entry in quiz_score_entries:
        entry.delete(0, tk.END)
    for entry in quiz_total_entries:
        entry.delete(0, tk.END)
    # Clear all project input fields
    for entry in project_score_entries:
        entry.delete(0, tk.END)
    for entry in project_total_entries:
        entry.delete(0, tk.END)
    # Clear attendance and midterm fields
    attendance_score_entry.delete(0, tk.END)
    attendance_total_entry.delete(0, tk.END)
    midterm_score_entry.delete(0, tk.END)
    midterm_total_entry.delete(0, tk.END)
    
def remove_quiz_input(score_entry, total_entry, remove_button):
    score_entry.destroy()
    total_entry.destroy()
    remove_button.destroy()
    quiz_score_entries.remove(score_entry)
    quiz_total_entries.remove(total_entry)
def remove_project_input(score_entry, total_entry, remove_button):
    score_entry.destroy()
    total_entry.destroy()
    remove_button.destroy()
    project_score_entries.remove(score_entry)
    project_total_entries.remove(total_entry)

def show_new_ui():
    new_ui_frame = tk.Toplevel(root)
    new_ui_frame.title("PUPTrack | Sinta Grading System")
    new_ui_frame.geometry("1024x576")
    new_ui_frame.configure(bg="#800000")

    # Quote Section
    quote_label = tk.Label(new_ui_frame, text="You are not denied, only redirected.", font=("Times New Roman", 36, "bold"), fg="#FFD700", bg="#800000")
    quote_label.pack(pady=(20, 0))
    
    # Thank You Message
    thank_you_label = tk.Label(
        new_ui_frame,
        text="Thank you for using PUPTrack, Sinta Grading System Application. Your trust inspires us to continue providing efficient and reliable solutions for your needs.",
        font=("Times New Roman", 14),
        fg="white",
        bg="#800000",
        wraplength=900,
        justify="center"
    )
    thank_you_label.pack(pady=(20, 40))
    
    # Buttons
    button_frame = tk.Frame(new_ui_frame, bg="#800000")
    button_frame.pack()

    calculate_again_button = tk.Button(
        button_frame,
        text="Calculate Again",
        font=("Times New Roman", 14, "bold"),
        bg="#FFD700",
        fg="#800000",
        width=15,
        command=lambda: [clear_inputs(), new_ui_frame.destroy(), show_frame(grade_input_frame)]
    )
    calculate_again_button.grid(row=0, column=0, padx=10, pady=10)

    about_button = tk.Button(
        button_frame,
        text="About",
        font=("Times New Roman", 14, "bold"),
        bg="#FFD700",
        fg="#800000",
        width=15,
        command=lambda: messagebox.showinfo("About", """Prepared by <THE PYTHONISTAS>
Team Leader: MILAN, Aedhriane Curt G.
Project Manager: DAEL, Izienne Kyle B.
Developers: ONG, Marriel Maribao & ABO, John Mark V.
Quality Assurance: JOSE, John Andrei & ROSALES, Orlando Rada Jr.""")
    )
    about_button.grid(row=0, column=1, padx=10, pady=10)
    exit_button = tk.Button(
        button_frame,
        text="Exit",
        font=("Times New Roman", 14, "bold"),
        bg="#FFD700",
        fg="#800000",
        width=15,
        command=root.quit
    )
    exit_button.grid(row=0, column=2, padx=10, pady=10)

    # Terms and Policy Label
    terms_label = tk.Label(
        new_ui_frame,
        text="By using this application, you agree to our Terms of Service and Privacy Policy, which govern the collection and use of your data to provide accurate grade assessments.",
        font=("Times New Roman", 10),
        bg="#800000",
        fg="white",
        wraplength=600,
        justify="center"
    )
    terms_label.pack(side=tk.BOTTOM, pady=10)

def show_final_grade(final_grade, status):
    final_window = Toplevel()
    final_window.title("Final Grade")
    final_window.geometry("600x400")
    final_window.configure(bg="#8B0000")

    final_grade_label = tk.Label(final_window, text=f"You have an Exam Grade of: {final_grade:.2f}", 
                                 font=("Times New Roman", 20, "bold"), bg="#8B0000", fg="yellow")
    final_grade_label.pack(pady=20)

    status_label = tk.Label(final_window, text=f"Status: {status}", 
                            font=("Times New Roman", 20, "bold"), bg="#8B0000", fg="yellow")
    status_label.pack(pady=20)

    if final_grade >= 95:
        quote = "So proud of you! keep it up! <3"
    elif final_grade >= 90:
        quote = "Congratulations! Deserve mo mag McDo, woooho!"
    elif final_grade >= 85:
        quote = "You did your best, but I know there's more about you. so, fighting!"
    elif final_grade >= 75:
        quote = "Aral pa at hindi pa huli! Go, go, fight, fight, win, win!"
    else:
        quote = "Huwag susuko, may pag-asa pa!"

    quote_label = tk.Label(final_window, text=f"{quote}", 
                           font=("Times New Roman", 18, "italic"), bg="#8B0000", fg="yellow")
    quote_label.pack(pady=30)

    okay_button = tk.Button(final_window, text="Okay", command=lambda: [final_window.destroy(), show_new_ui()], 
                            font=("Times New Roman", 15), bg="#8B0000", fg="yellow")
    okay_button.pack(pady=20)
    

def calculate_grade():
    try:
        # Calculate Quiz Score
        quiz_scores = [float(entry.get()) for entry in quiz_score_entries]
        quiz_totals = [float(entry.get()) for entry in quiz_total_entries]
        quiz_percentage = sum(quiz_scores) / sum(quiz_totals) * 35 if sum(quiz_totals) > 0 else 0

        # Calculate Project Score
        project_scores = [float(entry.get()) for entry in project_score_entries]
        project_totals = [float(entry.get()) for entry in project_total_entries]
        project_percentage = sum(project_scores) / sum(project_totals) * 25 if sum(project_totals) > 0 else 0

        # Calculate Attendance Score
        attendance_score = float(attendance_score_entry.get())
        attendance_total = float(attendance_total_entry.get())
        attendance_percentage = (attendance_score / attendance_total * 10) if attendance_total > 0 else 0

        # Calculate Midterm Score
        midterm_score = float(midterm_score_entry.get())
        midterm_total = float(midterm_total_entry.get())
        midterm_percentage = midterm_score / midterm_total * 30 if midterm_total > 0 else 0

        # Total Final Grade
        final_grade = quiz_percentage + project_percentage + attendance_percentage + midterm_percentage

        # Determine Pass or Fail
        status = "Passed" if final_grade >= 75 else "Failed"
        result_label.config(text=f"Final Grade: {final_grade:.2f}\nStatus: {status}")

        # Show the final grade window
        show_final_grade(final_grade, status)
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for all inputs.")
# --- Main Application ---
root = tk.Tk()
root.title("PUPTRACK | Sinta Grading System")
root.geometry("1024x576")
root.configure(bg="")

# --- Frames and UI Elements ---
login_frame = tk.Frame(root, bg="#800000")
program_selection_frame = tk.Frame(root, bg="#800000")
year_section_selection_frame = tk.Frame(root, bg="#800000")
goal_selection_frame = tk.Frame(root, bg="#800000")
grade_input_frame = tk.Frame(root, bg="#800000")
profile_frame = tk.Frame(root, bg="#800000")

for frame in (login_frame, program_selection_frame, year_section_selection_frame, goal_selection_frame, grade_input_frame, profile_frame):
    frame.place(relwidth=1, relheight=1)

# --- Login Frame ---
login_frame = tk.Frame(root)
login_frame.place(relwidth=1, relheight=1)

# Add a background image to the login frame
bg_image_path = "C:\\Users\\Administrator\\Documents\\PUPproject\\Picture\\PUPTRACKlogin.png"
bg_image = PhotoImage(file=bg_image_path)
bg_label = tk.Label(login_frame, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

title = tk.Label(
    login_frame,
    text="PUPTRACK",
    font=("Times New Roman", 48, "bold"),
    fg="#FFD700",  # Gold text color for visibility
    bg="#800000",  # Use a matching or blended background color
)
title.pack(pady=(200, 0))  # Adjust padding to move down for the logo

subtitle = tk.Label(
    login_frame,
    text="Sinta Grading System",
    font=("Times New Roman", 24),
    fg="#FFD700",
    bg="#800000",  # Matching background color
)
subtitle.pack(pady=(10, 40))

email_label = tk.Label(
    login_frame,
    text="Student ID",
    font=("Times New Roman", 14),
    fg="white",
    bg="#800000",  # Matching background color
)
email_label.pack(pady=(10, 0))

email_entry = tk.Entry(login_frame, font=("Times New Roman", 14), width=30)
email_entry.pack(pady=10)

password_label = tk.Label(
    login_frame,
    text="Password",
    font=("Times New Roman", 14),
    fg="white",
    bg="#800000",  # Matching background color
)
password_label.pack(pady=(10, 0))

password_entry = tk.Entry(login_frame, font=("Times New Roman", 14), width=30, show="*")
password_entry.pack(pady=10)

login_button = tk.Button(
    login_frame,
    text="Login",
    font=("Times New Roman", 14, "bold"),
    bg="#800000",
    fg="#FFD700",
    width=10,
    command=on_login,
)
login_button.pack(pady=20)

signup_button = tk.Button(
    login_frame,
    text="Sign Up",
    font=("Times New Roman", 14, "bold"),
    bg="#800000",
    fg="#FFD700",
    width=10,
    command=on_signup,
)
signup_button.pack()

# --- Program Selection Frame ---
program_title = tk.Label(program_selection_frame, text="Choose your Program:", font=("Times New Roman", 36, "bold"), fg="#FFD700", bg="#800000")
program_title.pack(pady=(20, 40))

programs = [
    "BS Information Technology",
    "BS Computer Engineer",
    "BS Hospitality Management",
    "BS Office Administration"
]

for program in programs:
    program_button = tk.Button(
        program_selection_frame,
        text=program,
        font=("Times New Roman", 18),
        bg="white",
        fg="black",
        width=30,
        command=lambda p=program: save_year_section(p)  # Updated function to save year and section
    )
    program_button.pack(pady=10)

# --- Year and Section Selection Frame ---
year_section_title = tk.Label(year_section_selection_frame, text="Choose your Year and Section:", font=("Times New Roman", 36, "bold"), fg="#FFD700", bg="#800000")
year_section_title.pack(pady=(20, 40))

year_sections = [
    "1-1", "1-2", "1-3",
    "2-1", "2-2",
    "3-1", "3-2",
    "4-1", "4-2"
]

for year_section in year_sections:
    year_section_button = tk.Button(
        year_section_selection_frame,
        text=year_section,
        font=("Times New Roman", 18),
        bg="white",
        fg="black",
        width=30,
        command=lambda ys=year_section: save_year_section(ys)
    )
    year_section_button.pack(pady=10)

# --- Goal Selection Frame ---
goal_title = tk.Label(goal_selection_frame, text="What is your Specific Goal Grade/Mark this Midterm?", font=("Times New Roman", 25, "bold"), fg="#FFD700", bg="#800000")
goal_title.pack(pady=(20, 40))

goals = ["1.0", "1.25", "1.5", "1.75", "2.0"]

for goal in goals:
    goal_button = tk.Button(
        goal_selection_frame,
        text=goal,
        font=("Times New Roman", 18),
        bg="white",
        fg="black",
        width=30,
        command=lambda g=goal: save_goal(g)
    )
    goal_button.pack(pady=10)

# --- Grade Input Frame ---
grade_title = tk.Label(grade_input_frame, text="Input your Scores!", font=("Times New Roman", 36, "bold"), fg="#FFD700", bg="#800000")
grade_title.pack(pady=(20, 20))

# Scrollable frame for quizzes and projects
scroll_canvas = tk.Canvas(grade_input_frame, bg="#800000")
scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(grade_input_frame, orient="vertical", command=scroll_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scroll_canvas.configure(yscrollcommand=scrollbar.set)
scroll_canvas.bind('<Configure>', lambda e: scroll_canvas.configure(scrollregion=scroll_canvas.bbox('all')))

scroll_frame = tk.Frame(scroll_canvas, bg="#800000")
scroll_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

# Quizzes
quiz_frame = tk.Frame(scroll_frame, bg="#800000")
quiz_frame.pack(pady=(10, 10), anchor='w')
tk.Label(quiz_frame, text="Quiz Score (35%)", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Label(quiz_frame, text="Quiz Total", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=1, padx=5, pady=5, sticky='w')
quiz_score_entries = [tk.Entry(quiz_frame, font=("Times New Roman", 14))]
quiz_score_entries[0].grid(row=1, column=0, padx=5, pady=5, sticky='w')
quiz_total_entries = [tk.Entry(quiz_frame, font=("Times New Roman", 14))]
quiz_total_entries[0].grid(row=1, column=1, padx=5, pady=5, sticky='w')
tk.Button(scroll_frame, text="Add Quiz", font=("Times New Roman", 12), command=add_quiz_inputs).pack()

# Projects
project_frame = tk.Frame(scroll_frame, bg="#800000")
project_frame.pack(pady=(10, 10), anchor='w')
tk.Label(project_frame, text="Project Score (25%)", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Label(project_frame, text="Project Total", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=1, padx=5, pady=5, sticky='w')
project_score_entries = [tk.Entry(project_frame, font=("Times New Roman", 14))]
project_score_entries[0].grid(row=1, column=0, padx=5, pady=5, sticky='w')
project_total_entries = [tk.Entry(project_frame, font=("Times New Roman", 14))]
project_total_entries[0].grid(row=1, column=1, padx=5, pady=5, sticky='w')
tk.Button(scroll_frame, text="Add Project", font=("Times New Roman", 12), command=add_project_inputs).pack()

# Attendance and Midterm
attendance_frame = tk.Frame(grade_input_frame, bg="#800000")
attendance_frame.pack(pady=(10, 10), anchor='w')
tk.Label(attendance_frame, text="Attendance (10%)", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Label(attendance_frame, text="Attendance Total", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=1, padx=5, pady=5, sticky='w')
attendance_score_entry = tk.Entry(attendance_frame, font=("Times New Roman", 14))
attendance_score_entry.grid(row=1, column=0, padx=5, pady=5, sticky='w')
attendance_total_entry = tk.Entry(attendance_frame, font=("Times New Roman", 14))
attendance_total_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')

midterm_frame = tk.Frame(grade_input_frame, bg="#800000")
midterm_frame.pack(pady=(10, 10), anchor='w')
tk.Label(midterm_frame, text="Midterm Exam Score (30%)", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=0, padx=5, pady=5, sticky='w')
tk.Label(midterm_frame, text="Midterm Total", font=("Times New Roman", 12), fg="white", bg="#800000").grid(row=0, column=1, padx=5, pady=5, sticky='w')
midterm_score_entry = tk.Entry(midterm_frame, font=("Times New Roman", 14))
midterm_score_entry.grid(row=1, column=0, padx=5, pady=5, sticky='w')
midterm_total_entry = tk.Entry(midterm_frame, font=("Times New Roman", 14))
midterm_total_entry.grid(row=1, column=1, padx=5, pady=5, sticky='w')
# Calculate Button
calculate_button = tk.Button(grade_input_frame, text="Calculate Grade", font=("Times New Roman", 14, "bold"), bg="#FFD700", fg="#800000", command=calculate_grade)
calculate_button.pack(pady=20)

# Result Label
result_label = tk.Label(grade_input_frame, text="", font=("Times New Roman", 16), fg="white", bg="#800000")
result_label.pack()

# --- Profile Frame ---
profile_title = tk.Label(profile_frame, text="Welcome to Your Profile", font=("Times New Roman", 36, "bold"), fg="#FFD700", bg="#800000")
profile_title.pack(pady=(20, 40))

user_info_label = tk.Label(profile_frame, text="", font=("Times New Roman", 18), fg="white", bg="#800000")
user_info_label.pack(pady=10)

edit_button = tk.Button(profile_frame, text="Edit Information", font=("Times New Roman", 14), bg="#FFD700", fg="#800000", command=edit_information)
edit_button.pack(pady=10)

calculate_grade_button = tk.Button(profile_frame, text="Calculate Grade", font=("Times New Roman", 14), bg="#FFD700", fg="#800000", command=lambda: show_frame(grade_input_frame))
calculate_grade_button.pack(pady=10)

exit_button = tk.Button(profile_frame, text="Exit", font=("Times New Roman", 14), bg="#FFD700", fg="#800000", command=root.quit)
exit_button.pack(pady=10)

# Show the initial frame
show_frame(login_frame)

# Start the application
root.mainloop()
