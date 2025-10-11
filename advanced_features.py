"""
고급 기능: 실시간 그래프, 테마, 사용자 정의 연습, 타임 어택, 소리 효과
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time
import random
import winsound
import threading
from practice_modes import BasePractice


class RealtimeGraphWidget(tk.Frame):
    """실시간 WPM/CPM 그래프 위젯"""

    def __init__(self, parent):
        super().__init__(parent, bg='white', relief=tk.RAISED, borderwidth=2)

        self.data_points = []  # [(시간, cpm)]
        self.max_points = 30  # 최대 30개 포인트

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self,
            text="⚡ 실시간 타수",
            font=('맑은 고딕', 10, 'bold'),
            bg='white'
        ).pack(pady=5)

        # matplotlib 그래프
        self.fig = Figure(figsize=(5, 2), facecolor='white')
        self.ax = self.fig.add_subplot(111)

        self.ax.set_title('타수 (CPM)', fontsize=10)
        self.ax.set_xlabel('시간 (초)')
        self.ax.set_ylabel('CPM')
        self.ax.grid(True, alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack()

        # 초기 그래프
        self.update_graph()

    def add_data_point(self, elapsed_time, cpm):
        """데이터 포인트 추가"""
        self.data_points.append((elapsed_time, cpm))

        # 최대 포인트 수 제한
        if len(self.data_points) > self.max_points:
            self.data_points.pop(0)

        self.update_graph()

    def update_graph(self):
        """그래프 업데이트"""
        self.ax.clear()

        if self.data_points:
            times = [p[0] for p in self.data_points]
            cpms = [p[1] for p in self.data_points]

            self.ax.plot(times, cpms, marker='o', linewidth=2, markersize=4, color='#3498DB')
            self.ax.fill_between(times, cpms, alpha=0.3, color='#3498DB')

        self.ax.set_title('타수 (CPM)', fontsize=10)
        self.ax.set_xlabel('시간 (초)')
        self.ax.set_ylabel('CPM')
        self.ax.grid(True, alpha=0.3)

        self.fig.tight_layout()
        self.canvas.draw()

    def reset(self):
        """그래프 초기화"""
        self.data_points = []
        self.update_graph()


class ThemeManager:
    """테마 관리자"""

    THEMES = {
        'light': {
            'name': '라이트 모드',
            'bg': '#E8F4F8',
            'fg': '#2C3E50',
            'header_bg': '#3498DB',
            'header_fg': 'white',
            'button_bg': '#3498DB',
            'button_fg': 'white',
            'entry_bg': 'white',
            'entry_fg': 'black',
            'frame_bg': 'white'
        },
        'dark': {
            'name': '다크 모드',
            'bg': '#2C3E50',
            'fg': '#ECF0F1',
            'header_bg': '#34495E',
            'header_fg': '#ECF0F1',
            'button_bg': '#3498DB',
            'button_fg': 'white',
            'entry_bg': '#34495E',
            'entry_fg': '#ECF0F1',
            'frame_bg': '#34495E'
        },
        'ocean': {
            'name': '오션 모드',
            'bg': '#1B4F72',
            'fg': '#EAF2F8',
            'header_bg': '#154360',
            'header_fg': '#EAF2F8',
            'button_bg': '#21618C',
            'button_fg': 'white',
            'entry_bg': '#2874A6',
            'entry_fg': 'white',
            'frame_bg': '#2874A6'
        },
        'forest': {
            'name': '포레스트 모드',
            'bg': '#1D8348',
            'fg': '#E8F8F5',
            'header_bg': '#186A3B',
            'header_fg': '#E8F8F5',
            'button_bg': '#229954',
            'button_fg': 'white',
            'entry_bg': '#27AE60',
            'entry_fg': 'white',
            'frame_bg': '#27AE60'
        },
        'sunset': {
            'name': '선셋 모드',
            'bg': '#78281F',
            'fg': '#FADBD8',
            'header_bg': '#641E16',
            'header_fg': '#FADBD8',
            'button_bg': '#943126',
            'button_fg': 'white',
            'entry_bg': '#A93226',
            'entry_fg': 'white',
            'frame_bg': '#A93226'
        }
    }

    @classmethod
    def get_theme(cls, theme_name):
        """테마 가져오기"""
        return cls.THEMES.get(theme_name, cls.THEMES['light'])

    @classmethod
    def apply_theme(cls, widget, theme_name):
        """위젯에 테마 적용"""
        theme = cls.get_theme(theme_name)

        try:
            widget.configure(bg=theme['bg'])
        except:
            pass

        # 모든 자식 위젯에 재귀적으로 적용
        for child in widget.winfo_children():
            cls._apply_theme_recursive(child, theme)

    @classmethod
    def _apply_theme_recursive(cls, widget, theme):
        """재귀적으로 테마 적용"""
        widget_type = widget.winfo_class()

        try:
            if widget_type in ['Frame', 'Toplevel']:
                widget.configure(bg=theme['bg'])
            elif widget_type == 'Label':
                widget.configure(bg=theme.get('frame_bg', theme['bg']), fg=theme['fg'])
            elif widget_type == 'Button':
                widget.configure(bg=theme['button_bg'], fg=theme['button_fg'])
            elif widget_type == 'Entry':
                widget.configure(bg=theme['entry_bg'], fg=theme['entry_fg'])
            elif widget_type == 'Text':
                widget.configure(bg=theme['entry_bg'], fg=theme['entry_fg'])
            elif widget_type == 'Canvas':
                widget.configure(bg=theme['frame_bg'])
        except:
            pass

        for child in widget.winfo_children():
            cls._apply_theme_recursive(child, theme)


class ThemeSelectorDialog:
    """테마 선택 다이얼로그"""

    def __init__(self, parent, database, user_id, callback=None):
        self.window = tk.Toplevel(parent)
        self.window.title("테마 선택")
        self.window.geometry("500x600")
        self.window.configure(bg='#E8F4F8')
        self.window.transient(parent)
        self.window.grab_set()

        self.db = database
        self.user_id = user_id
        self.callback = callback

        self.create_widgets()

    def create_widgets(self):
        tk.Label(
            self.window,
            text="🎨 테마 선택",
            font=('맑은 고딕', 18, 'bold'),
            bg='#E8F4F8'
        ).pack(pady=20)

        # 테마 버튼들
        for theme_name, theme_data in ThemeManager.THEMES.items():
            frame = tk.Frame(
                self.window,
                bg=theme_data['bg'],
                relief=tk.RAISED,
                borderwidth=3,
                cursor='hand2'
            )
            frame.pack(fill=tk.X, padx=20, pady=5)

            # 클릭 이벤트
            frame.bind('<Button-1>', lambda e, t=theme_name: self.select_theme(t))

            # 테마 이름
            name_label = tk.Label(
                frame,
                text=theme_data['name'],
                font=('맑은 고딕', 14, 'bold'),
                bg=theme_data['header_bg'],
                fg=theme_data['header_fg']
            )
            name_label.pack(fill=tk.X, padx=10, pady=5)
            name_label.bind('<Button-1>', lambda e, t=theme_name: self.select_theme(t))

            # 샘플 텍스트
            sample_label = tk.Label(
                frame,
                text="샘플 텍스트 - 이것이 테마의 모습입니다",
                font=('맑은 고딕', 10),
                bg=theme_data['bg'],
                fg=theme_data['fg']
            )
            sample_label.pack(padx=10, pady=5)
            sample_label.bind('<Button-1>', lambda e, t=theme_name: self.select_theme(t))

    def select_theme(self, theme_name):
        """테마 선택"""
        if self.user_id:
            self.db.update_theme(self.user_id, theme_name)

        if self.callback:
            self.callback(theme_name)

        self.window.destroy()
        messagebox.showinfo("테마 변경", f"테마가 변경되었습니다!\n프로그램을 재시작하면 완전히 적용됩니다.")


class CustomPracticeMode(BasePractice):
    """사용자 정의 연습 모드"""

    def __init__(self, parent, database, user_id):
        self.db = database
        self.user_id = user_id
        self.custom_lists = []
        self.current_word_list = []
        self.current_word_index = 0

        super().__init__(parent)

    def create_widgets(self):
        # 제목
        header_frame = tk.Frame(self, bg='#8E44AD', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="사용자 정의 연습",
            font=('맑은 고딕', 18, 'bold'),
            bg='#8E44AD',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        # 단어 리스트 관리 프레임
        list_frame = tk.LabelFrame(self, text="나만의 단어 리스트", font=('맑은 고딕', 12, 'bold'), bg='#E8F4F8')
        list_frame.pack(fill=tk.BOTH, padx=20, pady=10)

        # 새 리스트 생성
        create_frame = tk.Frame(list_frame, bg='#E8F4F8')
        create_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(create_frame, text="리스트 이름:", font=('맑은 고딕', 10), bg='#E8F4F8').pack(side=tk.LEFT, padx=5)
        self.list_name_entry = tk.Entry(create_frame, font=('맑은 고딕', 10), width=15)
        self.list_name_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(create_frame, text="단어 (쉼표 구분):", font=('맑은 고딕', 10), bg='#E8F4F8').pack(side=tk.LEFT, padx=5)
        self.words_entry = tk.Entry(create_frame, font=('맑은 고딕', 10), width=30)
        self.words_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(create_frame, text="리스트 생성", command=self.create_word_list).pack(side=tk.LEFT, padx=5)

        # 기존 리스트 표시
        self.lists_listbox = tk.Listbox(list_frame, height=5, font=('맑은 고딕', 10))
        self.lists_listbox.pack(fill=tk.X, padx=10, pady=5)

        btn_frame = tk.Frame(list_frame, bg='#E8F4F8')
        btn_frame.pack(pady=5)

        ttk.Button(btn_frame, text="이 리스트로 연습", command=self.start_custom_practice).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="삭제", command=self.delete_word_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="새로고침", command=self.load_word_lists).pack(side=tk.LEFT, padx=5)

        # 연습 영역
        practice_frame = tk.LabelFrame(self, text="연습", font=('맑은 고딕', 12, 'bold'), bg='#ECF0F1')
        practice_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.word_label = tk.Label(
            practice_frame,
            text="단어 리스트를 선택하고 '이 리스트로 연습'을 클릭하세요",
            font=('맑은 고딕', 20, 'bold'),
            fg='#2C3E50',
            bg='#ECF0F1',
            height=3
        )
        self.word_label.pack(pady=20)

        self.input_entry = tk.Entry(practice_frame, font=('맑은 고딕', 16), justify='center', width=30)
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.check_word)

        self.progress_label = tk.Label(practice_frame, text="", font=('맑은 고딕', 10), bg='#ECF0F1')
        self.progress_label.pack(pady=5)

        self.stats_label = tk.Label(practice_frame, text="타수: 0 | 정확도: 100% | 시간: 0초", font=('맑은 고딕', 10), bg='#ECF0F1')
        self.stats_label.pack(pady=5)

        # 단어 리스트 로드
        self.load_word_lists()

    def load_word_lists(self):
        """단어 리스트 로드"""
        if not self.user_id:
            return

        self.custom_lists = self.db.get_custom_word_lists(self.user_id)
        self.lists_listbox.delete(0, tk.END)

        for lst in self.custom_lists:
            self.lists_listbox.insert(tk.END, f"{lst['list_name']} ({len(lst['words'])}개 단어)")

    def create_word_list(self):
        """새 단어 리스트 생성"""
        if not self.user_id:
            messagebox.showerror("오류", "로그인이 필요합니다.")
            return

        list_name = self.list_name_entry.get().strip()
        words_str = self.words_entry.get().strip()

        if not list_name or not words_str:
            messagebox.showerror("오류", "리스트 이름과 단어를 입력하세요.")
            return

        words = [w.strip() for w in words_str.split(',') if w.strip()]

        if len(words) < 3:
            messagebox.showerror("오류", "최소 3개 이상의 단어를 입력하세요.")
            return

        self.db.create_custom_word_list(self.user_id, list_name, words)
        self.load_word_lists()

        self.list_name_entry.delete(0, tk.END)
        self.words_entry.delete(0, tk.END)

        messagebox.showinfo("성공", "단어 리스트가 생성되었습니다!")

    def delete_word_list(self):
        """단어 리스트 삭제"""
        selection = self.lists_listbox.curselection()
        if not selection:
            messagebox.showerror("오류", "삭제할 리스트를 선택하세요.")
            return

        idx = selection[0]
        list_id = self.custom_lists[idx]['list_id']

        if messagebox.askyesno("확인", "정말 삭제하시겠습니까?"):
            self.db.delete_custom_word_list(list_id)
            self.load_word_lists()
            messagebox.showinfo("성공", "리스트가 삭제되었습니다.")

    def start_custom_practice(self):
        """사용자 정의 연습 시작"""
        selection = self.lists_listbox.curselection()
        if not selection:
            messagebox.showerror("오류", "연습할 리스트를 선택하세요.")
            return

        idx = selection[0]
        self.current_word_list = self.custom_lists[idx]['words']
        random.shuffle(self.current_word_list)

        self.current_word_index = 0
        self.typed_chars = 0
        self.errors = 0
        self.start_time = None

        self.show_next_word()

    def show_next_word(self):
        """다음 단어 표시"""
        if self.current_word_index >= len(self.current_word_list):
            self.show_completion()
            return

        word = self.current_word_list[self.current_word_index]
        self.word_label.config(text=word, fg='#2C3E50')
        self.progress_label.config(text=f"{self.current_word_index + 1}/{len(self.current_word_list)}")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

    def check_word(self, event):
        """단어 확인"""
        if not self.start_time:
            self.start_time = time.time()

        if self.current_word_index >= len(self.current_word_list):
            return

        expected = self.current_word_list[self.current_word_index]
        typed = self.input_entry.get()

        self.typed_chars += len(typed)

        if typed == expected:
            self.word_label.config(fg='green')
            self.current_word_index += 1
            self.after(300, self.show_next_word)
        else:
            self.errors += len(expected)
            self.word_label.config(fg='red')
            self.after(300, lambda: self.word_label.config(fg='#2C3E50'))

        self.update_stats()

    def update_stats(self):
        """통계 업데이트"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.stats_label.config(text=f"타수: {cpm} | 정확도: {accuracy}% | 시간: {elapsed}초")

    def show_completion(self):
        """완료"""
        cpm, accuracy, elapsed = self.calculate_stats()
        self.word_label.config(text=f"완료!\n타수: {cpm} CPM\n정확도: {accuracy}%", fg='green')


