"""
타자 게임: 산성비, 침략자, 자원 캐기, 케이크 던지기, 해상 구조 SOS
"""
import tkinter as tk
from tkinter import ttk
import random
import time


class BaseGame(tk.Frame):
    """게임 기본 클래스"""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        self.score = 0
        self.is_running = False

    def create_widgets(self):
        """위젯 생성 - 하위 클래스에서 오버라이드"""
        pass


class AcidRainGame(BaseGame):
    """산성비 게임 - 떨어지는 단어를 타이핑하여 제거"""

    WORDS = [
        '사과', '바나나', '포도', '수박', '딸기', '키위', '오렌지', '망고',
        'apple', 'banana', 'grape', 'water', 'melon', 'orange', 'kiwi', 'mango',
        '컴퓨터', '키보드', '마우스', '모니터', '프린터',
        'computer', 'keyboard', 'mouse', 'monitor', 'printer'
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.falling_words = []  # [(word, x, y, speed, id)]
        self.lives = 3
        self.level = 1
        self.create_widgets()

    def create_widgets(self):
        # 제목
        title_label = tk.Label(self, text="산성비 게임", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 정보 표시
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=5)

        self.score_label = tk.Label(info_frame, text="점수: 0", font=('맑은 고딕', 12))
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.lives_label = tk.Label(info_frame, text="생명: ♥♥♥", font=('맑은 고딕', 12), fg='red')
        self.lives_label.pack(side=tk.LEFT, padx=10)

        self.level_label = tk.Label(info_frame, text="레벨: 1", font=('맑은 고딕', 12))
        self.level_label.pack(side=tk.LEFT, padx=10)

        # 게임 캔버스
        self.canvas = tk.Canvas(self, width=600, height=400, bg='#87CEEB')
        self.canvas.pack(pady=10)

        # 바닥선
        self.canvas.create_line(0, 380, 600, 380, fill='brown', width=3)

        # 입력 필드
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 14), justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.check_input)

        # 버튼
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        self.start_button = ttk.Button(button_frame, text="게임 시작", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="중지", command=self.stop_game).pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """게임 시작"""
        self.is_running = True
        self.score = 0
        self.lives = 3
        self.level = 1
        self.falling_words = []
        self.canvas.delete("word")

        self.update_display()
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

        self.spawn_word()
        self.update_game()

    def stop_game(self):
        """게임 중지"""
        self.is_running = False

    def spawn_word(self):
        """새 단어 생성"""
        if not self.is_running:
            return

        word = random.choice(self.WORDS)
        x = random.randint(50, 550)
        y = 10
        speed = 1 + (self.level - 1) * 0.5

        text_id = self.canvas.create_text(
            x, y,
            text=word,
            font=('맑은 고딕', 14, 'bold'),
            fill='red',
            tags="word"
        )

        self.falling_words.append([word, x, y, speed, text_id])

        # 다음 단어 생성 (레벨에 따라 간격 조정)
        delay = max(1000 - (self.level - 1) * 100, 500)
        self.after(delay, self.spawn_word)

    def update_game(self):
        """게임 업데이트"""
        if not self.is_running:
            return

        # 단어들 이동
        words_to_remove = []
        for i, word_data in enumerate(self.falling_words):
            word, x, y, speed, text_id = word_data
            y += speed

            if y >= 380:
                # 바닥에 도달
                self.canvas.delete(text_id)
                words_to_remove.append(i)
                self.lives -= 1
                self.update_display()

                if self.lives <= 0:
                    self.game_over()
                    return
            else:
                # 위치 업데이트
                self.canvas.coords(text_id, x, y)
                word_data[2] = y

        # 제거할 단어들 삭제
        for i in reversed(words_to_remove):
            del self.falling_words[i]

        # 레벨업 체크
        if self.score >= self.level * 10:
            self.level += 1
            self.update_display()

        # 다음 프레임
        self.after(50, self.update_game)

    def check_input(self, event):
        """입력 확인"""
        typed = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not typed:
            return

        # 일치하는 단어 찾기
        for i, word_data in enumerate(self.falling_words):
            word, x, y, speed, text_id = word_data
            if word == typed:
                # 맞춤!
                self.canvas.delete(text_id)
                del self.falling_words[i]
                self.score += 1
                self.update_display()
                break

    def update_display(self):
        """화면 업데이트"""
        self.score_label.config(text=f"점수: {self.score}")
        self.lives_label.config(text=f"생명: {'♥' * self.lives}")
        self.level_label.config(text=f"레벨: {self.level}")

    def game_over(self):
        """게임 오버"""
        self.is_running = False
        self.canvas.create_text(
            300, 200,
            text=f"게임 오버!\n최종 점수: {self.score}",
            font=('맑은 고딕', 24, 'bold'),
            fill='red'
        )


