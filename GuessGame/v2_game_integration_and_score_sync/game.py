"""This is the GUI for the Guess Game (GamePage). """
import os
import tkinter as tk
from tkinter import messagebox


class GameData:
    """Game data"""

    class MockQuestion:
        """Define the structure for questions"""
        def __init__(self, question_id, question, options, correct_answer):
            self.question_id = question_id
            self.question = question
            self.options = options
            self.correct_answer = correct_answer

    class GameDataService:
        """Record the questions"""

        def __init__(self):
            self.questions = [
                GameData.MockQuestion(1, "1", ["1", "2", "3", "4"], "1"),
                GameData.MockQuestion(2, "2", ["1", "2", "3", "4"], "2"),
                GameData.MockQuestion(3, "3", ["1", "2", "3", "4"], "3"),
                GameData.MockQuestion(4, "4", ["1", "2", "3", "4"], "4"),
            ]

        def get_questions_for_game(self):
            """Retrieve all question"""
            return self.questions



class Game(tk.Toplevel):
    """Main part of the program"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Quiz Game")
        self.geometry("800x600")


        self.data_service = GameData.GameDataService()
        self.questions_list = self.data_service.get_questions_for_game()
        self.current_index = 0
        self.score = 0


        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)


        self.question_area()
        self.options_area()
        self.footer_area()
        self.load_question()


    def question_area(self):
        """Questions will stay here"""

        self.question_label = tk.Label(
            self,
            text="Loading...",
            font=("Arial", 20, "bold"),
            bg="#405263",
            fg="white",
            wraplength=600,
            justify="center"
        )
        self.question_label.grid(row=0, column=0, sticky="nsew")

    def options_area(self):
        """Options will stay here"""

        self.options_container = tk.Frame(self)
        self.options_container.grid(row=1, column=0, padx=40, pady=20, sticky="nsew")

        self.options_container.columnconfigure(0, weight=1)
        self.options_container.columnconfigure(1, weight=1)
        self.options_container.rowconfigure(0, weight=1)
        self.options_container.rowconfigure(1, weight=1)

        colors = ["#e21b3c", "#1368ce", "#d89e00", "#26890c"]
        self.option_buttons = []

        for i in range(4):
            row = i // 2
            col = i % 2
            button = tk.Button(
                self.options_container,
                text="",
                font=("Arial", 14, "bold"),
                bg=colors[i],
                fg="white",
                activebackground=colors[i],
                activeforeground="white",
                bd=0,
                command=lambda idx=i: self.check_answer(idx)
            )
            button.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            self.option_buttons.append(button)

    def footer_area(self):
        """Current score and button to next question"""

        self.footer_frame = tk.Frame(self, bg="#ecf0f1", height=50)
        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.status_label = tk.Label(
            self.footer_frame,
            text=f"Score: {self.score}",
            font=("Arial", 12),
            bg="#ecf0f1"
        )
        self.status_label.pack(padx=20, pady=10)


    def load_question(self):
        """Load the questions"""

        if self.current_index < len(self.questions_list):
            q = self.questions_list[self.current_index]
            self.question_label.config(text=f"Q{self.current_index + 1}: {q.question}")

            for i, option in enumerate(q.options):
                self.option_buttons[i].config(text=option, state="normal")
        else:
            self.show_game_over()


    def check_answer(self, button_index):
        """Check for errors"""

        q = self.questions_list[self.current_index]
        selected_answer = q.options[button_index]

        for button in self.option_buttons:
            button.config(state="disabled")

        if selected_answer == q.correct_answer:
            self.score += 100
            self.status_label.config(text=f"Score: {self.score}")
            messagebox.showinfo("", "Correct!")
        else:
            messagebox.showerror("", f"Wrong, the answer is: {q.correct_answer}")

        self.next_question()


    def next_question(self):
        """Show the next question"""
        self.current_index += 1
        self.load_question()


    def show_game_over(self):
        """Game Over"""
        messagebox.showinfo("Settle the score", f"The end! Your final score is: {self.score}")

        if hasattr(self.parent, 'update_user_score'):
            self.parent.update_user_score(self.score)

        self.on_close()


    def on_close(self):
        """Close current page and open the main page"""
        self.parent.deiconify()
        self.destroy()
