"""This is the GUI for the Guess Game. """
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


base_path = os.path.dirname(os.path.abspath(__file__))


class GuessGameApp:
    """This is the basic properties (with navbar)"""

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1024x768")
        self.root.title("Guess Game")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=1)

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
        nav_bar = tk.Frame(self.root, bg="#2c3e50", height=50)
        nav_bar.grid(row=0, column=0, sticky="ew")
        nav_bar.grid_propagate(False)

        # Add logo to the navigation bar
        logo_btn = tk.Button(
            nav_bar,
            text="GUESS GAME",
            font=("Arial", 14, "bold"),
            fg="white",
            bg="#2c3e50",
            activeforeground="white",
            activebackground="#2c3e50",
            bd=0,
            command=lambda: self.show_page(MainMenu),
        )
        logo_btn.pack(side="left", padx=20, fill="y")

        # Add buttons to the navigation bar
        tk.Button(
            nav_bar,
            text="My account",
            bg="#34495e",
            fg="white",
            bd=0,
            padx=20,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page(Account),
        ).pack(side="right", padx=10)

        tk.Button(
            nav_bar,
            text="Login",
            bg="#34495e",
            fg="white",
            bd=0,
            padx=20,
            font=("Arial", 12, "bold"),
            command=lambda: self.show_page(Login),
            ).pack(side="right", padx=10)

        # Create a container for the search bar
        search_container = tk.Frame(nav_bar, bg="#2c3e50")
        search_container.pack(side="top", pady=10)

        # Add search entry and button to the search container
        tk.Button(
            search_container,
            text="Search",
            bg="#34495e",
            fg="white",
            bd=0,
            padx=20,
            font=("Arial", 12, "bold"),
        ).pack(side="right", padx=10)

        tk.Entry(
            search_container,
            width=30,
            font=("Arial", 12),
            bd=0,
            relief="solid",
        ).pack(side="left", ipady=5, padx=10)


