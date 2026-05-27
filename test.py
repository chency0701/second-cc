"""
🐶 毛茸茸的边牧小狗 - A Fluffy Border Collie Puppy
使用 tkinter 实现 GUI 展示
"""

import tkinter as tk
import math
import random


# ===== 边牧配色 =====
BC_BLACK = '#252525'
BC_BLACK_SOFT = '#2E2E2E'
WHITE = '#FEFEFE'
CREAM = '#FFFCF7'
INNER_EAR = '#EDB8B8'
NOSE_COLOR = '#151515'
EYE_DARK = '#2C1808'
COLLAR_RED = '#D84040'
COLLAR_GOLD = '#F0C040'
TONGUE_PINK = '#FF8899'
PAW_PINK = '#FFB5AB'
BLUSH_PINK = '#FFBBC8'
OUTLINE = '#1A1A1A'
FUR_TUFT = '#2C2C2C'


class AnimatedPuppy:
    def __init__(self, root):
        self.root = root
        self.root.title("🐶 毛茸茸的边牧小狗 - Fluffy Border Collie")
        self.root.geometry("600x650")
        self.root.configure(bg='#E8F0E8')
        self.root.resizable(False, False)

        self.time = 0
        self.bounce_offset = 0
        self.tail_angle = 0
        self.blink_timer = 0
        self.tongue_out = False
        self.tongue_timer = 0
        self.ear_wiggle = 0
        self.eye_look_x = 0
        self.eye_look_y = 0
        self.sparkle_timer = 0
        self.is_blinking = False
        self.sparkle_x = 0
        self.sparkle_y = 0

        self.canvas = tk.Canvas(root, width=600, height=550, bg='#E8F0E8',
                                highlightthickness=0)
        self.canvas.pack(pady=10)

        self.label = tk.Label(root, text="🐾 摸摸小狗的头吧！🐾",
                              font=('微软雅黑', 16, 'bold'),
                              bg='#E8F0E8', fg='#5A7A5A')
        self.label.pack(pady=5)

        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_click)

        self.animate()

    def on_mouse_move(self, event):
        dx = event.x - 300
        dy = event.y - 275
        max_offset = 6
        dist = math.sqrt(dx ** 2 + dy ** 2)
        if dist > 0:
            scale = min(max_offset / dist, max_offset / 30)
            self.eye_look_x = dx * scale
            self.eye_look_y = dy * scale

    def on_click(self, event):
        self.bounce_offset = -40
        self.tongue_out = True
        self.tongue_timer = 30
        self.sparkle_timer = 15
        self.sparkle_x = event.x
        self.sparkle_y = event.y

    # ------------------------------------------------------------------
    #   fluffy helpers
    # ------------------------------------------------------------------

    def _fur_tufts(self, cx, cy, rx, ry, color, count=14):
        """在椭圆边缘画一圈毛茸茸的小凸起"""
        for i in range(count):
            base = (i / count) * 2 * math.pi
            jitter = math.sin(i * 2.3) * 0.25 + math.cos(i * 4.7) * 0.18
            angle = base + jitter
            size = 4 + math.sin(i * 3.1) * 2.5
            ex = cx + math.cos(angle) * rx
            ey = cy + math.sin(angle) * ry
            ox = ex + math.cos(angle) * size * 0.55
            oy = ey + math.sin(angle) * size * 0.55
            self.canvas.create_oval(ox - size, oy - size,
                                    ox + size, oy + size,
                                    fill=color, outline='')

    def _fluffy_oval(self, cx, cy, rx, ry, color, tuft_color=None,
                     count=14, outline=''):
        """画一个带毛边的椭圆"""
        self.canvas.create_oval(cx - rx, cy - ry, cx + rx, cy + ry,
                                fill=color, outline=outline)
        tc = tuft_color if tuft_color else color
        self._fur_tufts(cx, cy, rx - 2, ry - 2, tc, count)

    def _draw_leg(self, x, y_top, y_bottom, upper_color, sock_color,
                  sock_ratio=0.35, width=18):
        """画一条腿：上部 + 白色袜子 + 爪子"""
        leg_h = y_bottom - y_top
        sock_h = leg_h * sock_ratio
        upper_h = leg_h - sock_h
        sock_top = y_top + upper_h

        # 上段
        self.canvas.create_oval(x - width, y_top,
                                x + width, sock_top + 4,
                                fill=upper_color, outline='')
        # 白袜子
        self.canvas.create_oval(x - width + 1, sock_top - 2,
                                x + width + 1, y_bottom - 2,
                                fill=sock_color, outline='')
        # 爪爪
        paw_w = width + 4
        self.canvas.create_oval(x - paw_w, y_bottom - 8,
                                x + paw_w, y_bottom + 6,
                                fill=sock_color, outline='')
        # 肉垫
        for px in [x - 5, x + 5]:
            self.canvas.create_oval(px - 4, y_bottom - 4,
                                    px + 4, y_bottom + 4,
                                    fill=PAW_PINK, outline='')
        self.canvas.create_oval(x - 5, y_bottom - 6,
                                x + 5, y_bottom + 2,
                                fill=PAW_PINK, outline='')

    def draw_heart(self, x, y, size, color='#FF6B8A'):
        points = []
        for angle in range(0, 360, 5):
            rad = math.radians(angle)
            px = 16 * math.sin(rad) ** 3
            py = -(13 * math.cos(rad) - 5 * math.cos(2 * rad)
                   - 2 * math.cos(3 * rad) - math.cos(4 * rad))
            points.append(x + px * size / 16)
            points.append(y + py * size / 16)
        if len(points) >= 4:
            self.canvas.create_polygon(points, fill=color, outline='')

    # ------------------------------------------------------------------
    #   main drawing
    # ------------------------------------------------------------------

    def draw_puppy(self):
        self.canvas.delete("all")

        t = self.time
        bounce = self.bounce_offset

        # ===== 背景草地 =====
        for i in range(14):
            gx = 20 + i * 45
            gy = 505 + math.sin(t * 0.04 + i * 0.7) * 4
            blade_h = 12 + math.sin(i * 1.8) * 6
            self.canvas.create_line(gx, 520, gx + math.sin(i) * 4,
                                    gy - blade_h,
                                    fill='#A8C8A0', width=2)
        # 小花
        for i in range(5):
            fx = 70 + i * 115 + math.sin(i * 2.1) * 20
            fy = 470 + math.cos(i * 1.7) * 8
            for pi in range(5):
                a = math.radians(pi * 72)
                ps = 3
                self.canvas.create_oval(fx + math.cos(a) * ps - 2,
                                        fy + math.sin(a) * ps - 2,
                                        fx + math.cos(a) * ps + 2,
                                        fy + math.sin(a) * ps + 2,
                                        fill='#FFFDF5', outline='')
            self.canvas.create_oval(fx - 2, fy - 2, fx + 2, fy + 2,
                                    fill='#FFEE88', outline='')

        # ===== 地面阴影 =====
        shadow_y = 500 + abs(bounce) * 0.12
        shadow_w = 130 - abs(bounce) * 0.5
        self.canvas.create_oval(300 - shadow_w / 2, shadow_y - 4,
                                300 + shadow_w / 2, shadow_y + 4,
                                fill='#C0CFC0', outline='')

        # ===== 身体 =====
        body_x, body_y = 300, 388 + bounce
        body_rx, body_ry = 58, 40

        self._fluffy_oval(body_x, body_y, body_rx, body_ry,
                          BC_BLACK, FUR_TUFT, count=16)

        # 白色胸腹毛
        chest_y = body_y + 4
        self.canvas.create_oval(body_x - 32, chest_y - 18,
                                body_x + 32, chest_y + 28,
                                fill=WHITE, outline='')
        self._fur_tufts(body_x, chest_y + 5, 28, 22, CREAM, count=10)

        # ===== 后腿（在身体后面，先画）=====
        for lx in [body_x - 35, body_x + 35]:
            self._draw_leg(lx, body_y + 10, 495,
                           BC_BLACK, WHITE, sock_ratio=0.3, width=16)

        # ===== 尾巴 =====
        tail_base_x = body_x + 52
        tail_base_y = body_y - 8
        self.tail_angle = math.sin(t * 0.12) * 22 + 8
        tail_wag = math.sin(t * 0.18) * 7
        angle_rad = math.radians(self.tail_angle + tail_wag)
        tail_len = 50

        # 毛茸茸的尾巴：用多个重叠椭圆
        for seg in range(5):
            frac = (seg + 1) / 5
            sx = tail_base_x + math.cos(angle_rad) * tail_len * frac
            sy = tail_base_y - math.sin(angle_rad) * tail_len * frac - frac * 10
            seg_w = 14 - frac * 1.5
            seg_h = 8 - frac * 0.5
            tail_color = WHITE if frac > 0.55 else BC_BLACK
            self.canvas.create_oval(sx - seg_w, sy - seg_h,
                                    sx + seg_w, sy + seg_h,
                                    fill=tail_color, outline='')
            # 绒毛（用确定性计算，避免每帧抖动）
            for j in range(3):
                tx = sx + math.sin(seg * 7.3 + j * 2.1) * 5
                ty = sy + math.cos(seg * 5.7 + j * 3.1) * 4
                ts = 3 + math.sin(seg * 4.1 + j) * 1.5
                self.canvas.create_oval(tx - ts, ty - ts, tx + ts, ty + ts,
                                        fill=tail_color, outline='')
        # 尾巴末端白色绒毛球
        tip_x = tail_base_x + math.cos(angle_rad) * tail_len
        tip_y = tail_base_y - math.sin(angle_rad) * tail_len - 10
        self.canvas.create_oval(tip_x - 10, tip_y - 8, tip_x + 10, tip_y + 8,
                                fill=WHITE, outline='')
        self._fur_tufts(tip_x, tip_y, 6, 5, CREAM, count=6)

        # ===== 前腿（在身体前面）=====
        for lx in [body_x - 24, body_x + 24]:
            self._draw_leg(lx, body_y + 6, 495,
                           BC_BLACK, WHITE, sock_ratio=0.32, width=18)

        # ===== 颈部毛茸茸的白色围脖 =====
        ruff_y = body_y - 25
        for i in range(7):
            ra = math.radians(-60 + i * 20)
            rx = body_x + math.cos(ra) * 32
            ry = ruff_y + math.sin(ra) * 18
            rs = 9 + math.sin(i * 1.4) * 4
            self.canvas.create_oval(rx - rs, ry - rs, rx + rs, ry + rs,
                                    fill=WHITE, outline='')
        # 更多围脖绒毛
        for i in range(5):
            ra = math.radians(-40 + i * 20)
            rx = body_x + math.cos(ra) * 38
            ry = ruff_y + math.sin(ra) * 14
            self.canvas.create_oval(rx - 7, ry - 7, rx + 7, ry + 7,
                                    fill=CREAM, outline='')

        # ===== 头部 =====
        head_x = body_x
        head_y = body_y - 55 + bounce * 0.5
        head_rx, head_ry = 50, 46

        # 头部黑色底
        self._fluffy_oval(head_x, head_y, head_rx, head_ry,
                          BC_BLACK, FUR_TUFT, count=16)

        # 白色脸纹（边牧标志性的额头到鼻梁的白条纹 + 白嘴）
        blaze_top = head_y - 25
        blaze_bottom = head_y + 30
        blaze_mid_y = head_y + 5

        blaze_points = [
            head_x - 8, blaze_top,          # 额头窄
            head_x + 8, blaze_top,
            head_x + 18, blaze_mid_y,        # 中间展开
            head_x + 24, blaze_bottom - 5,   # 嘴部宽
            head_x - 24, blaze_bottom - 5,
            head_x - 18, blaze_mid_y,
        ]
        self.canvas.create_polygon(blaze_points, fill=WHITE,
                                   outline='', smooth=True)

        # 嘴部白色区域
        self.canvas.create_oval(head_x - 24, head_y + 10,
                                head_x + 24, head_y + 40,
                                fill=WHITE, outline='')

        # ===== 耳朵（边牧的立耳，尖尖的三角形）=====
        self.ear_wiggle = math.sin(t * 0.15) * 3

        for side, sign in [('left', -1), ('right', 1)]:
            # 耳朵基部在头顶两侧
            ear_left_x = head_x + sign * 15
            ear_right_x = head_x + sign * 40
            ear_base_y = head_y - 35
            wiggle = self.ear_wiggle if side == 'left' else -self.ear_wiggle

            # 外耳 - 尖三角形
            ear_points = [
                ear_left_x, ear_base_y,
                head_x + sign * 50, ear_base_y - 52 + wiggle,
                ear_right_x, ear_base_y,
            ]
            self.canvas.create_polygon(ear_points, fill=BC_BLACK,
                                       outline='')

            # 耳朵尖端绒毛
            tip_x = head_x + sign * 50
            tip_y = ear_base_y - 52 + wiggle
            self.canvas.create_oval(tip_x - 5, tip_y - 4,
                                    tip_x + 5, tip_y + 4,
                                    fill=BC_BLACK, outline='')

            # 内耳粉色
            inner_points = [
                head_x + sign * 19, ear_base_y - 2,
                head_x + sign * 42, ear_base_y - 38 + wiggle,
                head_x + sign * 35, ear_base_y - 2,
            ]
            self.canvas.create_polygon(inner_points, fill=INNER_EAR,
                                       outline='')

        # ===== 眼睛 =====
        eye_left_x = head_x - 20 + self.eye_look_x
        eye_left_y = head_y - 6 + self.eye_look_y
        eye_right_x = head_x + 20 + self.eye_look_x
        eye_right_y = head_y - 6 + self.eye_look_y

        self.blink_timer -= 1
        if self.blink_timer <= 0:
            self.blink_timer = random.randint(40, 100)
            self.is_blinking = True
        elif self.blink_timer <= 4:
            self.is_blinking = True
        else:
            self.is_blinking = False

        for ex, ey in [(eye_left_x, eye_left_y), (eye_right_x, eye_right_y)]:
            # 眼眶（白色底）
            self.canvas.create_oval(ex - 12, ey - 12, ex + 12, ey + 12,
                                    fill='white', outline=OUTLINE, width=1.5)
            if self.is_blinking:
                self.canvas.create_line(ex - 12, ey, ex + 12, ey,
                                        fill=OUTLINE, width=2.5)
            else:
                # 瞳孔
                self.canvas.create_oval(ex - 5, ey - 5, ex + 5, ey + 5,
                                        fill=EYE_DARK, outline='')
                # 高光
                self.canvas.create_oval(ex - 3, ey - 5, ex + 1, ey - 2,
                                        fill='white', outline='')
                self.canvas.create_oval(ex + 2, ey + 1, ex + 4.5, ey + 3.5,
                                        fill='white', outline='')

        # 白色"眉毛"（边牧特征）
        for bx, by in [(head_x - 24, head_y - 16),
                       (head_x + 24, head_y - 16)]:
            self.canvas.create_oval(bx - 5, by - 3, bx + 5, by + 3,
                                    fill=CREAM, outline='')

        # ===== 鼻子 =====
        nose_y = head_y + 12
        self.canvas.create_oval(head_x - 10, nose_y - 7,
                                head_x + 10, nose_y + 7,
                                fill=NOSE_COLOR, outline='')
        # 鼻子高光
        self.canvas.create_oval(head_x - 4, nose_y - 5,
                                head_x + 1, nose_y - 1,
                                fill='#4A4A4A', outline='')
        self.canvas.create_oval(head_x - 5, nose_y - 6,
                                head_x - 2, nose_y - 3,
                                fill='#6A6A6A', outline='')

        # ===== 嘴巴 =====
        mouth_y = nose_y + 7
        # 嘴线
        self.canvas.create_arc(head_x - 18, mouth_y - 3,
                               head_x + 18, mouth_y + 14,
                               start=0, extent=-180,
                               style=tk.ARC, outline='#555', width=1.8)
        # 人中
        self.canvas.create_line(head_x, nose_y + 6,
                                head_x, mouth_y + 1,
                                fill='#555', width=1.5)

        # ===== 舌头 =====
        if self.tongue_out:
            self.tongue_timer -= 1
            tongue_y = mouth_y + 4
            tongue_progress = min(self.tongue_timer / 10, 1.0)
            if tongue_progress > 0:
                tongue_len = 15 * tongue_progress
                self.canvas.create_oval(head_x - 7, tongue_y,
                                        head_x + 7, tongue_y + tongue_len,
                                        fill=TONGUE_PINK, outline='#D06070',
                                        width=1.5)
                self.canvas.create_line(head_x, tongue_y + 2,
                                        head_x, tongue_y + tongue_len - 3,
                                        fill='#D06070', width=1.5)
            if self.tongue_timer <= 0:
                self.tongue_out = False

        # ===== 腮红 =====
        for bx, by in [(head_x - 27, head_y + 14),
                       (head_x + 27, head_y + 14)]:
            self.canvas.create_oval(bx - 9, by - 4, bx + 9, by + 4,
                                    fill=BLUSH_PINK, outline='')

        # ===== 项圈 =====
        collar_y = body_y - 30
        self.canvas.create_line(head_x - 34, collar_y,
                                head_x + 34, collar_y,
                                fill=COLLAR_RED, width=5)
        # 吊牌
        tag_x = head_x + 37
        tag_y = collar_y + 2
        self.canvas.create_oval(tag_x - 6, tag_y - 6, tag_x + 6, tag_y + 6,
                                fill=COLLAR_GOLD, outline='#C09020', width=1.5)
        self.canvas.create_oval(tag_x - 3, tag_y - 3, tag_x + 3, tag_y + 3,
                                fill='#FFF8DC', outline='')

        # ===== 点击爱心特效 =====
        if self.sparkle_timer > 0:
            self.sparkle_timer -= 1
            for i in range(5):
                angle = math.radians(i * 72 + self.sparkle_timer * 10)
                dist = (15 - self.sparkle_timer) * 2
                sx = self.sparkle_x + math.cos(angle) * dist
                sy = self.sparkle_y + math.sin(angle) * dist
                size = max(2, (15 - self.sparkle_timer) * 0.4)
                self.canvas.create_oval(sx - size, sy - size,
                                        sx + size, sy + size,
                                        fill='#FFD700', outline='')
            heart_size = (15 - self.sparkle_timer) * 2
            if heart_size > 0:
                self.draw_heart(self.sparkle_x, self.sparkle_y,
                                heart_size, '#FF6B8A')

    # ------------------------------------------------------------------
    #   animation
    # ------------------------------------------------------------------

    def animate(self):
        self.time += 1

        if self.bounce_offset < 0:
            self.bounce_offset += 2
            if self.bounce_offset > 0:
                self.bounce_offset = 0

        if random.random() < 0.01 and self.bounce_offset == 0:
            self.bounce_offset = -12

        self.draw_puppy()
        self.root.after(40, self.animate)


if __name__ == '__main__':
    root = tk.Tk()
    app = AnimatedPuppy(root)
    root.mainloop()