class InvadersGame(BaseGame):
    """침략자 게임 - 스페이스 인베이더 스타일"""

    ENEMIES = ['👾', '👽', '🛸', '💀', '🤖']

    def __init__(self, parent):
        super().__init__(parent)
        self.enemies = []  # [(word, x, y, id, text_id)]
        self.bullets = []  # [(x, y, id)]
        self.player_x = 300
        self.lives = 3
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="침략자 게임", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 정보
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=5)

        self.score_label = tk.Label(info_frame, text="점수: 0", font=('맑은 고딕', 12))
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.lives_label = tk.Label(info_frame, text="생명: ♥♥♥", font=('맑은 고딕', 12), fg='red')
        self.lives_label.pack(side=tk.LEFT, padx=10)

        # 캔버스
        self.canvas = tk.Canvas(self, width=600, height=400, bg='black')
        self.canvas.pack(pady=10)

        # 플레이어
        self.player = self.canvas.create_text(
            self.player_x, 380,
            text='🚀',
            font=('맑은 고딕', 20),
            fill='white'
        )

        # 입력
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 14), justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.shoot)

        # 버튼
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="게임 시작", command=self.start_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="중지", command=self.stop_game).pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """게임 시작"""
        self.is_running = True
        self.score = 0
        self.lives = 3
        self.enemies = []
        self.bullets = []
        self.canvas.delete("enemy")
        self.canvas.delete("bullet")

        self.update_display()
        self.spawn_enemies()
        self.update_game()

    def stop_game(self):
        """게임 중지"""
        self.is_running = False

    def spawn_enemies(self):
        """적 생성"""
        if not self.is_running:
            return

        words = ['공격', '위험', '격파', 'attack', 'danger', 'destroy', '적군', 'enemy']

        # 3줄 생성
        for row in range(3):
            for col in range(5):
                word = random.choice(words)
                x = 100 + col * 100
                y = 50 + row * 60

                emoji = random.choice(self.ENEMIES)
                emoji_id = self.canvas.create_text(
                    x, y - 20,
                    text=emoji,
                    font=('맑은 고딕', 16),
                    fill='yellow',
                    tags="enemy"
                )

                text_id = self.canvas.create_text(
                    x, y,
                    text=word,
                    font=('맑은 고딕', 10),
                    fill='white',
                    tags="enemy"
                )

                self.enemies.append([word, x, y, emoji_id, text_id])

    def shoot(self, event):
        """총알 발사"""
        typed = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not typed or not self.is_running:
            return

        # 일치하는 적 찾기
        for i, enemy_data in enumerate(self.enemies):
            word, x, y, emoji_id, text_id = enemy_data
            if word == typed:
                # 명중!
                bullet_id = self.canvas.create_oval(
                    self.player_x - 3, 370,
                    self.player_x + 3, 376,
                    fill='yellow',
                    tags="bullet"
                )
                self.bullets.append([self.player_x, 370, bullet_id, x, y, i])
                break

    def update_game(self):
        """게임 업데이트"""
        if not self.is_running:
            return

        # 총알 이동
        bullets_to_remove = []
        for i, bullet_data in enumerate(self.bullets):
            bx, by, bullet_id, target_x, target_y, enemy_idx = bullet_data

            # 목표 지점으로 이동
            dx = (target_x - bx) * 0.1
            dy = (target_y - by) * 0.1

            bx += dx
            by += dy

            self.canvas.coords(bullet_id, bx - 3, by - 3, bx + 3, by + 3)
            bullet_data[0] = bx
            bullet_data[1] = by

            # 목표 도달 확인
            if abs(bx - target_x) < 10 and abs(by - target_y) < 10:
                # 적 제거
                if enemy_idx < len(self.enemies):
                    _, _, _, emoji_id, text_id = self.enemies[enemy_idx]
                    self.canvas.delete(emoji_id)
                    self.canvas.delete(text_id)
                    del self.enemies[enemy_idx]

                    self.score += 1
                    self.update_display()

                # 총알 제거
                self.canvas.delete(bullet_id)
                bullets_to_remove.append(i)

                # 모든 적이 제거되었으면 새로운 적 생성
                if len(self.enemies) == 0:
                    self.after(1000, self.spawn_enemies)

        # 제거할 총알 삭제
        for i in reversed(bullets_to_remove):
            del self.bullets[i]

        # 적 하강
        enemies_reached_bottom = False
        for enemy_data in self.enemies:
            enemy_data[2] += 0.2  # y 좌표 증가
            _, x, y, emoji_id, text_id = enemy_data
            self.canvas.coords(emoji_id, x, y - 20)
            self.canvas.coords(text_id, x, y)

            if y > 350:
                enemies_reached_bottom = True

        if enemies_reached_bottom:
            self.lives -= 1
            self.update_display()

            # 적들 제거 및 재생성
            for _, _, _, emoji_id, text_id in self.enemies:
                self.canvas.delete(emoji_id)
                self.canvas.delete(text_id)
            self.enemies = []

            if self.lives > 0:
                self.spawn_enemies()
            else:
                self.game_over()
                return

        self.after(50, self.update_game)

    def update_display(self):
        """화면 업데이트"""
        self.score_label.config(text=f"점수: {self.score}")
        self.lives_label.config(text=f"생명: {'♥' * self.lives}")

    def game_over(self):
        """게임 오버"""
        self.is_running = False
        self.canvas.create_text(
            300, 200,
            text=f"게임 오버!\n최종 점수: {self.score}",
            font=('맑은 고딕', 24, 'bold'),
            fill='red'
        )


