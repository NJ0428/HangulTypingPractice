"""
소셜 기능 모듈
- 친구 시스템
- 클랜/그룹 시스템
- 통계 내보내기
- 리포트 생성
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime, timedelta


class FriendsWindow:
    """친구 시스템 창"""

    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

        self.window = tk.Toplevel(root)
        self.window.title("친구 관리")
        self.window.geometry("800x600")
        self.window.configure(bg='#ECF0F1')
        self.window.transient(root)

        self.setup_ui()
        self.load_friends()

    def setup_ui(self):
        """UI 설정"""
        # 헤더
        header_frame = tk.Frame(self.window, bg='#3498DB', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="👥",
            font=('맑은 고딕', 40),
            bg='#3498DB'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="친구 관리",
            font=('맑은 고딕', 20, 'bold'),
            bg='#3498DB',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 탭
        tab_frame = tk.Frame(self.window, bg='#ECF0F1')
        tab_frame.pack(fill=tk.X, padx=20, pady=10)

        self.current_tab = tk.StringVar(value='friends')

        tk.Button(
            tab_frame,
            text="친구 목록",
            command=lambda: self.change_tab('friends'),
            bg='#3498DB',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            tab_frame,
            text="친구 요청",
            command=lambda: self.change_tab('requests'),
            bg='#9B59B6',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            tab_frame,
            text="친구 추가",
            command=lambda: self.change_tab('add'),
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        # 콘텐츠 프레임
        self.content_frame = tk.Frame(self.window, bg='#ECF0F1')
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def change_tab(self, tab):
        """탭 변경"""
        self.current_tab.set(tab)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if tab == 'friends':
            self.show_friends_list()
        elif tab == 'requests':
            self.show_friend_requests()
        elif tab == 'add':
            self.show_add_friend()

    def show_friends_list(self):
        """친구 목록 표시"""
        friends = self.db.get_friends(self.user_id)

        if not friends:
            tk.Label(
                self.content_frame,
                text="아직 친구가 없습니다.\n친구를 추가해보세요!",
                font=('맑은 고딕', 14),
                bg='#ECF0F1',
                fg='#7F8C8D'
            ).pack(expand=True)
            return

        # 스크롤 가능한 프레임
        canvas = tk.Canvas(self.content_frame, bg='#ECF0F1', highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ECF0F1')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        for friend in friends:
            friend_frame = tk.Frame(scrollable_frame, bg='white', relief=tk.RAISED, borderwidth=2)
            friend_frame.pack(fill=tk.X, padx=5, pady=5)

            # 친구 정보
            info_frame = tk.Frame(friend_frame, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

            tk.Label(
                info_frame,
                text=f"👤 {friend['username']}",
                font=('맑은 고딕', 14, 'bold'),
                bg='white',
                fg='#2C3E50'
            ).pack(anchor=tk.W)

            tk.Label(
                info_frame,
                text=f"점수: {friend['total_score']:,}점",
                font=('맑은 고딕', 11),
                bg='white',
                fg='#7F8C8D'
            ).pack(anchor=tk.W)

            tk.Label(
                info_frame,
                text=f"친구된 날: {friend['accepted_at'][:10]}",
                font=('맑은 고딕', 10),
                bg='white',
                fg='#95A5A6'
            ).pack(anchor=tk.W)

            # 버튼
            btn_frame = tk.Frame(friend_frame, bg='white')
            btn_frame.pack(side=tk.RIGHT, padx=10)

            tk.Button(
                btn_frame,
                text="도전장 보내기",
                command=lambda f=friend: self.send_challenge(f),
                bg='#F39C12',
                fg='white',
                font=('맑은 고딕', 9, 'bold'),
                width=12,
                cursor='hand2'
            ).pack(pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def show_friend_requests(self):
        """친구 요청 목록 표시"""
        requests = self.db.get_friend_requests(self.user_id)

        if not requests:
            tk.Label(
                self.content_frame,
                text="받은 친구 요청이 없습니다.",
                font=('맑은 고딕', 14),
                bg='#ECF0F1',
                fg='#7F8C8D'
            ).pack(expand=True)
            return

        for request in requests:
            request_frame = tk.Frame(self.content_frame, bg='white', relief=tk.RAISED, borderwidth=2)
            request_frame.pack(fill=tk.X, padx=5, pady=5)

            # 요청 정보
            info_frame = tk.Frame(request_frame, bg='white')
            info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=10)

            tk.Label(
                info_frame,
                text=f"👤 {request['username']}",
                font=('맑은 고딕', 14, 'bold'),
                bg='white',
                fg='#2C3E50'
            ).pack(anchor=tk.W)

            tk.Label(
                info_frame,
                text=f"점수: {request['total_score']:,}점",
                font=('맑은 고딕', 11),
                bg='white',
                fg='#7F8C8D'
            ).pack(anchor=tk.W)

            # 버튼
            btn_frame = tk.Frame(request_frame, bg='white')
            btn_frame.pack(side=tk.RIGHT, padx=10)

            tk.Button(
                btn_frame,
                text="수락",
                command=lambda r=request: self.accept_request(r['user_id']),
                bg='#27AE60',
                fg='white',
                font=('맑은 고딕', 10, 'bold'),
                width=10,
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=2)

            tk.Button(
                btn_frame,
                text="거절",
                command=lambda r=request: self.reject_request(r['user_id']),
                bg='#E74C3C',
                fg='white',
                font=('맑은 고딕', 10, 'bold'),
                width=10,
                cursor='hand2'
            ).pack(side=tk.LEFT, padx=2)

    def show_add_friend(self):
        """친구 추가 화면"""
        tk.Label(
            self.content_frame,
            text="친구 추가",
            font=('맑은 고딕', 18, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        ).pack(pady=20)

        tk.Label(
            self.content_frame,
            text="친구의 사용자명을 입력하세요:",
            font=('맑은 고딕', 12),
            bg='#ECF0F1'
        ).pack(pady=10)

        self.username_entry = tk.Entry(
            self.content_frame,
            font=('맑은 고딕', 14),
            width=30
        )
        self.username_entry.pack(pady=10)

        tk.Button(
            self.content_frame,
            text="친구 요청 보내기",
            command=self.send_friend_request,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 12, 'bold'),
            width=20,
            cursor='hand2'
        ).pack(pady=20)

    def send_friend_request(self):
        """친구 요청 보내기"""
        username = self.username_entry.get().strip()

        if not username:
            messagebox.showwarning("알림", "사용자명을 입력하세요.")
            return

        success, message = self.db.send_friend_request(self.user_id, username)

        if success:
            messagebox.showinfo("성공", message)
            self.username_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("실패", message)

    def accept_request(self, friend_id):
        """친구 요청 수락"""
        self.db.accept_friend_request(self.user_id, friend_id)
        messagebox.showinfo("성공", "친구 요청을 수락했습니다!")
        self.change_tab('requests')

    def reject_request(self, friend_id):
        """친구 요청 거절"""
        # 거절 기능은 간단히 무시
        messagebox.showinfo("알림", "친구 요청을 거절했습니다.")
        self.change_tab('requests')

    def send_challenge(self, friend):
        """도전장 보내기"""
        messagebox.showinfo(
            "도전장",
            f"{friend['username']}님에게 도전장을 보냈습니다!\n(실제 구현은 멀티플레이 기능이 필요합니다)"
        )

    def load_friends(self):
        """친구 로드"""
        self.show_friends_list()


class ClanWindow:
    """클랜 시스템 창"""

    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

        self.window = tk.Toplevel(root)
        self.window.title("클랜 관리")
        self.window.geometry("800x600")
        self.window.configure(bg='#ECF0F1')
        self.window.transient(root)

        self.user_clan = self.db.get_user_clan(user_id)

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 헤더
        header_frame = tk.Frame(self.window, bg='#8E44AD', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="🛡️",
            font=('맑은 고딕', 40),
            bg='#8E44AD'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="클랜 관리",
            font=('맑은 고딕', 20, 'bold'),
            bg='#8E44AD',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 콘텐츠
        content = tk.Frame(self.window, bg='#ECF0F1')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        if self.user_clan:
            self.show_clan_info(content)
        else:
            self.show_create_clan(content)

    def show_clan_info(self, parent):
        """클랜 정보 표시"""
        # 클랜 정보
        info_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=3)
        info_frame.pack(fill=tk.X, pady=10)

        tk.Label(
            info_frame,
            text=f"🛡️ {self.user_clan['clan_name']}",
            font=('맑은 고딕', 20, 'bold'),
            bg='white',
            fg='#8E44AD'
        ).pack(pady=10)

        tk.Label(
            info_frame,
            text=self.user_clan['description'],
            font=('맑은 고딕', 12),
            bg='white',
            fg='#7F8C8D'
        ).pack(pady=5)

        stats_frame = tk.Frame(info_frame, bg='white')
        stats_frame.pack(pady=10)

        tk.Label(
            stats_frame,
            text=f"멤버 수: {self.user_clan['total_members']}명",
            font=('맑은 고딕', 11, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            stats_frame,
            text=f"내 역할: {self.user_clan['role']}",
            font=('맑은 고딕', 11, 'bold'),
            bg='white',
            fg='#2C3E50'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            stats_frame,
            text=f"기여도: {self.user_clan['contribution']}",
            font=('맑은 고딕', 11, 'bold'),
            bg='white',
            fg='#F39C12'
        ).pack(side=tk.LEFT, padx=20)

        # 멤버 목록
        tk.Label(
            parent,
            text="클랜 멤버",
            font=('맑은 고딕', 14, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        ).pack(anchor=tk.W, pady=(10, 5))

        members_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
        members_frame.pack(fill=tk.BOTH, expand=True)

        members = self.db.get_clan_members(self.user_clan['clan_id'])

        # 헤더
        header = tk.Frame(members_frame, bg='#ECF0F1')
        header.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(header, text="사용자명", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=15).pack(side=tk.LEFT)
        tk.Label(header, text="역할", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT)
        tk.Label(header, text="기여도", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=10).pack(side=tk.LEFT)
        tk.Label(header, text="가입일", font=('맑은 고딕', 10, 'bold'), bg='#ECF0F1', width=15).pack(side=tk.LEFT)

        # 데이터
        for i, member in enumerate(members):
            bg_color = '#F8F9FA' if i % 2 == 0 else 'white'
            row = tk.Frame(members_frame, bg=bg_color)
            row.pack(fill=tk.X, padx=10, pady=2)

            tk.Label(row, text=member['username'], font=('맑은 고딕', 9), bg=bg_color, width=15).pack(side=tk.LEFT)
            tk.Label(row, text=member['role'], font=('맑은 고딕', 9), bg=bg_color, width=10).pack(side=tk.LEFT)
            tk.Label(row, text=member['contribution'], font=('맑은 고딕', 9), bg=bg_color, width=10).pack(side=tk.LEFT)
            tk.Label(row, text=member['joined_at'][:10], font=('맑은 고딕', 9), bg=bg_color, width=15).pack(side=tk.LEFT)

    def show_create_clan(self, parent):
        """클랜 생성 화면"""
        tk.Label(
            parent,
            text="클랜을 생성하거나 가입하세요",
            font=('맑은 고딕', 18, 'bold'),
            bg='#ECF0F1',
            fg='#2C3E50'
        ).pack(pady=30)

        # 클랜 생성
        create_frame = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=3)
        create_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(
            create_frame,
            text="새 클랜 만들기",
            font=('맑은 고딕', 16, 'bold'),
            bg='white',
            fg='#8E44AD'
        ).pack(pady=15)

        tk.Label(create_frame, text="클랜 이름:", font=('맑은 고딕', 11), bg='white').pack(pady=5)
        self.clan_name_entry = tk.Entry(create_frame, font=('맑은 고딕', 12), width=30)
        self.clan_name_entry.pack(pady=5)

        tk.Label(create_frame, text="클랜 설명:", font=('맑은 고딕', 11), bg='white').pack(pady=5)
        self.clan_desc_entry = tk.Entry(create_frame, font=('맑은 고딕', 12), width=30)
        self.clan_desc_entry.pack(pady=5)

        tk.Button(
            create_frame,
            text="클랜 생성",
            command=self.create_clan,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 12, 'bold'),
            width=20,
            cursor='hand2'
        ).pack(pady=20)

    def create_clan(self):
        """클랜 생성"""
        clan_name = self.clan_name_entry.get().strip()
        description = self.clan_desc_entry.get().strip()

        if not clan_name:
            messagebox.showwarning("알림", "클랜 이름을 입력하세요.")
            return

        success, result = self.db.create_clan(clan_name, description, self.user_id)

        if success:
            messagebox.showinfo("성공", f"클랜 '{clan_name}'을(를) 생성했습니다!")
            self.window.destroy()
            # 창 새로고침
            ClanWindow(self.root, self.db, self.user_id)
        else:
            messagebox.showwarning("실패", result)


class StatisticsExporter:
    """통계 데이터 내보내기"""

    @staticmethod
    def export_to_csv(db, user_id, filepath):
        """CSV로 내보내기"""
        try:
            records = db.get_user_records(user_id, limit=1000)

            with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.DictWriter(f, fieldnames=['mode_name', 'score', 'accuracy', 'speed', 'practice_time', 'created_at'])
                writer.writeheader()
                writer.writerows(records)

            return True, "CSV 파일로 내보내기 완료!"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def generate_weekly_report(db, user_id):
        """주간 리포트 생성"""
        history = db.get_practice_history(user_id, days=7)

        report = "=" * 50 + "\n"
        report += "주간 타자 연습 리포트\n"
        report += "=" * 50 + "\n\n"

        if not history:
            report += "지난 7일간 연습 기록이 없습니다.\n"
            return report

        total_sessions = sum(h['session_count'] for h in history)
        total_score = sum(h['total_score'] for h in history)
        total_time = sum(h['total_time'] for h in history)
        avg_accuracy = sum(h['avg_accuracy'] for h in history) / len(history)
        avg_speed = sum(h['avg_speed'] for h in history) / len(history)

        report += f"📊 전체 통계\n"
        report += f"  - 총 연습 세션: {total_sessions}회\n"
        report += f"  - 총 획득 점수: {total_score:,}점\n"
        report += f"  - 총 연습 시간: {total_time}분\n"
        report += f"  - 평균 정확도: {avg_accuracy:.1f}%\n"
        report += f"  - 평균 속도: {avg_speed:.1f}타/분\n\n"

        report += "📅 일별 기록\n"
        for h in history:
            report += f"  {h['practice_date']}: {h['session_count']}회, "
            report += f"{h['total_score']}점, "
            report += f"{h['avg_accuracy']:.1f}% 정확도\n"

        report += "\n" + "=" * 50 + "\n"

        return report

    @staticmethod
    def generate_monthly_report(db, user_id):
        """월간 리포트 생성"""
        history = db.get_practice_history(user_id, days=30)

        report = "=" * 50 + "\n"
        report += "월간 타자 연습 리포트\n"
        report += "=" * 50 + "\n\n"

        if not history:
            report += "지난 30일간 연습 기록이 없습니다.\n"
            return report

        total_sessions = sum(h['session_count'] for h in history)
        total_score = sum(h['total_score'] for h in history)
        total_time = sum(h['total_time'] for h in history)
        avg_accuracy = sum(h['avg_accuracy'] for h in history) / len(history)
        avg_speed = sum(h['avg_speed'] for h in history) / len(history)

        report += f"📊 전체 통계\n"
        report += f"  - 총 연습 세션: {total_sessions}회\n"
        report += f"  - 총 획득 점수: {total_score:,}점\n"
        report += f"  - 총 연습 시간: {total_time}분 ({total_time/60:.1f}시간)\n"
        report += f"  - 평균 정확도: {avg_accuracy:.1f}%\n"
        report += f"  - 평균 속도: {avg_speed:.1f}타/분\n\n"

        # 모드별 분포
        mode_dist = db.get_mode_distribution(user_id)
        if mode_dist:
            report += "🎯 모드별 연습 분포\n"
            for mode in mode_dist[:5]:
                report += f"  - {mode['mode_name']}: {mode['count']}회 ({mode['total_time']}분)\n"

        report += "\n" + "=" * 50 + "\n"

        return report


class ReportWindow:
    """리포트 창"""

    def __init__(self, root, db, user_id):
        self.root = root
        self.db = db
        self.user_id = user_id

        self.window = tk.Toplevel(root)
        self.window.title("연습 리포트")
        self.window.geometry("700x600")
        self.window.configure(bg='#ECF0F1')
        self.window.transient(root)

        self.setup_ui()

    def setup_ui(self):
        """UI 설정"""
        # 헤더
        header_frame = tk.Frame(self.window, bg='#16A085', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame,
            text="📊",
            font=('맑은 고딕', 40),
            bg='#16A085'
        ).pack(side=tk.LEFT, padx=20)

        tk.Label(
            header_frame,
            text="연습 리포트",
            font=('맑은 고딕', 20, 'bold'),
            bg='#16A085',
            fg='white'
        ).pack(side=tk.LEFT, pady=20)

        # 버튼 프레임
        btn_frame = tk.Frame(self.window, bg='#ECF0F1')
        btn_frame.pack(fill=tk.X, padx=20, pady=10)

        tk.Button(
            btn_frame,
            text="주간 리포트",
            command=self.show_weekly_report,
            bg='#3498DB',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="월간 리포트",
            command=self.show_monthly_report,
            bg='#9B59B6',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="CSV 내보내기",
            command=self.export_csv,
            bg='#27AE60',
            fg='white',
            font=('맑은 고딕', 11, 'bold'),
            width=15,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        # 리포트 텍스트 영역
        text_frame = tk.Frame(self.window, bg='#ECF0F1')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.report_text = tk.Text(
            text_frame,
            font=('맑은 고딕', 10),
            bg='white',
            wrap=tk.WORD
        )
        self.report_text.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(text_frame, command=self.report_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text.config(yscrollcommand=scrollbar.set)

    def show_weekly_report(self):
        """주간 리포트 표시"""
        report = StatisticsExporter.generate_weekly_report(self.db, self.user_id)
        self.report_text.delete('1.0', tk.END)
        self.report_text.insert('1.0', report)

    def show_monthly_report(self):
        """월간 리포트 표시"""
        report = StatisticsExporter.generate_monthly_report(self.db, self.user_id)
        self.report_text.delete('1.0', tk.END)
        self.report_text.insert('1.0', report)

    def export_csv(self):
        """CSV 내보내기"""
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if filepath:
            success, message = StatisticsExporter.export_to_csv(self.db, self.user_id, filepath)

            if success:
                messagebox.showinfo("성공", message)
            else:
                messagebox.showerror("오류", f"내보내기 실패: {message}")
