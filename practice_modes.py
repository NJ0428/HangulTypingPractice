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

    # 자리 연습 단계별 키 (누적 방식)
    STAGES = [
        {
            'name': '1단계: 기본 자리',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';']
        },
        {
            'name': '2단계: 왼손 위',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ']
        },
        {
            'name': '3단계: 오른손 위',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ']
        },
        {
            'name': '4단계: 중앙 자리',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ',
                     'ㅅ', 'ㅛ', 'ㅎ', 'ㅗ', 'ㅠ', 'ㅜ']
        },
        {
            'name': '5단계: 왼손 아래',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ',
                     'ㅅ', 'ㅛ', 'ㅎ', 'ㅗ', 'ㅠ', 'ㅜ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ']
        },
        {
            'name': '6단계: 오른손 아래',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ',
                     'ㅅ', 'ㅛ', 'ㅎ', 'ㅗ', 'ㅠ', 'ㅜ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅡ', ',', '.']
        },
        {
            'name': '7단계: 숫자',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ',
                     'ㅅ', 'ㅛ', 'ㅎ', 'ㅗ', 'ㅠ', 'ㅜ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅡ', ',', '.',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        },
        {
            'name': '8단계: 전체',
            'keys': ['ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅓ', 'ㅏ', 'ㅣ', ';', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ',
                     'ㅅ', 'ㅛ', 'ㅎ', 'ㅗ', 'ㅠ', 'ㅜ', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅡ', ',', '.',
                     '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
                     'ㅃ', 'ㅉ', 'ㄸ', 'ㄲ', 'ㅆ', 'ㅒ', 'ㅖ']
        }
    ]

    def __init__(self, parent):
        self.current_stage_index = 0
        self.target_text = ""
        self.current_index = 0
        super().__init__(parent)

    def create_widgets(self):
        # 제목 및 현재 단계 표시
        header_frame = tk.Frame(self, bg='#3498DB', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="자리 연습",
            font=('맑은 고딕', 18, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        self.stage_title_label = tk.Label(
            header_frame,
            text=self.STAGES[self.current_stage_index]['name'],
            font=('맑은 고딕', 14, 'bold'),
            bg='#3498DB',
            fg='#FFEB3B'
        )
        self.stage_title_label.pack(side=tk.LEFT, padx=20)

        # 단계 선택 버튼들
        stage_control_frame = tk.Frame(self, bg='#ECF0F1', relief=tk.RAISED, borderwidth=2)
        stage_control_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(
            stage_control_frame,
            text="단계 선택:",
            font=('맑은 고딕', 11, 'bold'),
            bg='#ECF0F1'
        ).pack(side=tk.LEFT, padx=10)

        # 8개 단계 버튼
        self.stage_buttons = []
        for i, stage in enumerate(self.STAGES):
            btn = tk.Button(
                stage_control_frame,
                text=f"{i+1}단계",
                command=lambda idx=i: self.change_stage(idx),
                bg='#3498DB' if i == self.current_stage_index else '#95A5A6',
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                width=6,
                height=1,
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2, pady=5)
            self.stage_buttons.append(btn)

        # 이전/다음 단계 버튼
        nav_frame = tk.Frame(stage_control_frame, bg='#ECF0F1')
        nav_frame.pack(side=tk.RIGHT, padx=10)

        self.prev_btn = tk.Button(
            nav_frame,
            text="← 이전",
            command=self.prev_stage,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 9, 'bold'),
            width=6,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.prev_btn.pack(side=tk.LEFT, padx=2)

        self.next_btn = tk.Button(
            nav_frame,
            text="다음 →",
            command=self.next_stage,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 9, 'bold'),
            width=6,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.next_btn.pack(side=tk.LEFT, padx=2)

        # 현재 단계 연습 글자 표시
        keys_frame = tk.Frame(self, bg='white', relief=tk.RAISED, borderwidth=2)
        keys_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(
            keys_frame,
            text="연습 글자:",
            font=('맑은 고딕', 10, 'bold'),
            bg='white'
        ).pack(side=tk.LEFT, padx=10)

        self.keys_label = tk.Label(
            keys_frame,
            text="",
            font=('맑은 고딕', 11),
            bg='white',
            fg='#E67E22',
            wraplength=900
        )
        self.keys_label.pack(side=tk.LEFT, padx=10, pady=8)

        self.update_keys_display()

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

        # 초기 네비게이션 버튼 상태 업데이트
        self.update_nav_buttons()

    def update_keys_display(self):
        """현재 단계의 연습 글자 표시 업데이트"""
        keys = self.STAGES[self.current_stage_index]['keys']
        keys_text = ' '.join(keys)
        self.keys_label.config(text=keys_text)

    def update_nav_buttons(self):
        """네비게이션 버튼 상태 업데이트"""
        # 이전 버튼
        if self.current_stage_index == 0:
            self.prev_btn.config(state=tk.DISABLED, bg='#95A5A6')
        else:
            self.prev_btn.config(state=tk.NORMAL, bg='#E74C3C')

        # 다음 버튼
        if self.current_stage_index == len(self.STAGES) - 1:
            self.next_btn.config(state=tk.DISABLED, bg='#95A5A6')
        else:
            self.next_btn.config(state=tk.NORMAL, bg='#27AE60')

    def change_stage(self, stage_index):
        """단계 변경"""
        self.current_stage_index = stage_index

        # 단계 제목 업데이트
        self.stage_title_label.config(text=self.STAGES[self.current_stage_index]['name'])

        # 단계 버튼 색상 업데이트
        for i, btn in enumerate(self.stage_buttons):
            if i == self.current_stage_index:
                btn.config(bg='#3498DB')
            else:
                btn.config(bg='#95A5A6')

        # 연습 글자 표시 업데이트
        self.update_keys_display()

        # 네비게이션 버튼 업데이트
        self.update_nav_buttons()

        # 연습 시작
        self.start_practice()

    def prev_stage(self):
        """이전 단계로"""
        if self.current_stage_index > 0:
            self.change_stage(self.current_stage_index - 1)

    def next_stage(self):
        """다음 단계로"""
        if self.current_stage_index < len(self.STAGES) - 1:
            self.change_stage(self.current_stage_index + 1)

    def start_practice(self):
        """연습 시작"""
        keys = self.STAGES[self.current_stage_index]['keys']
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

    # 낱말 연습 단계별 단어 목록 (난이도별)
    STAGES = [
        {
            'name': '1단계: 매우 쉬운 단어 (2-3글자)',
            'words_hangul': ['나', '나무', '사과', '하늘', '물', '불', '손', '발', '집', '밥',
                           '책', '꽃', '새', '산', '강', '바다', '눈', '비', '달', '별'],
            'words_english': ['cat', 'dog', 'run', 'see', 'book', 'pen', 'sun', 'moon', 'car', 'bag',
                            'cup', 'hat', 'bed', 'red', 'big', 'top', 'map', 'sit', 'fox', 'box']
        },
        {
            'name': '2단계: 쉬운 단어 (3-4글자)',
            'words_hangul': ['가방', '학교', '친구', '선생', '공부', '연필', '우산', '신발', '모자', '안경',
                           '의자', '책상', '시계', '전화', '문', '창문', '방', '거실', '화장실', '부엌'],
            'words_english': ['hello', 'world', 'apple', 'music', 'table', 'chair', 'house', 'water',
                            'paper', 'night', 'happy', 'smile', 'friend', 'study', 'write', 'phone',
                            'green', 'white', 'black', 'brown']
        },
        {
            'name': '3단계: 보통 단어 (4-5글자)',
            'words_hangul': ['컴퓨터', '키보드', '모니터', '마우스', '노트북', '휴대폰', '텔레비전', '냉장고',
                           '세탁기', '청소기', '에어컨', '선풍기', '카메라', '운동화', '가위', '풀',
                           '자전거', '오토바이', '버스', '지하철'],
            'words_english': ['python', 'typing', 'school', 'pencil', 'window', 'button', 'coffee',
                            'market', 'orange', 'yellow', 'purple', 'Monday', 'Friday', 'summer',
                            'winter', 'spring', 'letter', 'number', 'garden', 'forest']
        },
        {
            'name': '4단계: 약간 어려운 단어 (5-6글자)',
            'words_hangul': ['프로그램', '타자연습', '인터넷', '홈페이지', '아이스크림', '초콜릿', '과자',
                           '사탕', '주스', '음료수', '샌드위치', '피자', '치킨', '햄버거', '스파게티',
                           '라면', '김치찌개', '된장찌개', '불고기', '갈비'],
            'words_english': ['program', 'keyboard', 'network', 'website', 'document', 'favorite',
                            'language', 'business', 'birthday', 'computer', 'tomorrow', 'yesterday',
                            'hospital', 'restaurant', 'wonderful', 'beautiful', 'telephone', 'umbrella',
                            'chocolate', 'sandwich']
        },
        {
            'name': '5단계: 어려운 단어 (6-7글자)',
            'words_hangul': ['프로그래밍', '소프트웨어', '운영체제', '데이터', '알고리즘', '변수', '함수',
                           '객체지향', '데이터베이스', '네트워크', '인터페이스', '프레임워크', '라이브러리',
                           '컴파일러', '디버깅', '테스트', '배포', '버전관리', '보안', '암호화'],
            'words_english': ['software', 'function', 'variable', 'database', 'interface', 'framework',
                            'algorithm', 'debugging', 'security', 'password', 'developer', 'engineer',
                            'information', 'technology', 'important', 'different', 'education', 'community',
                            'environment', 'temperature']
        },
        {
            'name': '6단계: 복잡한 단어 (7-8글자)',
            'words_hangul': ['하드웨어', '클라우드', '빅데이터', '머신러닝', '딥러닝', '블록체인', '가상현실',
                           '증강현실', '사물인터넷', '자율주행', '드론', '로봇', '나노기술', '바이오', '유전자',
                           '양자컴퓨터', '슈퍼컴퓨터', '메인프레임', '서버', '클라이언트'],
            'words_english': ['hardware', 'operation', 'application', 'entertainment', 'organization',
                            'development', 'understanding', 'communication', 'transportation', 'professional',
                            'international', 'relationship', 'responsibility', 'availability', 'collaboration',
                            'performance', 'maintenance', 'generation', 'explanation', 'presentation']
        },
        {
            'name': '7단계: 매우 복잡한 단어 (8글자 이상)',
            'words_hangul': ['인공지능', '대한민국', '서울특별시', '프론트엔드', '백엔드', '풀스택', '데브옵스',
                           '마이크로서비스', '아키텍처', '리팩토링', '최적화', '동시성', '병렬처리', '분산시스템',
                           '클라우드컴퓨팅', '빅데이터분석', '정보보안', '사이버보안', '네트워크보안', '시스템관리'],
            'words_english': ['programming', 'implementation', 'demonstration', 'configuration', 'administration',
                            'authentication', 'authorization', 'infrastructure', 'microservices', 'containerization',
                            'orchestration', 'visualization', 'documentation', 'specification', 'recommendation',
                            'functionality', 'compatibility', 'optimization', 'architectural', 'comprehensive']
        },
        {
            'name': '8단계: 전체 혼합',
            'words_hangul': [],  # 모든 단어 혼합
            'words_english': []  # 모든 단어 혼합
        }
    ]

    def __init__(self, parent):
        self.current_stage_index = 0
        self.language = '한글'
        self.word_list = []
        self.current_word_index = 0
        super().__init__(parent)

    def create_widgets(self):
        # 제목 및 현재 단계 표시
        header_frame = tk.Frame(self, bg='#9B59B6', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="낱말 연습",
            font=('맑은 고딕', 18, 'bold'),
            bg='#9B59B6',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        self.stage_title_label = tk.Label(
            header_frame,
            text=self.STAGES[self.current_stage_index]['name'],
            font=('맑은 고딕', 14, 'bold'),
            bg='#9B59B6',
            fg='#FFEB3B'
        )
        self.stage_title_label.pack(side=tk.LEFT, padx=20)

        # 단계 선택 버튼들
        stage_control_frame = tk.Frame(self, bg='#ECF0F1', relief=tk.RAISED, borderwidth=2)
        stage_control_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(
            stage_control_frame,
            text="단계 선택:",
            font=('맑은 고딕', 11, 'bold'),
            bg='#ECF0F1'
        ).pack(side=tk.LEFT, padx=10)

        # 8개 단계 버튼
        self.stage_buttons = []
        for i, stage in enumerate(self.STAGES):
            btn = tk.Button(
                stage_control_frame,
                text=f"{i+1}단계",
                command=lambda idx=i: self.change_stage(idx),
                bg='#9B59B6' if i == self.current_stage_index else '#95A5A6',
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                width=6,
                height=1,
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2, pady=5)
            self.stage_buttons.append(btn)

        # 이전/다음 단계 버튼
        nav_frame = tk.Frame(stage_control_frame, bg='#ECF0F1')
        nav_frame.pack(side=tk.RIGHT, padx=10)

        self.prev_btn = tk.Button(
            nav_frame,
            text="← 이전",
            command=self.prev_stage,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 9, 'bold'),
            width=6,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.prev_btn.pack(side=tk.LEFT, padx=2)

        self.next_btn = tk.Button(
            nav_frame,
            text="다음 →",
            command=self.next_stage,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 9, 'bold'),
            width=6,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.next_btn.pack(side=tk.LEFT, padx=2)

        # 언어 선택
        lang_frame = tk.Frame(self, bg='white', relief=tk.RAISED, borderwidth=2)
        lang_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(lang_frame, text="언어:", font=('맑은 고딕', 10, 'bold'), bg='white').pack(side=tk.LEFT, padx=10)
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

        # 초기 네비게이션 버튼 상태 업데이트
        self.update_nav_buttons()

    def update_nav_buttons(self):
        """네비게이션 버튼 상태 업데이트"""
        # 이전 버튼
        if self.current_stage_index == 0:
            self.prev_btn.config(state=tk.DISABLED, bg='#95A5A6')
        else:
            self.prev_btn.config(state=tk.NORMAL, bg='#E74C3C')

        # 다음 버튼
        if self.current_stage_index == len(self.STAGES) - 1:
            self.next_btn.config(state=tk.DISABLED, bg='#95A5A6')
        else:
            self.next_btn.config(state=tk.NORMAL, bg='#27AE60')

    def change_stage(self, stage_index):
        """단계 변경"""
        self.current_stage_index = stage_index

        # 단계 제목 업데이트
        self.stage_title_label.config(text=self.STAGES[self.current_stage_index]['name'])

        # 단계 버튼 색상 업데이트
        for i, btn in enumerate(self.stage_buttons):
            if i == self.current_stage_index:
                btn.config(bg='#9B59B6')
            else:
                btn.config(bg='#95A5A6')

        # 네비게이션 버튼 업데이트
        self.update_nav_buttons()

        # 연습 시작
        self.start_practice()

    def prev_stage(self):
        """이전 단계로"""
        if self.current_stage_index > 0:
            self.change_stage(self.current_stage_index - 1)

    def next_stage(self):
        """다음 단계로"""
        if self.current_stage_index < len(self.STAGES) - 1:
            self.change_stage(self.current_stage_index + 1)

    def change_language(self):
        """언어 변경"""
        self.language = self.lang_var.get()
        kb_lang = 'hangul' if self.language == '한글' else 'english'
        self.keyboard.switch_language(kb_lang)
        self.start_practice()

    def get_words_for_stage(self):
        """현재 단계의 단어 목록 가져오기"""
        stage = self.STAGES[self.current_stage_index]

        # 8단계(전체 혼합)인 경우 모든 단어 합치기
        if self.current_stage_index == 7:
            all_words = []
            word_key = 'words_hangul' if self.language == '한글' else 'words_english'
            for s in self.STAGES[:-1]:  # 마지막 단계 제외
                all_words.extend(s[word_key])
            return all_words
        else:
            # 해당 단계의 단어 반환
            word_key = 'words_hangul' if self.language == '한글' else 'words_english'
            return stage[word_key]

    def start_practice(self):
        """연습 시작"""
        words = self.get_words_for_stage()
        self.word_list = random.sample(words, min(10, len(words)))
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