class MiningGame(BaseGame):
    """자원 캐기 게임 - 광산에서 자원을 캐는 게임"""

    RESOURCES = {
        '석탄': ('⬛', 1),
        '철': ('🔳', 2),
        '금': ('🟨', 3),
        '다이아': ('💎', 5),
        '에메랄드': ('💚', 10)
    }

    def __init__(self, parent):
        super().__init__(parent)
        self.mines = []  # [(resource, word, x, y, emoji_id, text_id)]
        self.inventory = {name: 0 for name in self.RESOURCES.keys()}
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="자원 캐기 게임", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 정보
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=5)

        self.score_label = tk.Label(info_frame, text="점수: 0", font=('맑은 고딕', 12))
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.inventory_label = tk.Label(
            info_frame,
            text="인벤토리: ",
            font=('맑은 고딕', 10)
        )
        self.inventory_label.pack(side=tk.LEFT, padx=10)

        # 캔버스
        self.canvas = tk.Canvas(self, width=600, height=400, bg='#8B4513')
        self.canvas.pack(pady=10)

        # 광부
        self.miner = self.canvas.create_text(
            300, 380,
            text='⛏️',
            font=('맑은 고딕', 24)
        )

        # 입력
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 14), justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.mine_resource)

        # 버튼
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="게임 시작", command=self.start_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="중지", command=self.stop_game).pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """게임 시작"""
        self.is_running = True
        self.score = 0
        self.mines = []
        self.inventory = {name: 0 for name in self.RESOURCES.keys()}
        self.canvas.delete("mine")

        self.update_display()
        self.generate_mines()

    def stop_game(self):
        """게임 중지"""
        self.is_running = False

    def generate_mines(self):
        """광산 생성"""
        words = ['캐기', '채굴', '광산', 'mine', 'dig', 'drill', '발굴', 'extract']

        for i in range(15):
            resource_name = random.choices(
                list(self.RESOURCES.keys()),
                weights=[40, 30, 20, 7, 3]
            )[0]

            emoji, value = self.RESOURCES[resource_name]
            word = random.choice(words)

            x = random.randint(50, 550)
            y = random.randint(50, 350)

            emoji_id = self.canvas.create_text(
                x, y - 20,
                text=emoji,
                font=('맑은 고딕', 20),
                tags="mine"
            )

            text_id = self.canvas.create_text(
                x, y,
                text=word,
                font=('맑은 고딕', 10),
                fill='white',
                tags="mine"
            )

            self.mines.append([resource_name, word, x, y, emoji_id, text_id])

    def mine_resource(self, event):
        """자원 채굴"""
        typed = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not typed or not self.is_running:
            return

        # 일치하는 자원 찾기
        for i, mine_data in enumerate(self.mines):
            resource_name, word, x, y, emoji_id, text_id = mine_data
            if word == typed:
                # 채굴 성공!
                self.canvas.delete(emoji_id)
                self.canvas.delete(text_id)

                _, value = self.RESOURCES[resource_name]
                self.score += value
                self.inventory[resource_name] += 1

                del self.mines[i]
                self.update_display()

                # 모든 자원 채굴 시 새로 생성
                if len(self.mines) == 0:
                    self.generate_mines()

                break

    def update_display(self):
        """화면 업데이트"""
        self.score_label.config(text=f"점수: {self.score}")

        inventory_text = " | ".join([f"{name}: {count}" for name, count in self.inventory.items()])
        self.inventory_label.config(text=f"인벤토리: {inventory_text}")


