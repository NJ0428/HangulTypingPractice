"""
한글/영어 타자 연습 소프트웨어
Python + Tkinter 기반
"""
import tkinter as tk
from tkinter import ttk, font
import sys
import os

# 모듈 임포트
from keyboard_widget import VirtualKeyboard
from practice_modes import (
    PositionPractice, WordPractice, ShortTextPractice,
    LongTextPractice, TranscriptionMode
)
from games import (
    AcidRainGame, InvadersGame, MiningGame,
    CakeThrowGame, MaritimeSOSGame
)
from quizzes import SpellingQuiz, ChoSeongQuiz


class TypingPracticeApp:
    """메인 타자 연습 애플리케이션"""

    def __init__(self, root):
        self.root = root
        self.root.title("한글/영어 타자 연습")
        self.root.geometry("1200x800")
        self.root.configure(bg='#E8F4F8')

        # 폰트 설정
        self.default_font = font.Font(family="맑은 고딕", size=10)
        self.title_font = font.Font(family="맑은 고딕", size=14, weight="bold")
        self.big_font = font.Font(family="맑은 고딕", size=16, weight="bold")

        # 사용자 정보
        self.user_name = "손님"
        self.user_score = 0

        # 현재 모드
        self.current_mode = None
        self.in_game = False  # 게임/연습 중인지 여부

        # UI 생성
        self.create_ui()

    def create_ui(self):
        """UI 구성"""
        # 메인 컨테이너
        self.main_container = tk.Frame(self.root, bg='#E8F4F8')
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 시작 화면 표시
        self.show_start_menu()

    def show_start_menu(self):
        """시작 메뉴 화면"""
        # 기존 위젯 제거
        for widget in self.main_container.winfo_children():
            widget.destroy()

        self.in_game = False

        # 상단 헤더
        header_frame = tk.Frame(self.main_container, bg='#87CEEB', height=80)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        # 사용자 정보 (왼쪽)
        user_frame = tk.Frame(header_frame, bg='white', relief=tk.RAISED, borderwidth=2)
        user_frame.pack(side=tk.LEFT, padx=20, pady=10)

        user_icon = tk.Label(user_frame, text='👤', font=('맑은 고딕', 30), bg='white')
        user_icon.pack(side=tk.LEFT, padx=10)

        user_info_frame = tk.Frame(user_frame, bg='white')
        user_info_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(user_info_frame, text=self.user_name, font=('맑은 고딕', 12, 'bold'), bg='white').pack(anchor=tk.W)
        tk.Label(user_info_frame, text=f"{self.user_score}", font=('맑은 고딕', 14, 'bold'), bg='white', fg='#E67E22').pack(anchor=tk.W)

        # 메인 타이틀 (중앙)
        tk.Label(
            header_frame,
            text="⌨️ 한글/영어 타자 연습 ⌨️",
            font=('맑은 고딕', 20, 'bold'),
            bg='#87CEEB',
            fg='white'
        ).pack(side=tk.LEFT, expand=True)

        # 메인 콘텐츠 영역
        content_container = tk.Frame(self.main_container, bg='#E8F4F8')
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 탭 프레임
        tab_frame = tk.Frame(content_container, bg='#E8F4F8')
        tab_frame.pack(fill=tk.X, pady=(0, 10))

        # 탭 버튼 스타일
        self.current_tab = tk.StringVar(value='자리연습')

        tabs = [
            ('자리연습', '🎯'), ('낱말연습', '📝'), ('짧은글연습', '📄'),
            ('긴글연습', '📚'), ('필사', '✍️'), ('산성비', '☔'),
            ('침략자', '👾'), ('자원캐기', '⛏️'), ('케이크던지기', '🎂'),
            ('해상구조SOS', '🚢'), ('맞춤법퀴즈', '📖'), ('초성퀴즈', '🔤')
        ]

        for i, (tab_name, emoji) in enumerate(tabs):
            btn = tk.Button(
                tab_frame,
                text=f"{emoji}\n{tab_name}",
                command=lambda t=tab_name: self.change_tab(t),
                bg='#3498DB' if i < 5 else '#E74C3C' if i < 10 else '#9B59B6',
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                relief=tk.RAISED,
                borderwidth=3,
                width=10,
                height=3,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=2)

        # 콘텐츠 프레임 (모드별 설명 및 시작 버튼)
        self.start_content_frame = tk.Frame(content_container, bg='white', relief=tk.RAISED, borderwidth=3)
        self.start_content_frame.pack(fill=tk.BOTH, expand=True)

        # 기본 탭 표시
        self.change_tab('자리연습')

        # 하단 상태바
        status_frame = tk.Frame(self.main_container, bg='#34495E', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        status_frame.pack_propagate(False)

        tk.Label(
            status_frame,
            text="한글/영어 타자 연습 | Python + Tkinter",
            font=('맑은 고딕', 9),
            bg='#34495E',
            fg='white'
        ).pack(side=tk.LEFT, padx=10)

    def change_tab(self, tab_name):
        """탭 변경"""
        self.current_tab.set(tab_name)

        # 콘텐츠 프레임 초기화
        for widget in self.start_content_frame.winfo_children():
            widget.destroy()

        # 탭별 콘텐츠 정의
        tab_content = {
            '자리연습': {
                'icon': '⌨️',
                'title': '자리 연습',
                'desc': '글자판의 위치를 익히는 곳입니다.\n\n글자판에 익숙하지 않다면 제일 먼저 자리 연습을 합니다. 좌우 확실표 글쇠나 마우스로 자리 연습 단계를 바꿀 수 있습니다.',
                'stages': '기본 자리 → 윗줄 → 아랫줄',
                'command': self.start_position_practice
            },
            '낱말연습': {
                'icon': '📝',
                'title': '낱말 연습',
                'desc': '자주 쓰이는 낱말을 익히는 곳입니다.\n\n한글 또는 영어 단어를 연습할 수 있습니다. 다양한 낱말을 타이핑하며 속도와 정확도를 향상시키세요.',
                'stages': '한글 낱말 / 영어 낱말',
                'command': self.start_word_practice
            },
            '짧은글연습': {
                'icon': '📄',
                'title': '짧은 글 연습',
                'desc': '짧은 문장을 연습하는 곳입니다.\n\n실제 문장 형태의 텍스트를 타이핑하며 실전 감각을 익힐 수 있습니다.',
                'stages': '1-2줄 분량의 짧은 문장',
                'command': self.start_short_text
            },
            '긴글연습': {
                'icon': '📚',
                'title': '긴 글 연습',
                'desc': '긴 문단을 연습하는 곳입니다.\n\n여러 줄의 긴 텍스트를 타이핑하며 지구력과 집중력을 기를 수 있습니다.',
                'stages': '여러 줄의 긴 문단',
                'command': self.start_long_text
            },
            '필사': {
                'icon': '✍️',
                'title': '필사 연습',
                'desc': '원하는 텍스트를 입력하여 연습하는 곳입니다.\n\n책이나 문서의 내용을 그대로 입력하여 타이핑 연습을 할 수 있습니다.',
                'stages': '사용자 정의 텍스트',
                'command': self.start_transcription
            },
            '산성비': {
                'icon': '☔',
                'title': '산성비 게임',
                'desc': '떨어지는 단어를 타이핑하여 제거하는 게임입니다.\n\n단어가 바닥에 닿기 전에 정확하게 입력하세요. 레벨이 올라갈수록 속도가 빨라집니다!',
                'stages': '생명 3개 | 레벨업 시스템',
                'command': self.start_acid_rain
            },
            '침략자': {
                'icon': '👾',
                'title': '침략자 게임',
                'desc': '스페이스 인베이더 스타일의 타자 게임입니다.\n\n적의 단어를 입력하여 격파하세요. 적이 바닥에 닿으면 생명이 줄어듭니다!',
                'stages': '우주 방어 전투',
                'command': self.start_invaders
            },
            '자원캐기': {
                'icon': '⛏️',
                'title': '자원 캐기 게임',
                'desc': '광산에서 자원을 채굴하는 게임입니다.\n\n단어를 입력하여 다양한 자원을 채굴하고 점수를 획득하세요. 희귀 자원일수록 높은 점수!',
                'stages': '석탄→철→금→다이아→에메랄드',
                'command': self.start_mining
            },
            '케이크던지기': {
                'icon': '🎂',
                'title': '케이크 던지기 게임',
                'desc': '움직이는 타겟에 케이크를 던지는 게임입니다.\n\n타겟의 단어를 정확하게 입력하여 케이크를 명중시키세요!',
                'stages': '움직이는 타겟 명중',
                'command': self.start_cake_throw
            },
            '해상구조SOS': {
                'icon': '🚢',
                'title': '해상 구조 SOS 게임',
                'desc': '조난당한 배들을 구조하는 게임입니다.\n\n시간 제한 내에 SOS 신호의 단어를 입력하여 배를 구조하세요!',
                'stages': '시간 제한 구조 미션',
                'command': self.start_maritime_sos
            },
            '맞춤법퀴즈': {
                'icon': '📖',
                'title': '맞춤법 퀴즈',
                'desc': '올바른 한글 표현을 찾는 퀴즈입니다.\n\n자주 틀리는 맞춤법을 퀴즈를 통해 재미있게 학습할 수 있습니다.',
                'stages': '4지선다 10문제',
                'command': self.start_spelling_quiz
            },
            '초성퀴즈': {
                'icon': '🔤',
                'title': '초성 퀴즈',
                'desc': '초성을 보고 단어를 맞추는 퀴즈입니다.\n\n힌트를 참고하여 정답을 입력하세요. 한글 실력 향상에 도움이 됩니다!',
                'stages': '초성 힌트 10문제',
                'command': self.start_choseong_quiz
            }
        }

        content = tab_content.get(tab_name, tab_content['자리연습'])

        # 왼쪽: 설명 영역
        left_frame = tk.Frame(self.start_content_frame, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # 아이콘과 제목
        title_frame = tk.Frame(left_frame, bg='white')
        title_frame.pack(pady=(0, 20))

        tk.Label(
            title_frame,
            text=content['icon'],
            font=('맑은 고딕', 48),
            bg='white'
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(
            title_frame,
            text=content['title'],
            font=('맑은 고딕', 24, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(side=tk.LEFT)

        # 설명
        tk.Label(
            left_frame,
            text=content['desc'],
            font=('맑은 고딕', 12),
            bg='white',
            fg='#34495E',
            justify=tk.LEFT,
            wraplength=450
        ).pack(pady=10, anchor=tk.W)

        # 단계 정보
        stage_frame = tk.Frame(left_frame, bg='#ECF0F1', relief=tk.RAISED, borderwidth=2)
        stage_frame.pack(fill=tk.X, pady=20)

        tk.Label(
            stage_frame,
            text=f"📊 {content['stages']}",
            font=('맑은 고딕', 11, 'bold'),
            bg='#ECF0F1',
            fg='#16A085'
        ).pack(pady=10)

        # 시작 버튼
        start_btn = tk.Button(
            left_frame,
            text="▶ 시작하기",
            command=content['command'],
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 16, 'bold'),
            relief=tk.RAISED,
            borderwidth=4,
            cursor='hand2',
            width=20,
            height=2
        )
        start_btn.pack(pady=20)

        # 오른쪽: 미리보기 영역
        right_frame = tk.Frame(self.start_content_frame, bg='#F8F9FA')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=20, pady=20)

        tk.Label(
            right_frame,
            text="미리보기",
            font=('맑은 고딕', 14, 'bold'),
            bg='#F8F9FA',
            fg='#2C3E50'
        ).pack(pady=10)

        # 간단한 키보드 미리보기 (이미지 대신 텍스트로 표시)
        preview_canvas = tk.Canvas(right_frame, width=400, height=200, bg='#34495E', relief=tk.SUNKEN, borderwidth=3)
        preview_canvas.pack(pady=10)

        preview_canvas.create_text(
            200, 100,
            text=f"{content['icon']}\n{content['title']}",
            font=('맑은 고딕', 24, 'bold'),
            fill='white',
            justify=tk.CENTER
        )

        # 팁
        tip_frame = tk.Frame(right_frame, bg='#FFF9C4', relief=tk.RAISED, borderwidth=2)
        tip_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            tip_frame,
            text="💡 Tip",
            font=('맑은 고딕', 11, 'bold'),
            bg='#FFF9C4',
            fg='#F39C12'
        ).pack(anchor=tk.W, padx=10, pady=(5, 0))

        tips = {
            '자리연습': '올바른 손가락 위치를 익히면\n타이핑 속도가 2배 빨라집니다!',
            '낱말연습': '자주 사용하는 단어부터\n연습하는 것이 효과적입니다!',
            '짧은글연습': '문장 부호도 정확하게\n입력하는 습관을 기르세요!',
            '긴글연습': '긴 글을 칠 때는 자세와\n손목 위치에 주의하세요!',
            '필사': '좋아하는 책이나 명언을\n필사해보세요!',
            '산성비': '처음엔 느리게, 정확하게\n입력하는 것이 중요합니다!',
            '침략자': '리듬감 있게 입력하면\n더 높은 점수를 얻을 수 있습니다!',
            '자원캐기': '희귀 자원은 높은 점수를\n제공합니다!',
            '케이크던지기': '타겟의 움직임을 예측하여\n미리 단어를 입력하세요!',
            '해상구조SOS': '시간 관리가 생명입니다!\n빠르고 정확하게!',
            '맞춤법퀴즈': '틀린 문제는 꼭 복습하세요!',
            '초성퀴즈': '힌트를 적극 활용하세요!'
        }

        tk.Label(
            tip_frame,
            text=tips.get(tab_name, '꾸준한 연습이 실력 향상의 지름길입니다!'),
            font=('맑은 고딕', 10),
            bg='#FFF9C4',
            fg='#34495E',
            justify=tk.LEFT
        ).pack(anchor=tk.W, padx=10, pady=(0, 5))

    def show_welcome_screen(self):
        """시작 화면"""
        self.show_start_menu()

    def clear_main_container(self):
        """메인 컨테이너 초기화"""
        for widget in self.main_container.winfo_children():
            widget.destroy()

        if self.current_mode:
            self.current_mode = None

    def start_mode(self, mode_class, mode_name):
        """연습/게임 모드 시작"""
        self.clear_main_container()
        self.in_game = True

        # 상단 헤더 (뒤로가기 버튼 포함)
        header_frame = tk.Frame(self.main_container, bg='#2C3E50', height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        # 뒤로가기 버튼
        back_btn = tk.Button(
            header_frame,
            text='← 메인 메뉴로',
            command=self.show_start_menu,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            width=15
        )
        back_btn.pack(side=tk.LEFT, padx=20, pady=10)

        # 모드 제목
        tk.Label(
            header_frame,
            text=mode_name,
            font=('맑은 고딕', 18, 'bold'),
            bg='#2C3E50',
            fg='white'
        ).pack(side=tk.LEFT, expand=True)

        # 콘텐츠 프레임
        content_frame = tk.Frame(self.main_container, bg='#ECF0F1')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 모드 인스턴스 생성
        self.current_mode = mode_class(content_frame)

    # 연습 모드 시작 메서드들
    def start_position_practice(self):
        self.start_mode(PositionPractice, '⌨️ 자리 연습')

    def start_word_practice(self):
        self.start_mode(WordPractice, '📝 낱말 연습')

    def start_short_text(self):
        self.start_mode(ShortTextPractice, '📄 짧은 글 연습')

    def start_long_text(self):
        self.start_mode(LongTextPractice, '📚 긴 글 연습')

    def start_transcription(self):
        self.start_mode(TranscriptionMode, '✍️ 필사 연습')

    # 게임 시작 메서드들
    def start_acid_rain(self):
        self.start_mode(AcidRainGame, '☔ 산성비 게임')

    def start_invaders(self):
        self.start_mode(InvadersGame, '👾 침략자 게임')

    def start_mining(self):
        self.start_mode(MiningGame, '⛏️ 자원 캐기 게임')

    def start_cake_throw(self):
        self.start_mode(CakeThrowGame, '🎂 케이크 던지기 게임')

    def start_maritime_sos(self):
        self.start_mode(MaritimeSOSGame, '🚢 해상 구조 SOS 게임')

    # 퀴즈 시작 메서드들
    def start_spelling_quiz(self):
        self.start_mode(SpellingQuiz, '📖 맞춤법 퀴즈')

    def start_choseong_quiz(self):
        self.start_mode(ChoSeongQuiz, '🔤 초성 퀴즈')


def main():
    root = tk.Tk()
    app = TypingPracticeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
