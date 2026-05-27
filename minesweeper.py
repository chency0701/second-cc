import tkinter as tk
from tkinter import messagebox
import random
import time


class Minesweeper:
    LEVELS = {
        '初级': (9, 9, 10),
        '中级': (16, 16, 40),
        '高级': (25, 40, 156),
    }

    COLORS = {
        1: '#0000FF',
        2: '#008000',
        3: '#FF0000',
        4: '#000080',
        5: '#800000',
        6: '#008080',
        7: '#000000',
        8: '#808080',
    }

    def __init__(self, root):
        self.root = root
        self.root.title('扫雷')
        self.root.resizable(False, False)

        self.rows = 0
        self.cols = 0
        self.mine_count = 0
        self.flags = 0
        self.revealed = 0
        self.total_safe = 0
        self.first_click = True
        self.game_over = False
        self.timer_running = False
        self.start_time = 0
        self.elapsed = 0

        self.board = []
        self.mines = set()
        self.buttons = []
        self.flagged = set()

        self._build_ui()
        self._new_game('初级')

    def _build_ui(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        tk.Label(top_frame, text='难度:').pack(side=tk.LEFT, padx=5)
        self.level_var = tk.StringVar(value='初级')
        level_menu = tk.OptionMenu(top_frame, self.level_var, *self.LEVELS.keys(),
                                   command=lambda _: self._new_game(self.level_var.get()))
        level_menu.pack(side=tk.LEFT, padx=5)

        self.mine_label = tk.Label(top_frame, text='💣 10', font=('Arial', 14, 'bold'))
        self.mine_label.pack(side=tk.LEFT, padx=20)

        self.timer_label = tk.Label(top_frame, text='⏱ 000', font=('Arial', 14, 'bold'))
        self.timer_label.pack(side=tk.LEFT, padx=20)

        restart_btn = tk.Button(top_frame, text='😊', font=('Arial', 16),
                                command=lambda: self._new_game(self.level_var.get()),
                                width=3, height=1)
        restart_btn.pack(side=tk.LEFT, padx=20)

        self.canvas_frame = tk.Frame(self.root)
        self.canvas_frame.pack(padx=10, pady=10)

    def _new_game(self, level):
        self.rows, self.cols, self.mine_count = self.LEVELS[level]

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        self.board = [[0] * self.cols for _ in range(self.rows)]
        self.mines = set()
        self.buttons = [[None] * self.cols for _ in range(self.rows)]
        self.flagged = set()
        self.flags = 0
        self.revealed = 0
        self.total_safe = self.rows * self.cols - self.mine_count
        self.first_click = True
        self.game_over = False
        self.timer_running = False
        self.start_time = 0
        self.elapsed = 0

        self._update_mine_label()
        self._update_timer_label()

        cell_size = 28
        self.canvas_frame.config(width=self.cols * cell_size, height=self.rows * cell_size)

        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.canvas_frame,
                    width=2, height=1,
                    font=('Arial', 11, 'bold'),
                    relief=tk.RAISED,
                    bg='#C0C0C0',
                    activebackground='#D0D0D0',
                )
                btn.grid(row=r, column=c, sticky='nsew')
                btn.bind('<Button-1>', lambda e, rr=r, cc=c: self._left_click(rr, cc))
                btn.bind('<Button-3>', lambda e, rr=r, cc=c: self._right_click(rr, cc))
                self.buttons[r][c] = btn

    def _generate_mines(self, safe_r, safe_c):
        positions = [(r, c) for r in range(self.rows) for c in range(self.cols)
                     if (r, c) != (safe_r, safe_c)]
        mine_positions = random.sample(positions, self.mine_count)
        self.mines = set(mine_positions)

        for r, c in self.mines:
            self.board[r][c] = -1

        for r, c in self.mines:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] != -1:
                        self.board[nr][nc] += 1

    def _start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            self.start_time = time.time()
            self._tick()

    def _tick(self):
        if not self.timer_running:
            return
        self.elapsed = int(time.time() - self.start_time)
        self._update_timer_label()
        if self.elapsed < 999 and not self.game_over:
            self.root.after(200, self._tick)

    def _update_timer_label(self):
        self.timer_label.config(text=f'⏱ {self.elapsed:03d}')

    def _update_mine_label(self):
        remaining = self.mine_count - self.flags
        self.mine_label.config(text=f'💣 {remaining}')

    def _left_click(self, r, c):
        if self.game_over:
            return
        if (r, c) in self.flagged:
            return
        if self.buttons[r][c]['state'] == tk.DISABLED:
            return

        if self.first_click:
            self._generate_mines(r, c)
            self.first_click = False
            self._start_timer()

        if (r, c) in self.mines:
            self._game_lose(r, c)
            return

        self._reveal(r, c)
        if self.revealed >= self.total_safe:
            self._game_win()

    def _reveal(self, r, c):
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return
        if self.buttons[r][c]['state'] == tk.DISABLED:
            return
        if (r, c) in self.flagged:
            return

        btn = self.buttons[r][c]
        btn.config(state=tk.DISABLED, relief=tk.SUNKEN, bg='#D0D0D0',
                   activebackground='#D0D0D0')
        self.revealed += 1

        if self.board[r][c] > 0:
            btn.config(text=str(self.board[r][c]),
                       fg=self.COLORS.get(self.board[r][c], '#000000'),
                       disabledforeground=self.COLORS.get(self.board[r][c], '#000000'))
        elif self.board[r][c] == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    self._reveal(r + dr, c + dc)

    def _right_click(self, r, c):
        if self.game_over:
            return
        if self.first_click:
            return
        if self.buttons[r][c]['state'] == tk.DISABLED:
            return

        btn = self.buttons[r][c]
        if (r, c) in self.flagged:
            self.flagged.remove((r, c))
            self.flags -= 1
            btn.config(text='')
            self._update_mine_label()
        elif self.flags < self.mine_count:
            self.flagged.add((r, c))
            self.flags += 1
            btn.config(text='🚩')
            self._update_mine_label()

    def _game_lose(self, clicked_r, clicked_c):
        self.game_over = True
        self.timer_running = False

        for r, c in self.mines:
            btn = self.buttons[r][c]
            if (r, c) == (clicked_r, clicked_c):
                btn.config(text='💥', bg='#FF0000', state=tk.DISABLED, relief=tk.SUNKEN)
            elif (r, c) in self.flagged:
                continue
            else:
                btn.config(text='💣', state=tk.DISABLED, relief=tk.SUNKEN)

        for r, c in self.flagged:
            if (r, c) not in self.mines:
                self.buttons[r][c].config(text='❌', state=tk.DISABLED, relief=tk.SUNKEN)

        self.root.after(500, lambda: messagebox.showinfo('游戏结束', '你踩到地雷了！'))

    def _game_win(self):
        self.game_over = True
        self.timer_running = False

        for r, c in self.mines:
            if (r, c) not in self.flagged:
                self.buttons[r][c].config(text='🚩')
                self.flags += 1
        self._update_mine_label()

        self.root.after(300, lambda: messagebox.showinfo('恭喜', 
            f'你赢了！\n用时: {self.elapsed} 秒'))


if __name__ == '__main__':
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
