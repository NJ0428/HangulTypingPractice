"""
연습 모드: 자리 연습, 낱말 연습, 짧은 글, 긴 글, 필사
"""
import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import random
from keyboard_widget import VirtualKeyboard


class BasePractice(tk.Frame):
    """연습 모드 기본 클래스"""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        self.start_time = None
        self.typed_chars = 0
        self.errors = 0

        self.create_widgets()

    def create_widgets(self):
        """기본 위젯 생성 - 하위 클래스에서 오버라이드"""
        pass

    def calculate_stats(self):
        """통계 계산: 타수, 정확도"""
        if not self.start_time:
            return 0, 0, 0

        elapsed_time = time.time() - self.start_time
        if elapsed_time == 0:
            return 0, 0, 0

        # 분당 타수 (CPM: Characters Per Minute)
        cpm = int((self.typed_chars / elapsed_time) * 60)

        # 정확도
        accuracy = 100 if self.typed_chars == 0 else int(((self.typed_chars - self.errors) / self.typed_chars) * 100)

        return cpm, accuracy, int(elapsed_time)


class PositionPractice(BasePractice):
    """자리 연습 (홈 포지션)"""

    # 자리 연습 단계별 키
    STAGES = {
        '기본 자리': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅗ', 'ㅓ', 'ㅏ'],  # asdfghjkl
        '윗줄 연습': ['ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ'],  # qwertyuiop
        '아랫줄 연습': ['ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅠ', 'ㅜ', 'ㅡ'],  # zxcvbnm
    }

    def __init__(self, parent):
        self.current_stage = '기본 자리'
        self.target_text = ""
        self.current_index = 0
        super().__init__(parent)

    def create_widgets(self):
        # 제목
        title_label = tk.Label(self, text="자리 연습", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 단계 선택
        stage_frame = ttk.Frame(self)
        stage_frame.pack(pady=5)

        tk.Label(stage_frame, text="단계 선택:", font=('맑은 고딕', 10)).pack(side=tk.LEFT, padx=5)
        self.stage_var = tk.StringVar(value=self.current_stage)

        for stage in self.STAGES.keys():
            ttk.Radiobutton(
                stage_frame,
                text=stage,
                variable=self.stage_var,
                value=stage,
                command=self.change_stage
            ).pack(side=tk.LEFT, padx=5)

        # 목표 텍스트 표시
        self.target_label = tk.Label(
            self,
            text="",
            font=('맑은 고딕', 20),
            fg='black',
            bg='#ECF0F1',
            height=3,
            width=50
        )
        self.target_label.pack(pady=10)

        # 입력 필드
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 16), justify='center')
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<KeyPress>', self.on_key_press)
        self.input_entry.focus()

        # 통계 표시
        self.stats_label = tk.Label(self, text="타수: 0 | 정확도: 100% | 시간: 0초", font=('맑은 고딕', 10))
        self.stats_label.pack(pady=5)

        # 가상 키보드
        self.keyboard = VirtualKeyboard(self, language='hangul')
        self.keyboard.pack(pady=10)

        # 시작 버튼
        ttk.Button(self, text="연습 시작", command=self.start_practice).pack(pady=10)

    def change_stage(self):
        """단계 변경"""
        self.current_stage = self.stage_var.get()
        self.start_practice()

    def start_practice(self):
        """연습 시작"""
        keys = self.STAGES[self.current_stage]
        # 랜덤하게 20개 키 생성
        self.target_text = ' '.join(random.choices(keys, k=20))
        self.current_index = 0
        self.typed_chars = 0
        self.errors = 0
        self.start_time = None

        self.update_target_display()
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

    def update_target_display(self):
        """목표 텍스트 표시 업데이트"""
        if self.current_index >= len(self.target_text):
            self.target_label.config(text="완료!", fg='green')
            self.keyboard.clear_highlight()
            return

        # 현재 타이핑할 글자 강조
        display_text = ""
        for i, char in enumerate(self.target_text):
            if i < self.current_index:
                display_text += char  # 완료된 글자
            elif i == self.current_index:
                display_text += f"[{char}]"  # 현재 글자
            else:
                display_text += char

        self.target_label.config(text=display_text, fg='black')

        # 가상 키보드에서 현재 키 강조
        current_char = self.target_text[self.current_index]
        if current_char != ' ':
            self.keyboard.highlight_key(current_char)
        else:
            self.keyboard.highlight_key('Space')

    def on_key_press(self, event):
        """키 입력 처리"""
        if not self.start_time:
            self.start_time = time.time()

        # 현재 입력해야 할 글자
        if self.current_index >= len(self.target_text):
            return

        expected_char = self.target_text[self.current_index]

        # 입력된 글자와 비교
        if event.char == expected_char:
            self.current_index += 1
            self.typed_chars += 1
            self.update_target_display()
            self.update_stats()

            # 완료 확인
            if self.current_index >= len(self.target_text):
                self.show_completion()
        else:
            # 오류
            self.errors += 1
            self.update_stats()

        # 입력 필드는 항상 비워둠 (한 글자씩 입력)
        self.after(50, lambda: self.input_entry.delete(0, tk.END))

    def update_stats(self):
        """통계 업데이트"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(text=f"타수: {cpm} | 정확도: {accuracy}% | 시간: {elapsed}초")

    def show_completion(self):
        """완료 메시지"""
        cpm, accuracy, elapsed = self.calculate_stats()
        result_text = f"\n완료!\n타수: {cpm} CPM | 정확도: {accuracy}% | 시간: {elapsed}초"
        self.target_label.config(text=result_text, fg='green')


class WordPractice(BasePractice):
    """낱말 연습"""

    # 연습용 단어 목록
    WORDS = {
        '한글': ['안녕하세요', '감사합니다', '사랑합니다', '컴퓨터', '키보드', '프로그래밍', '타자연습',
                '대한민국', '서울특별시', '인공지능', '개발자', '소프트웨어', '하드웨어', '네트워크'],
        '영어': ['hello', 'world', 'python', 'programming', 'keyboard', 'computer', 'software',
                'developer', 'algorithm', 'function', 'variable', 'typing', 'practice', 'code']
    }

    def __init__(self, parent):
        self.language = '한글'
        self.word_list = []
        self.current_word_index = 0
        super().__init__(parent)

    def create_widgets(self):
        # 제목
        title_label = tk.Label(self, text="낱말 연습", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 언어 선택
        lang_frame = ttk.Frame(self)
        lang_frame.pack(pady=5)

        tk.Label(lang_frame, text="언어:", font=('맑은 고딕', 10)).pack(side=tk.LEFT, padx=5)
        self.lang_var = tk.StringVar(value='한글')

        ttk.Radiobutton(lang_frame, text="한글", variable=self.lang_var, value='한글',
                       command=self.change_language).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(lang_frame, text="영어", variable=self.lang_var, value='영어',
                       command=self.change_language).pack(side=tk.LEFT, padx=5)

        # 단어 표시
        self.word_label = tk.Label(
            self,
            text="",
            font=('맑은 고딕', 24, 'bold'),
            fg='#2C3E50',
            bg='#ECF0F1',
            height=2,
            width=30
        )
        self.word_label.pack(pady=20)

        # 입력 필드
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 16), justify='center', width=30)
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.check_word)
        self.input_entry.focus()

        # 진행 상황
        self.progress_label = tk.Label(self, text="0/0", font=('맑은 고딕', 10))
        self.progress_label.pack(pady=5)

        # 통계
        self.stats_label = tk.Label(self, text="타수: 0 | 정확도: 100% | 시간: 0초", font=('맑은 고딕', 10))
        self.stats_label.pack(pady=5)

        # 가상 키보드
        self.keyboard = VirtualKeyboard(self, language='hangul')
        self.keyboard.pack(pady=10)

        # 시작 버튼
        ttk.Button(self, text="연습 시작", command=self.start_practice).pack(pady=10)

    def change_language(self):
        """언어 변경"""
        self.language = self.lang_var.get()
        kb_lang = 'hangul' if self.language == '한글' else 'english'
        self.keyboard.switch_language(kb_lang)
        self.start_practice()

    def start_practice(self):
        """연습 시작"""
        self.word_list = random.sample(self.WORDS[self.language], min(10, len(self.WORDS[self.language])))
        self.current_word_index = 0
        self.typed_chars = 0
        self.errors = 0
        self.start_time = None

        self.show_next_word()

    def show_next_word(self):
        """다음 단어 표시"""
        if self.current_word_index >= len(self.word_list):
            self.show_completion()
            return

        word = self.word_list[self.current_word_index]
        self.word_label.config(text=word, fg='#2C3E50')
        self.progress_label.config(text=f"{self.current_word_index + 1}/{len(self.word_list)}")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

    def check_word(self, event):
        """단어 확인"""
        if not self.start_time:
            self.start_time = time.time()

        if self.current_word_index >= len(self.word_list):
            return

        expected = self.word_list[self.current_word_index]
        typed = self.input_entry.get()

        self.typed_chars += len(typed)

        if typed == expected:
            # 정답
            self.word_label.config(fg='green')
            self.current_word_index += 1
            self.after(500, self.show_next_word)
        else:
            # 오답
            self.errors += len(expected)
            self.word_label.config(fg='red')
            self.after(500, lambda: self.word_label.config(fg='#2C3E50'))

        self.update_stats()

    def update_stats(self):
        """통계 업데이트"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(text=f"타수: {cpm} | 정확도: {accuracy}% | 시간: {elapsed}초")

    def show_completion(self):
        """완료"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.word_label.config(text=f"완료!\n타수: {cpm} CPM\n정확도: {accuracy}%", fg='green')


class ShortTextPractice(BasePractice):
    """짧은 글 연습"""

    TEXTS = [
        "안녕하세요. 타자 연습을 시작합니다.",
        "빠르고 정확한 타이핑은 많은 연습을 필요로 합니다.",
        "꾸준히 연습하면 반드시 실력이 향상됩니다.",
        "The quick brown fox jumps over the lazy dog.",
        "Practice makes perfect in typing skills.",
    ]

    def create_widgets(self):
        title_label = tk.Label(self, text="짧은 글 연습", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 목표 텍스트
        self.target_text_widget = tk.Text(
            self,
            font=('맑은 고딕', 14),
            height=4,
            width=60,
            wrap=tk.WORD,
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.target_text_widget.pack(pady=10)
        self.target_text_widget.config(state=tk.DISABLED)

        # 입력 필드
        self.input_text_widget = scrolledtext.ScrolledText(
            self,
            font=('맑은 고딕', 14),
            height=4,
            width=60,
            wrap=tk.WORD
        )
        self.input_text_widget.pack(pady=10)
        self.input_text_widget.bind('<KeyRelease>', self.on_typing)
        self.input_text_widget.focus()

        # 통계
        self.stats_label = tk.Label(self, text="타수: 0 | 정확도: 100% | 시간: 0초", font=('맑은 고딕', 10))
        self.stats_label.pack(pady=5)

        # 시작 버튼
        ttk.Button(self, text="연습 시작", command=self.start_practice).pack(pady=10)

    def start_practice(self):
        """연습 시작"""
        text = random.choice(self.TEXTS)
        self.target_text = text
        self.typed_chars = 0
        self.errors = 0
        self.start_time = None

        self.target_text_widget.config(state=tk.NORMAL)
        self.target_text_widget.delete('1.0', tk.END)
        self.target_text_widget.insert('1.0', text)
        self.target_text_widget.config(state=tk.DISABLED)

        self.input_text_widget.delete('1.0', tk.END)
        self.input_text_widget.focus()

    def on_typing(self, event):
        """타이핑 중"""
        if not self.start_time:
            self.start_time = time.time()

        typed = self.input_text_widget.get('1.0', 'end-1c')
        self.typed_chars = len(typed)

        # 오류 계산
        self.errors = 0
        for i, char in enumerate(typed):
            if i < len(self.target_text) and char != self.target_text[i]:
                self.errors += 1

        self.update_stats()

        # 완료 확인
        if typed == self.target_text:
            self.show_completion()

    def update_stats(self):
        """통계 업데이트"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(text=f"타수: {cpm} | 정확도: {accuracy}% | 시간: {elapsed}초")

    def show_completion(self):
        """완료"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(
            text=f"완료! 타수: {cpm} CPM | 정확도: {accuracy}% | 시간: {elapsed}초",
            fg='green',
            font=('맑은 고딕', 12, 'bold')
        )


class LongTextPractice(ShortTextPractice):
    """긴 글 연습"""

    TEXTS = [
        """파이썬은 1991년 귀도 반 로섬이 개발한 프로그래밍 언어입니다.
