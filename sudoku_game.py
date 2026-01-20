import tkinter as tk
from tkinter import messagebox
import random
import copy
from datetime import datetime
import json
import os

class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.geometry("700x750")
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.difficulty = None
        self.board = [[0]*9 for _ in range(9)]
        self.solution = [[0]*9 for _ in range(9)]
        self.initial_board = [[0]*9 for _ in range(9)]
        self.selected_cell = None
        self.cells = {}
        self.start_time = None
        self.mistakes = 0
        self.max_mistakes = 3

        self.difficulty_settings = {
            "Easy": 35,
            "Medium": 45,
            "Hard": 50,
            "Expert": 55
        }

        self.difficulty_scores = {
            "Easy": 100,
            "Medium": 200,
            "Hard": 400,
            "Expert": 800
        }

        self.high_scores_file = os.path.join(os.path.dirname(__file__), "high_scores.json")
        self.high_scores = self.load_high_scores()

        self.show_welcome_screen()

    def show_welcome_screen(self):
        """Display welcome screen with difficulty selection"""
        # Only clear if there are existing widgets
        if self.root.winfo_children():
            self.clear_window()

        # Title
        title = tk.Label(self.root, text="SUDOKU",
                        font=("Arial", 48, "bold"),
                        bg="white", fg="#1a73e8")
        title.pack(pady=60)

        subtitle = tk.Label(self.root, text="Select Difficulty",
                          font=("Arial", 18),
                          bg="white", fg="#666")
        subtitle.pack(pady=20)

        # Difficulty buttons
        button_frame = tk.Frame(self.root, bg="white")
        button_frame.pack(pady=30)

        colors = {
            "Easy": "#4CAF50",
            "Medium": "#FF9800",
            "Hard": "#F44336",
            "Expert": "#9C27B0"
        }

        for difficulty in self.difficulty_settings.keys():
            btn = tk.Button(button_frame, text=difficulty,
                          font=("Arial", 18, "bold"),
                          bg=colors[difficulty], fg="white",
                          width=15, height=2,
                          relief=tk.FLAT,
                          cursor="hand2",
                          command=lambda d=difficulty: self.start_game(d))
            btn.pack(pady=10)

        # High scores button
        high_scores_btn = tk.Button(button_frame, text="🏆 High Scores",
                                   font=("Arial", 16),
                                   bg="#FFC107", fg="white",
                                   width=15, height=1,
                                   relief=tk.FLAT,
                                   cursor="hand2",
                                   command=self.show_high_scores)
        high_scores_btn.pack(pady=20)

    def start_game(self, difficulty):
        """Start a new game with selected difficulty"""
        print(f"Starting game with difficulty: {difficulty}")  # Debug
        self.difficulty = difficulty
        self.mistakes = 0
        self.selected_cell = None
        print("Generating puzzle...")  # Debug
        self.generate_puzzle(self.difficulty_settings[difficulty])
        print("Puzzle generated!")  # Debug
        self.start_time = datetime.now()
        self.show_game_screen()

    def generate_puzzle(self, cells_to_remove):
        """Generate a valid Sudoku puzzle"""
        # Use a pre-made puzzle for testing
        self.solution = [
            [5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 7, 6, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9]
        ]

        self.board = copy.deepcopy(self.solution)

        # Remove cells based on difficulty
        cells_removed = 0
        attempts = 0
        while cells_removed < cells_to_remove and attempts < 100:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cells_removed += 1
            attempts += 1

        # Copy initial board
        self.initial_board = copy.deepcopy(self.board)

    def fill_box(self, row, col):
        """Fill a 3x3 box with random numbers"""
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                self.board[row + i][col + j] = nums[i * 3 + j]

    def is_valid(self, board, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[i][col] for i in range(9)]:
            return False

        # Check 3x3 box
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def solve_sudoku(self, board):
        """Solve Sudoku using backtracking"""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_valid(board, i, j, num):
                            board[i][j] = num
                            if self.solve_sudoku(board):
                                return True
                            board[i][j] = 0
                    return False
        return True

    def show_game_screen(self):
        """Display the game screen with Sudoku grid"""
        print("show_game_screen called")  # Debug
        self.clear_window()
        print("Window cleared")  # Debug
        self.cells = {}
        print("Creating grid...")  # Debug

        # Main container
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Top info bar
        info_frame = tk.Frame(main_frame, bg="white")
        info_frame.pack(fill="x", pady=(0, 20))

        # Difficulty tabs
        tab_frame = tk.Frame(info_frame, bg="white")
        tab_frame.pack(side="left")

        for diff in self.difficulty_settings.keys():
            color = "#1a73e8" if diff == self.difficulty else "#ccc"
            tab = tk.Label(tab_frame, text=diff, font=("Arial", 12, "bold"),
                          bg="white", fg=color, padx=10)
            tab.pack(side="left", padx=5)

        # Right side info
        right_info = tk.Frame(info_frame, bg="white")
        right_info.pack(side="right")

        self.mistakes_label = tk.Label(right_info,
                                       text=f"Mistakes\n{self.mistakes}/{self.max_mistakes}",
                                       font=("Arial", 12),
                                       bg="white", fg="#666")
        self.mistakes_label.pack(side="left", padx=20)

        self.time_label = tk.Label(right_info, text="Time\n00:00",
                                   font=("Arial", 12),
                                   bg="white", fg="#666")
        self.time_label.pack(side="left")

        # Grid frame - Add scrollbar support for smaller screens
        grid_container = tk.Frame(main_frame, bg="white")
        grid_container.pack(pady=10, fill="both", expand=True)

        # Canvas for scrolling on small screens
        canvas = tk.Canvas(grid_container, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(grid_container, orient="vertical", command=canvas.yview)

        grid_frame = tk.Frame(canvas, bg="#344861", bd=3, relief=tk.SOLID)

        # Configure canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        # Create window in canvas
        canvas_window = canvas.create_window((0, 0), window=grid_frame, anchor="n")

        # Configure scroll region after grid is populated
        def configure_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Center the grid horizontally
            canvas_width = canvas.winfo_width()
            frame_width = grid_frame.winfo_reqwidth()
            x_position = max(0, (canvas_width - frame_width) // 2)
            canvas.coords(canvas_window, x_position, 0)

        grid_frame.bind("<Configure>", configure_scroll_region)
        canvas.bind("<Configure>", configure_scroll_region)

        # Create 9x9 grid
        for i in range(9):
            for j in range(9):
                # Thicker borders for 3x3 boxes
                relief_type = tk.SOLID
                bd = 1

                # Add thicker borders for 3x3 sections
                padx_left = 3 if j % 3 == 0 and j != 0 else 1
                padx_right = 3 if j % 3 == 2 and j != 8 else 1
                pady_top = 3 if i % 3 == 0 and i != 0 else 1
                pady_bottom = 3 if i % 3 == 2 and i != 8 else 1

                # Alternating background color for 3x3 boxes
                box_row = i // 3
                box_col = j // 3
                if (box_row + box_col) % 2 == 0:
                    bg_color = "#e8f0fe"
                else:
                    bg_color = "white"

                cell = tk.Label(grid_frame, text="",
                              font=("Arial", 24),
                              bg=bg_color, fg="#344861",
                              width=2, height=1,
                              relief=relief_type, bd=bd)

                cell.grid(row=i, column=j,
                         padx=(padx_left, padx_right),
                         pady=(pady_top, pady_bottom),
                         ipadx=8, ipady=8)

                if self.initial_board[i][j] != 0:
                    cell.config(text=str(self.initial_board[i][j]),
                              font=("Arial", 24, "bold"),
                              fg="#000")
                    cell.is_fixed = True
                else:
                    cell.is_fixed = False
                    cell.bind("<Button-1>", lambda e, r=i, c=j: self.select_cell(r, c))

                self.cells[(i, j)] = cell

        # Number pad
        numpad_frame = tk.Frame(main_frame, bg="white")
        numpad_frame.pack(pady=20)

        for num in range(1, 10):
            btn = tk.Button(numpad_frame, text=str(num),
                          font=("Arial", 20, "bold"),
                          width=3, height=1,
                          bg="#e8f0fe", fg="#1a73e8",
                          relief=tk.FLAT,
                          cursor="hand2",
                          activebackground="#1a73e8",
                          activeforeground="white",
                          command=lambda n=num: self.place_number(n))
            btn.grid(row=(num-1)//3, column=(num-1)%3, padx=5, pady=5)

        # Control buttons
        button_frame = tk.Frame(main_frame, bg="white")
        button_frame.pack(pady=10)

        new_game_btn = tk.Button(button_frame, text="New Game",
                                font=("Arial", 14),
                                width=12, bg="#1a73e8", fg="white",
                                relief=tk.FLAT, cursor="hand2",
                                command=self.show_welcome_screen)
        new_game_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(button_frame, text="Clear",
                            font=("Arial", 14),
                            width=12, bg="#f44336", fg="white",
                            relief=tk.FLAT, cursor="hand2",
                            command=self.clear_cell)
        clear_btn.grid(row=0, column=1, padx=5)

        hint_btn = tk.Button(button_frame, text="Hint",
                           font=("Arial", 14),
                           width=12, bg="#4CAF50", fg="white",
                           relief=tk.FLAT, cursor="hand2",
                           command=self.show_hint)
        hint_btn.grid(row=0, column=2, padx=5)

        # Start timer
        self.update_timer()

    def select_cell(self, row, col):
        """Select a cell"""
        # Deselect previous cell
        if self.selected_cell:
            r, c = self.selected_cell
            box_row = r // 3
            box_col = c // 3
            if (box_row + box_col) % 2 == 0:
                bg_color = "#e8f0fe"
            else:
                bg_color = "white"
            self.cells[(r, c)].config(bg=bg_color)

        # Select new cell
        self.selected_cell = (row, col)
        self.cells[(row, col)].config(bg="#bbdefb")

    def place_number(self, num):
        """Place a number in the selected cell"""
        if not self.selected_cell:
            return

        row, col = self.selected_cell

        # Check if correct
        if self.solution[row][col] == num:
            self.board[row][col] = num
            self.cells[(row, col)].config(text=str(num), fg="#1a73e8",
                                         font=("Arial", 24))

            # Check if puzzle is complete
            if self.is_complete():
                self.game_won()
        else:
            self.mistakes += 1
            self.mistakes_label.config(text=f"Mistakes\n{self.mistakes}/{self.max_mistakes}")

            # Flash red
            self.cells[(row, col)].config(bg="#ffcdd2")
            self.root.after(300, lambda: self.select_cell(row, col))

            if self.mistakes >= self.max_mistakes:
                self.game_over()

    def clear_cell(self):
        """Clear the selected cell"""
        if not self.selected_cell:
            messagebox.showinfo("Info", "Please select a cell first!")
            return

        row, col = self.selected_cell
        if not self.cells[(row, col)].is_fixed:
            self.board[row][col] = 0
            self.cells[(row, col)].config(text="")

    def show_hint(self):
        """Show hint for selected cell"""
        if not self.selected_cell:
            messagebox.showinfo("Hint", "Please select a cell first!")
            return

        row, col = self.selected_cell
        if self.cells[(row, col)].is_fixed:
            messagebox.showinfo("Hint", "This cell is already filled!")
            return

        if self.board[row][col] != 0:
            messagebox.showinfo("Hint", "This cell already has a number!")
            return

        hint = self.solution[row][col]
        messagebox.showinfo("Hint", f"The correct number is: {hint}")

    def is_complete(self):
        """Check if puzzle is complete"""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True

    def game_won(self):
        """Handle game won"""
        elapsed = (datetime.now() - self.start_time).seconds
        score = self.calculate_score(elapsed)

        message = f"🎉 Congratulations!\n\n"
        message += f"Difficulty: {self.difficulty}\n"
        message += f"Time: {self.format_time(elapsed)}\n"
        message += f"Mistakes: {self.mistakes}\n"
        message += f"Score: {score}"

        # Save high score
        self.save_high_score(score, elapsed)

        messagebox.showinfo("You Won!", message)
        self.show_welcome_screen()

    def calculate_score(self, time_seconds):
        """Calculate score based on difficulty, time, and mistakes"""
        base_score = self.difficulty_scores[self.difficulty]

        # Time bonus: lose points for every minute (max penalty: 50% of base score)
        time_penalty = min(time_seconds // 60 * 10, base_score // 2)

        # Mistake penalty: -20 points per mistake
        mistake_penalty = self.mistakes * 20

        final_score = max(base_score - time_penalty - mistake_penalty, 0)
        return final_score

    def game_over(self):
        """Handle game over with user-friendly options"""
        # Create custom dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Game Over")
        dialog.geometry("400x250")
        dialog.configure(bg="white")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"400x250+{x}+{y}")

        # Message
        msg_frame = tk.Frame(dialog, bg="white")
        msg_frame.pack(pady=30, padx=20)

        title_label = tk.Label(msg_frame, text="⚠️ Game Over",
                              font=("Arial", 20, "bold"),
                              bg="white", fg="#f44336")
        title_label.pack()

        msg_label = tk.Label(msg_frame,
                            text=f"You've made {self.max_mistakes} mistakes!\n\nWhat would you like to do?",
                            font=("Arial", 12),
                            bg="white", fg="#333",
                            justify="center")
        msg_label.pack(pady=10)

        # Buttons
        btn_frame = tk.Frame(dialog, bg="white")
        btn_frame.pack(pady=10)

        def restart_lost():
            dialog.destroy()
            self.restart_game()

        def new_game():
            dialog.destroy()
            self.show_welcome_screen()

        restart_btn = tk.Button(btn_frame, text="Restart the Lost Game",
                               font=("Arial", 13, "bold"),
                               bg="#FF9800", fg="white",
                               width=20, height=2,
                               relief=tk.FLAT,
                               cursor="hand2",
                               command=restart_lost)
        restart_btn.pack(pady=5)

        new_game_btn = tk.Button(btn_frame, text="Start a New Game",
                                font=("Arial", 13, "bold"),
                                bg="#1a73e8", fg="white",
                                width=20, height=2,
                                relief=tk.FLAT,
                                cursor="hand2",
                                command=new_game)
        new_game_btn.pack(pady=5)

    def restart_game(self):
        """Restart the current game with the same puzzle"""
        self.mistakes = 0
        self.board = copy.deepcopy(self.initial_board)
        self.selected_cell = None
        self.start_time = datetime.now()
        self.show_game_screen()

    def update_timer(self):
        """Update the timer"""
        if hasattr(self, 'time_label') and self.start_time:
            elapsed = (datetime.now() - self.start_time).seconds
            self.time_label.config(text=f"Time\n{self.format_time(elapsed)}")
            self.root.after(1000, self.update_timer)

    def format_time(self, seconds):
        """Format time as MM:SS"""
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
        self.root.update()

    def load_high_scores(self):
        """Load high scores from file"""
        if os.path.exists(self.high_scores_file):
            try:
                with open(self.high_scores_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_high_score(self, score, time_seconds):
        """Save high score and keep only top 10"""
        high_score_entry = {
            "score": score,
            "difficulty": self.difficulty,
            "time": time_seconds,
            "mistakes": self.mistakes,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M")
        }

        self.high_scores.append(high_score_entry)

        # Sort by score (descending) and keep only top 10
        self.high_scores.sort(key=lambda x: x["score"], reverse=True)
        self.high_scores = self.high_scores[:10]

        # Save to file
        try:
            with open(self.high_scores_file, 'w') as f:
                json.dump(self.high_scores, f, indent=2)
        except Exception as e:
            print(f"Error saving high scores: {e}")

    def show_high_scores(self):
        """Display high scores screen"""
        self.clear_window()

        # Title
        title = tk.Label(self.root, text="🏆 HIGH SCORES",
                        font=("Arial", 36, "bold"),
                        bg="white", fg="#FFC107")
        title.pack(pady=40)

        # Scores frame
        scores_frame = tk.Frame(self.root, bg="white")
        scores_frame.pack(pady=20, padx=40, fill="both", expand=True)

        if self.high_scores:
            # Header
            header_frame = tk.Frame(scores_frame, bg="#1a73e8")
            header_frame.pack(fill="x", pady=(0, 10))

            headers = ["Rank", "Score", "Difficulty", "Time", "Mistakes", "Date"]
            widths = [5, 8, 10, 8, 10, 15]

            for i, (header, width) in enumerate(zip(headers, widths)):
                lbl = tk.Label(header_frame, text=header,
                             font=("Arial", 11, "bold"),
                             bg="#1a73e8", fg="white",
                             width=width, anchor="w", padx=5)
                lbl.grid(row=0, column=i, padx=2, pady=5, sticky="w")

            # Scores
            for idx, score_entry in enumerate(self.high_scores, 1):
                row_frame = tk.Frame(scores_frame, bg="#f5f5f5" if idx % 2 == 0 else "white",
                                   relief=tk.FLAT, bd=1)
                row_frame.pack(fill="x", pady=2)

                rank_color = "#FFD700" if idx == 1 else "#C0C0C0" if idx == 2 else "#CD7F32" if idx == 3 else "#666"

                data = [
                    f"#{idx}",
                    str(score_entry["score"]),
                    score_entry["difficulty"],
                    self.format_time(score_entry["time"]),
                    str(score_entry["mistakes"]),
                    score_entry["date"]
                ]

                for i, (value, width) in enumerate(zip(data, widths)):
                    lbl = tk.Label(row_frame, text=value,
                                 font=("Arial", 10, "bold" if i == 0 else "normal"),
                                 bg=row_frame["bg"],
                                 fg=rank_color if i == 0 else "#333",
                                 width=width, anchor="w", padx=5)
                    lbl.grid(row=0, column=i, padx=2, pady=5, sticky="w")
        else:
            no_scores = tk.Label(scores_frame,
                               text="No high scores yet!\nPlay a game to set a record.",
                               font=("Arial", 16),
                               bg="white", fg="#999")
            no_scores.pack(pady=50)

        # Back button
        back_btn = tk.Button(self.root, text="← Back to Menu",
                           font=("Arial", 14),
                           bg="#1a73e8", fg="white",
                           width=20, height=2,
                           relief=tk.FLAT,
                           cursor="hand2",
                           command=self.show_welcome_screen)
        back_btn.pack(pady=30)

def main():
    root = tk.Tk()
    game = SudokuGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
