"""
새로운 기능들: 리더보드, 업적, 통계 대시보드, 약점 분석, 일일 목표
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import random


class LeaderboardWindow:
    """리더보드/랭킹 시스템"""

    def __init__(self, parent, database, user_id):
        self.window = tk.Toplevel(parent)
        self.window.title("리더보드")
        self.window.geometry("900x700")
        self.window.configure(bg='#E8F4F8')
        self.window.transient(parent)

        self.db = database
        self.user_id = user_id

        self.create_widgets()
        self.load_leaderboard()

    def create_widgets(self):
        # 헤더
        header_frame = tk.Frame(self.window, bg='#3498DB', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text='🏆',
            font=('맑은 고딕', 40),
            bg='#3498DB'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="리더보드",
            font=('맑은 고딕', 20, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 탭 프레임
        tab_frame = tk.Frame(self.window, bg='#E8F4F8')
        tab_frame.pack(fill=tk.X, padx=20, pady=10)

        self.current_tab = tk.StringVar(value='전체')

        tabs = ['전체', '자리연습', '낱말연습', '짧은글연습', '긴글연습', '산성비', '침략자', '자원캐기']

        for tab in tabs:
            btn = tk.Button(
                tab_frame,
                text=tab,
                command=lambda t=tab: self.change_tab(t),
                bg='#3498DB' if tab == '전체' else '#95A5A6',
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                relief=tk.RAISED,
                borderwidth=2,
                cursor='hand2',
                width=10
            )
            btn.pack(side=tk.LEFT, padx=2)

        # 콘텐츠 프레임
        content_frame = tk.Frame(self.window, bg='white', relief=tk.RAISED, borderwidth=3)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 스크롤 가능한 캔버스
        canvas = tk.Canvas(content_frame, bg='white', highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='white')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 닫기 버튼
        close_btn = tk.Button(
            self.window,
            text="닫기",
            command=self.window.destroy,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            width=15
        )
        close_btn.pack(pady=10)

    def change_tab(self, tab_name):
        self.current_tab.set(tab_name)
        self.load_leaderboard()

    def load_leaderboard(self):
        # 기존 위젯 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tab = self.current_tab.get()

        if tab == '전체':
            records = self.db.get_leaderboard(mode_name=None, limit=50)
            columns = ['순위', '사용자명', '총 점수', '총 연습시간']
        else:
            records = self.db.get_leaderboard(mode_name=tab, limit=50)
            columns = ['순위', '사용자명', '최고 점수', '최고 정확도', '최고 속도']

        # 헤더
        header_frame = tk.Frame(self.scrollable_frame, bg='#3498DB')
        header_frame.pack(fill=tk.X, padx=15, pady=(10, 0))

        for i, col in enumerate(columns):
            width = 8 if i == 0 else 15 if i == 1 else 12
            tk.Label(
                header_frame,
                text=col,
                font=('맑은 고딕', 10, 'bold'),
                bg='#3498DB',
                fg='white',
                width=width,
                anchor=tk.W if i == 1 else tk.CENTER
            ).pack(side=tk.LEFT, padx=5, pady=5)

        # 데이터
        for rank, record in enumerate(records, 1):
            bg_color = '#FFD700' if rank == 1 else '#C0C0C0' if rank == 2 else '#CD7F32' if rank == 3 else '#F8F9FA' if rank % 2 == 0 else 'white'

            row_frame = tk.Frame(self.scrollable_frame, bg=bg_color, relief=tk.RAISED, borderwidth=1)
            row_frame.pack(fill=tk.X, padx=15, pady=1)

            # 순위
            rank_text = '🥇' if rank == 1 else '🥈' if rank == 2 else '🥉' if rank == 3 else str(rank)
            tk.Label(
                row_frame,
                text=rank_text,
                font=('맑은 고딕', 11, 'bold'),
                bg=bg_color,
                width=8
            ).pack(side=tk.LEFT, padx=5)

            if tab == '전체':
                tk.Label(row_frame, text=record['username'], font=('맑은 고딕', 10), bg=bg_color, width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
                tk.Label(row_frame, text=f"{record['total_score']:,}", font=('맑은 고딕', 10), bg=bg_color, width=12).pack(side=tk.LEFT, padx=5)
                tk.Label(row_frame, text=f"{record['total_practice_time']}분", font=('맑은 고딕', 10), bg=bg_color, width=12).pack(side=tk.LEFT, padx=5)
            else:
                tk.Label(row_frame, text=record['username'], font=('맑은 고딕', 10), bg=bg_color, width=15, anchor=tk.W).pack(side=tk.LEFT, padx=5)
                tk.Label(row_frame, text=f"{record['high_score']:,}", font=('맑은 고딕', 10), bg=bg_color, width=12).pack(side=tk.LEFT, padx=5)
                tk.Label(row_frame, text=f"{record['best_accuracy']:.1f}%", font=('맑은 고딕', 10), bg=bg_color, width=12).pack(side=tk.LEFT, padx=5)
                tk.Label(row_frame, text=f"{record['best_speed']}타/분", font=('맑은 고딕', 10), bg=bg_color, width=12).pack(side=tk.LEFT, padx=5)


class AchievementsWindow:
    """업적 시스템"""

    # 모든 가능한 업적 정의
    ALL_ACHIEVEMENTS = [
        {"name": "첫 발자국", "desc": "첫 연습을 완료하였습니다", "icon": "👣", "condition": "연습 1회 완료"},
        {"name": "타자 초보", "desc": "총 점수 1000점 달성", "icon": "🌱", "condition": "총 점수 1000점"},
        {"name": "타자 고수", "desc": "총 점수 10000점 달성", "icon": "🌟", "condition": "총 점수 10000점"},
        {"name": "타자 마스터", "desc": "총 점수 50000점 달성", "icon": "👑", "condition": "총 점수 50000점"},
        {"name": "연습벌레", "desc": "총 1시간 이상 연습", "icon": "🐛", "condition": "총 연습 시간 60분"},
        {"name": "끈기왕", "desc": "총 10시간 이상 연습", "icon": "💪", "condition": "총 연습 시간 600분"},
        {"name": "일주일 연속", "desc": "7일 연속 로그인", "icon": "🔥", "condition": "7일 연속 로그인"},
        {"name": "한 달 연속", "desc": "30일 연속 로그인", "icon": "🏆", "condition": "30일 연속 로그인"},
        {"name": "완벽주의자", "desc": "정확도 100% 달성", "icon": "💯", "condition": "정확도 100%"},
        {"name": "속도광", "desc": "600 CPM 이상 달성", "icon": "⚡", "condition": "600 CPM 이상"},
    ]

    def __init__(self, parent, database, user_id):
        self.window = tk.Toplevel(parent)
        self.window.title("업적")
        self.window.geometry("800x700")
        self.window.configure(bg='#E8F4F8')
        self.window.transient(parent)

        self.db = database
        self.user_id = user_id

        self.create_widgets()
        self.load_achievements()

    def create_widgets(self):
        # 헤더
        header_frame = tk.Frame(self.window, bg='#9B59B6', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text='🎖️',
            font=('맑은 고딕', 40),
            bg='#9B59B6'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="업적",
            font=('맑은 고딕', 20, 'bold'),
            bg='#9B59B6',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 진행도 표시
        self.progress_label = tk.Label(
            header_frame,
            text="",
            font=('맑은 고딕', 12, 'bold'),
            bg='#9B59B6',
            fg='#FFEB3B'
        )
        self.progress_label.pack(side=tk.RIGHT, padx=20)

        # 스크롤 가능한 콘텐츠
        canvas = tk.Canvas(self.window, bg='#E8F4F8', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#E8F4F8')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        # 닫기 버튼
        close_btn = tk.Button(
            self.window,
            text="닫기",
            command=self.window.destroy,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            width=15
        )
        close_btn.pack(pady=10)

    def load_achievements(self):
        # 기존 위젯 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 사용자가 달성한 업적 가져오기
        unlocked_achievements = self.db.get_achievements(self.user_id)
        unlocked_names = {ach['achievement_name'] for ach in unlocked_achievements}

        # 진행도 업데이트
        total = len(self.ALL_ACHIEVEMENTS)
        unlocked_count = len(unlocked_names)
        self.progress_label.config(text=f"달성: {unlocked_count}/{total}")

        # 모든 업적 표시
        for ach in self.ALL_ACHIEVEMENTS:
            is_unlocked = ach['name'] in unlocked_names

            frame = tk.Frame(
                self.scrollable_frame,
                bg='white' if is_unlocked else '#D5D8DC',
                relief=tk.RAISED,
                borderwidth=3
            )
            frame.pack(fill=tk.X, pady=5)

            # 아이콘
            icon_label = tk.Label(
                frame,
                text=ach['icon'] if is_unlocked else '🔒',
                font=('맑은 고딕', 40),
                bg=frame['bg']
            )
            icon_label.pack(side=tk.LEFT, padx=20, pady=10)

            # 정보
            info_frame = tk.Frame(frame, bg=frame['bg'])
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

            tk.Label(
                info_frame,
                text=ach['name'],
                font=('맑은 고딕', 14, 'bold'),
                bg=frame['bg'],
                fg='#2C3E50' if is_unlocked else '#7F8C8D'
            ).pack(anchor=tk.W)

            tk.Label(
                info_frame,
                text=ach['desc'],
                font=('맑은 고딕', 10),
                bg=frame['bg'],
                fg='#34495E' if is_unlocked else '#95A5A6'
            ).pack(anchor=tk.W)

            tk.Label(
                info_frame,
                text=f"조건: {ach['condition']}",
                font=('맑은 고딕', 9),
                bg=frame['bg'],
                fg='#7F8C8D'
            ).pack(anchor=tk.W, pady=(5, 0))

            # 달성 시간
            if is_unlocked:
                for unlocked_ach in unlocked_achievements:
                    if unlocked_ach['achievement_name'] == ach['name']:
                        achieved_time = unlocked_ach['achieved_at'][:16]
                        tk.Label(
                            info_frame,
                            text=f"달성일: {achieved_time}",
                            font=('맑은 고딕', 8),
                            bg=frame['bg'],
                            fg='#16A085'
                        ).pack(anchor=tk.W)
                        break


class StatisticsWindow:
    """통계 대시보드 (matplotlib 사용)"""

    def __init__(self, parent, database, user_id):
        self.window = tk.Toplevel(parent)
        self.window.title("통계 대시보드")
        self.window.geometry("1000x800")
        self.window.configure(bg='#E8F4F8')
        self.window.transient(parent)

        self.db = database
        self.user_id = user_id

        self.create_widgets()
        self.load_statistics()

    def create_widgets(self):
        # 헤더
        header_frame = tk.Frame(self.window, bg='#16A085', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text='📊',
            font=('맑은 고딕', 40),
            bg='#16A085'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="통계 대시보드",
            font=('맑은 고딕', 20, 'bold'),
            bg='#16A085',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 스크롤 가능한 콘텐츠
        canvas = tk.Canvas(self.window, bg='#E8F4F8', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#E8F4F8')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        # 닫기 버튼
        close_btn = tk.Button(
            self.window,
            text="닫기",
            command=self.window.destroy,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            width=15
        )
        close_btn.pack(pady=10)

    def load_statistics(self):
        # 기존 위젯 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            # 최근 7일 연습 기록
            history = self.db.get_practice_history(self.user_id, days=7)

            if history:
                self.create_practice_history_chart(history)

            # 모드별 분포
            mode_dist = self.db.get_mode_distribution(self.user_id)

            if mode_dist:
                self.create_mode_distribution_chart(mode_dist)

        except Exception as e:
            tk.Label(
                self.scrollable_frame,
                text=f"통계 로드 중 오류: {str(e)}",
                font=('맑은 고딕', 12),
                bg='#E8F4F8',
                fg='red'
            ).pack(pady=20)

    def create_practice_history_chart(self, history):
        """최근 7일 연습 기록 차트"""
        frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.X, pady=10)

        tk.Label(
            frame,
            text="📈 최근 7일 연습 기록",
            font=('맑은 고딕', 14, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(pady=10)

        fig = Figure(figsize=(9, 4), facecolor='white')

        # 속도 차트
        ax1 = fig.add_subplot(121)
        dates = [h['practice_date'][-5:] for h in reversed(history)]  # MM-DD 형식
        speeds = [h['avg_speed'] or 0 for h in reversed(history)]

        ax1.plot(dates, speeds, marker='o', linewidth=2, markersize=8, color='#3498DB')
        ax1.set_title('평균 타수 (CPM)', fontsize=12, pad=10)
        ax1.set_xlabel('날짜')
        ax1.set_ylabel('타수')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)

        # 정확도 차트
        ax2 = fig.add_subplot(122)
        accuracies = [h['avg_accuracy'] or 0 for h in reversed(history)]

        ax2.plot(dates, accuracies, marker='s', linewidth=2, markersize=8, color='#E74C3C')
        ax2.set_title('평균 정확도 (%)', fontsize=12, pad=10)
        ax2.set_xlabel('날짜')
        ax2.set_ylabel('정확도')
        ax2.grid(True, alpha=0.3)
        ax2.tick_params(axis='x', rotation=45)
        ax2.set_ylim([0, 105])

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10)

    def create_mode_distribution_chart(self, mode_dist):
        """모드별 연습 분포 차트"""
        frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.X, pady=10)

        tk.Label(
            frame,
            text="📊 모드별 연습 분포",
            font=('맑은 고딕', 14, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(pady=10)

        fig = Figure(figsize=(9, 4), facecolor='white')

        # 횟수 파이 차트
        ax1 = fig.add_subplot(121)
        labels = [m['mode_name'] for m in mode_dist[:6]]  # 상위 6개만
        sizes = [m['count'] for m in mode_dist[:6]]
        colors = ['#3498DB', '#E74C3C', '#F39C12', '#9B59B6', '#1ABC9C', '#95A5A6']

        ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax1.set_title('연습 횟수', fontsize=12, pad=10)

        # 시간 파이 차트
        ax2 = fig.add_subplot(122)
        time_labels = [m['mode_name'] for m in mode_dist[:6]]
        time_sizes = [m['total_time'] for m in mode_dist[:6]]

        ax2.pie(time_sizes, labels=time_labels, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title('연습 시간 (분)', fontsize=12, pad=10)

        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10, padx=10)


class WeaknessAnalysisWindow:
    """약점 분석 기능"""

    def __init__(self, parent, database, user_id):
        self.window = tk.Toplevel(parent)
        self.window.title("약점 분석")
        self.window.geometry("900x700")
        self.window.configure(bg='#E8F4F8')
        self.window.transient(parent)

        self.db = database
        self.user_id = user_id

        self.create_widgets()
        self.load_analysis()

    def create_widgets(self):
        # 헤더
        header_frame = tk.Frame(self.window, bg='#E67E22', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text='🎯',
            font=('맑은 고딕', 40),
            bg='#E67E22'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="약점 분석",
            font=('맑은 고딕', 20, 'bold'),
            bg='#E67E22',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 스크롤 가능한 콘텐츠
        canvas = tk.Canvas(self.window, bg='#E8F4F8', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg='#E8F4F8')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        # 닫기 버튼
        close_btn = tk.Button(
            self.window,
            text="닫기",
            command=self.window.destroy,
            bg='#E74C3C',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            relief=tk.RAISED,
            borderwidth=2,
            cursor='hand2',
            width=15
        )
        close_btn.pack(pady=10)

    def load_analysis(self):
        # 기존 위젯 제거
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # 약한 키 (정확도 낮은 키)
        weak_keys = self.db.get_weak_keys(self.user_id, limit=10)

        if weak_keys:
            self.create_weak_keys_section(weak_keys)
        else:
            tk.Label(
                self.scrollable_frame,
                text="아직 데이터가 충분하지 않습니다.\n더 많이 연습하면 분석 결과를 볼 수 있습니다!",
                font=('맑은 고딕', 12),
                bg='#E8F4F8',
                fg='#7F8C8D',
                justify=tk.CENTER
            ).pack(pady=50)
            return

        # 느린 키
        slow_keys = self.db.get_slow_keys(self.user_id, limit=10)

        if slow_keys:
            self.create_slow_keys_section(slow_keys)

    def create_weak_keys_section(self, weak_keys):
        """약한 키 섹션"""
        frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.X, pady=10)

        tk.Label(
            frame,
            text="❌ 자주 틀리는 키 TOP 10",
            font=('맑은 고딕', 14, 'bold'),
            bg='white',
            fg='#E74C3C'
        ).pack(pady=10)

        # 헤더
        header = tk.Frame(frame, bg='#ECF0F1')
        header.pack(fill=tk.X, padx=15, pady=(5, 0))

        tk.Label(header, text="키", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="총 입력", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="정확도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="오류 횟수", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)

        # 데이터
        for i, key in enumerate(weak_keys):
            bg_color = '#FFF5F5' if i % 2 == 0 else 'white'
            row = tk.Frame(frame, bg=bg_color)
            row.pack(fill=tk.X, padx=15, pady=1)

            tk.Label(row, text=key['key_char'], font=('맑은 고딕', 12, 'bold'), bg=bg_color, width=8).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=str(key['total_presses']), font=('맑은 고딕', 10), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=f"{key['accuracy']:.1f}%", font=('맑은 고딕', 10), bg=bg_color, fg='#E74C3C', width=10).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=str(key['incorrect_presses']), font=('맑은 고딕', 10), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="", bg='white').pack(pady=5)

    def create_slow_keys_section(self, slow_keys):
        """느린 키 섹션"""
        frame = tk.Frame(self.scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        frame.pack(fill=tk.X, pady=10)

        tk.Label(
            frame,
            text="🐢 느린 키 TOP 10",
            font=('맑은 고딕', 14, 'bold'),
            bg='white',
            fg='#F39C12'
        ).pack(pady=10)

        # 헤더
        header = tk.Frame(frame, bg='#ECF0F1')
        header.pack(fill=tk.X, padx=15, pady=(5, 0))

        tk.Label(header, text="키", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="총 입력", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="평균 시간", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)
        tk.Label(header, text="정확도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT, padx=5)

        # 데이터
        for i, key in enumerate(slow_keys):
            bg_color = '#FFFBF0' if i % 2 == 0 else 'white'
            row = tk.Frame(frame, bg=bg_color)
            row.pack(fill=tk.X, padx=15, pady=1)

            tk.Label(row, text=key['key_char'], font=('맑은 고딕', 12, 'bold'), bg=bg_color, width=8).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=str(key['total_presses']), font=('맑은 고딕', 10), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=f"{key['avg_time']:.3f}s", font=('맑은 고딕', 10), bg=bg_color, fg='#F39C12', width=10).pack(side=tk.LEFT, padx=5)
            tk.Label(row, text=f"{key['accuracy']:.1f}%", font=('맑은 고딕', 10), bg=bg_color, width=10).pack(side=tk.LEFT, padx=5)

        tk.Label(frame, text="", bg='white').pack(pady=5)


class DailyGoalWidget(tk.Frame):
    """일일 목표 위젯 (메인 화면에 표시)"""

    def __init__(self, parent, database, user_id):
        super().__init__(parent, bg='white', relief=tk.RAISED, borderwidth=3)

        self.db = database
        self.user_id = user_id

        self.create_widgets()
        self.load_goal()

    def create_widgets(self):
        # 제목
        title_frame = tk.Frame(self, bg='#3498DB')
        title_frame.pack(fill=tk.X)

        tk.Label(
            title_frame,
            text="📅 오늘의 목표",
            font=('맑은 고딕', 12, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(pady=5)

        # 목표 정보
        self.goal_label = tk.Label(
            self,
            text="",
            font=('맑은 고딕', 10),
            bg='white',
            justify=tk.LEFT
        )
        self.goal_label.pack(pady=10, padx=10, anchor=tk.W)

        # 진행률 바
        self.progress_frame = tk.Frame(self, bg='white')
        self.progress_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(self.progress_frame, text="시간:", font=('맑은 고딕', 9), bg='white').pack(anchor=tk.W)
        self.time_progress_bar = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.time_progress_bar.pack(fill=tk.X, pady=2)

        tk.Label(self.progress_frame, text="점수:", font=('맑은 고딕', 9), bg='white').pack(anchor=tk.W, pady=(5, 0))
        self.score_progress_bar = ttk.Progressbar(self.progress_frame, length=200, mode='determinate')
        self.score_progress_bar.pack(fill=tk.X, pady=2)

        # 설정 버튼
        ttk.Button(
            self,
            text="목표 설정",
            command=self.set_goal_dialog
        ).pack(pady=5)

    def load_goal(self):
        """목표 로드"""
        if not self.user_id:
            return

        goal = self.db.get_daily_goal(self.user_id)

        if goal:
            target_time = goal['target_time']
            target_score = goal['target_score']
            achieved_time = goal['achieved_time']
            achieved_score = goal['achieved_score']
            completed = goal['completed']

            self.goal_label.config(
                text=f"목표: {target_time}분 연습, {target_score}점 획득\n"
                     f"달성: {achieved_time}분 / {achieved_score}점\n"
                     f"{'✅ 목표 달성!' if completed else '🔥 화이팅!'}"
            )

            # 진행률 바 업데이트
            time_percent = min(100, (achieved_time / target_time * 100) if target_time > 0 else 0)
            score_percent = min(100, (achieved_score / target_score * 100) if target_score > 0 else 0)

            self.time_progress_bar['value'] = time_percent
            self.score_progress_bar['value'] = score_percent

    def set_goal_dialog(self):
        """목표 설정 다이얼로그"""
        dialog = tk.Toplevel(self)
        dialog.title("목표 설정")
        dialog.geometry("300x200")
        dialog.configure(bg='#E8F4F8')
        dialog.transient(self)
        dialog.grab_set()

        tk.Label(
            dialog,
            text="일일 목표 설정",
            font=('맑은 고딕', 14, 'bold'),
            bg='#E8F4F8'
        ).pack(pady=10)

        # 시간 목표
        time_frame = tk.Frame(dialog, bg='#E8F4F8')
        time_frame.pack(pady=5)

        tk.Label(time_frame, text="연습 시간 (분):", font=('맑은 고딕', 10), bg='#E8F4F8').pack(side=tk.LEFT, padx=5)
        time_entry = tk.Entry(time_frame, font=('맑은 고딕', 10), width=10)
        time_entry.pack(side=tk.LEFT)
        time_entry.insert(0, "30")

        # 점수 목표
        score_frame = tk.Frame(dialog, bg='#E8F4F8')
        score_frame.pack(pady=5)

        tk.Label(score_frame, text="목표 점수:", font=('맑은 고딕', 10), bg='#E8F4F8').pack(side=tk.LEFT, padx=5)
        score_entry = tk.Entry(score_frame, font=('맑은 고딕', 10), width=10)
        score_entry.pack(side=tk.LEFT)
        score_entry.insert(0, "100")

        def save_goal():
            try:
                target_time = int(time_entry.get())
                target_score = int(score_entry.get())

                if target_time <= 0 or target_score <= 0:
                    messagebox.showerror("오류", "목표는 0보다 커야 합니다.")
                    return

                self.db.set_daily_goal_targets(self.user_id, target_time, target_score)
                self.load_goal()
                dialog.destroy()
                messagebox.showinfo("성공", "목표가 설정되었습니다!")
            except ValueError:
                messagebox.showerror("오류", "올바른 숫자를 입력하세요.")

        ttk.Button(dialog, text="저장", command=save_goal).pack(pady=20)
