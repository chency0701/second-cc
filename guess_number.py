"""
🎯 猜数字小游戏 - Number Guessing Game
使用 tkinter 实现 GUI 展示，支持难度选择
"""

import tkinter as tk
import random
from tkinter import messagebox


class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 猜数字小游戏")
        self.root.geometry("500x480")
        self.root.configure(bg='#1A1A2E')
        self.root.resizable(False, False)

        # 游戏参数
        self.target_number = 0
        self.guess_count = 0
        self.max_attempts = 10
        self.min_range = 1
        self.max_range = 100
        self.game_active = False

        # 颜色主题
        self.bg_dark = '#1A1A2E'
        self.card_bg = '#16213E'
        self.accent = '#E94560'
        self.gold = '#F0A500'
        self.text_color = '#EEEEEE'
        self.hint_color = '#A8D8EA'
        self.success_color = '#00D2A0'

        self.build_ui()
        self.start_new_game()

    def build_ui(self):
        # ===== 标题 =====
        title_frame = tk.Frame(self.root, bg=self.bg_dark)
        title_frame.pack(pady=(20, 10))

        tk.Label(title_frame, text="🎯", font=('Arial', 48),
                 bg=self.bg_dark).pack()
        tk.Label(title_frame, text="猜 数 字 游 戏",
                 font=('微软雅黑', 22, 'bold'),
                 bg=self.bg_dark, fg=self.gold).pack()

        # ===== 难度选择 =====
        diff_frame = tk.Frame(self.root, bg=self.bg_dark)
        diff_frame.pack(pady=10)

        tk.Label(diff_frame, text="难度：",
                 font=('微软雅黑', 12),
                 bg=self.bg_dark, fg=self.text_color,
                 ).pack(side=tk.LEFT, padx=(0, 10))

        self.difficulty = tk.StringVar(value='普通')
        self.diff_menu = tk.OptionMenu(diff_frame, self.difficulty,
                                        '😊 简单', '🤔 普通', '😈 困难',
                                        command=self.on_difficulty_change)
        self.diff_menu.config(font=('微软雅黑', 11), width=10,
                              bg=self.card_bg, fg=self.text_color,
                              activebackground=self.accent)
        self.diff_menu["menu"].config(bg=self.card_bg, fg=self.text_color,
                                      font=('微软雅黑', 10))
        self.diff_menu.pack(side=tk.LEFT)

        # ===== 信息卡片 =====
        info_frame = tk.Frame(self.root, bg=self.card_bg,
                              highlightbackground='#0F3460',
                              highlightthickness=2)
        info_frame.pack(pady=10, padx=40, fill=tk.X)

        self.info_label = tk.Label(info_frame,
                                    text=f"范围：1 ~ 100\n剩余次数：10",
                                    font=('微软雅黑', 13),
                                    bg=self.card_bg, fg=self.hint_color,
                                    justify=tk.LEFT)
        self.info_label.pack(pady=12, padx=20)

        # ===== 输入区域 =====
        input_frame = tk.Frame(self.root, bg=self.bg_dark)
        input_frame.pack(pady=10)

        self.entry = tk.Entry(input_frame, font=('Arial', 20, 'bold'),
                               width=10, justify='center',
                               bg=self.card_bg, fg='white',
                               insertbackground='white',
                               relief=tk.FLAT,
                               highlightbackground='#0F3460',
                               highlightthickness=2)
        self.entry.pack(pady=5)
        self.entry.bind('<Return>', lambda e: self.make_guess())
        self.entry.focus_set()

        # ===== 按钮区域 =====
        btn_frame = tk.Frame(self.root, bg=self.bg_dark)
        btn_frame.pack(pady=10)

        guess_btn = tk.Button(btn_frame, text="🎲 猜测",
                              command=self.make_guess,
                              font=('微软雅黑', 14, 'bold'),
                              bg=self.accent, fg='white',
                              activebackground='#FF6B7A',
                              relief=tk.FLAT,
                              padx=30, pady=8,
                              cursor='hand2')
        guess_btn.pack(side=tk.LEFT, padx=5)

        restart_btn = tk.Button(btn_frame, text="🔄 重新开始",
                                command=self.start_new_game,
                                font=('微软雅黑', 14, 'bold'),
                                bg='#0F3460', fg='white',
                                activebackground='#1A4A80',
                                relief=tk.FLAT,
                                padx=20, pady=8,
                                cursor='hand2')
        restart_btn.pack(side=tk.LEFT, padx=5)

        # ===== 提示标签 =====
        self.hint_label = tk.Label(self.root, text="",
                                    font=('微软雅黑', 13, 'bold'),
                                    bg=self.bg_dark, fg=self.hint_color)
        self.hint_label.pack(pady=5)

        # ===== 历史记录 =====
        history_frame = tk.Frame(self.root, bg=self.card_bg,
                                 highlightbackground='#0F3460',
                                 highlightthickness=1)
        history_frame.pack(pady=10, padx=40, fill=tk.X)

        tk.Label(history_frame, text="📝 猜测记录",
                 font=('微软雅黑', 11, 'bold'),
                 bg=self.card_bg, fg='#AAA').pack(pady=(8, 4))

        self.history_text = tk.Label(history_frame, text="还没有猜测",
                                      font=('Consolas', 10),
                                      bg=self.card_bg, fg='#888',
                                      wraplength=380)
        self.history_text.pack(pady=(0, 8), padx=15)

        # ===== 底部提示 =====
        tk.Label(self.root, text="按 Enter 键快速猜测",
                 font=('微软雅黑', 9),
                 bg=self.bg_dark, fg='#555').pack(side=tk.BOTTOM, pady=10)

    def on_difficulty_change(self, choice):
        self.start_new_game()

    def start_new_game(self):
        """开始新一局游戏"""
        diff = self.difficulty.get()

        if '简单' in diff:
            self.min_range = 1
            self.max_range = 50
            self.max_attempts = 12
        elif '普通' in diff:
            self.min_range = 1
            self.max_range = 100
            self.max_attempts = 10
        else:
            self.min_range = 1
            self.max_range = 200
            self.max_attempts = 8

        self.target_number = random.randint(self.min_range, self.max_range)
        self.guess_count = 0
        self.game_active = True
        self.guess_history = []

        print(f"[DEBUG] 正确答案是: {self.target_number}")

        self.info_label.config(
            text=f"范围：{self.min_range} ~ {self.max_range}\n"
                 f"剩余次数：{self.max_attempts}"
        )
        self.hint_label.config(text="我已经想好数字了，来猜猜看吧！😄",
                               fg=self.hint_color)
        self.history_text.config(text="还没有猜测")
        self.entry.delete(0, tk.END)
        self.entry.config(state=tk.NORMAL)
        self.entry.focus_set()

    def make_guess(self):
        """处理猜测"""
        if not self.game_active:
            return

        guess_str = self.entry.get().strip()

        # 输入验证
        if not guess_str:
            self.hint_label.config(text="请输入一个数字！", fg='#FFA500')
            self.entry.delete(0, tk.END)
            return

        try:
            guess = int(guess_str)
        except ValueError:
            self.hint_label.config(text="⚠️ 请输入有效的整数！", fg='#FFA500')
            self.entry.delete(0, tk.END)
            return

        if guess < self.min_range or guess > self.max_range:
            self.hint_label.config(
                text=f"⚠️ 数字应在 {self.min_range} ~ {self.max_range} 之间！",
                fg='#FFA500'
            )
            self.entry.delete(0, tk.END)
            return

        # 处理猜测
        self.guess_count += 1
        self.guess_history.append(guess)
        remaining = self.max_attempts - self.guess_count

        if guess == self.target_number:
            self.game_won()
            return

        if self.guess_count >= self.max_attempts:
            self.game_lost()
            return

        # 提示
        if guess < self.target_number:
            diff_text = "太小了"
            if self.target_number - guess <= 5:
                diff_text += "，但很接近了！🔥"
            elif self.target_number - guess <= 15:
                diff_text += " 📈"
            self.hint_label.config(text=f"📉 {guess} —— {diff_text}",
                                   fg='#FF6B6B')
        else:
            diff_text = "太大了"
            if guess - self.target_number <= 5:
                diff_text += "，但很接近了！🔥"
            elif guess - self.target_number <= 15:
                diff_text += " 📉"
            self.hint_label.config(text=f"📈 {guess} —— {diff_text}",
                                   fg='#6BCBFF')

        self.info_label.config(
            text=f"范围：{self.min_range} ~ {self.max_range}\n"
                 f"剩余次数：{remaining}"
        )

        # 更新历史记录
        history_display = " ← ".join(str(h) for h in self.guess_history)
        if len(history_display) > 55:
            recent = self.guess_history[-6:]
            history_display = "… ← ".join(str(h) for h in recent)
        self.history_text.config(text=history_display)

        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def game_won(self):
        """赢得游戏"""
        self.game_active = False
        self.entry.config(state=tk.DISABLED)

        msg = (
            f"🎉 太厉害了！\n\n"
            f"你猜中了：{self.target_number}\n"
            f"用了 {self.guess_count} 次猜测！"
        )

        if self.guess_count == 1:
            rating = "🏆 一发入魂！你简直是神！"
        elif self.guess_count <= 3:
            rating = "🥇 非常聪明！"
        elif self.guess_count <= 6:
            rating = "🥈 表现不错！"
        else:
            rating = "🥉 猜到了就好！"

        self.hint_label.config(text=rating, fg=self.success_color)
        self.info_label.config(
            text=f"🎯 答案就是：{self.target_number}\n"
                 f"猜测次数：{self.guess_count}/{self.max_attempts}"
        )

        history_display = " ← ".join(str(h) for h in self.guess_history)
        if len(history_display) > 55:
            recent = self.guess_history[-6:]
            history_display = "… ← ".join(str(h) for h in recent)
        self.history_text.config(text=history_display)

        messagebox.showinfo("🎉 恭喜！", msg)

    def game_lost(self):
        """输掉游戏"""
        self.game_active = False
        self.entry.config(state=tk.DISABLED)

        self.hint_label.config(
            text=f"😢 答案是 {self.target_number}，再试一次吧！",
            fg='#FF6B6B'
        )
        self.info_label.config(
            text=f"💔 游戏结束\n正确答案：{self.target_number}"
        )

        history_display = " ← ".join(str(h) for h in self.guess_history)
        if len(history_display) > 55:
            recent = self.guess_history[-6:]
            history_display = "… ← ".join(str(h) for h in recent)
        self.history_text.config(text=history_display)

        messagebox.showinfo("😢 游戏结束",
                            f"你没有猜中！\n正确答案是：{self.target_number}")


if __name__ == '__main__':
    root = tk.Tk()
    app = GuessNumberGame(root)
    root.mainloop()