class TimeAttackMode(BasePractice):
    """타임 어택 모드"""

    TIME_MODES = {
        '1분': 60,
        '3분': 180,
        '5분': 300
    }

    WORDS = [
        '컴퓨터', '키보드', '마우스', '모니터', '프린터', '스캐너', '웹캠', '스피커',
        'computer', 'keyboard', 'mouse', 'monitor', 'printer', 'scanner', 'webcam', 'speaker',
        '프로그램', '소프트웨어', '하드웨어', '네트워크', '인터넷', '데이터',
        'program', 'software', 'hardware', 'network', 'internet', 'data'
    ]

    def __init__(self, parent):
        self.time_limit = 60
        self.time_remaining = 60
        self.score = 0
        self.is_running = False

        super().__init__(parent)

    def create_widgets(self):
        # 제목
        header_frame = tk.Frame(self, bg='#E74C3C', height=80)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="⏱️ 타임 어택",
            font=('맑은 고딕', 18, 'bold'),
            bg='#E74C3C',
            fg='white'
        ).pack(side=tk.LEFT, padx=20)

        # 시간 선택
        mode_frame = tk.Frame(self, bg='#ECF0F1', relief=tk.RAISED, borderwidth=2)
        mode_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(mode_frame, text="제한 시간:", font=('맑은 고딕', 11, 'bold'), bg='#ECF0F1').pack(side=tk.LEFT, padx=10)

        for mode_name, seconds in self.TIME_MODES.items():
            btn = tk.Button(
                mode_frame,
                text=mode_name,
                command=lambda s=seconds: self.set_time_limit(s),
                bg='#3498DB',
                fg='white',
                font=('맑은 고딕', 10, 'bold'),
                width=8,
                relief=tk.RAISED,
                cursor='hand2'
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)

        # 정보 표시
        info_frame = tk.Frame(self, bg='white', relief=tk.RAISED, borderwidth=2)
        info_frame.pack(fill=tk.X, padx=20, pady=10)

        self.time_label = tk.Label(info_frame, text="60초", font=('맑은 고딕', 20, 'bold'), fg='#E74C3C', bg='white')
        self.time_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.score_label = tk.Label(info_frame, text="점수: 0", font=('맑은 고딕', 16, 'bold'), fg='#27AE60', bg='white')
        self.score_label.pack(side=tk.LEFT, padx=20, pady=10)

        self.stats_label = tk.Label(info_frame, text="타수: 0 | 정확도: 100%", font=('맑은 고딕', 12), bg='white')
        self.stats_label.pack(side=tk.LEFT, padx=20, pady=10)

        # 단어 표시
        self.word_label = tk.Label(
            self,
            text="",
            font=('맑은 고딕', 28, 'bold'),
            fg='#2C3E50',
            bg='#ECF0F1',
            height=2
        )
        self.word_label.pack(pady=20)

        # 입력
        self.input_entry = tk.Entry(self, font=('맑은 고딕', 18), justify='center', width=30)
        self.input_entry.pack(pady=10)
        self.input_entry.bind('<Return>', self.check_word)

        # 시작 버튼
        self.start_button = tk.Button(
            self,
            text="▶ 시작",
            command=self.start_game,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 14, 'bold'),
            width=20,
            height=2,
            relief=tk.RAISED,
            cursor='hand2'
        )
        self.start_button.pack(pady=20)

    def set_time_limit(self, seconds):
        """제한 시간 설정"""
        if not self.is_running:
            self.time_limit = seconds
            self.time_remaining = seconds
            self.time_label.config(text=f"{seconds}초")

    def start_game(self):
        """게임 시작"""
        self.is_running = True
        self.score = 0
        self.typed_chars = 0
        self.errors = 0
        self.time_remaining = self.time_limit
        self.start_time = time.time()

        self.start_button.config(state=tk.DISABLED)
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus()

        self.show_next_word()
        self.update_timer()

    def show_next_word(self):
        """다음 단어 표시"""
        if self.is_running:
            word = random.choice(self.WORDS)
            self.word_label.config(text=word, fg='#2C3E50')

    def check_word(self, event):
        """단어 확인"""
        if not self.is_running:
            return

        expected = self.word_label.cget('text')
        typed = self.input_entry.get()

        self.typed_chars += len(typed)

        if typed == expected:
            self.word_label.config(fg='green')
            self.score += len(expected)
            self.after(200, self.show_next_word)
        else:
            self.errors += len(expected)
            self.word_label.config(fg='red')
            self.after(200, lambda: self.word_label.config(fg='#2C3E50') if self.is_running else None)

        self.input_entry.delete(0, tk.END)
        self.update_display()

    def update_timer(self):
        """타이머 업데이트"""
        if not self.is_running:
            return

        self.time_remaining -= 1
        self.time_label.config(text=f"{self.time_remaining}초")

        if self.time_remaining <= 10:
            self.time_label.config(fg='red')

        if self.time_remaining <= 0:
            self.game_over()
        else:
            self.after(1000, self.update_timer)

    def update_display(self):
        """화면 업데이트"""
        self.score_label.config(text=f"점수: {self.score}")

        cpm, accuracy, _ = self.calculate_stats()
        self.stats_label.config(text=f"타수: {cpm} | 정확도: {accuracy}%")

    def game_over(self):
        """게임 오버"""
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)

        cpm, accuracy, elapsed = self.calculate_stats()
        self.word_label.config(
            text=f"시간 종료!\n\n점수: {self.score}\n타수: {cpm} CPM\n정확도: {accuracy}%",
            fg='#E74C3C'
        )


