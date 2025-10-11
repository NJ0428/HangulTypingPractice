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
from auth import AuthScreen
from database import Database
from features import (
    LeaderboardWindow, AchievementsWindow, StatisticsWindow,
    WeaknessAnalysisWindow, DailyGoalWidget
)
from advanced_features import (
    ThemeManager, ThemeSelectorDialog, CustomPracticeMode,
    TimeAttackMode, SoundManager
)


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

        # 데이터베이스
        self.db = Database()

        # 사용자 정보
        self.user_id = None
        self.user_name = "손님"
        self.user_score = 0
        self.login_streak = 0

        # 현재 모드
        self.current_mode = None
        self.in_game = False  # 게임/연습 중인지 여부

        # 소리 관리자
        self.sound_manager = SoundManager()

        # 테마
        self.current_theme = 'light'

        # 로그인 화면 표시
        self.show_auth_screen()

    def show_auth_screen(self):
        """로그인/회원가입 화면 표시"""
        AuthScreen(self.root, self.on_login_success)

    def on_login_success(self, user_info):
        """로그인 성공 시 호출되는 콜백"""
        self.user_id = user_info.get('user_id')
        self.user_name = user_info.get('username', '손님')
        self.user_score = user_info.get('total_score', 0)

        # 로그인 스트릭 업데이트
        if self.user_id:
            self.db.update_login_streak(self.user_id)

            # 업적 체크
            unlocked = self.db.check_achievements(self.user_id)
            if unlocked:
                self.sound_manager.play_achievement_sound()
                from tkinter import messagebox
                messagebox.showinfo("업적 달성!", f"새로운 업적을 달성했습니다:\n" + "\n".join(unlocked))

            # 테마 로드
            self.current_theme = self.db.get_user_theme(self.user_id)

            # 사용자 설정 로드
            settings = self.db.get_user_settings(self.user_id)
            if settings:
                self.sound_manager.set_enabled(settings['sound_enabled'])
                self.sound_manager.set_volume(settings['volume'])

            # 스트릭 정보 가져오기
            user_full_info = self.db.get_user_info(self.user_id)
            if user_full_info:
                self.login_streak = user_full_info.get('login_streak', 0)

        # 메인 UI 생성
        self.create_ui()

    def create_ui(self):
        """UI 구성"""
        # 메인 컨테이너
        self.main_container = tk.Frame(self.root, bg='#E8F4F8')
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # 시작 화면 표시
        self.show_start_menu()

    def show_profile_dialog(self):
        """프로필 정보 다이얼로그 표시"""
        # 새 창 생성
        profile_window = tk.Toplevel(self.root)
        profile_window.title("프로필 정보")
        profile_window.geometry("700x600")
        profile_window.configure(bg='#E8F4F8')
        profile_window.transient(self.root)  # 부모 창 위에 표시
        profile_window.grab_set()  # 모달 다이얼로그로 설정

        # 헤더
        header_frame = tk.Frame(profile_window, bg='#3498DB', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text='👤',
            font=('맑은 고딕', 40),
            bg='#3498DB'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="프로필 정보",
            font=('맑은 고딕', 20, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 메인 콘텐츠 스크롤 프레임
        canvas = tk.Canvas(profile_window, bg='#E8F4F8', highlightthickness=0)
        scrollbar = tk.Scrollbar(profile_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#E8F4F8')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 사용자 정보 가져오기
        if self.user_id:
            user_info = self.db.get_user_info(self.user_id)
            recent_records = self.db.get_user_records(self.user_id, limit=5)
            high_scores = self.db.get_high_scores(self.user_id)
        else:
            user_info = None
            recent_records = []
            high_scores = []

        # 기본 정보 섹션
        info_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        info_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(
            info_frame,
            text="📋 기본 정보",
            font=('맑은 고딕', 14, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, padx=15, pady=(10, 5))

        if user_info:
            info_items = [
                ('사용자명', user_info.get('username', '손님')),
                ('이메일', user_info.get('email', '미등록') or '미등록'),
                ('총 점수', f"{user_info.get('total_score', 0):,}점"),
                ('총 연습 시간', f"{user_info.get('total_practice_time', 0)}분"),
                ('가입일', user_info.get('created_at', 'N/A')[:10] if user_info.get('created_at') else 'N/A'),
                ('마지막 로그인', user_info.get('last_login', 'N/A')[:16] if user_info.get('last_login') else 'N/A')
            ]
        else:
            info_items = [
                ('사용자명', self.user_name),
                ('총 점수', f"{self.user_score:,}점")
            ]

        for label, value in info_items:
            item_frame = tk.Frame(info_frame, bg='white')
            item_frame.pack(fill=tk.X, padx=15, pady=2)

            tk.Label(
                item_frame,
                text=f"{label}:",
                font=('맑은 고딕', 11),
                bg='white',
                fg='#7F8C8D',
                width=15,
                anchor=tk.W
            ).pack(side=tk.LEFT)

            tk.Label(
                item_frame,
                text=str(value),
                font=('맑은 고딕', 11, 'bold'),
                bg='white',
                fg='#2C3E50'
            ).pack(side=tk.LEFT, padx=10)

        # 최고 기록 섹션
        if high_scores:
            high_score_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
            high_score_frame.pack(fill=tk.X, padx=20, pady=10)

            tk.Label(
                high_score_frame,
                text="🏆 최고 기록",
                font=('맑은 고딕', 14, 'bold'),
                bg='white',
                fg='#2C3E50'
            ).pack(anchor=tk.W, padx=15, pady=(10, 5))

            # 헤더
            header = tk.Frame(high_score_frame, bg='#ECF0F1')
            header.pack(fill=tk.X, padx=15, pady=(5, 0))

            tk.Label(header, text="모드", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="최고점수", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="최고정확도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="최고속도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)

            # 데이터
            for i, record in enumerate(high_scores[:5]):
                bg_color = '#F8F9FA' if i % 2 == 0 else 'white'
                row = tk.Frame(high_score_frame, bg=bg_color)
                row.pack(fill=tk.X, padx=15, pady=1)

                tk.Label(row, text=record['mode_name'], font=('맑은 고딕', 9), bg=bg_color, width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=f"{record['high_score']:,}", font=('맑은 고딕', 9), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=f"{record['best_accuracy']:.1f}%", font=('맑은 고딕', 9), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=f"{record['best_speed']}타/분", font=('맑은 고딕', 9), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)

            tk.Label(high_score_frame, text="", bg='white').pack(pady=5)

        # 최근 연습 기록 섹션
        if recent_records:
            recent_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
            recent_frame.pack(fill=tk.X, padx=20, pady=10)

            tk.Label(
                recent_frame,
                text="📊 최근 연습 기록",
                font=('맑은 고딕', 14, 'bold'),
                bg='white',
                fg='#2C3E50'
            ).pack(anchor=tk.W, padx=15, pady=(10, 5))

            # 헤더
            header = tk.Frame(recent_frame, bg='#ECF0F1')
            header.pack(fill=tk.X, padx=15, pady=(5, 0))

            tk.Label(header, text="모드", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=12, anchor=tk.W).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="점수", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=8).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="정확도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=8).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="속도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=8).pack(side=tk.LEFT, padx=5)
            tk.Label(header, text="날짜", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)

            # 데이터
            for i, record in enumerate(recent_records):
                bg_color = '#F8F9FA' if i % 2 == 0 else 'white'
                row = tk.Frame(recent_frame, bg=bg_color)
                row.pack(fill=tk.X, padx=15, pady=1)

                tk.Label(row, text=record['mode_name'], font=('맑은 고딕', 9), bg=bg_color, width=12, anchor=tk.W).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=f"{record['score']:,}", font=('맑은 고딕', 9), bg=bg_color, width=8).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=f"{record['accuracy']:.1f}%", font=('맑은 고딕', 9), bg=bg_color, width=8).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=f"{record['speed']}타/분", font=('맑은 고딕', 9), bg=bg_color, width=8).pack(side=tk.LEFT, padx=5)
                tk.Label(row, text=record['created_at'][:10], font=('맑은 고딕', 9), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)

            tk.Label(recent_frame, text="", bg='white').pack(pady=5)

        # 빈 공간 (스크롤을 위한)
        tk.Label(scrollable_frame, text="", bg='#E8F4F8').pack(pady=10)

        # 스크롤바 배치
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 닫기 버튼
        close_btn = tk.Button(
            profile_window,
            text="닫기",
            command=profile_window.destroy,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            width=15
        )
        close_btn.pack(pady=10)

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
        user_frame = tk.Frame(header_frame, bg='white', relief=tk.RAISED, borderwidth=2, cursor='hand2')
        user_frame.pack(side=tk.LEFT, padx=20, pady=10)
        # 프로필 클릭 이벤트 바인딩
        user_frame.bind('<Button-1>', lambda e: self.show_profile_dialog())

        user_icon = tk.Label(user_frame, text='👤', font=('맑은 고딕', 30), bg='white', cursor='hand2')
        user_icon.pack(side=tk.LEFT, padx=10)
        user_icon.bind('<Button-1>', lambda e: self.show_profile_dialog())

        user_info_frame = tk.Frame(user_frame, bg='white', cursor='hand2')
        user_info_frame.pack(side=tk.LEFT, padx=10)
        user_info_frame.bind('<Button-1>', lambda e: self.show_profile_dialog())

        user_name_label = tk.Label(user_info_frame, text=self.user_name, font=('맑은 고딕', 12, 'bold'), bg='white', cursor='hand2')
        user_name_label.pack(anchor=tk.W)
        user_name_label.bind('<Button-1>', lambda e: self.show_profile_dialog())

        # 스트릭 표시
        if self.login_streak > 0:
            streak_text = f"🔥 {self.login_streak}일 연속"
            user_score_label = tk.Label(user_info_frame, text=f"{self.user_score} | {streak_text}", font=('맑은 고딕', 11, 'bold'), bg='white', fg='#E67E22', cursor='hand2')
        else:
            user_score_label = tk.Label(user_info_frame, text=f"{self.user_score}", font=('맑은 고딕', 14, 'bold'), bg='white', fg='#E67E22', cursor='hand2')
        user_score_label.pack(anchor=tk.W)
        user_score_label.bind('<Button-1>', lambda e: self.show_profile_dialog())

        # 메인 타이틀 (중앙)
        tk.Label(
            header_frame,
            text="⌨️ 한글/영어 타자 연습 ⌨️",
            font=('맑은 고딕', 20, 'bold'),
            bg='#87CEEB',
            fg='white'
        ).pack(side=tk.LEFT, expand=True)

        # 로그아웃 버튼 (오른쪽)
        if self.user_id is not None:  # 게스트가 아닌 경우에만 표시
            logout_btn = tk.Button(
                header_frame,
                text='로그아웃',
                command=self.logout,
                bg='#E74C3C',
                fg='white',
                font=('맑은 고딕', 10, 'bold'),
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2',
                width=10
            )
            logout_btn.pack(side=tk.RIGHT, padx=20)

        # 메인 콘텐츠 영역
        content_container = tk.Frame(self.main_container, bg='#E8F4F8')
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 왼쪽: 일일 목표 & 기능 버튼
        left_panel = tk.Frame(content_container, bg='#E8F4F8', width=250)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)

        # 일일 목표 위젯
        if self.user_id:
            daily_goal = DailyGoalWidget(left_panel, self.db, self.user_id)
            daily_goal.pack(fill=tk.X, pady=(0, 10))

        # 기능 버튼들
        features_frame = tk.LabelFrame(left_panel, text="기능", font=('맑은 고딕', 11, 'bold'), bg='#E8F4F8')
        features_frame.pack(fill=tk.X, pady=(0, 10))

        feature_buttons = [
            ('🏆 리더보드', self.show_leaderboard, '#F39C12'),
            ('🎖️ 업적', self.show_achievements, '#9B59B6'),
            ('📊 통계', self.show_statistics, '#16A085'),
            ('🎯 약점 분석', self.show_weakness_analysis, '#E67E22'),
            ('⏱️ 타임 어택', self.start_time_attack, '#E74C3C'),
            ('📝 사용자 정의', self.start_custom_practice, '#8E44AD'),
            ('🎨 테마 변경', self.show_theme_selector, '#3498DB'),
            ('⚙️ 설정', self.show_settings, '#95A5A6'),
        ]

        for text, command, color in feature_buttons:
            btn = tk.Button(
                features_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2',
                width=22,
                anchor=tk.W,
                padx=10
            )
            btn.pack(fill=tk.X, padx=5, pady=2)

        # 오른쪽: 기존 탭들
        right_panel = tk.Frame(content_container, bg='#E8F4F8')
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 탭 프레임
        tab_frame = tk.Frame(right_panel, bg='#E8F4F8')
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
        self.start_content_frame = tk.Frame(right_panel, bg='white', relief=tk.RAISED, borderwidth=3)
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

    def logout(self):
        """로그아웃"""
        from tkinter import messagebox
        if messagebox.askyesno("로그아웃", "로그아웃 하시겠습니까?"):
            # 메인 컨테이너 제거
            if hasattr(self, 'main_container'):
                self.main_container.destroy()

            # 사용자 정보 초기화
            self.user_id = None
            self.user_name = "손님"
            self.user_score = 0
            self.login_streak = 0

            # 로그인 화면으로 이동
            self.show_auth_screen()

    # ========== 새 기능 메서드들 ==========
    def show_leaderboard(self):
        """리더보드 표시"""
        LeaderboardWindow(self.root, self.db, self.user_id)

    def show_achievements(self):
        """업적 표시"""
        if not self.user_id:
            from tkinter import messagebox
            messagebox.showwarning("알림", "로그인이 필요한 기능입니다.")
            return
        AchievementsWindow(self.root, self.db, self.user_id)

    def show_statistics(self):
        """통계 대시보드 표시"""
        if not self.user_id:
            from tkinter import messagebox
            messagebox.showwarning("알림", "로그인이 필요한 기능입니다.")
            return
        StatisticsWindow(self.root, self.db, self.user_id)

    def show_weakness_analysis(self):
        """약점 분석 표시"""
        if not self.user_id:
            from tkinter import messagebox
            messagebox.showwarning("알림", "로그인이 필요한 기능입니다.")
            return
        WeaknessAnalysisWindow(self.root, self.db, self.user_id)

    def show_theme_selector(self):
        """테마 선택기 표시"""
        if not self.user_id:
            from tkinter import messagebox
            messagebox.showwarning("알림", "로그인이 필요한 기능입니다.")
            return

        def apply_theme_callback(theme_name):
            self.current_theme = theme_name
            # 테마 적용 (재시작 필요)
            pass

        ThemeSelectorDialog(self.root, self.db, self.user_id, apply_theme_callback)

    def show_settings(self):
        """설정 다이얼로그 표시"""
        if not self.user_id:
            from tkinter import messagebox
            messagebox.showwarning("알림", "로그인이 필요한 기능입니다.")
            return

        # 설정 다이얼로그
        dialog = tk.Toplevel(self.root)
        dialog.title("설정")
        dialog.geometry("400x300")
        dialog.configure(bg='#E8F4F8')
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="⚙️ 설정",
            font=('맑은 고딕', 16, 'bold'),
            bg='#E8F4F8'
        ).pack(pady=20)

        # 소리 설정
        sound_frame = tk.Frame(dialog, bg='#E8F4F8')
        sound_frame.pack(pady=10)

        tk.Label(sound_frame, text="소리 효과:", font=('맑은 고딕', 11), bg='#E8F4F8').pack(side=tk.LEFT, padx=10)

        sound_var = tk.IntVar(value=1 if self.sound_manager.enabled else 0)

        def toggle_sound():
            enabled = sound_var.get() == 1
            self.sound_manager.set_enabled(enabled)
            self.db.update_user_settings(self.user_id, sound_enabled=enabled)
            if enabled:
                self.sound_manager.play_correct_sound()

        tk.Checkbutton(
            sound_frame,
            text="활성화",
            variable=sound_var,
            command=toggle_sound,
            bg='#E8F4F8',
            font=('맑은 고딕', 10)
        ).pack(side=tk.LEFT)

        # 볼륨 설정
        volume_frame = tk.Frame(dialog, bg='#E8F4F8')
        volume_frame.pack(pady=10)

        tk.Label(volume_frame, text="볼륨:", font=('맑은 고딕', 11), bg='#E8F4F8').pack(side=tk.LEFT, padx=10)

        volume_scale = tk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            length=200,
            bg='#E8F4F8'
        )
        volume_scale.set(self.sound_manager.volume)
        volume_scale.pack(side=tk.LEFT)

        def update_volume(val):
            self.sound_manager.set_volume(int(val))
            self.db.update_user_settings(self.user_id, volume=int(val))

        volume_scale.config(command=update_volume)

        # 닫기 버튼
        ttk.Button(dialog, text="닫기", command=dialog.destroy).pack(pady=20)

    def start_time_attack(self):
        """타임 어택 모드 시작"""
        self.start_mode(TimeAttackMode, '⏱️ 타임 어택')

    def start_custom_practice(self):
        """사용자 정의 연습 시작"""
        if not self.user_id:
            from tkinter import messagebox
            messagebox.showwarning("알림", "로그인이 필요한 기능입니다.")
            return

        self.clear_main_container()
        self.in_game = True

        # 상단 헤더
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
            text='📝 사용자 정의 연습',
            font=('맑은 고딕', 18, 'bold'),
            bg='#2C3E50',
            fg='white'
        ).pack(side=tk.LEFT, expand=True)

        # 콘텐츠 프레임
        content_frame = tk.Frame(self.main_container, bg='#ECF0F1')
        content_frame.pack(fill=tk.BOTH, expand=True)

        # 모드 인스턴스 생성
        self.current_mode = CustomPracticeMode(content_frame, self.db, self.user_id)


def main():
    root = tk.Tk()
    app = TypingPracticeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