간결하고 읽기 쉬운 문법으로 초보자부터 전문가까지 널리 사용되고 있습니다.
웹 개발, 데이터 분석, 인공지능 등 다양한 분야에서 활용됩니다.""",
        """The art of programming is the art of organizing complexity.
Programming is not about typing, it's about thinking.
Good code is its own best documentation.
As you're about to add a comment, ask yourself how can I improve the code."""
    ]

    def create_widgets(self):
        title_label = tk.Label(self, text="긴 글 연습", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 목표 텍스트 (더 큰 영역)
        self.target_text_widget = scrolledtext.ScrolledText(
            self,
            font=('맑은 고딕', 12),
            height=8,
            width=70,
            wrap=tk.WORD,
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.target_text_widget.pack(pady=10)
        self.target_text_widget.config(state=tk.DISABLED)

        # 입력 필드 (더 큰 영역)
        self.input_text_widget = scrolledtext.ScrolledText(
            self,
            font=('맑은 고딕', 12),
            height=8,
            width=70,
            wrap=tk.WORD
        )
        self.input_text_widget.pack(pady=10)
        self.input_text_widget.bind('<KeyRelease>', self.on_typing)
        self.input_text_widget.focus()

        # 통계
        self.stats_label = tk.Label(self, text="타수: 0 | 정확도: 100% | 시간: 0초", font=('맑은 고딕', 10))
        self.stats_label.pack(pady=5)

        # 시작 버튼
        ttk.Button(self, text="연습 시작", command=self.start_practice).pack(pady=10)


class TranscriptionMode(BasePractice):
    """필사 모드 - 사용자가 원하는 텍스트를 입력하여 연습"""

    def create_widgets(self):
        title_label = tk.Label(self, text="필사 연습", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 설정 프레임
        setup_frame = ttk.LabelFrame(self, text="필사할 텍스트 입력", padding=10)
        setup_frame.pack(fill=tk.BOTH, padx=10, pady=5)

        self.setup_text_widget = scrolledtext.ScrolledText(
            setup_frame,
            font=('맑은 고딕', 11),
            height=6,
            width=70,
            wrap=tk.WORD
        )
        self.setup_text_widget.pack(pady=5)

        ttk.Button(setup_frame, text="이 텍스트로 연습 시작", command=self.start_practice).pack(pady=5)

        # 연습 프레임
        practice_frame = ttk.LabelFrame(self, text="연습", padding=10)
        practice_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 목표 텍스트 표시
        tk.Label(practice_frame, text="목표 텍스트:", font=('맑은 고딕', 10, 'bold')).pack(anchor=tk.W)
        self.target_text_widget = scrolledtext.ScrolledText(
            practice_frame,
            font=('맑은 고딕', 11),
            height=6,
            width=70,
            wrap=tk.WORD,
            bg='#ECF0F1',
            fg='#2C3E50'
        )
        self.target_text_widget.pack(pady=5)
        self.target_text_widget.config(state=tk.DISABLED)

        # 입력 필드
        tk.Label(practice_frame, text="입력:", font=('맑은 고딕', 10, 'bold')).pack(anchor=tk.W, pady=(10, 0))
        self.input_text_widget = scrolledtext.ScrolledText(
            practice_frame,
            font=('맑은 고딕', 11),
            height=6,
            width=70,
            wrap=tk.WORD
        )
        self.input_text_widget.pack(pady=5)
        self.input_text_widget.bind('<KeyRelease>', self.on_typing)

        # 통계
        self.stats_label = tk.Label(practice_frame, text="타수: 0 | 정확도: 100% | 시간: 0초", font=('맑은 고딕', 10))
        self.stats_label.pack(pady=5)

    def start_practice(self):
        """연습 시작"""
        text = self.setup_text_widget.get('1.0', 'end-1c').strip()
        if not text:
            return

        self.target_text = text
        self.typed_chars = 0
        self.errors = 0
        self.start_time = None

        self.target_text_widget.config(state=tk.NORMAL)
        self.target_text_widget.delete('1.0', tk.END)
        self.target_text_widget.insert('1.0', text)
        self.target_text_widget.config(state=tk.DISABLED)

        self.input_text_widget.delete('1.0', tk.END)
        self.input_text_widget.focus()

    def on_typing(self, event):
        """타이핑 중"""
        if not self.start_time:
            self.start_time = time.time()

        typed = self.input_text_widget.get('1.0', 'end-1c')
        self.typed_chars = len(typed)

        # 오류 계산
        self.errors = 0
        for i, char in enumerate(typed):
            if i < len(self.target_text) and char != self.target_text[i]:
                self.errors += 1

        self.update_stats()

        # 완료 확인
        if typed == self.target_text:
            self.show_completion()

    def update_stats(self):
        """통계 업데이트"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(text=f"타수: {cpm} | 정확도: {accuracy}% | 시간: {elapsed}초")

    def show_completion(self):
        """완료"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(
            text=f"완료! 타수: {cpm} CPM | 정확도: {accuracy}% | 시간: {elapsed}초",
            fg='green',
            font=('맑은 고딕', 12, 'bold')
        )