class CakeThrowGame(BaseGame):
    """케이크 던지기 게임 - 움직이는 타겟에 케이크 던지기"""

    def __init__(self, parent):
        super().__init__(parent)
        self.targets = []  # [(word, x, y, dx, dy, id, text_id)]
        self.cakes = []  # [(x, y, id)]
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="케이크 던지기 게임", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 정보
        self.score_label = tk.Label(self, text="점수: 0", font=('맑은 고딕', 12))
        self.score_label.pack(pady=5)

        # 캔버스
        self.canvas = tk.Canvas(self, width=600, height=400, bg='#FFE4E1')
        self.canvas.pack(pady=10)

        # 플레이어
        self.player = self.canvas.create_text(
            300, 380,
            text='👨‍🍳',
            font=('맑은 고딕', 24)
        )

        # 입력
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 14), justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.throw_cake)

        # 버튼
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="게임 시작", command=self.start_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="중지", command=self.stop_game).pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """게임 시작"""
        self.is_running = True
        self.score = 0
        self.targets = []
        self.cakes = []
        self.canvas.delete("target")
        self.canvas.delete("cake")

        self.update_display()
        self.spawn_targets()
        self.update_game()

    def stop_game(self):
        """게임 중지"""
        self.is_running = False

    def spawn_targets(self):
        """타겟 생성"""
        if not self.is_running:
            return

        words = ['던지기', '명중', '타겟', 'throw', 'hit', 'target', '케이크', 'cake']

        for i in range(5):
            word = random.choice(words)
            x = random.randint(50, 550)
            y = random.randint(50, 200)
            dx = random.choice([-2, -1, 1, 2])
            dy = random.choice([-1, 0, 1])

            emoji_id = self.canvas.create_text(
                x, y - 20,
                text='🎯',
                font=('맑은 고딕', 20),
                tags="target"
            )

            text_id = self.canvas.create_text(
                x, y,
                text=word,
                font=('맑은 고딕', 10),
                fill='blue',
                tags="target"
            )

            self.targets.append([word, x, y, dx, dy, emoji_id, text_id])

    def throw_cake(self, event):
        """케이크 던지기"""
        typed = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not typed or not self.is_running:
            return

        # 일치하는 타겟 찾기
        for i, target_data in enumerate(self.targets):
            word, x, y, dx, dy, emoji_id, text_id = target_data
            if word == typed:
                # 케이크 생성
                cake_id = self.canvas.create_text(
                    300, 370,
                    text='🎂',
                    font=('맑은 고딕', 16),
                    tags="cake"
                )
                self.cakes.append([300, 370, cake_id, x, y, i])
                break

    def update_game(self):
        """게임 업데이트"""
        if not self.is_running:
            return

        # 타겟 이동
        for target_data in self.targets:
            word, x, y, dx, dy, emoji_id, text_id = target_data

            x += dx
            y += dy

            # 벽 반사
            if x <= 20 or x >= 580:
                target_data[3] = -dx
                dx = -dx
            if y <= 20 or y >= 220:
                target_data[4] = -dy
                dy = -dy

            target_data[1] = x
            target_data[2] = y

            self.canvas.coords(emoji_id, x, y - 20)
            self.canvas.coords(text_id, x, y)

        # 케이크 이동
        cakes_to_remove = []
        for i, cake_data in enumerate(self.cakes):
            cx, cy, cake_id, target_x, target_y, target_idx = cake_data

            # 목표 지점으로 이동
            dx = (target_x - cx) * 0.15
            dy = (target_y - cy) * 0.15

            cx += dx
            cy += dy

            self.canvas.coords(cake_id, cx, cy)
            cake_data[0] = cx
            cake_data[1] = cy

            # 목표 도달 확인
            if abs(cx - target_x) < 15 and abs(cy - target_y) < 15:
                # 타겟 제거
                if target_idx < len(self.targets):
                    _, _, _, _, _, emoji_id, text_id = self.targets[target_idx]
                    self.canvas.delete(emoji_id)
                    self.canvas.delete(text_id)
                    del self.targets[target_idx]

                    self.score += 1
                    self.update_display()

                # 케이크 제거
                self.canvas.delete(cake_id)
                cakes_to_remove.append(i)

                # 타겟이 모두 제거되면 새로 생성
                if len(self.targets) == 0:
                    self.spawn_targets()

        # 제거할 케이크 삭제
        for i in reversed(cakes_to_remove):
            del self.cakes[i]

        self.after(50, self.update_game)

    def update_display(self):
        """화면 업데이트"""
        self.score_label.config(text=f"점수: {self.score}")


