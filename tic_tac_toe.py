import tkinter as tk
from tkinter import messagebox
import random

internal_board = [' '] * 10
PLAYER_LETTER = 'X'
AI_LETTER = 'O'

def make_move(board, letter, move):
    board[move] = letter

def is_winner(bo, le):
    win_combos = [
        [7, 8, 9], [4, 5, 6], [1, 2, 3], 
        [7, 4, 1], [8, 5, 2], [9, 6, 3], 
        [7, 5, 3], [9, 5, 1]            
    ]
    for combo in win_combos:
        if bo[combo[0]] == le and bo[combo[1]] == le and bo[combo[2]] == le:
            return combo
    return None

def get_possible_moves(board):
    moves = []
    for i in range(1, 10):
        if board[i] == ' ':
            moves.append(i)
    return moves

def is_board_full(board):
    for i in range(1, 10):
        if board[i] == ' ':
            return False
    return True

def minimax(current_board, is_maximizing_player):
    if is_winner(current_board, AI_LETTER): return (None, 10)
    elif is_winner(current_board, PLAYER_LETTER): return (None, -10)
    elif is_board_full(current_board): return (None, 0)
    
    if is_maximizing_player:
        best_score = -1000
        best_move = None
        for move in get_possible_moves(current_board):
            make_move(current_board, AI_LETTER, move)
            _, score = minimax(current_board, False)
            make_move(current_board, ' ', move)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move, best_score
    else:
        best_score = 1000
        best_move = None
        for move in get_possible_moves(current_board):
            make_move(current_board, PLAYER_LETTER, move)
            _, score = minimax(current_board, True)
            make_move(current_board, ' ', move)
            if score < best_score:
                best_score = score
                best_move = move
        return best_move, best_score

def get_ai_move(board):
    move, _ = minimax(board, True)
    if move is None:
        return get_possible_moves(board)[0]
    return move