class MainMenu(tk.Frame):
    """ Main Page of the project (Menu) """

    def __init__(self, root, show_page):
        super().__init__(root)
        self.show_page = show_page
        self.build_page()
        self.game_card()

        for row in (1, 2):
            self.grid_rowconfigure(row, weight=1)
        for column in range(3):
            self.grid_columnconfigure(column, weight=1)


    def build_page(self):
        """welcome text"""
        tk.Label(
            self,
            text="Welcome to Guess Game!",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50"
        ).grid(row=0, column=0, columnspan=3,padx=20, pady=20, sticky="ew")


    def game_card(self):
        """Add game cards to the main content area"""

        # Row 1, Column 0, 1, 2 - Game cards
        # Game card 1 (Row1, Column0)
        card1 = tk.Frame(self, bg="white", bd=1, relief="solid")
        card1.grid(row=1, column=0, padx=40, pady=40, sticky="nsew")

        cover1 = tk.Frame(card1, bg="#1a6fa1", height=60)
        cover1.pack(side="top", fill="x")

        title1 = tk.Label(card1, text="1", font=("Arial", 14, "bold"), bg="white", anchor="w")
        title1.pack(side="top", fill="x", padx=10, pady=(10, 2))

        type1 = tk.Label(card1, text="1", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        type1.pack(side="top", fill="x", padx=10, pady=(0, 10))

        play_btn1 = tk.Button(card1, text="Start", bg="#3b7799", fg="white", font=("Arial", 11, "bold"), bd=0)
        play_btn1.pack(side="bottom", fill="x", padx=10, pady=10)


        # Game card 2 (Row1, Column1)
        card2 = tk.Frame(self, bg="white", bd=1, relief="solid")
        card2.grid(row=1, column=1, padx=40, pady=40, sticky="nsew")

        cover2 = tk.Frame(card2, bg="#1a6fa1", height=60)
        cover2.pack(side="top", fill="x")

        title2 = tk.Label(card2, text="2", font=("Arial", 14, "bold"), bg="white", anchor="w")
        title2.pack(side="top", fill="x", padx=10, pady=(10, 2))

        type2 = tk.Label(card2, text="2", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        type2.pack(side="top", fill="x", padx=10, pady=(0, 10))

        play_btn2 = tk.Button(card2, text="Start", bg="#3b7799", fg="white", font=("Arial", 11, "bold"), bd=0)
        play_btn2.pack(side="bottom", fill="x", padx=10, pady=10)


        # Game card 3 (Row1, Column2)
        card3 = tk.Frame(self, bg="white", bd=1, relief="solid")
        card3.grid(row=1, column=2, padx=40, pady=40, sticky="nsew")

        cover3 = tk.Frame(card3, bg="#1a6fa1", height=60)
        cover3.pack(side="top", fill="x")

        title3 = tk.Label(card3, text="3", font=("Arial", 14, "bold"), bg="white", anchor="w")
        title3.pack(side="top", fill="x", padx=10, pady=(10, 2))

        type3 = tk.Label(card3, text="3", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        type3.pack(side="top", fill="x", padx=10, pady=(0, 10))

        play_btn3 = tk.Button(card3, text="Start", bg="#3b7799", fg="white", font=("Arial", 11, "bold"), bd=0)
        play_btn3.pack(side="bottom", fill="x", padx=10, pady=10)



        # Row 2, Column 0, 1, 2 - Game cards
        # Game card 4
        card4 = tk.Frame(self, bg="white", bd=1, relief="solid")
        card4.grid(row=2, column=0, padx=40, pady=40, sticky="nsew")

        cover4 = tk.Frame(card4, bg="#1a6fa1", height=60)
        cover4.pack(side="top", fill="x")

        title4 = tk.Label(card4, text="4", font=("Arial", 14, "bold"), bg="white", anchor="w")
        title4.pack(side="top", fill="x", padx=10, pady=(10, 2))

        type4 = tk.Label(card4, text="4", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        type4.pack(side="top", fill="x", padx=10, pady=(0, 10))

        play_btn4 = tk.Button(card4, text="Start", bg="#3b7799", fg="white", font=("Arial", 11, "bold"), bd=0)
        play_btn4.pack(side="bottom", fill="x", padx=10, pady=10)


        # Game card 5
        card5 = tk.Frame(self, bg="white", bd=1, relief="solid")
        card5.grid(row=2, column=1, padx=40, pady=40, sticky="nsew")

        cover5 = tk.Frame(card5, bg="#1a6fa1", height=60)
        cover5.pack(side="top", fill="x")

        title5 = tk.Label(card5, text="5", font=("Arial", 14, "bold"), bg="white", anchor="w")
        title5.pack(side="top", fill="x", padx=10, pady=(10, 2))

        type5 = tk.Label(card5, text="5", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        type5.pack(side="top", fill="x", padx=10, pady=(0, 10))

        play_btn5 = tk.Button(card5, text="Start", bg="#3b7799", fg="white", font=("Arial", 11, "bold"), bd=0)
        play_btn5.pack(side="bottom", fill="x", padx=10, pady=10)


        # Game card 6
        card6 = tk.Frame(self, bg="white", bd=1, relief="solid")
        card6.grid(row=2, column=2, padx=40, pady=40, sticky="nsew")

        cover6 = tk.Frame(card6, bg="#1a6fa1", height=60)
        cover6.pack(side="top", fill="x")

        title6 = tk.Label(card6, text="6", font=("Arial", 14, "bold"), bg="white", anchor="w")
        title6.pack(side="top", fill="x", padx=10, pady=(10, 2))

        type6 = tk.Label(card6, text="6", font=("Arial", 10), fg="gray", bg="white", anchor="w")
        type6.pack(side="top", fill="x", padx=10, pady=(0, 10))

        play_btn6 = tk.Button(card6, text="Start", bg="#3b7799", fg="white", font=("Arial", 11, "bold"), bd=0)
        play_btn6.pack(side="bottom", fill="x", padx=10, pady=10)



class Login(tk.Frame):
    """Loing page"""

    def __init__(self, root, show_page):
        super().__init__(root)
        self.show_page = show_page
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
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=1, column=0, padx=20, pady=20, sticky="e")

        tk.Entry(
            self,
            width=10,
            font=("Arial", 18),
            bd=0,
            relief="solid",
        ).grid(row=1, column=1, padx=20, pady=20, sticky="w")

    def password(self):
        "Ask user to set a password"
        tk.Label(
            self,
            text="Password:",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=2, column=0, padx=20, pady=20, sticky="e")

        tk.Entry(
            self,
            width=10,
            font=("Arial", 18),
            bd=0,
            relief="solid",
            show="*",
        ).grid(row=2, column=1, padx=20, pady=20, sticky="w")


    def button(self):
        """Button for login and sign up"""
        tk.Button(
            self,
            text="Login",
            bg="#63a3c8",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0
        ).grid(row=3, column=0, padx=20, pady=20, sticky="e")

        tk.Button(
            self,
            text="Sign Up",
            bg="#63a3c8",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0
        ).grid(row=3, column=1, padx=20, pady=20, sticky="w")



class Account(tk.Frame):
    """Account page, show user's score"""

    def __init__(self, root, show_page):
        super().__init__(root)
        self.show_page = show_page
        self.user_name()
        self.highest_score()
        self.total_score()


        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=10)
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(4, weight=2)


    def user_name(self):
        "Display user's name"
        tk.Label(
            self,
            text="User Name:",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=1, column=0, padx=20, pady=20, sticky="e")

        tk.Label(
            self,
            text="1",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=1, column=1, padx=20, pady=20, sticky="w")


    def highest_score(self):
        "Display user's highest score"
        tk.Label(
            self,
            text="Highest Score:",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=2, column=0, padx=20, pady=20, sticky="e")

        tk.Label(
            self,
            text="2",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=2, column=1, padx=20, pady=20, sticky="w")


    def total_score(self):
        "Display user's total score"
        tk.Label(
            self,
            text="Total Score:",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=3, column=0,padx=20, pady=20, sticky="e")

        tk.Label(
            self,
            text="3",
            font=("Arial", 18),
            bg="#ecf0f1",
            fg="#2c3e50",
        ).grid(row=3, column=1, padx=20, pady=20, sticky="w")


if __name__ == "__main__":
    app = GuessGameApp()
    app.run()