class MaritimeSOSGame(BaseGame):
    """해상 구조 SOS 게임 - 조난당한 배들을 구조하는 게임"""

    def __init__(self, parent):
        super().__init__(parent)
        self.ships = []  # [(word, x, y, id, text_id, timer)]
        self.rescued = 0
        self.lost = 0
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="해상 구조 SOS 게임", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 정보
        info_frame = ttk.Frame(self)
        info_frame.pack(pady=5)

        self.rescued_label = tk.Label(info_frame, text="구조: 0", font=('맑은 고딕', 12), fg='green')
        self.rescued_label.pack(side=tk.LEFT, padx=10)

        self.lost_label = tk.Label(info_frame, text="실종: 0", font=('맑은 고딕', 12), fg='red')
        self.lost_label.pack(side=tk.LEFT, padx=10)

        # 캔버스
        self.canvas = tk.Canvas(self, width=600, height=400, bg='#4682B4')
        self.canvas.pack(pady=10)

        # 구조선
        self.rescue_ship = self.canvas.create_text(
            300, 380,
            text='🚢',
            font=('맑은 고딕', 30)
        )

        # 입력
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 14), justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.rescue_ship_action)

        # 버튼
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=5)

        ttk.Button(button_frame, text="게임 시작", command=self.start_game).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="중지", command=self.stop_game).pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """게임 시작"""
        self.is_running = True
        self.rescued = 0
        self.lost = 0
        self.ships = []
        self.canvas.delete("ship")

        self.update_display()
        self.spawn_ship()
        self.update_game()

    def stop_game(self):
        """게임 중지"""
        self.is_running = False

    def spawn_ship(self):
        """조난 선박 생성"""
        if not self.is_running:
            return

        words = ['구조', '도움', '살려', 'help', 'save', 'rescue', 'SOS', 'MAYDAY']
        word = random.choice(words)

        x = random.randint(50, 550)
        y = random.randint(50, 300)

        ship_id = self.canvas.create_text(
            x, y - 20,
            text='⛵',
            font=('맑은 고딕', 24),
            tags="ship"
        )

        text_id = self.canvas.create_text(
            x, y,
            text=word,
            font=('맑은 고딕', 12, 'bold'),
            fill='red',
            tags="ship"
        )

        # SOS 신호
        sos_id = self.canvas.create_text(
            x, y + 20,
            text='🆘',
            font=('맑은 고딕', 16),
            tags="ship"
        )

        # 타이머 (10초)
        timer = 10

        self.ships.append([word, x, y, ship_id, text_id, sos_id, timer])

        # 다음 선박 생성
        self.after(3000, self.spawn_ship)

    def rescue_ship_action(self, event):
        """선박 구조"""
        typed = self.input_entry.get().strip()
        self.input_entry.delete(0, tk.END)

        if not typed or not self.is_running:
            return

        # 일치하는 선박 찾기
        for i, ship_data in enumerate(self.ships):
            word, x, y, ship_id, text_id, sos_id, timer = ship_data
            if word == typed:
                # 구조 성공!
                self.canvas.delete(ship_id)
                self.canvas.delete(text_id)
                self.canvas.delete(sos_id)

                del self.ships[i]
                self.rescued += 1
                self.update_display()
                break

    def update_game(self):
        """게임 업데이트"""
        if not self.is_running:
            return

        ships_to_remove = []

        for i, ship_data in enumerate(self.ships):
            word, x, y, ship_id, text_id, sos_id, timer = ship_data

            # 타이머 감소
            timer -= 0.1
            ship_data[6] = timer

            # 타이머에 따라 색 변경
            if timer < 3:
                self.canvas.itemconfig(text_id, fill='darkred')
            elif timer < 6:
                self.canvas.itemconfig(text_id, fill='orange')

            # 시간 초과
            if timer <= 0:
                self.canvas.delete(ship_id)
                self.canvas.delete(text_id)
                self.canvas.delete(sos_id)
                ships_to_remove.append(i)
                self.lost += 1
                self.update_display()

        # 제거할 선박 삭제
        for i in reversed(ships_to_remove):
            del self.ships[i]

        self.after(100, self.update_game)

    def update_display(self):
        """화면 업데이트"""
        self.rescued_label.config(text=f"구조: {self.rescued}")
        self.lost_label.config(text=f"실종: {self.lost}")
