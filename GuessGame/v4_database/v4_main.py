"""
main.py
This is the main file of the Guess Game project. It contains the main GUI and navigation bar
"""

import os
import tkinter as tk

from tkinter import messagebox

import database

from PIL import Image, ImageTk
from v4_game import Game

database.init_db()
base_path = os.path.dirname(os.path.abspath(__file__))


# ═══ Palette ═════════════════════════════════════════════════════
BG       = "#ecf0f1"
DARK     = "#2c3e50"
DB       = "#34495e"
BLUE     = "#1368ce"
WHITE    = "#ffffff"



# ═══ APP ═════════════════════════════════════════════════════════
class GuessGameApp:
    """This is the basic properties (with navbar)"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("800x600")
        self.root.title("Guess Game")


        self.current_user = "Default User"
        user_info = database.get_user(self.current_user)
        if user_info:
            self.highest_score = user_info["highest_score"]
            self.total_score = user_info["total_score"]
        else:
            self.highest_score = 0
            self.total_score = 0

        self.root.app = self


        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)


        self.latest_game_score = 0
        self.root.update_user_score = self.update_user_score


        # --- Window icon ---
        icon_path = os.path.join(base_path,"image", "icon.ico")
        self.icon = ImageTk.PhotoImage(Image.open(icon_path))
        self.root.iconphoto(True, self.icon)

        self.navigationbar()

        self.current_page = None
        self.show_page(MainMenu)


    def show_page(self, page_class):
        """changing page function"""

        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = page_class(self.root, self.show_page)
        self.current_page.grid(row=1, column=0, sticky="nsew")


    def run(self):
        """Running the program"""
        self.root.mainloop()


    def navigationbar(self):
        """ Navigation Bar (always on top of the page)"""

        # Create frame of Nevigation Bar
        nav_bar = tk.Frame(self.root, bg=DARK, height=50)
        nav_bar.grid(row=0, column=0, sticky="ew")
        nav_bar.grid_propagate(False)

        # Add logo to the navigation bar
        logo_btn = tk.Button(
            nav_bar,
            text="GUESS GAME",
            font=("Arial", 14, "bold"),
            fg=WHITE,
            bg=DARK,
            activeforeground=WHITE,
            activebackground=DARK,
            bd=0,
            command=lambda: self.show_page(MainMenu),
        )
        logo_btn.pack(side="left", padx=20, fill="y")

        # Add buttons to the navigation bar
        tk.Button(
            nav_bar,
            text="My account",
            bg=DB,
            fg=WHITE,
            bd=0,
            padx=20,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page(Account),
        ).pack(side="right", padx=10)

        tk.Button(
            nav_bar,
            text="Login",
            bg=DB,
            fg=WHITE,
            bd=0,
            padx=20,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page(Login),
            ).pack(side="right", padx=10)

        # Create a container for the search bar
        search_container = tk.Frame(nav_bar, bg=DARK)
        search_container.pack(side="top", pady=10)

        # Add search entry and button to the search container
        search_button = tk.Button(
            search_container,
            text="Search",
            bg=DB,
            fg=WHITE,
            bd=0,
            padx=20,
            font=("Arial", 12, "bold"),
            command=self.perform_search
        )
        search_button.pack(side="right", padx=10)

        self.search_entry = tk.Entry(
            search_container,
            width=30,
            font=("Arial", 12),
            bd=0,
            relief="solid",
        )
        self.search_entry.pack(side="left", ipady=5, padx=10)
        self.search_entry.bind("<Return>", lambda event: self.perform_search())


    def perform_search(self):
        """execute search program"""
        keyword = self.search_entry.get().strip()

        if not isinstance(self.current_page, MainMenu):
            self.show_page(MainMenu)

        if isinstance(self.current_page, MainMenu):
            self.current_page.filter_games(keyword)


    def set_active_user(self, username):
        """Set the current active user and update their scores"""
        self.current_user = username
        user_info = database.get_user(username)
        if user_info:
            self.highest_score = user_info["highest_score"]
            self.total_score = user_info["total_score"]
            self.latest_game_score = 0


    def update_user_score(self, score, game_id=1):
        """update the score"""
        self.latest_game_score = score

        updated_data = database.update_user_score_in_db(self.current_user, score, game_id)
        if updated_data:
            self.highest_score = updated_data["highest_score"]
            self.total_score = updated_data["total_score"]

        self.show_page(Account)



class MainMenu(tk.Frame):
    """ Main Page of the project (Menu) """

    def __init__(self, root, show_page):
        super().__init__(root)
        self.show_page = show_page
        self.cards_list = []
        self.build_page()
        self.game_card()

        for row in (1, 2):
            self.grid_rowconfigure(row, weight=1)
        for column in range(3):
            self.grid_columnconfigure(column, weight=1, uniform="group1")


    def start_independent_game(self, game_id):
        """Pop up the game window and hide the main one"""
        main_root = self.master
        main_root.withdraw()

        game_window = Game(main_root, game_id)


    def build_page(self):
        """welcome text"""
        tk.Label(
            self,
            text="Welcome to Guess Game!",
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=0, column=0, columnspan=3,padx=20, pady=20, sticky="ew")


    def game_card(self):
        """Add game cards to the main content area"""


        game_data = database.get_all_games()


        cards_per_row = 3
        for index, data in enumerate(game_data):
            row = (index // cards_per_row) + 1
            column = index % cards_per_row


            card = tk.Frame(self, bg=BG, bd=1, relief="solid")
            card.grid(row=row, column=column, padx=20, pady=20, sticky="nsew")

            cover = tk.Frame(card, bg=data["cover_colour"], height=60)
            cover.pack(side="top", fill="x")

            title = tk.Label(
                card,
                text=data["title"],
                font=("Arial", 14, "bold"),
                bg=BG,
                anchor="w",
                wraplength=190
            )
            title.pack(side="top", fill="x", padx=10, pady=(10, 2))

            play_button = tk.Button(
                card,
                text="Start",
                bg=BLUE,
                fg=WHITE,
                font=("Arial", 11, "bold"),
                bd=0,
                command=lambda g_id=data["id"]: self.start_independent_game(g_id)
            )
            play_button.pack(side="bottom", fill="x", padx=10, pady=10)

            self.cards_list.append({
                "widget": card,
                "title": data["title"].lower()
            })


    def filter_games(self, keyword):
        """Filter and realign the card grid based on the keywords."""
        keyword = keyword.lower()
        visible_index = 0
        cards_per_row = 3

        for item in self.cards_list:
            if not keyword or keyword in item["title"]:
                row = (visible_index // cards_per_row) + 1
                col = visible_index % cards_per_row
                item["widget"].grid(row=row, column=col, padx=40, pady=40, sticky="nsew")
                visible_index += 1
            else:
                item["widget"].grid_remove()



class Login(tk.Frame):
    """Login page"""

    def __init__(self, root, show_page):
        super().__init__(root)
        self.show_page = show_page
        self.root = root
        self.app = getattr(root, 'app', None)

        self.user_name()
        self.password()
        self.button()

        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(4, weight=2)


    def user_name(self):
        "Ask user to enter the name"
        tk.Label(
            self,
            text="User Name:",
            font=("Arial", 18),
            bg=BG,
            fg=BLUE,
        ).grid(row=1, column=0, padx=20, pady=20, sticky="e")

        self.username_entry = tk.Entry(
            self,
            width=20,
            font=("Arial", 18),
            bd=0,
            relief="solid",
        )
        self.username_entry.grid(row=1, column=1, padx=20, pady=20, sticky="w")


    def password(self):
        "Ask user to set a password"
        tk.Label(
            self,
            text="Password:",
            font=("Arial", 18),
            bg=BG,
            fg=BLUE,
        ).grid(row=2, column=0, padx=20, pady=20, sticky="e")

        self.password_entry = tk.Entry(
            self,
            width=20,
            font=("Arial", 18),
            bd=0,
            relief="solid",
            show="*",
        )
        self.password_entry.grid(row=2, column=1, padx=20, pady=20, sticky="w")


    def button(self):
        """Button for login and sign up"""
        tk.Button(
            self,
            text="Login",
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            bd=0,
            command=self.login_user
        ).grid(row=3, column=0, padx=20, pady=20, sticky="e")

        tk.Button(
            self,
            text="Sign Up",
            bg=BLUE,
            fg=WHITE,
            font=("Arial", 11, "bold"),
            bd=0,
            command=self.sign_up_user
        ).grid(row=3, column=1, padx=20, pady=20, sticky="w")


    def login_user(self):
        """Login user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return

        if database.verify_user(username, password):
            messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
            if self.app:
                self.app.set_active_user(username)
            self.show_page(MainMenu)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")


    def sign_up_user(self):
        """Sign up user"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password!")
            return

        if database.register_user(username, password):
            messagebox.showinfo("Success", "Account created successfully! Logging you in...")
            if self.app:
                self.app.set_active_user(username)
            self.show_page(MainMenu)
        else:
            messagebox.showerror("Sign Up Failed", "Username already exists.")



class Account(tk.Frame):
    """Account page, show user's score"""

    def __init__(self, root, show_page):
        super().__init__(root)
        self.root= root
        self.show_page = show_page
        self.app = getattr(root, 'app', None)
        self.user_name()
        self.highest_score()
        self.total_score()
        self.show_latest_score()


        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(5, weight=2)

    def user_name(self):
        "Display user's name"
        tk.Label(
            self,
            text="User Name:",
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=1, column=0, padx=20, pady=20, sticky="e")

        username = self.app.current_user if self.app else "Default User"
        tk.Label(
            self,
            text=username,
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
            ).grid(row=1, column=1, padx=20, pady=20, sticky="w")


    def highest_score(self):
        "Display user's highest score"
        tk.Label(
            self,
            text="Highest Score:",
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=2, column=0, padx=20, pady=20, sticky="e")

        highest_score = self.app.highest_score if self.app else 0
        tk.Label(
            self,
            text=highest_score,
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=2, column=1, padx=20, pady=20, sticky="w")


    def total_score(self):
        "Display user's total score"
        tk.Label(
            self,
            text="Total Score:",
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=3, column=0,padx=20, pady=20, sticky="e")

        total_score = self.app.total_score if self.app else 0
        tk.Label(
            self,
            text=total_score,
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=3, column=1, padx=20, pady=20, sticky="w")


    def show_latest_score(self):
        """Show last game score"""

        tk.Label(
            self,
            text="Score in last game:",
            font=("Arial", 18),
            bg=BG,
            fg=DARK,
        ).grid(row=4, column=0, padx=20, pady=20, sticky="e")

        latest_game_score = self.app.latest_game_score if self.app else 0
        tk.Label(
            self,
            text=latest_game_score,
            font=("Arial", 18, "bold"),
            bg=BG,
            fg=DARK,
        ).grid(row=4, column=1, padx=20, pady=20, sticky="w")



if __name__ == "__main__":
    app = GuessGameApp()
    app.run()