class SoundManager:
    """소리 효과 관리자"""

    def __init__(self):
        self.enabled = True
        self.volume = 50  # 0-100

    def play_key_sound(self):
        """키 입력 소리"""
        if self.enabled:
            threading.Thread(target=lambda: winsound.Beep(800, 50), daemon=True).start()

    def play_correct_sound(self):
        """정답 소리"""
        if self.enabled:
            threading.Thread(target=lambda: winsound.Beep(1000, 100), daemon=True).start()

    def play_error_sound(self):
        """오류 소리"""
        if self.enabled:
            threading.Thread(target=lambda: winsound.Beep(400, 200), daemon=True).start()

    def play_complete_sound(self):
        """완료 소리"""
        if self.enabled:
            def play():
                winsound.Beep(800, 100)
                winsound.Beep(1000, 100)
                winsound.Beep(1200, 200)

            threading.Thread(target=play, daemon=True).start()

    def play_achievement_sound(self):
        """업적 달성 소리"""
        if self.enabled:
            def play():
                winsound.Beep(1200, 150)
                winsound.Beep(1400, 150)
                winsound.Beep(1600, 300)

            threading.Thread(target=play, daemon=True).start()

    def set_enabled(self, enabled):
        """소리 활성화/비활성화"""
        self.enabled = enabled

    def set_volume(self, volume):
        """볼륨 설정 (0-100)"""
        self.volume = max(0, min(100, volume))
