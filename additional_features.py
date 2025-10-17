"""
추가 기능 모듈
- 튜토리얼 시스템
- 외국어 지원
- UI 커스터마이징
- 시즌 패스 UI
- 타이핑 팁
- 음성 피드백
- 실시간 타수 분석
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, font as tkfont
import random
import time
from collections import deque


class TutorialSystem:
    """타자 강좌/튜토리얼 시스템"""

    TUTORIALS = [
        {
            'title': '기본 자세',
            'description': '올바른 타자 자세를 배워봅시다.',
            'content': '''
🎯 올바른 타자 자세

1. 의자 높이 조절
   - 팔꿈치가 90도가 되도록 조절합니다
   - 발이 바닥에 평평하게 닿아야 합니다

2. 손목 위치
   - 손목은 키보드와 같은 높이로 유지합니다
   - 손목 받침대를 사용하면 좋습니다

3. 화면 거리
   - 모니터는 눈높이보다 약간 아래에 위치
   - 50-70cm 거리를 유지합니다

4. 조명
   - 충분한 조명으로 눈의 피로를 줄입니다
   - 화면에 빛이 반사되지 않도록 합니다

💡 Tip: 30분마다 5분씩 휴식을 취하세요!
            '''
        },
        {
            'title': '홈 포지션',
            'description': '기본 손가락 위치를 익힙니다.',
            'content': '''
⌨️ 홈 포지션 (Home Position)

왼손:
- 새끼: A
- 약지: S
- 중지: D
- 검지: F (돌기가 있음)

오른손:
- 검지: J (돌기가 있음)
- 중지: K
- 약지: L
- 새끼: ;

엄지: 스페이스바

💡 Tip: F와 J 키에는 돌기가 있어서
        손가락을 올려놓으면 느껴집니다!

항상 홈 포지션으로 돌아오는 습관을 들이세요.
            '''
        },
        {
            'title': '한글 타자 기초',
            'description': '한글 자판 배열을 학습합니다.',
            'content': '''
🇰🇷 한글 두벌식 자판

자음 (왼쪽):
- ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ

모음 (오른쪽):
- ㅏㅑㅓㅕㅗㅛㅜㅠㅡㅣ

쌍자음:
- Shift + 자음 키로 입력
- 예: Shift + ㄱ = ㄲ

받침:
- 초성과 같은 키로 입력
- 예: 간 = ㄱ + ㅏ + ㄴ

💡 Tip: 자음은 왼손, 모음은 오른손!
        리듬감 있게 번갈아가며 치세요.
            '''
        },
        {
            'title': '영문 타자 기초',
            'description': '영문 자판 배열을 학습합니다.',
            'content': '''
🔤 QWERTY 자판 배열

윗줄: Q W E R T Y U I O P
중간줄: A S D F G H J K L ;
아랫줄: Z X C V B N M , . /

각 손가락의 담당 키:
- 검지: 4개 키 (F, G, H, J 및 인접 키)
- 중지: 2개 키 (D, K 및 인접 키)
- 약지: 2개 키 (S, L 및 인접 키)
- 새끼: 나머지 키

💡 Tip: 검지손가락이 가장 많이 움직입니다!
        처음엔 느리더라도 정확하게 치는 것이 중요합니다.
            '''
        },
        {
            'title': '속도 향상 비법',
            'description': '타자 속도를 높이는 방법을 배웁니다.',
            'content': '''
⚡ 타자 속도 향상 비법

1. 정확도 우선
   - 속도는 나중에 자연스럽게 늘어납니다
   - 오타를 줄이는 것이 가장 중요!

2. 리듬 유지
   - 일정한 속도로 타이핑하세요
   - 빠르다 느리다를 반복하지 마세요

3. 시선 고정
   - 화면만 보고 키보드는 보지 마세요
   - 처음엔 어렵지만 연습하면 자연스러워집니다

4. 꾸준한 연습
   - 매일 20-30분씩 연습하세요
   - 짧고 집중적인 연습이 효과적입니다

5. 약한 손가락 집중 연습
   - 약지와 새끼손가락을 특별히 연습하세요

💡 Tip: 2주 꾸준히 연습하면 확실한 변화를 느낄 수 있습니다!
            '''
        },
        {
            'title': '특수문자 마스터',
            'description': '특수문자와 숫자 입력을 배웁니다.',
            'content': '''
🔢 특수문자 & 숫자

숫자열 (윗줄):
- 1 2 3 4 5 6 7 8 9 0
- Shift와 함께: ! @ # $ % ^ & * ( )

자주 쓰는 특수문자:
- 마침표: .
- 쉼표: ,
- 물음표: Shift + ?
- 느낌표: Shift + !
- 따옴표: Shift + "

프로그래밍 특수문자:
- 중괄호: Shift + { }
- 대괄호: [ ]
- 백슬래시: \\
- 파이프: Shift + |

💡 Tip: 특수문자는 프로그래밍할 때 필수!
        코딩 연습 모드로 특수문자를 마스터하세요.
            '''
        }
    ]

    def __init__(self, root):
        self.root = root

        self.window = tk.Toplevel(root)
        self.window.title("타자 강좌")
        self.window.geometry("800x600")
        self.window.configure(bg='#ECF0F1')
        self.window.transient(root)

        self.current_tutorial = 0

        self.setup_ui()
        self.show_tutorial(0)

    def setup_ui(self):
        """UI 설정"""
        # 헤더
        header_frame = tk.Frame(self.window, bg='#E67E22', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📚",
            font=('맑은 고딕', 40),
            bg='#E67E22'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="타자 강좌",
            font=('맑은 고딕', 20, 'bold'),
            bg='#E67E22',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 사이드바 (강좌 목록)
        sidebar_frame = tk.Frame(self.window, bg='#34495E', width=200)
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)

        tk.Label(
            sidebar_frame,
            text="강좌 목록",
            font=('맑은 고딕', 12, 'bold'),
            bg='#34495E',
            fg='white'
        ).pack(pady=10)

        for i, tutorial in enumerate(self.TUTORIALS):
            btn = tk.Button(
                sidebar_frame,
                text=f"{i+1}. {tutorial['title']}",
                command=lambda idx=i: self.show_tutorial(idx),
                bg='#2C3E50',
                fg='white',
                font=('맑은 고딕', 9),
                relief=tk.FLAT,
                anchor=tk.W,
                padx=10,
                cursor='hand2'
            )
            btn.pack(fill=tk.X, padx=5, pady=2)

        # 콘텐츠 영역
        self.content_frame = tk.Frame(self.window, bg='#ECF0F1')
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

    def show_tutorial(self, index):
        """강좌 표시"""
        self.current_tutorial = index

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tutorial = self.TUTORIALS[index]

        # 제목
        tk.Label(
            self.content_frame,
            text=tutorial['title'],
            font=('맑은 고딕', 20, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        ).pack(pady=(0, 5))

        # 설명
        tk.Label(
            self.content_frame,
            text=tutorial['description'],
            font=('맑은 고딕', 12),
            bg='#ECF0F1',
            fg='#7F8C8D'
        ).pack(pady=(0, 20))

        # 내용
        text_widget = tk.Text(
            self.content_frame,
            font=('맑은 고딕', 11),
            bg='white',
            wrap=tk.WORD,
            padx=20,
            pady=20
        )
        text_widget.pack(fill=tk.BOTH, expand=True)
        text_widget.insert('1.0', tutorial['content'])
        text_widget.config(state=tk.DISABLED)

        # 네비게이션 버튼
        nav_frame = tk.Frame(self.content_frame, bg='#ECF0F1')
        nav_frame.pack(fill=tk.X, pady=(10, 0))

        if index > 0:
            tk.Button(
                nav_frame,
                text="← 이전",
                command=lambda: self.show_tutorial(index - 1),
                bg='#95A5A6',
                fg='white',
                font=('맑은 고딕', 11, 'bold'),
                width=10,
                cursor='hand2'
            ).pack(side=tk.LEFT)

        if index < len(self.TUTORIALS) - 1:
            tk.Button(
                nav_frame,
                text="다음 →",
                command=lambda: self.show_tutorial(index + 1),
                bg='#3498DB',
                fg='white',
                font=('맑은 고딕', 11, 'bold'),
                width=10,
                cursor='hand2'
            ).pack(side=tk.RIGHT)


class LanguagePracticeMode:
    """외국어 타이핑 연습 모드"""

    LANGUAGES = {
        'Japanese': {
            'name': '일본어 (히라가나)',
            'words': [
                'こんにちは', 'ありがとう', 'さようなら', 'おはよう', 'おやすみ',
                'すみません', 'わかりました', 'いただきます', 'ごちそうさま', 'よろしく',
                'たべもの', 'のみもの', 'がっこう', 'せんせい', 'がくせい'
            ]
        },
        'Chinese': {
            'name': '중국어 (간체)',
            'words': [
                '你好', '谢谢', '再见', '早上好', '晚安',
                '对不起', '没关系', '不客气', '请', '是',
                '朋友', '学校', '老师', '学生', '中国'
            ]
        },
        'Spanish': {
            'name': '스페인어',
            'words': [
                'hola', 'gracias', 'adiós', 'buenos días', 'buenas noches',
                'por favor', 'de nada', 'sí', 'no', 'perdón',
                'amigo', 'escuela', 'profesor', 'estudiante', 'casa'
            ]
        },
        'French': {
            'name': '프랑스어',
            'words': [
                'bonjour', 'merci', 'au revoir', 'bonsoir', 'bonne nuit',
                's\'il vous plaît', 'de rien', 'oui', 'non', 'pardon',
                'ami', 'école', 'professeur', 'étudiant', 'maison'
            ]
        }
    }

    def __init__(self, parent, db=None, user_id=None):
        self.parent = parent
        self.db = db
        self.user_id = user_id
        self.current_language = 'Japanese'
        self.words_practiced = 0
        self.correct_count = 0
        self.start_time = None

        self.setup_ui()
        self.next_word()

    def setup_ui(self):
        """UI 설정"""
        # 언어 선택
        lang_frame = tk.Frame(self.parent, bg='#2C3E50', height=60)
        lang_frame.pack(fill=tk.X, pady=(0, 10))
        lang_frame.pack_propagate(False)

        tk.Label(
            lang_frame,
            text="언어 선택:",
            font=('맑은 고딕', 12, 'bold'),
            bg='#2C3E50',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        for lang_key, lang_data in self.LANGUAGES.items():
            tk.Button(
                lang_frame,
                text=lang_data['name'],
                command=lambda l=lang_key: self.change_language(l),
                bg='#3498DB',
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=5)

        # 단어 표시
        word_frame = tk.Frame(self.parent, bg='#ECF0F1')
        word_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(
            word_frame,
            text="타이핑할 단어:",
            font=('맑은 고딕', 14, 'bold'),
            bg='#ECF0F1'
        ).pack(pady=10)

        self.word_label = tk.Label(
            word_frame,
            text="",
            font=('맑은 고딕', 36, 'bold'),
            bg='white',
            fg='#2C3E50',
            relief=tk.RAISED,
            borderwidth=3,
            padx=50,
            pady=30
        )
        self.word_label.pack(pady=20)

        # 입력 영역
        self.input_entry = tk.Entry(
            word_frame,
            font=('맑은 고딕', 18),
            width=30,
            justify='center'
        )
        self.input_entry.pack(pady=20)
        self.input_entry.bind('<Return>', self.check_word)

        # 통계
        self.stats_label = tk.Label(
            word_frame,
            text="연습한 단어: 0개 | 정확도: 100%",
            font=('맑은 고딕', 12),
            bg='#ECF0F1'
        )
        self.stats_label.pack(pady=10)

    def change_language(self, language):
        """언어 변경"""
        self.current_language = language
        self.words_practiced = 0
        self.correct_count = 0
        self.start_time = time.time()
        self.next_word()

    def next_word(self):
        """다음 단어"""
        if not self.start_time:
            self.start_time = time.time()

        words = self.LANGUAGES[self.current_language]['words']
        self.current_word = random.choice(words)
        self.word_label.config(text=self.current_word)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

    def check_word(self, event):
        """단어 체크"""
        user_input = self.input_entry.get().strip()

        self.words_practiced += 1

        if user_input == self.current_word:
            self.correct_count += 1
            self.word_label.config(bg='#27AE60')
            self.parent.after(200, lambda: self.word_label.config(bg='white'))
        else:
            self.word_label.config(bg='#E74C3C')
            self.parent.after(200, lambda: self.word_label.config(bg='white'))

        accuracy = (self.correct_count / self.words_practiced * 100) if self.words_practiced > 0 else 100
        self.stats_label.config(
            text=f"연습한 단어: {self.words_practiced}개 | 정확도: {accuracy:.1f}%"
        )

        self.next_word()


class SeasonPassWindow:
    """시즌 패스 UI"""

    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

        self.window = tk.Toplevel(root)
        self.window.title("시즌 패스")
        self.window.geometry("900x600")
        self.window.configure(bg='#1A1A1A')
        self.window.transient(root)

        self.season_data = self.db.get_season_pass(user_id, season_number=1)

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 헤더
        header_frame = tk.Frame(self.window, bg='#F39C12', height=100)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🎁",
            font=('맑은 고딕', 50),
            bg='#F39C12'
        ).pack(side=tk.LEFT, padx=20)

        title_frame = tk.Frame(header_frame, bg='#F39C12')
        title_frame.pack(side=tk.LEFT, pady=20)

        tk.Label(
            title_frame,
            text="시즌 1 패스",
            font=('맑은 고딕', 24, 'bold'),
            bg='#F39C12',
            fg='white'
        ).pack(anchor=tk.W)

        tk.Label(
            title_frame,
            text=f"티어 {self.season_data['tier']}/50 | EXP: {self.season_data['season_exp']}",
            font=('맑은 고딕', 14),
            bg='#F39C12',
            fg='white'
        ).pack(anchor=tk.W)

        # 프리미엄 버튼
        if not self.season_data['is_premium']:
            tk.Button(
                header_frame,
                text="프리미엄 구매\n(1000 골드)",
                command=self.buy_premium,
                bg='#E67E22',
                fg='white',
                font=('맑은 고딕', 11, 'bold'),
                width=15,
                height=3,
                cursor='hand2'
            ).pack(side=tk.RIGHT, padx=20)

        # 진행도 바
        progress_frame = tk.Frame(self.window, bg='#2C3E50', height=50)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        progress_frame.pack_propagate(False)

        current_tier_exp = self.season_data['season_exp'] % 100
        progress_percent = current_tier_exp / 100

        tk.Label(
            progress_frame,
            text=f"다음 티어까지: {100 - current_tier_exp} EXP",
            font=('맑은 고딕', 12, 'bold'),
            bg='#2C3E50',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        canvas = tk.Canvas(progress_frame, width=500, height=30, bg='#34495E', highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=10)
        canvas.create_rectangle(0, 0, 500 * progress_percent, 30, fill='#F39C12', outline='')

        # 보상 목록
        rewards_frame = tk.Frame(self.window, bg='#1A1A1A')
        rewards_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 스크롤 가능한 캔버스
        canvas = tk.Canvas(rewards_frame, bg='#1A1A1A', highlightthickness=0)
        scrollbar = tk.Scrollbar(rewards_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = tk.Frame(canvas, bg='#1A1A1A')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=scrollbar.set)

        # 보상 생성 (50개 티어)
        rewards = [
            '🎨 테마', '💎 다이아', '⭐ EXP 부스트', '🎁 상자', '🏆 칭호',
            '🎯 업적', '💰 골드', '🔮 아이템', '🎪 이모티콘', '🎭 아바타'
        ]

        for tier in range(50):
            tier_frame = tk.Frame(scrollable_frame, bg='#2C3E50', width=100, height=150, relief=tk.RAISED, borderwidth=2)
            tier_frame.pack(side=tk.LEFT, padx=5, pady=5)
            tier_frame.pack_propagate(False)

            # 티어 번호
            tk.Label(
                tier_frame,
                text=f"Tier {tier + 1}",
                font=('맑은 고딕', 10, 'bold'),
                bg='#2C3E50',
                fg='#F39C12'
            ).pack(pady=5)

            # 무료 보상
            reward_free = random.choice(rewards[:5])
            tk.Label(
                tier_frame,
                text=reward_free,
                font=('맑은 고딕', 20),
                bg='#34495E',
                fg='white'
            ).pack(pady=5)

            tk.Label(
                tier_frame,
                text="무료",
                font=('맑은 고딕', 8),
                bg='#2C3E50',
                fg='#95A5A6'
            ).pack()

            # 프리미엄 보상
            if self.season_data['is_premium']:
                reward_premium = random.choice(rewards)
                tk.Label(
                    tier_frame,
                    text=reward_premium,
                    font=('맑은 고딕', 20),
                    bg='#E67E22',
                    fg='white'
                ).pack(pady=5)

            # 잠금/해제 표시
            if tier <= self.season_data['tier']:
                tk.Label(
                    tier_frame,
                    text="✓ 획득",
                    font=('맑은 고딕', 9, 'bold'),
                    bg='#27AE60',
                    fg='white'
                ).pack(pady=2)
            else:
                tk.Label(
                    tier_frame,
                    text="🔒 잠김",
                    font=('맑은 고딕', 9),
                    bg='#7F8C8D',
                    fg='white'
                ).pack(pady=2)

        canvas.pack(side="top", fill="both", expand=True)
        scrollbar.pack(side="bottom", fill="x")

    def buy_premium(self):
        """프리미엄 구매"""
        if messagebox.askyesno("프리미엄 구매", "1000 골드를 사용하여 프리미엄을 구매하시겠습니까?"):
            # 실제로는 골드 차감 로직이 필요
            messagebox.showinfo("구매 완료", "프리미엄 시즌 패스를 구매했습니다!")
            self.window.destroy()


class DailyTipWidget:
    """매일 랜덤 타이핑 팁 표시 위젯"""

    TIPS = [
        "💡 올바른 손가락으로 키를 누르는 것이 속도 향상의 첫걸음입니다!",
        "💡 키보드를 보지 않고 치는 '블라인드 타치'를 연습하세요.",
        "💡 30분마다 5분씩 휴식을 취하면 타자 효율이 높아집니다.",
        "💡 정확도가 98% 이상이 되면 자연스럽게 속도도 빨라집니다.",
        "💡 리듬감 있게 일정한 속도로 타이핑하세요.",
        "💡 자주 틀리는 키는 따로 집중 연습하세요.",
        "💡 손목 받침대를 사용하면 피로가 줄어듭니다.",
        "💡 매일 20-30분 꾸준히 연습하는 것이 가장 효과적입니다.",
        "💡 F와 J 키의 돌기를 느끼며 홈 포지션을 유지하세요.",
        "💡 특수문자 연습도 중요합니다! 코딩 모드를 활용하세요.",
        "💡 짧은 글부터 시작해서 점진적으로 긴 글로 늘려가세요.",
        "💡 타이핑할 때 어깨에 힘을 빼고 편안하게 하세요.",
        "💡 약지와 새끼손가락이 약하다면 집중 연습이 필요합니다.",
        "💡 모니터는 눈높이보다 약간 아래에 위치시키세요.",
        "💡 타자 속도보다 정확도를 먼저 높이세요!"
    ]

    def __init__(self, parent):
        self.parent = parent

        # 프레임
        frame = tk.Frame(parent, bg='#FFF9C4', relief=tk.RAISED, borderwidth=2)
        frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            frame,
            text="📌 오늘의 타이핑 팁",
            font=('맑은 고딕', 11, 'bold'),
            bg='#FFF9C4',
            fg='#F39C12'
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))

        tip = random.choice(self.TIPS)
        tk.Label(
            frame,
            text=tip,
            font=('맑은 고딕', 10),
            bg='#FFF9C4',
            fg='#34495E',
            wraplength=400,
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=10, pady=(0, 5))


class RealtimeAnalysisWidget:
    """실시간 타수 분석 위젯"""

    def __init__(self, parent):
        self.parent = parent
        self.typing_data = deque(maxlen=60)  # 최근 60초 데이터
        self.last_update = time.time()

        # 프레임
        self.frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(
            self.frame,
            text="📈 실시간 타수 분석",
            font=('맑은 고딕', 12, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(pady=5)

        # 그래프 캔버스
        self.canvas = tk.Canvas(
            self.frame,
            width=400,
            height=150,
            bg='#F8F9FA',
            highlightthickness=0
        ).pack(pady=5, padx=10)

        # 통계 레이블
        self.stats_label = tk.Label(
            self.frame,
            text="평균 타수: 0 타/분 | 리듬 안정성: 100%",
            font=('맑은 고딕', 10),
            bg='white'
        )
        self.stats_label.pack(pady=5)

    def add_typing_event(self, chars_per_second):
        """타이핑 이벤트 추가"""
        current_time = time.time()
        self.typing_data.append((current_time, chars_per_second))
        self.update_display()

    def update_display(self):
        """디스플레이 업데이트"""
        if not self.typing_data:
            return

        # 평균 타수 계산
        avg_cps = sum(d[1] for d in self.typing_data) / len(self.typing_data)
        avg_cpm = avg_cps * 60

        # 리듬 안정성 (표준편차 기반)
        if len(self.typing_data) > 1:
            speeds = [d[1] for d in self.typing_data]
            mean = sum(speeds) / len(speeds)
            variance = sum((x - mean) ** 2 for x in speeds) / len(speeds)
            std_dev = variance ** 0.5
            stability = max(0, 100 - std_dev * 10)
        else:
            stability = 100

        self.stats_label.config(
            text=f"평균 타수: {int(avg_cpm)} 타/분 | 리듬 안정성: {int(stability)}%"
        )


class UICustomizer:
    """UI 커스터마이징 설정"""

    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

        self.window = tk.Toplevel(root)
        self.window.title("UI 커스터마이징")
        self.window.geometry("600x500")
        self.window.configure(bg='#ECF0F1')
        self.window.transient(root)

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 헤더
        header_frame = tk.Frame(self.window, bg='#9B59B6', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🎨 UI 커스터마이징",
            font=('맑은 고딕', 20, 'bold'),
            bg='#9B59B6',
            fg='white'
        ).pack(pady=20)

        # 설정 영역
        settings_frame = tk.Frame(self.window, bg='#ECF0F1')
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 글꼴 크기
        font_frame = tk.Frame(settings_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        font_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            font_frame,
            text="글꼴 크기",
            font=('맑은 고딕', 12, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=20, pady=10)

        font_size_var = tk.IntVar(value=12)
        tk.Scale(
            font_frame,
            from_=10,
            to=20,
            orient=tk.HORIZONTAL,
            variable=font_size_var,
            bg='white',
            length=200
        ).pack(side=tk.LEFT, padx=10)

        # 배경색
        color_frame = tk.Frame(settings_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        color_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            color_frame,
            text="배경색",
            font=('맑은 고딕', 12, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=20, pady=10)

        tk.Button(
            color_frame,
            text="색상 선택",
            command=self.choose_color,
            bg='#3498DB',
            fg='white',
            font=('맑은 고딕', 10, 'bold'),
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=10)

        # 적용 버튼
        tk.Button(
            settings_frame,
            text="적용",
            command=lambda: self.apply_settings(font_size_var.get()),
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 12, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(pady=20)

    def choose_color(self):
        """색상 선택"""
        color = colorchooser.askcolor()
        if color[1]:
            messagebox.showinfo("색상 선택", f"선택한 색상: {color[1]}")

    def apply_settings(self, font_size):
        """설정 적용"""
        self.db.update_user_settings(self.user_id, font_size=font_size)
        messagebox.showinfo("적용 완료", "설정이 적용되었습니다!\n재시작 후 적용됩니다.")
        self.window.destroy()
