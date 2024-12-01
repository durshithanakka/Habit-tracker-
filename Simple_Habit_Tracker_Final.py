import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from customtkinter import CTk, CTkEntry, CTkButton, CTkLabel
from tkinter import Checkbutton

# Global Variables
habits = []
target_days = 0
current_day_index = 0
habit_data = {}
start_date = datetime.today()

class HabitTrackerApp(CTk):
    def __init__(self):
        super().__init__()
        self.title("Simple Habit Tracker")
        self.geometry("600x700")  # Increased window size for a more spacious layout
        self.configure(bg="#F7F7F7")  # Soft neutral background color
        self.create_main_page()

    # Main page to input habits and target days
    def create_main_page(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Title with modern font and increased size
        title_label = CTkLabel(self, text="Set Your Habits and Target Days", font=("Helvetica", 20, "bold"), text_color="#3F3F3F")
        title_label.pack(pady=20)

        # Habit input
        self.habit_entry = CTkEntry(self, placeholder_text="Enter a habit", font=("Arial", 14), width=300)
        self.habit_entry.pack(pady=10)

        self.habits_listbox = tk.Listbox(self, height=5, font=("Arial", 12))
        self.habits_listbox.pack(pady=10)

        # Add habit button with new color
        add_habit_btn = CTkButton(self, text="Add Habit", command=self.add_habit, width=200, height=40, fg_color="#4CAF50", hover_color="#45a049")
        add_habit_btn.pack(pady=10)

        # Target days entry
        self.target_days_entry = CTkEntry(self, placeholder_text="Enter target days", font=("Arial", 14), width=300)
        self.target_days_entry.pack(pady=10)

        # Confirm, Reset Habits, and Reset Target buttons with updated styles
        confirm_button = CTkButton(self, text="Confirm Habits & Target", command=self.confirm_habits_and_target, width=200, height=40, fg_color="#008CBA", hover_color="#007BB5")
        confirm_button.pack(pady=10)

        reset_habits_button = CTkButton(self, text="Reset Habits", command=self.reset_habits, width=200, height=40, fg_color="#FF5733", hover_color="#e74c3c")
        reset_habits_button.pack(pady=10)

        reset_target_button = CTkButton(self, text="Reset Target", command=self.reset_target, width=200, height=40, fg_color="#FF5733", hover_color="#e74c3c")
        reset_target_button.pack(pady=10)

    # Add a habit to the list
    def add_habit(self):
        habit = self.habit_entry.get()
        if habit:
            habits.append(habit)
            self.habits_listbox.insert(tk.END, habit)
            self.habit_entry.delete(0, tk.END)
    
    # Confirm habits and target days
    def confirm_habits_and_target(self):
        global target_days, start_date
        try:
            target_days = int(self.target_days_entry.get())
            start_date = datetime.today().date()  # Ensuring only the date part is used
            if not habits or target_days <= 0:
                raise ValueError("Please add habits and enter a valid target day.")
            self.create_tracking_page()
        except ValueError:
            messagebox.showerror("Error", "Please add habits and enter a valid target day.")

    # Reset habits list
    def reset_habits(self):
        global habits
        habits = []
        self.habits_listbox.delete(0, tk.END)

    # Reset target days
    def reset_target(self):
        self.target_days_entry.delete(0, tk.END)

    # Create the tracking page for daily habit tracking
    def create_tracking_page(self):
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Top-right Reset button with improved color
        reset_button = CTkButton(self, text="Reset Habits and Target", command=self.reset_all, width=20, height=40, fg_color="#FF5733", hover_color="#e74c3c")
        reset_button.pack(pady=10, anchor="ne", padx=10)

        # Current date label with increased font size
        date_label = CTkLabel(self, text=f"Date: {start_date + timedelta(days=current_day_index):%Y-%m-%d}", font=("Arial", 18, "bold"), text_color="#3F3F3F")
        date_label.pack(pady=10)

        # Habit checkboxes with modern style and larger font
        self.habit_vars = {}
        for habit in habits:
            var = tk.BooleanVar()
            checkbox = Checkbutton(self, text=habit, variable=var, font=("Arial", 14))
            checkbox.pack(pady=8)
            self.habit_vars[habit] = var

        # Submit button with new color and larger size
        submit_button = CTkButton(self, text="Submit", command=self.submit_day_progress, width=200, height=40, fg_color="#4CAF50", hover_color="#45a049")
        submit_button.pack(pady=10)

        # Analyze button with updated look
        analyze_button = CTkButton(self, text="Analyze Performance", command=self.create_analysis_page, width=200, height=40, fg_color="#FF9800", hover_color="#e68900")
        analyze_button.pack(pady=10)

    # Submit daily progress and update date
    def submit_day_progress(self):
        global current_day_index
        day_data = {habit: var.get() for habit, var in self.habit_vars.items()}
        habit_data[current_day_index] = day_data
        current_day_index += 1
        
        if current_day_index >= target_days:
            self.show_completion_graph()
        else:
            self.create_tracking_page()

    # Show completion message and visualize graph when target days are reached
    def show_completion_graph(self):
        # Calculate habit completion counts
        habit_counts = {habit: 0 for habit in habits}
        for day, data in habit_data.items():
            for habit, completed in data.items():
                if completed:
                    habit_counts[habit] += 1

        # Display completion message
        messagebox.showinfo("Target Complete", "Congratulations! You have successfully completed your target days.")

        # Show graph of habit completion
        plt.figure(figsize=(8, 4))
        plt.bar(habit_counts.keys(), habit_counts.values())
        plt.title("Habit Completion Over Target Period")
        plt.xlabel("Habits")
        plt.ylabel("Days Completed")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Display plot in the window
        for widget in self.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=5)

        # Add confirm button to reset all
        confirm_button = CTkButton(self, text="Confirm", command=self.reset_all, width=200, height=40, fg_color="#008CBA", hover_color="#007BB5")
        confirm_button.pack(pady=10)

    # Create the analysis page with a scrollable area for graphs
    def create_analysis_page(self):
        # Clear existing widgets
        for widget in self.winfo_children():
            widget.destroy()

        # Back button to go back to tracking page
        back_button = CTkButton(self, text="Back to Tracking", command=self.create_tracking_page, width=200, height=40, fg_color="#4CAF50", hover_color="#45a049")
        back_button.pack(pady=10)

        # Number of days entry with modern style
        days_label = CTkLabel(self, text="Enter number of days to analyze:", font=("Arial", 14))
        days_label.pack(pady=10)

        self.days_entry = CTkEntry(self, font=("Arial", 14), width=300)
        self.days_entry.pack(pady=10)

        analyze_button = CTkButton(self, text="Analyze", command=self.perform_analysis, width=200, height=40, fg_color="#FF9800", hover_color="#e68900")
        analyze_button.pack(pady=10)

        # Verify a specific date
        verify_label = CTkLabel(self, text="Verify a day (YYYY-MM-DD):", font=("Arial", 14))
        verify_label.pack(pady=10)

        self.date_entry = CTkEntry(self, font=("Arial", 14), width=300)
        self.date_entry.pack(pady=10)

        verify_button = CTkButton(self, text="Verify", command=self.verify_date, width=200, height=40, fg_color="#008CBA", hover_color="#007BB5")
        verify_button.pack(pady=10)

        # Scrollable Frame for Graphs
        self.canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(pady=10, expand=True, fill=tk.BOTH)
        self.scrollbar.pack(side="right", fill="y")

    # Perform analysis on the habit data
    def perform_analysis(self):
        days_to_analyze = int(self.days_entry.get())
        if days_to_analyze <= 0 or days_to_analyze > current_day_index:
            messagebox.showerror("Error", "Enter a valid number of days to analyze.")
            return

        # Count habit completion over specified days
        habit_counts = {habit: 0 for habit in habits}
        for day in range(days_to_analyze):
            for habit, completed in habit_data.get(day, {}).items():
                if completed:
                    habit_counts[habit] += 1

        # Display multiple graphs
        plt.figure(figsize=(8, 4))
        plt.bar(habit_counts.keys(), habit_counts.values())
        plt.title(f"Habit Completion Over Last {days_to_analyze} Days")
        plt.xlabel("Habits")
        plt.ylabel("Days Completed")
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Show plot in the scrollable frame
        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.scrollable_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    # Verify if habits were done on a specific date
    def verify_date(self):
        date_str = self.date_entry.get()
        try:
            # Parse entered_date as date only
            entered_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            
            # Calculate the day_index based on dates only
            day_index = (entered_date - start_date).days

            # Check if day_index is in the range and has data in habit_data
            if day_index < 0 or day_index >= current_day_index or day_index not in habit_data:
                raise ValueError("Date out of range or not tracked.")

            # Retrieve completed habits on this date
            day_data = habit_data.get(day_index, {})
            completed_habits = [habit for habit, done in day_data.items() if done]

            if completed_habits:
                message = f"Habits done on {entered_date}:\n" + "\n".join(completed_habits)
            else:
                message = f"No habits were completed on {entered_date}."

            messagebox.showinfo("Habits Done", message)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid date in the format YYYY-MM-DD & Date should be in the range of [Start date-currentdate)")

    # Reset all data (habits, target days, etc.)
    def reset_all(self):
        global habits, target_days, current_day_index, habit_data
        habits = []
        target_days = 0
        current_day_index = 0
        habit_data = {}
        self.create_main_page()

# Run the app
if __name__ == "__main__":
    app = HabitTrackerApp()
    app.mainloop()
