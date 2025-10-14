"""
확장 기능 모듈
- 프로그래밍 코드 타이핑
- 배틀 로얄 게임
- RPG 스토리 모드
- 친구 시스템
- 클랜 시스템
- 통계 내보내기
- 튜토리얼
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
from datetime import datetime
import csv
import json


class ProgrammingTypingMode:
    """프로그래밍 코드 타이핑 연습 모드"""

    LANGUAGES = {
        'Python': [
            'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)',
            'class Calculator:\n    def __init__(self):\n        self.result = 0\n    \n    def add(self, x):\n        self.result += x\n        return self.result',
            'for i in range(10):\n    if i % 2 == 0:\n        print(f"{i} is even")\n    else:\n        print(f"{i} is odd")',
            'import requests\n\ndef fetch_data(url):\n    response = requests.get(url)\n    return response.json()',
            'lambda x, y: x**2 + y**2 if x > 0 and y > 0 else 0'
        ],
        'JavaScript': [
            'const factorial = (n) => {\n    return n <= 1 ? 1 : n * factorial(n - 1);\n};',
            'async function fetchData(url) {\n    const response = await fetch(url);\n    return response.json();\n}',
            'const users = [\n    { name: "Alice", age: 25 },\n    { name: "Bob", age: 30 }\n];\nusers.map(u => u.name);',
            'class Rectangle {\n    constructor(width, height) {\n        this.width = width;\n        this.height = height;\n    }\n}',
            'arr.filter(x => x > 10).map(x => x * 2).reduce((a, b) => a + b, 0);'
        ],
        'Java': [
            'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello World");\n    }\n}',
            'public int factorial(int n) {\n    if (n <= 1) return 1;\n    return n * factorial(n - 1);\n}',
            'List<String> names = new ArrayList<>();\nnames.add("Alice");\nnames.add("Bob");',
            'try {\n    int result = 10 / 0;\n} catch (ArithmeticException e) {\n    e.printStackTrace();\n}',
            'interface Drawable {\n    void draw();\n    default void print() {\n        System.out.println("Drawing");\n    }\n}'
        ],
        'C++': [
            '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello World" << endl;\n    return 0;\n}',
            'template<typename T>\nT max(T a, T b) {\n    return (a > b) ? a : b;\n}',
            'class Vector {\npublic:\n    int x, y;\n    Vector(int x, int y) : x(x), y(y) {}\n};',
            'vector<int> nums = {1, 2, 3, 4, 5};\nfor (auto n : nums) {\n    cout << n << endl;\n}',
            'unique_ptr<int> ptr = make_unique<int>(42);'
        ]
    }

    def __init__(self, parent, db=None, user_id=None):
        self.parent = parent
        self.db = db
        self.user_id = user_id
        self.current_language = 'Python'
        self.current_code = ''
        self.user_input = ''
        self.start_time = None
        self.errors = 0

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 상단: 언어 선택
        top_frame = tk.Frame(self.parent, bg='#2C3E50', height=60)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        top_frame.pack_propagate(False)

        tk.Label(
            top_frame,
            text="언어 선택:",
            font=('맑은 고딕', 12, 'bold'),
            bg='#2C3E50',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        lang_var = tk.StringVar(value='Python')
        for lang in self.LANGUAGES.keys():
            tk.Radiobutton(
                top_frame,
                text=lang,
                variable=lang_var,
                value=lang,
                command=lambda l=lang: self.change_language(l),
                bg='#2C3E50',
                fg='white',
                selectcolor='#34495E',
                font=('맑은 고딕', 10)
            ).pack(side=tk.LEFT, padx=5)

        # 중앙: 코드 표시 영역
        code_frame = tk.Frame(self.parent, bg='#ECF0F1')
        code_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            code_frame,
            text="타이핑할 코드:",
            font=('맑은 고딕', 12, 'bold'),
            bg='#ECF0F1'
        ).pack(anchor=tk.W, pady=(5, 5))

        self.code_text = tk.Text(
            code_frame,
            font=('Consolas', 11),
            bg='#1E1E1E',
            fg='#DCDCDC',
            wrap=tk.NONE,
            height=10,
            state=tk.DISABLED
        )
        self.code_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 입력 영역
        tk.Label(
            code_frame,
            text="여기에 입력하세요:",
            font=('맑은 고딕', 12, 'bold'),
            bg='#ECF0F1'
        ).pack(anchor=tk.W, pady=(10, 5))

        self.input_text = tk.Text(
            code_frame,
            font=('Consolas', 11),
            bg='white',
            fg='black',
            wrap=tk.NONE,
            height=10
        )
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.input_text.bind('<KeyRelease>', self.on_key_release)

        # 하단: 통계 및 버튼
        bottom_frame = tk.Frame(self.parent, bg='#ECF0F1')
        bottom_frame.pack(fill=tk.X, padx=20, pady=10)

        self.stats_label = tk.Label(
            bottom_frame,
            text="정확도: 100% | 오타: 0개 | 시간: 0초",
            font=('맑은 고딕', 12),
            bg='#ECF0F1'
        )
        self.stats_label.pack(side=tk.LEFT, padx=10)

        tk.Button(
            bottom_frame,
            text="새 코드",
            command=self.load_new_code,
            bg='#3498DB',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=12,
            cursor='hand2'
        ).pack(side=tk.RIGHT, padx=5)

        tk.Button(
            bottom_frame,
            text="완료",
            command=self.finish,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=12,
            cursor='hand2'
        ).pack(side=tk.RIGHT, padx=5)

        # 첫 코드 로드
        self.load_new_code()

    def change_language(self, language):
        """언어 변경"""
        self.current_language = language
        self.load_new_code()

    def load_new_code(self):
        """새 코드 로드"""
        self.current_code = random.choice(self.LANGUAGES[self.current_language])

        self.code_text.config(state=tk.NORMAL)
        self.code_text.delete('1.0', tk.END)
        self.code_text.insert('1.0', self.current_code)
        self.code_text.config(state=tk.DISABLED)

        self.input_text.delete('1.0', tk.END)
        self.user_input = ''
        self.errors = 0
        self.start_time = time.time()
        self.input_text.focus()

    def on_key_release(self, event):
        """키 입력 이벤트"""
        if not self.start_time:
            self.start_time = time.time()

        self.user_input = self.input_text.get('1.0', 'end-1c')

        # 오타 계산
        self.errors = 0
        for i, char in enumerate(self.user_input):
            if i < len(self.current_code):
                if char != self.current_code[i]:
                    self.errors += 1

        # 정확도 계산
        if len(self.user_input) > 0:
            accuracy = (1 - self.errors / len(self.user_input)) * 100
        else:
            accuracy = 100

        elapsed = int(time.time() - self.start_time)

        self.stats_label.config(
            text=f"정확도: {accuracy:.1f}% | 오타: {self.errors}개 | 시간: {elapsed}초"
        )

        # 완료 체크
        if self.user_input == self.current_code:
            self.finish()

    def finish(self):
        """연습 완료"""
        if not self.start_time:
            messagebox.showwarning("알림", "아직 시작하지 않았습니다.")
            return

        elapsed = int(time.time() - self.start_time)
        accuracy = (1 - self.errors / max(len(self.user_input), 1)) * 100 if len(self.user_input) > 0 else 0

        score = int(accuracy * (len(self.current_code) / max(elapsed, 1)) * 10)

        messagebox.showinfo(
            "완료",
            f"연습 완료!\n\n시간: {elapsed}초\n정확도: {accuracy:.1f}%\n점수: {score}점"
        )

        # 데이터베이스에 저장
        if self.db and self.user_id:
            self.db.save_practice_record(
                self.user_id,
                f"프로그래밍 타이핑 ({self.current_language})",
                score,
                accuracy,
                int(len(self.current_code) / max(elapsed, 1) * 60),
                int(elapsed / 60)
            )

            # 경험치 추가
            exp = int(score / 10)
            level_result = self.db.add_exp(self.user_id, exp)

            if level_result and level_result['leveled_up']:
                messagebox.showinfo(
                    "레벨 업!",
                    f"축하합니다! 레벨 {level_result['new_level']}로 올랐습니다!"
                )

        self.load_new_code()


class BattleRoyaleGame:
    """배틀 로얄 타자 게임"""

    def __init__(self, parent, db=None, user_id=None):
        self.parent = parent
        self.db = db
        self.user_id = user_id

        # 게임 상태
        self.players = []  # AI 플레이어들
        self.player_hp = 100
        self.player_position = 0
        self.zone_size = 100
        self.zone_center = 50
        self.current_word = ''
        self.words_typed = 0
        self.game_running = False
        self.start_time = None

        # 단어 리스트
        self.words = ['타자', '게임', '배틀', '로얄', '승리', '전투', '생존', '경쟁', '도전', '우승',
                     '키보드', '속도', '정확도', '연습', '실력', '마스터', '챔피언', '순위', '점수']

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 게임 영역
        game_frame = tk.Frame(self.parent, bg='#2C3E50')
        game_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 상태 표시
        status_frame = tk.Frame(game_frame, bg='#34495E', height=80)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        status_frame.pack_propagate(False)

        self.hp_label = tk.Label(
            status_frame,
            text="HP: 100/100",
            font=('맑은 고딕', 16, 'bold'),
            bg='#34495E',
            fg='#E74C3C'
        )
        self.hp_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.zone_label = tk.Label(
            status_frame,
            text="안전 지대: 100%",
            font=('맑은 고딕', 16, 'bold'),
            bg='#34495E',
            fg='#3498DB'
        )
        self.zone_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.players_label = tk.Label(
            status_frame,
            text="생존자: 10명",
            font=('맑은 고딕', 16, 'bold'),
            bg='#34495E',
            fg='#F39C12'
        )
        self.players_label.pack(side=tk.RIGHT, padx=20, pady=10)

        # 게임 캔버스
        self.canvas = tk.Canvas(
            game_frame,
            width=600,
            height=400,
            bg='#1E1E1E',
            highlightthickness=0
        )
        self.canvas.pack(pady=10)

        # 단어 입력 영역
        input_frame = tk.Frame(game_frame, bg='#2C3E50')
        input_frame.pack(pady=10)

        self.word_label = tk.Label(
            input_frame,
            text="게임을 시작하세요!",
            font=('맑은 고딕', 24, 'bold'),
            bg='#2C3E50',
            fg='white'
        )
        self.word_label.pack(pady=10)

        self.entry = tk.Entry(
            input_frame,
            font=('맑은 고딕', 18),
            width=30,
            justify='center'
        )
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', self.check_word)

        # 버튼
        btn_frame = tk.Frame(game_frame, bg='#2C3E50')
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(
            btn_frame,
            text="게임 시작",
            command=self.start_game,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 14, 'bold'),
            width=15,
            cursor='hand2'
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

    def start_game(self):
        """게임 시작"""
        self.game_running = True
        self.player_hp = 100
        self.player_position = 50
        self.zone_size = 100
        self.zone_center = 50
        self.words_typed = 0
        self.start_time = time.time()

        # AI 플레이어 생성
        self.players = [{'name': f'플레이어{i}', 'hp': 100, 'position': random.randint(0, 100)}
                       for i in range(1, 10)]

        self.start_btn.config(state=tk.DISABLED)
        self.next_word()
        self.update_game()

    def next_word(self):
        """다음 단어"""
        if self.game_running:
            self.current_word = random.choice(self.words)
            self.word_label.config(text=self.current_word)
            self.entry.delete(0, tk.END)
            self.entry.focus()

    def check_word(self, event):
        """단어 체크"""
        if not self.game_running:
            return

        user_input = self.entry.get().strip()

        if user_input == self.current_word:
            self.words_typed += 1
            # 플레이어 이동 (안전 지대 쪽으로)
            if self.player_position < self.zone_center:
                self.player_position += 5
            elif self.player_position > self.zone_center:
                self.player_position -= 5

            # 적 제거 (확률적)
            if len(self.players) > 0 and random.random() < 0.3:
                self.players.pop(random.randint(0, len(self.players) - 1))

            self.next_word()
        else:
            # 오타 시 HP 감소
            self.player_hp -= 5
            if self.player_hp <= 0:
                self.game_over(False)

    def update_game(self):
        """게임 업데이트"""
        if not self.game_running:
            return

        # 안전 지대 축소
        self.zone_size -= 0.1
        self.zone_center += random.randint(-1, 1)

        # 플레이어가 안전 지대 밖이면 피해
        distance_from_center = abs(self.player_position - self.zone_center)
        if distance_from_center > self.zone_size / 2:
            self.player_hp -= 1

        # AI 플레이어 제거 (랜덤)
        if len(self.players) > 0 and random.random() < 0.05:
            self.players.pop(random.randint(0, len(self.players) - 1))

        # 상태 업데이트
        self.hp_label.config(text=f"HP: {max(0, int(self.player_hp))}/100")
        self.zone_label.config(text=f"안전 지대: {int(self.zone_size)}%")
        self.players_label.config(text=f"생존자: {len(self.players) + 1}명")

        # 캔버스 그리기
        self.draw_game()

        # 게임 종료 조건
        if self.player_hp <= 0:
            self.game_over(False)
            return

        if len(self.players) == 0:
            self.game_over(True)
            return

        if self.zone_size < 5:
            self.game_over(self.player_hp > 50)
            return

        self.parent.after(100, self.update_game)

    def draw_game(self):
        """게임 화면 그리기"""
        self.canvas.delete('all')

        # 안전 지대
        zone_x = 300 + (self.zone_center - 50) * 4
        zone_width = self.zone_size * 4
        self.canvas.create_oval(
            zone_x - zone_width,
            200 - zone_width / 2,
            zone_x + zone_width,
            200 + zone_width / 2,
            outline='#3498DB',
            width=3
        )

        # 플레이어
        player_x = 300 + (self.player_position - 50) * 4
        self.canvas.create_oval(
            player_x - 15,
            185,
            player_x + 15,
            215,
            fill='#27AE60',
            outline='white',
            width=2
        )
        self.canvas.create_text(
            player_x,
            230,
            text='YOU',
            fill='white',
            font=('맑은 고딕', 10, 'bold')
        )

        # AI 플레이어들
        for i, player in enumerate(self.players):
            px = 300 + (player['position'] - 50) * 4
            py = 100 + (i % 3) * 100
            self.canvas.create_oval(
                px - 10,
                py - 10,
                px + 10,
                py + 10,
                fill='#E74C3C',
                outline='white'
            )

    def game_over(self, won):
        """게임 종료"""
        self.game_running = False
        self.start_btn.config(state=tk.NORMAL)

        elapsed = int(time.time() - self.start_time)

        if won:
            score = self.words_typed * 50 + int(self.player_hp) * 10
            messagebox.showinfo(
                "승리!",
                f"축하합니다! 배틀 로얄에서 우승했습니다!\n\n"
                f"타이핑한 단어: {self.words_typed}개\n"
                f"남은 HP: {int(self.player_hp)}\n"
                f"시간: {elapsed}초\n"
                f"점수: {score}점"
            )
        else:
            rank = len(self.players) + 2
            score = self.words_typed * 20
            messagebox.showinfo(
                "패배",
                f"아쉽게도 {rank}등으로 탈락했습니다.\n\n"
                f"타이핑한 단어: {self.words_typed}개\n"
                f"시간: {elapsed}초\n"
                f"점수: {score}점"
            )

        # 데이터베이스에 저장
        if self.db and self.user_id and won:
            self.db.save_practice_record(
                self.user_id,
                "배틀 로얄",
                score,
                100,
                int(self.words_typed / max(elapsed, 1) * 60),
                int(elapsed / 60)
            )


class RPGStoryMode:
    """RPG 스토리 모드 타자 게임"""

    def __init__(self, parent, db=None, user_id=None):
        self.parent = parent
        self.db = db
        self.user_id = user_id

        # 게임 상태
        self.player_level = 1
        self.player_hp = 100
        self.player_max_hp = 100
        self.player_exp = 0
        self.player_gold = 0

        self.current_enemy = None
        self.enemy_hp = 0
        self.enemy_max_hp = 0

        self.current_word = ''
        self.stage = 1
        self.battle_active = False

        # 적 데이터
        self.enemies = [
            {'name': '슬라임', 'hp': 30, 'exp': 10, 'gold': 5},
            {'name': '고블린', 'hp': 50, 'exp': 20, 'gold': 10},
            {'name': '오크', 'hp': 80, 'exp': 35, 'gold': 20},
            {'name': '드래곤', 'hp': 150, 'exp': 100, 'gold': 50},
            {'name': '마왕', 'hp': 300, 'exp': 200, 'gold': 100}
        ]

        # 타이핑 단어
        self.attack_words = ['공격', '베기', '찌르기', '마법', '화살', '폭발', '번개', '얼음',
                            '불꽃', '회복', '방어', '회피', '반격', '돌진', '질주']

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 전체 프레임
        main_frame = tk.Frame(self.parent, bg='#1A1A1A')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 플레이어 상태
        player_frame = tk.Frame(main_frame, bg='#2ECC71', height=100)
        player_frame.pack(fill=tk.X, pady=(0, 10))
        player_frame.pack_propagate(False)

        tk.Label(
            player_frame,
            text="👤 용사",
            font=('맑은 고딕', 18, 'bold'),
            bg='#2ECC71',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        self.player_stats_frame = tk.Frame(player_frame, bg='#2ECC71')
        self.player_stats_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        self.player_hp_label = tk.Label(
            self.player_stats_frame,
            text="HP: 100/100",
            font=('맑은 고딕', 12, 'bold'),
            bg='#2ECC71',
            fg='white'
        )
        self.player_hp_label.pack(anchor=tk.W)

        self.player_level_label = tk.Label(
            self.player_stats_frame,
            text="레벨: 1 | EXP: 0",
            font=('맑은 고딕', 12),
            bg='#2ECC71',
            fg='white'
        )
        self.player_level_label.pack(anchor=tk.W)

        self.player_gold_label = tk.Label(
            self.player_stats_frame,
            text="골드: 0",
            font=('맑은 고딕', 12),
            bg='#2ECC71',
            fg='#FFD700'
        )
        self.player_gold_label.pack(anchor=tk.W)

        # 전투 영역
        battle_frame = tk.Frame(main_frame, bg='#34495E', height=250)
        battle_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.battle_canvas = tk.Canvas(
            battle_frame,
            width=700,
            height=250,
            bg='#2C3E50',
            highlightthickness=0
        )
        self.battle_canvas.pack(fill=tk.BOTH, expand=True)

        # 적 상태
        enemy_frame = tk.Frame(main_frame, bg='#E74C3C', height=80)
        enemy_frame.pack(fill=tk.X, pady=(10, 0))
        enemy_frame.pack_propagate(False)

        tk.Label(
            enemy_frame,
            text="⚔️ 적",
            font=('맑은 고딕', 18, 'bold'),
            bg='#E74C3C',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        self.enemy_stats_frame = tk.Frame(enemy_frame, bg='#E74C3C')
        self.enemy_stats_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20)

        self.enemy_name_label = tk.Label(
            self.enemy_stats_frame,
            text="적이 없습니다",
            font=('맑은 고딕', 14, 'bold'),
            bg='#E74C3C',
            fg='white'
        )
        self.enemy_name_label.pack(anchor=tk.W)

        self.enemy_hp_label = tk.Label(
            self.enemy_stats_frame,
            text="HP: 0/0",
            font=('맑은 고딕', 12),
            bg='#E74C3C',
            fg='white'
        )
        self.enemy_hp_label.pack(anchor=tk.W)

        # 입력 영역
        input_frame = tk.Frame(main_frame, bg='#1A1A1A')
        input_frame.pack(fill=tk.X, pady=10)

        self.action_label = tk.Label(
            input_frame,
            text="전투를 시작하세요!",
            font=('맑은 고딕', 20, 'bold'),
            bg='#1A1A1A',
            fg='#F39C12'
        )
        self.action_label.pack(pady=10)

        self.input_entry = tk.Entry(
            input_frame,
            font=('맑은 고딕', 16),
            width=30,
            justify='center'
        )
        self.input_entry.pack(pady=5)
        self.input_entry.bind('<Return>', self.process_action)

        # 버튼
        btn_frame = tk.Frame(main_frame, bg='#1A1A1A')
        btn_frame.pack(pady=10)

        self.start_btn = tk.Button(
            btn_frame,
            text="전투 시작",
            command=self.start_battle,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 12, 'bold'),
            width=15,
            cursor='hand2'
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.heal_btn = tk.Button(
            btn_frame,
            text="회복 (10골드)",
            command=self.heal_player,
            bg='#3498DB',
            fg='white',
            font=('맑은 고딕', 12, 'bold'),
            width=15,
            cursor='hand2'
        )
        self.heal_btn.pack(side=tk.LEFT, padx=5)

    def start_battle(self):
        """전투 시작"""
        enemy_index = min(self.stage - 1, len(self.enemies) - 1)
        self.current_enemy = self.enemies[enemy_index].copy()
        self.enemy_hp = self.current_enemy['hp']
        self.enemy_max_hp = self.current_enemy['hp']

        self.battle_active = True
        self.start_btn.config(state=tk.DISABLED)

        self.update_display()
        self.next_action()

    def next_action(self):
        """다음 행동"""
        if self.battle_active:
            self.current_word = random.choice(self.attack_words)
            self.action_label.config(text=f"입력하세요: {self.current_word}")
            self.input_entry.delete(0, tk.END)
            self.input_entry.focus()

    def process_action(self, event):
        """행동 처리"""
        if not self.battle_active:
            return

        user_input = self.input_entry.get().strip()

        if user_input == self.current_word:
            # 공격 성공
            damage = random.randint(15, 25) + self.player_level * 5
            self.enemy_hp -= damage

            self.show_battle_message(f"적에게 {damage} 데미지!", '#27AE60')

            if self.enemy_hp <= 0:
                self.enemy_defeated()
            else:
                # 적의 반격
                enemy_damage = random.randint(5, 15)
                self.player_hp -= enemy_damage
                self.show_battle_message(f"적의 공격! {enemy_damage} 데미지를 받았습니다!", '#E74C3C')

                if self.player_hp <= 0:
                    self.game_over()
                else:
                    self.next_action()
        else:
            # 실패 - 적의 공격만
            enemy_damage = random.randint(10, 20)
            self.player_hp -= enemy_damage
            self.show_battle_message(f"오타! 적의 공격을 받았습니다! {enemy_damage} 데미지!", '#E74C3C')

            if self.player_hp <= 0:
                self.game_over()
            else:
                self.next_action()

        self.update_display()

    def enemy_defeated(self):
        """적 처치"""
        self.battle_active = False

        exp_gained = self.current_enemy['exp']
        gold_gained = self.current_enemy['gold']

        self.player_exp += exp_gained
        self.player_gold += gold_gained

        # 레벨업 체크
        if self.player_exp >= self.player_level * 50:
            self.player_level += 1
            self.player_max_hp += 20
            self.player_hp = self.player_max_hp
            messagebox.showinfo("레벨 업!", f"레벨 {self.player_level}로 올랐습니다!\nHP가 최대치로 회복되었습니다!")

        self.stage += 1

        if self.stage > len(self.enemies):
            self.victory()
        else:
            messagebox.showinfo(
                "승리!",
                f"{self.current_enemy['name']}를 물리쳤습니다!\n\n"
                f"경험치 +{exp_gained}\n"
                f"골드 +{gold_gained}"
            )
            self.start_btn.config(state=tk.NORMAL)

        self.current_enemy = None
        self.update_display()

    def heal_player(self):
        """플레이어 회복"""
        if self.player_gold >= 10:
            self.player_gold -= 10
            heal_amount = 30
            self.player_hp = min(self.player_hp + heal_amount, self.player_max_hp)
            messagebox.showinfo("회복", f"HP가 {heal_amount} 회복되었습니다!")
            self.update_display()
        else:
            messagebox.showwarning("골드 부족", "골드가 부족합니다!")

    def victory(self):
        """게임 승리"""
        total_score = self.player_level * 100 + self.player_gold * 2

        messagebox.showinfo(
            "게임 클리어!",
            f"모든 적을 물리치고 마왕을 처치했습니다!\n\n"
            f"최종 레벨: {self.player_level}\n"
            f"획득 골드: {self.player_gold}\n"
            f"최종 점수: {total_score}점"
        )

        # 데이터베이스에 저장
        if self.db and self.user_id:
            self.db.save_practice_record(
                self.user_id,
                "RPG 스토리 모드",
                total_score,
                100,
                0,
                10
            )

    def game_over(self):
        """게임 오버"""
        self.battle_active = False
        self.start_btn.config(state=tk.NORMAL)

        messagebox.showinfo(
            "게임 오버",
            f"HP가 0이 되었습니다!\n\n"
            f"도달 스테이지: {self.stage}\n"
            f"최종 레벨: {self.player_level}\n"
            f"획득 골드: {self.player_gold}"
        )

    def show_battle_message(self, message, color):
        """전투 메시지 표시"""
        self.action_label.config(text=message, fg=color)
        self.parent.after(1000, lambda: self.action_label.config(fg='#F39C12'))

    def update_display(self):
        """화면 업데이트"""
        # 플레이어 상태
        self.player_hp_label.config(text=f"HP: {max(0, int(self.player_hp))}/{self.player_max_hp}")
        self.player_level_label.config(text=f"레벨: {self.player_level} | EXP: {self.player_exp}")
        self.player_gold_label.config(text=f"골드: {self.player_gold}")

        # 적 상태
        if self.current_enemy:
            self.enemy_name_label.config(text=f"{self.current_enemy['name']} (스테이지 {self.stage})")
            self.enemy_hp_label.config(text=f"HP: {max(0, int(self.enemy_hp))}/{self.enemy_max_hp}")
        else:
            self.enemy_name_label.config(text="적이 없습니다")
            self.enemy_hp_label.config(text="HP: 0/0")

        # 캔버스 그리기
        self.draw_battle()

    def draw_battle(self):
        """전투 화면 그리기"""
        self.battle_canvas.delete('all')

        # 플레이어 (왼쪽)
        self.battle_canvas.create_text(
            150, 125,
            text="🗡️",
            font=('맑은 고딕', 80),
            fill='white'
        )

        # 적 (오른쪽)
        if self.current_enemy:
            emoji_map = {
                '슬라임': '🟢',
                '고블린': '👹',
                '오크': '👺',
                '드래곤': '🐉',
                '마왕': '😈'
            }
            enemy_emoji = emoji_map.get(self.current_enemy['name'], '👾')
            self.battle_canvas.create_text(
                550, 125,
                text=enemy_emoji,
                font=('맑은 고딕', 80),
                fill='white'
            )

        # VS
        self.battle_canvas.create_text(
            350, 125,
            text="⚔️",
            font=('맑은 고딕', 40),
            fill='#F39C12'
        )


# 파일이 너무 길어서 나머지 기능들은 계속됩니다...