class TicTacToeApp:
    def __init__(self, root, creator_name="Mili Srivastava"):
        self.root = root
        self.root.title("Tic-Tac-Toe") 
        self.root.resizable(False, False)
        
        self.COLOR_BG = "#1A1A2E"
        self.COLOR_GRID = "white"
        self.COLOR_TEXT = "white"
        self.COLOR_X = "#FF4136"
        self.COLOR_O = "#39FF14"
        self.COLOR_WIN = "#FCD12A"
        
        self.root.config(bg=self.COLOR_BG)

   
        self.buttons = {}
        self.current_player = PLAYER_LETTER
        self.game_mode = "PVE" 
        
      
        self.scores_pve = {"X": 0, "O": 0, "Ties": 0}
        self.scores_pvp = {"X": 0, "O": 0, "Ties": 0}
        
      
        self.title_font = ('Arial', 28, 'bold')
        self.turn_font = ('Arial', 16)
        self.score_font_text = ('Arial', 12)
        self.score_font_num = ('Arial', 16, 'bold')
        self.button_font = ('Arial', 32, 'bold')

        self.turn_label_var = tk.StringVar()
        self.score_x_var = tk.StringVar(value="0")
        self.score_o_var = tk.StringVar(value="0")
        self.score_ties_var = tk.StringVar(value="0")
        self.score_o_text_var = tk.StringVar()

      
        self.title_label = tk.Label(root, text="Tic-Tac-Toe", 
                                    font=self.title_font, 
                                    fg=self.COLOR_TEXT, bg=self.COLOR_BG)
        self.title_label.pack(pady=(15, 5))

        self.turn_label = tk.Label(root, textvariable=self.turn_label_var, 
                                   font=self.turn_font, 
                                   fg=self.COLOR_TEXT, bg=self.COLOR_BG)
        self.turn_label.pack(pady=5)
        
        grid_frame = tk.Frame(root, bg=self.COLOR_GRID)
        grid_frame.pack(pady=10)

        index_map = [
            (7, 0, 0), (8, 0, 1), (9, 0, 2),
            (4, 1, 0), (5, 1, 1), (6, 1, 2),
            (1, 2, 0), (2, 2, 1), (3, 2, 2)
        ]
        
        for (index, r, c) in index_map:
            button = tk.Button(grid_frame, text=' ', width=4, height=2,
                               font=self.button_font, 
                               bg=self.COLOR_BG,
                               fg=self.COLOR_TEXT,
                               activebackground="#202038",
                               activeforeground=self.COLOR_TEXT,
                               command=lambda idx=index: self.on_button_click(idx),
                               relief=tk.FLAT, bd=0)
            button.grid(row=r, column=c, padx=2, pady=2) 
            self.buttons[index] = button

        score_frame = tk.Frame(root, bg=self.COLOR_BG)
        score_frame.pack(pady=5, fill=tk.X, expand=True)
        
        frame_x = tk.Frame(score_frame, bg=self.COLOR_BG)
        frame_x.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(frame_x, text="Player 1 (X)", font=self.score_font_text, fg=self.COLOR_X, bg=self.COLOR_BG).pack()
        self.score_label_x = tk.Label(frame_x, textvariable=self.score_x_var, font=self.score_font_num, fg=self.COLOR_X, bg=self.COLOR_BG)
        self.score_label_x.pack()

        frame_tie = tk.Frame(score_frame, bg=self.COLOR_BG)
        frame_tie.pack(side=tk.LEFT, fill=tk.X, expand=True)
        tk.Label(frame_tie, text="Draws", font=self.score_font_text, fg=self.COLOR_TEXT, bg=self.COLOR_BG).pack()
        self.score_label_ties = tk.Label(frame_tie, textvariable=self.score_ties_var, font=self.score_font_num, fg=self.COLOR_TEXT, bg=self.COLOR_BG)
        self.score_label_ties.pack()
        
        frame_o = tk.Frame(score_frame, bg=self.COLOR_BG)
        frame_o.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.score_label_o_text = tk.Label(frame_o, textvariable=self.score_o_text_var, font=self.score_font_text, fg=self.COLOR_O, bg=self.COLOR_BG)
        self.score_label_o_text.pack()
        self.score_label_o = tk.Label(frame_o, textvariable=self.score_o_var, font=self.score_font_num, fg=self.COLOR_O, bg=self.COLOR_BG)
        self.score_label_o.pack()
        
      
        button_frame = tk.Frame(root, bg=self.COLOR_BG)
        button_frame.pack(pady=10)
        
      
        self.reset_score_button = tk.Button(button_frame, text="Reset Scores", 
                                            command=self.reset_scoreboard,
                                            bg=self.COLOR_X, fg="white", relief=tk.FLAT)
        self.reset_score_button.pack(pady=5, fill=tk.X)
        

        mode_button_frame = tk.Frame(button_frame, bg=self.COLOR_BG)
        mode_button_frame.pack()
        
        self.reset_ai_button = tk.Button(mode_button_frame, text="New Game (vs AI)", 
                                         command=lambda: self.start_new_game("PVE"),
                                         bg="#3E4452", fg=self.COLOR_TEXT, relief=tk.FLAT)
        self.reset_ai_button.pack(side=tk.LEFT, padx=10)
        
        self.reset_pvp_button = tk.Button(mode_button_frame, text="New Game (vs Player 1)", 
                                          command=lambda: self.start_new_game("PVP"),
                                          bg="#3E4452", fg=self.COLOR_TEXT, relief=tk.FLAT)
        self.reset_pvp_button.pack(side=tk.LEFT, padx=10)

        self.creator_label = tk.Label(root, text=f"Made with ❤️ by {creator_name}", 
                                      font=('Arial', 10, 'italic'), 
                                      fg="#ABB2BF", bg=self.COLOR_BG)
        self.creator_label.pack(pady=(0, 10)) 
        
        self.start_new_game(self.game_mode)

 

    def start_new_game(self, mode="PVE"):
        global internal_board
        internal_board = [' '] * 10
        self.game_mode = mode 
        self.current_player = PLAYER_LETTER
        
        for i in range(1, 10):
            if i in self.buttons:
                self.buttons[i].config(text=' ', fg=self.COLOR_TEXT, bg=self.COLOR_BG, state="normal")
        
        self.update_turn_label()
        self.update_scoreboard_labels()
    

    def reset_scoreboard(self):
        self.scores_pve = {"X": 0, "O": 0, "Ties": 0}
        self.scores_pvp = {"X": 0, "O": 0, "Ties": 0}
        self.update_scoreboard_labels() 

 
    def update_scoreboard_labels(self):
        if self.game_mode == "PVE":
            scores_to_show = self.scores_pve
            player_o_label = "AI (O)"
        else: 
            scores_to_show = self.scores_pvp
            player_o_label = "Player 2 (O)"
    
        self.score_x_var.set(str(scores_to_show['X']))
        self.score_o_text_var.set(player_o_label)
        self.score_o_var.set(str(scores_to_show['O']))
        self.score_ties_var.set(str(scores_to_show['Ties']))

    def update_turn_label(self):
        if self.game_mode == "PVP":
            player_name = "Player 1 (X) Turn" if self.current_player == PLAYER_LETTER else "Player 2 (O) Turn"
            color = self.COLOR_X if self.current_player == PLAYER_LETTER else self.COLOR_O
        else: 
            player_name = "Your Turn (X)" if self.current_player == PLAYER_LETTER else "AI's Turn (O)"
            color = self.COLOR_X if self.current_player == PLAYER_LETTER else self.COLOR_O
        
        self.turn_label_var.set(player_name)
        self.turn_label.config(fg=color)

    def on_button_click(self, index):
        global internal_board
        
        if internal_board[index] != ' ': return
        if self.game_mode == "PVE" and self.current_player == AI_LETTER:
            return 

        make_move(internal_board, self.current_player, index)
        color = self.COLOR_X if self.current_player == PLAYER_LETTER else self.COLOR_O
        self.buttons[index].config(text=self.current_player, fg=color, state="disabled", disabledforeground=color)

        winning_combo = is_winner(internal_board, self.current_player)
        if self.check_game_over(self.current_player, winning_combo):
            return

        if self.game_mode == "PVE":
            if self.current_player == PLAYER_LETTER:
                self.current_player = AI_LETTER
                self.update_turn_label()
                self.root.after(500, self.ai_make_move)
        elif self.game_mode == "PVP":
            self.current_player = AI_LETTER if self.current_player == PLAYER_LETTER else PLAYER_LETTER
            self.update_turn_label()

    def ai_make_move(self):
        global internal_board
        if is_board_full(internal_board): return
        
        move = get_ai_move(internal_board)
        
        make_move(internal_board, AI_LETTER, move)
        self.buttons[move].config(text=AI_LETTER, fg=self.COLOR_O, state="disabled", disabledforeground=self.COLOR_O)

        winning_combo = is_winner(internal_board, AI_LETTER)
        if self.check_game_over(AI_LETTER, winning_combo):
            return

        self.current_player = PLAYER_LETTER
        self.update_turn_label()

   
    def check_game_over(self, last_player, winning_combo):
        
       
        current_scores = self.scores_pve if self.game_mode == "PVE" else self.scores_pvp

        if winning_combo:
            self.highlight_winner(winning_combo)
            
            current_scores[last_player] += 1
            
            if self.game_mode == "PVE":
                msg = "Wow! 🎉 You actually won! Congratulations!" if last_player == PLAYER_LETTER else "Oops! 🤖 The AI outsmarted you!"
            else:
                msg = f"Player {last_player} wins! 🎉"
                
            messagebox.showinfo("Game Over", msg)
            self.start_new_game(self.game_mode)
            return True
            
        elif is_board_full(internal_board):
         
            current_scores["Ties"] += 1
            
            messagebox.showinfo("Game Over", "It's a draw! 🤝")
            self.start_new_game(self.game_mode)
            return True
        return False
        
    def highlight_winner(self, combo):
        for index in combo:
            self.buttons[index].config(bg=self.COLOR_WIN, disabledforeground=self.COLOR_TEXT)
        for i in range(1, 10):
            if i in self.buttons:
                self.buttons[i].config(state="disabled")

if __name__ == "__main__":
    main_window = tk.Tk()
    app = TicTacToeApp(main_window, creator_name="Mili Srivastava") 
    main_window.mainloop()