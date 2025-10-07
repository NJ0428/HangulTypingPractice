"""
퀴즈 모드: 맞춤법 퀴즈, 초성 퀴즈
"""
import tkinter as tk
from tkinter import ttk
import random


class BaseQuiz(tk.Frame):
    """퀴즈 기본 클래스"""

    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)

        self.score = 0
        self.total_questions = 0
        self.current_question = None

    def create_widgets(self):
        """위젯 생성 - 하위 클래스에서 오버라이드"""
        pass


class SpellingQuiz(BaseQuiz):
    """맞춤법 퀴즈"""

    # 맞춤법 문제 (올바른 표현, 틀린 표현들)
    QUESTIONS = [
        {
            'correct': '안녕하세요',
            'wrong': ['안녕하세요o', '안녕하세여', '안뇽하세요'],
            'explanation': '표준어는 "안녕하세요"입니다.'
        },
        {
            'correct': '되어',
            'wrong': ['돼어', '되여', '돼여'],
            'explanation': '"되다"의 어미는 "되어"가 맞습니다.'
        },
        {
            'correct': '왠지',
            'wrong': ['웬지', '왼지', '웬지모르게'],
            'explanation': '"왜인지"의 준말은 "왠지"입니다. "웬"은 "어찌된, 어떠한"의 뜻입니다.'
        },
        {
            'correct': '금세',
            'wrong': ['금새', '금방', '곰방'],
            'explanation': '"금시에"의 준말은 "금세"입니다.'
        },
        {
            'correct': '어떻게',
            'wrong': ['어떡해', '어떻케', '어케'],
            'explanation': '"어떻게"는 방법을 묻는 말이고, "어떡해"는 "어찌하여"의 준말입니다.'
        },
        {
            'correct': '가르치다',
            'wrong': ['가르키다', '갈키다', '갈치다'],
            'explanation': '지식이나 기술을 전달하는 것은 "가르치다"입니다.'
        },
        {
            'correct': '거칠다',
            'wrong': ['거칠어', '거칫다', '거친다'],
            'explanation': '형용사 "거칠다"의 기본형입니다.'
        },
        {
            'correct': '몇 개',
            'wrong': ['몇개', '몇게', '몃개'],
            'explanation': '수를 나타낼 때는 띄어씁니다: "몇 개"'
        },
        {
            'correct': '할게',
            'wrong': ['할께', '하께', '하깨'],
            'explanation': '"하다"의 어미는 "할게"가 맞습니다.'
        },
        {
            'correct': '봤어',
            'wrong': ['봤써', '봤서', '밨어'],
            'explanation': '"보다"의 과거형은 "봤어"입니다.'
        },
        {
            'correct': '설거지',
            'wrong': ['설겆이', '설걷이', '설거짓'],
            'explanation': '그릇을 씻는 일은 "설거지"입니다.'
        },
        {
            'correct': '문의',
            'wrong': ['문이', '뭉의', '묻이'],
            'explanation': '질문하는 것은 "문의"입니다.'
        },
        {
            'correct': '되레',
            'wrong': ['돼레', '되래', '돼래'],
            'explanation': '"오히려"의 뜻으로는 "되레"가 맞습니다.'
        },
        {
            'correct': '며칠',
            'wrong': ['몇일', '며일', '몇칠'],
            'explanation': '날짜를 물을 때는 "며칠"입니다.'
        },
        {
            'correct': '번거롭다',
            'wrong': ['번거럽다', '번거룹다', '번걸럽다'],
            'explanation': '형용사는 "번거롭다"가 표준어입니다.'
        }
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.questions_pool = []
        self.create_widgets()

    def create_widgets(self):
        # 제목
        title_label = tk.Label(self, text="맞춤법 퀴즈", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 점수 표시
        self.score_label = tk.Label(self, text="점수: 0 / 0", font=('맑은 고딕', 12))
        self.score_label.pack(pady=5)

        # 문제 표시
        question_frame = ttk.LabelFrame(self, text="다음 중 올바른 표현을 선택하세요", padding=20)
        question_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.question_label = tk.Label(
            question_frame,
            text="",
            font=('맑은 고딕', 14),
            wraplength=500
        )
        self.question_label.pack(pady=10)

        # 선택지 프레임
        self.choices_frame = ttk.Frame(question_frame)
        self.choices_frame.pack(pady=10)

        # 설명 레이블
        self.explanation_label = tk.Label(
            question_frame,
            text="",
            font=('맑은 고딕', 11),
            fg='blue',
            wraplength=500
        )
        self.explanation_label.pack(pady=10)

        # 다음 문제 버튼
        self.next_button = ttk.Button(question_frame, text="다음 문제", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(pady=10)

        # 시작 버튼
        self.start_button = ttk.Button(self, text="퀴즈 시작", command=self.start_quiz)
        self.start_button.pack(pady=10)

    def start_quiz(self):
        """퀴즈 시작"""
        self.score = 0
        self.total_questions = 0
        self.questions_pool = random.sample(self.QUESTIONS, min(10, len(self.QUESTIONS)))

        self.update_score()
        self.next_question()

    def next_question(self):
        """다음 문제"""
        if not self.questions_pool:
            self.show_result()
            return

        self.current_question = self.questions_pool.pop(0)
        self.total_questions += 1

        # 선택지 생성
        choices = [self.current_question['correct']] + self.current_question['wrong']
        random.shuffle(choices)

        # 선택지 프레임 초기화
        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        self.explanation_label.config(text="")
        self.next_button.config(state=tk.DISABLED)

        # 선택지 버튼 생성
        for i, choice in enumerate(choices):
            btn = ttk.Button(
                self.choices_frame,
                text=choice,
                command=lambda c=choice: self.check_answer(c)
            )
            btn.pack(pady=5, fill=tk.X, padx=20)

        self.question_label.config(text=f"문제 {self.total_questions}")

    def check_answer(self, selected):
        """답 확인"""
        correct = self.current_question['correct']

        # 모든 버튼 비활성화
        for widget in self.choices_frame.winfo_children():
            widget.config(state=tk.DISABLED)

        if selected == correct:
            # 정답
            self.score += 1
            self.explanation_label.config(text=f"정답! {self.current_question['explanation']}", fg='green')
        else:
            # 오답
            self.explanation_label.config(
                text=f"틀렸습니다. 정답은 '{correct}'입니다.\n{self.current_question['explanation']}",
                fg='red'
            )

        self.update_score()
        self.next_button.config(state=tk.NORMAL)

    def update_score(self):
        """점수 업데이트"""
        self.score_label.config(text=f"점수: {self.score} / {self.total_questions}")

    def show_result(self):
        """결과 표시"""
        for widget in self.choices_frame.winfo_children():
            widget.destroy()

        percentage = int((self.score / self.total_questions) * 100) if self.total_questions > 0 else 0

        result_text = f"퀴즈 완료!\n\n정답: {self.score} / {self.total_questions}\n정확도: {percentage}%"

        if percentage >= 90:
            result_text += "\n\n🏆 훌륭합니다!"
        elif percentage >= 70:
            result_text += "\n\n👍 잘했어요!"
        else:
            result_text += "\n\n💪 조금 더 연습해보세요!"

        self.question_label.config(text=result_text)
        self.explanation_label.config(text="")
        self.next_button.config(state=tk.DISABLED)


class ChoSeongQuiz(BaseQuiz):
    """초성 퀴즈 - 초성을 보고 단어 맞추기"""

    # 초성 분해 테이블
    CHOSEONG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']

    # 문제 목록 (단어, 힌트)
    WORDS = [
        ('사과', '빨간 과일'),
        ('컴퓨터', '전자 기기'),
        ('키보드', '타이핑 도구'),
        ('프로그래밍', '코딩'),
        ('대한민국', '우리나라'),
        ('서울특별시', '수도'),
        ('인공지능', 'AI'),
        ('타자연습', '이 프로그램'),
        ('개발자', '프로그래머'),
        ('소프트웨어', '프로그램'),
        ('안녕하세요', '인사말'),
        ('감사합니다', '고마움 표현'),
        ('사랑합니다', '애정 표현'),
        ('학교', '공부하는 곳'),
        ('선생님', '가르치는 분'),
        ('친구', '동료'),
        ('가족', '부모형제'),
        ('음악', '소리 예술'),
        ('영화', '영상 예술'),
        ('운동', '신체 활동'),
        ('축구', '공놀이'),
        ('야구', '배트 스포츠'),
        ('농구', '골대 스포츠'),
        ('수영', '물에서 하는 운동'),
        ('책', '읽는 것'),
        ('연필', '필기구'),
        ('지우개', '지우는 도구'),
        ('공책', '노트'),
        ('가방', '물건 담는 것'),
        ('시계', '시간 보는 것'),
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.questions_pool = []
        self.create_widgets()

    def create_widgets(self):
        # 제목
        title_label = tk.Label(self, text="초성 퀴즈", font=('맑은 고딕', 16, 'bold'))
        title_label.pack(pady=10)

        # 점수 표시
        self.score_label = tk.Label(self, text="점수: 0 / 0", font=('맑은 고딕', 12))
        self.score_label.pack(pady=5)

        # 문제 표시
        question_frame = ttk.LabelFrame(self, text="초성을 보고 단어를 맞추세요", padding=20)
        question_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 초성 표시
        self.choseong_label = tk.Label(
            question_frame,
            text="",
            font=('맑은 고딕', 36, 'bold'),
            fg='#2C3E50'
        )
        self.choseong_label.pack(pady=20)

        # 힌트
        self.hint_label = tk.Label(
            question_frame,
            text="",
            font=('맑은 고딕', 12),
            fg='gray'
        )
        self.hint_label.pack(pady=5)

        # 입력 필드
        self.answer_entry = tk.Entry(question_frame, font=('맑은 고딕', 16), justify='center')
        self.answer_entry.pack(pady=10)
        self.answer_entry.bind('<Return>', self.check_answer)

        # 결과 표시
        self.result_label = tk.Label(
            question_frame,
            text="",
            font=('맑은 고딕', 12, 'bold')
        )
        self.result_label.pack(pady=10)

        # 버튼
        button_frame = ttk.Frame(question_frame)
        button_frame.pack(pady=10)

        self.submit_button = ttk.Button(button_frame, text="제출", command=lambda: self.check_answer(None))
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.next_button = ttk.Button(button_frame, text="다음 문제", command=self.next_question, state=tk.DISABLED)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.hint_button = ttk.Button(button_frame, text="힌트 보기", command=self.show_hint)
        self.hint_button.pack(side=tk.LEFT, padx=5)

        # 시작 버튼
        self.start_button = ttk.Button(self, text="퀴즈 시작", command=self.start_quiz)
        self.start_button.pack(pady=10)

    def start_quiz(self):
        """퀴즈 시작"""
        self.score = 0
        self.total_questions = 0
        self.questions_pool = random.sample(self.WORDS, min(10, len(self.WORDS)))

        self.update_score()
        self.next_question()

    def next_question(self):
        """다음 문제"""
        if not self.questions_pool:
            self.show_result()
            return

        self.current_word, self.current_hint = self.questions_pool.pop(0)
        self.total_questions += 1

        # 초성 추출
        choseong = self.get_choseong(self.current_word)
        self.choseong_label.config(text=choseong)

        # 초기화
        self.hint_label.config(text="")
        self.answer_entry.delete(0, tk.END)
        self.answer_entry.config(state=tk.NORMAL)
        self.result_label.config(text="")
        self.next_button.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.NORMAL)
        self.hint_button.config(state=tk.NORMAL)
        self.answer_entry.focus()

    def get_choseong(self, word):
        """한글 단어에서 초성 추출"""
        choseong = ""

        for char in word:
            if '가' <= char <= '힣':
                # 한글 유니코드 처리
                code = ord(char) - ord('가')
                cho_idx = code // (21 * 28)
                choseong += self.CHOSEONG_LIST[cho_idx]
            else:
                # 한글이 아닌 경우 그대로
                choseong += char

        return choseong

    def show_hint(self):
        """힌트 보기"""
        self.hint_label.config(text=f"💡 힌트: {self.current_hint}")

    def check_answer(self, event):
        """답 확인"""
        answer = self.answer_entry.get().strip()

        if not answer:
            return

        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.hint_button.config(state=tk.DISABLED)

        if answer == self.current_word:
            # 정답
            self.score += 1
            self.result_label.config(text="✅ 정답입니다!", fg='green')
        else:
            # 오답
            self.result_label.config(text=f"❌ 틀렸습니다. 정답은 '{self.current_word}'입니다.", fg='red')

        self.update_score()
        self.next_button.config(state=tk.NORMAL)

    def update_score(self):
        """점수 업데이트"""
        self.score_label.config(text=f"점수: {self.score} / {self.total_questions}")

    def show_result(self):
        """결과 표시"""
        percentage = int((self.score / self.total_questions) * 100) if self.total_questions > 0 else 0

        result_text = f"퀴즈 완료!\n\n정답: {self.score} / {self.total_questions}\n정확도: {percentage}%"

        if percentage >= 90:
            result_text += "\n\n🏆 훌륭합니다!"
        elif percentage >= 70:
            result_text += "\n\n👍 잘했어요!"
        else:
            result_text += "\n\n💪 조금 더 연습해보세요!"

        self.choseong_label.config(text=result_text, font=('맑은 고딕', 18, 'bold'))
        self.hint_label.config(text="")
        self.result_label.config(text="")
        self.answer_entry.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.next_button.config(state=tk.DISABLED)
        self.hint_button.config(state=tk.DISABLED)
