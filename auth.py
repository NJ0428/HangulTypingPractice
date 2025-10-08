"""
사용자 인증 UI 모듈
로그인 및 회원가입 화면
"""
import tkinter as tk
from tkinter import messagebox, font
from database import Database


class AuthScreen:
    """인증 화면 클래스"""

    def __init__(self, root, on_login_success):
        """
        Args:
            root: Tkinter root 윈도우
            on_login_success: 로그인 성공 시 호출될 콜백 함수 (user_info를 인자로 받음)
        """
        self.root = root
        self.on_login_success = on_login_success
        self.db = Database()

        # 폰트 설정
        self.title_font = font.Font(family="맑은 고딕", size=20, weight="bold")
        self.label_font = font.Font(family="맑은 고딕", size=11)
        self.button_font = font.Font(family="맑은 고딕", size=12, weight="bold")

        self.create_login_screen()

    def create_login_screen(self):
        """로그인 화면 생성"""
        # 메인 프레임
        self.login_frame = tk.Frame(self.root, bg='#E8F4F8')
        self.login_frame.pack(fill=tk.BOTH, expand=True)

        # 로그인 카드
        card_frame = tk.Frame(self.login_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=550)

        # 타이틀
        title_frame = tk.Frame(card_frame, bg='#3498DB', height=100)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="⌨️",
            font=('맑은 고딕', 40),
            bg='#3498DB'
        ).pack(pady=(10, 0))

        tk.Label(
            title_frame,
            text="한글/영어 타자 연습",
            font=self.title_font,
            bg='#3498DB',
            fg='white'
        ).pack()

        # 로그인 폼
        form_frame = tk.Frame(card_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # 사용자명 입력
        tk.Label(
            form_frame,
            text="사용자명",
            font=self.label_font,
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(10, 5))

        self.username_entry = tk.Entry(
            form_frame,
            font=('맑은 고딕', 12),
            relief=tk.SOLID,
            borderwidth=2
        )
        self.username_entry.pack(fill=tk.X, ipady=8)

        # 비밀번호 입력
        tk.Label(
            form_frame,
            text="비밀번호",
            font=self.label_font,
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(20, 5))

        self.password_entry = tk.Entry(
            form_frame,
            font=('맑은 고딕', 12),
            show='●',
            relief=tk.SOLID,
            borderwidth=2
        )
        self.password_entry.pack(fill=tk.X, ipady=8)

        # Enter 키로 로그인
        self.password_entry.bind('<Return>', lambda e: self.login())

        # 로그인 버튼
        login_btn = tk.Button(
            form_frame,
            text="로그인",
            command=self.login,
            bg='#27AE60',
            fg='white',
            font=self.button_font,
            relief=tk.RAISED,
            borderwidth=3,
            cursor='hand2',
            height=2
        )
        login_btn.pack(fill=tk.X, pady=(30, 10))

        # 회원가입 버튼
        signup_btn = tk.Button(
            form_frame,
            text="회원가입",
            command=self.show_signup_screen,
            bg='#3498DB',
            fg='white',
            font=self.button_font,
            relief=tk.RAISED,
            borderwidth=3,
            cursor='hand2',
            height=2
        )
        signup_btn.pack(fill=tk.X, pady=(0, 10))

        # 게스트 로그인 버튼
        guest_btn = tk.Button(
            form_frame,
            text="게스트로 시작",
            command=self.guest_login,
            bg='#95A5A6',
            fg='white',
            font=('맑은 고딕', 10),
            relief=tk.FLAT,
            cursor='hand2'
        )
        guest_btn.pack(fill=tk.X)

        # 포커스 설정
        self.username_entry.focus()

    def login(self):
        """로그인 처리"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showwarning("입력 오류", "사용자명과 비밀번호를 입력하세요.")
            return

        success, user_info = self.db.verify_user(username, password)

        if success:
            messagebox.showinfo("로그인 성공", f"환영합니다, {username}님!")
            self.login_frame.destroy()
            self.on_login_success(user_info)
        else:
            messagebox.showerror("로그인 실패", "사용자명 또는 비밀번호가 올바르지 않습니다.")
            self.password_entry.delete(0, tk.END)

    def guest_login(self):
        """게스트 로그인"""
        guest_info = {
            'user_id': None,
            'username': '손님',
            'total_score': 0
        }
        self.login_frame.destroy()
        self.on_login_success(guest_info)

    def show_signup_screen(self):
        """회원가입 화면으로 전환"""
        self.login_frame.destroy()
        self.create_signup_screen()

    def create_signup_screen(self):
        """회원가입 화면 생성"""
        # 메인 프레임
        self.signup_frame = tk.Frame(self.root, bg='#E8F4F8')
        self.signup_frame.pack(fill=tk.BOTH, expand=True)

        # 회원가입 카드
        card_frame = tk.Frame(self.signup_frame, bg='white', relief=tk.RAISED, borderwidth=3)
        card_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=450, height=600)

        # 타이틀
        title_frame = tk.Frame(card_frame, bg='#3498DB', height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        tk.Label(
            title_frame,
            text="회원가입",
            font=self.title_font,
            bg='#3498DB',
            fg='white'
        ).pack(expand=True)

        # 회원가입 폼
        form_frame = tk.Frame(card_frame, bg='white')
        form_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        # 사용자명 입력
        tk.Label(
            form_frame,
            text="사용자명 *",
            font=self.label_font,
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(10, 5))

        self.signup_username_entry = tk.Entry(
            form_frame,
            font=('맑은 고딕', 12),
            relief=tk.SOLID,
            borderwidth=2
        )
        self.signup_username_entry.pack(fill=tk.X, ipady=8)

        # 비밀번호 입력
        tk.Label(
            form_frame,
            text="비밀번호 *",
            font=self.label_font,
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(15, 5))

        self.signup_password_entry = tk.Entry(
            form_frame,
            font=('맑은 고딕', 12),
            show='●',
            relief=tk.SOLID,
            borderwidth=2
        )
        self.signup_password_entry.pack(fill=tk.X, ipady=8)

        # 비밀번호 확인
        tk.Label(
            form_frame,
            text="비밀번호 확인 *",
            font=self.label_font,
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(15, 5))

        self.signup_password_confirm_entry = tk.Entry(
            form_frame,
            font=('맑은 고딕', 12),
            show='●',
            relief=tk.SOLID,
            borderwidth=2
        )
        self.signup_password_confirm_entry.pack(fill=tk.X, ipady=8)

        # 이메일 입력 (선택)
        tk.Label(
            form_frame,
            text="이메일 (선택)",
            font=self.label_font,
            bg='white',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(15, 5))

        self.signup_email_entry = tk.Entry(
            form_frame,
            font=('맑은 고딕', 12),
            relief=tk.SOLID,
            borderwidth=2
        )
        self.signup_email_entry.pack(fill=tk.X, ipady=8)

        # Enter 키로 회원가입
        self.signup_email_entry.bind('<Return>', lambda e: self.signup())

        # 회원가입 버튼
        signup_btn = tk.Button(
            form_frame,
            text="가입하기",
            command=self.signup,
            bg='#27AE60',
            fg='white',
            font=self.button_font,
            relief=tk.RAISED,
            borderwidth=3,
            cursor='hand2',
            height=2
        )
        signup_btn.pack(fill=tk.X, pady=(25, 10))

        # 뒤로가기 버튼
        back_btn = tk.Button(
            form_frame,
            text="← 로그인으로 돌아가기",
            command=self.show_login_screen,
            bg='#95A5A6',
            fg='white',
            font=('맑은 고딕', 10),
            relief=tk.FLAT,
            cursor='hand2'
        )
        back_btn.pack(fill=tk.X)

        # 포커스 설정
        self.signup_username_entry.focus()

    def signup(self):
        """회원가입 처리"""
        username = self.signup_username_entry.get().strip()
        password = self.signup_password_entry.get()
        password_confirm = self.signup_password_confirm_entry.get()
        email = self.signup_email_entry.get().strip()

        # 유효성 검사
        if not username or not password:
            messagebox.showwarning("입력 오류", "사용자명과 비밀번호는 필수입니다.")
            return

        if len(username) < 3:
            messagebox.showwarning("입력 오류", "사용자명은 최소 3자 이상이어야 합니다.")
            return

        if len(password) < 4:
            messagebox.showwarning("입력 오류", "비밀번호는 최소 4자 이상이어야 합니다.")
            return

        if password != password_confirm:
            messagebox.showwarning("입력 오류", "비밀번호가 일치하지 않습니다.")
            return

        # 사용자 생성
        success, result = self.db.create_user(username, password, email if email else None)

        if success:
            messagebox.showinfo("회원가입 성공", f"'{username}' 계정이 생성되었습니다!\n이제 로그인할 수 있습니다.")
            self.show_login_screen()
        else:
            messagebox.showerror("회원가입 실패", result)

    def show_login_screen(self):
        """로그인 화면으로 전환"""
        self.signup_frame.destroy()
        self.create_login_screen()
