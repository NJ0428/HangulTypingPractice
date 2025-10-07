"""
가상 키보드 위젯 및 손가락 표시
"""
import tkinter as tk
from tkinter import ttk


class VirtualKeyboard(tk.Frame):
    """가상 키보드 위젯 - 손가락 위치 표시 포함"""

    # 한글 자판 레이아웃 (두벌식)
    HANGUL_LAYOUT = [
        ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
        ['Tab', 'ㅂ', 'ㅈ', 'ㄷ', 'ㄱ', 'ㅅ', 'ㅛ', 'ㅕ', 'ㅑ', 'ㅐ', 'ㅔ', '[', ']', '\\'],
        ['Caps', 'ㅁ', 'ㄴ', 'ㅇ', 'ㄹ', 'ㅎ', 'ㅗ', 'ㅓ', 'ㅏ', 'ㅣ', ';', "'", 'Enter'],
        ['Shift', 'ㅋ', 'ㅌ', 'ㅊ', 'ㅍ', 'ㅠ', 'ㅜ', 'ㅡ', ',', '.', '/', 'Shift'],
        ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', 'Ctrl']
    ]

    # 영어 자판 레이아웃
    ENGLISH_LAYOUT = [
        ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
        ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
        ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'Enter'],
        ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift'],
        ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', 'Ctrl']
    ]

    # 손가락 색상 매핑
    FINGER_COLORS = {
        'left_pinky': '#FFB6C1',      # 왼손 새끼
        'left_ring': '#FFD700',        # 왼손 약지
        'left_middle': '#90EE90',      # 왼손 중지
        'left_index': '#87CEEB',       # 왼손 검지
        'left_thumb': '#DDA0DD',       # 왼손 엄지
        'right_thumb': '#DDA0DD',      # 오른손 엄지
        'right_index': '#87CEEB',      # 오른손 검지
        'right_middle': '#90EE90',     # 오른손 중지
        'right_ring': '#FFD700',       # 오른손 약지
        'right_pinky': '#FFB6C1',      # 오른손 새끼
    }

    # 키와 손가락 매핑
    KEY_FINGER_MAP = {
        # 왼손 새끼
        '`': 'left_pinky', '1': 'left_pinky', 'Tab': 'left_pinky', 'ㅂ': 'left_pinky',
        'q': 'left_pinky', 'Caps': 'left_pinky', 'ㅁ': 'left_pinky', 'a': 'left_pinky',
        'Shift': 'left_pinky', 'ㅋ': 'left_pinky', 'z': 'left_pinky',
        # 왼손 약지
        '2': 'left_ring', 'ㅈ': 'left_ring', 'w': 'left_ring',
        'ㄴ': 'left_ring', 's': 'left_ring', 'ㅌ': 'left_ring', 'x': 'left_ring',
        # 왼손 중지
        '3': 'left_middle', 'ㄷ': 'left_middle', 'e': 'left_middle',
        'ㅇ': 'left_middle', 'd': 'left_middle', 'ㅊ': 'left_middle', 'c': 'left_middle',
        # 왼손 검지
        '4': 'left_index', '5': 'left_index', 'ㄱ': 'left_index', 'ㅅ': 'left_index',
        'r': 'left_index', 't': 'left_index', 'ㄹ': 'left_index', 'ㅎ': 'left_index',
        'f': 'left_index', 'g': 'left_index', 'ㅍ': 'left_index', 'ㅠ': 'left_index',
        'v': 'left_index', 'b': 'left_index',
        # 왼손/오른손 엄지
        'Space': 'left_thumb',
        # 오른손 검지
        '6': 'right_index', '7': 'right_index', 'ㅛ': 'right_index', 'ㅕ': 'right_index',
        'y': 'right_index', 'u': 'right_index', 'ㅗ': 'right_index', 'ㅓ': 'right_index',
        'h': 'right_index', 'j': 'right_index', 'ㅜ': 'right_index', 'ㅡ': 'right_index',
        'n': 'right_index', 'm': 'right_index',
        # 오른손 중지
        '8': 'right_middle', 'ㅑ': 'right_middle', 'i': 'right_middle',
        'ㅏ': 'right_middle', 'k': 'right_middle', ',': 'right_middle',
        # 오른손 약지
        '9': 'right_ring', 'ㅐ': 'right_ring', 'o': 'right_ring',
        'ㅣ': 'right_ring', 'l': 'right_ring', '.': 'right_ring',
        # 오른손 새끼
        '0': 'right_pinky', '-': 'right_pinky', '=': 'right_pinky', 'Backspace': 'right_pinky',
        'ㅔ': 'right_pinky', '[': 'right_pinky', ']': 'right_pinky', '\\': 'right_pinky',
        'p': 'right_pinky', ';': 'right_pinky', "'": 'right_pinky', 'Enter': 'right_pinky',
        '/': 'right_pinky',
    }

    def __init__(self, parent, language='hangul'):
        super().__init__(parent)
        self.language = language
        self.key_buttons = {}
        self.current_highlighted = None

        self.create_keyboard()

    def create_keyboard(self):
        """키보드 생성"""
        layout = self.HANGUL_LAYOUT if self.language == 'hangul' else self.ENGLISH_LAYOUT

        # 키보드 프레임
        keyboard_frame = tk.Frame(self, bg='#2C3E50', padx=10, pady=10)
        keyboard_frame.pack()

        for row_idx, row in enumerate(layout):
            row_frame = tk.Frame(keyboard_frame, bg='#2C3E50')
            row_frame.pack(pady=2)

            for key in row:
                # 키 크기 결정
                width = self._get_key_width(key)

                # 손가락 색상
                finger = self.KEY_FINGER_MAP.get(key, None)
                bg_color = self.FINGER_COLORS.get(finger, '#ECF0F1') if finger else '#ECF0F1'

                btn = tk.Button(
                    row_frame,
                    text=key,
                    width=width,
                    height=2,
                    bg=bg_color,
                    fg='#2C3E50',
                    font=('맑은 고딕', 10, 'bold'),
                    relief=tk.RAISED,
                    borderwidth=2
                )
                btn.pack(side=tk.LEFT, padx=2)

                self.key_buttons[key] = btn

        # 범례 추가
        self.create_legend()

    def create_legend(self):
        """손가락 색상 범례"""
        legend_frame = tk.Frame(self, bg='white')
        legend_frame.pack(pady=10)

        tk.Label(legend_frame, text="손가락 위치:", font=('맑은 고딕', 9, 'bold')).pack(side=tk.LEFT, padx=5)

        fingers = [
            ('왼손 새끼', 'left_pinky'),
            ('왼손 약지', 'left_ring'),
            ('왼손 중지', 'left_middle'),
            ('왼손 검지', 'left_index'),
            ('엄지', 'left_thumb'),
            ('오른손 검지', 'right_index'),
            ('오른손 중지', 'right_middle'),
            ('오른손 약지', 'right_ring'),
            ('오른손 새끼', 'right_pinky'),
        ]

        for name, finger_key in fingers:
            color = self.FINGER_COLORS[finger_key]
            color_box = tk.Label(legend_frame, text='  ', bg=color, relief=tk.SOLID, borderwidth=1)
            color_box.pack(side=tk.LEFT, padx=2)
            tk.Label(legend_frame, text=name, font=('맑은 고딕', 8)).pack(side=tk.LEFT, padx=(0, 10))

    def _get_key_width(self, key):
        """키 너비 반환"""
        if key == 'Backspace':
            return 8
        elif key == 'Tab':
            return 6
        elif key == 'Caps':
            return 7
        elif key == 'Enter':
            return 8
        elif key == 'Shift':
            return 7
        elif key == 'Space':
            return 30
        elif key in ['Ctrl', 'Win', 'Alt', 'Fn']:
            return 5
        else:
            return 4

    def highlight_key(self, key):
        """특정 키 강조"""
        # 이전 강조 제거
        if self.current_highlighted and self.current_highlighted in self.key_buttons:
            btn = self.key_buttons[self.current_highlighted]
            finger = self.KEY_FINGER_MAP.get(self.current_highlighted, None)
            bg_color = self.FINGER_COLORS.get(finger, '#ECF0F1') if finger else '#ECF0F1'
            btn.config(bg=bg_color, relief=tk.RAISED)

        # 새 키 강조
        if key in self.key_buttons:
            btn = self.key_buttons[key]
            btn.config(bg='#E74C3C', relief=tk.SUNKEN)  # 빨간색으로 강조
            self.current_highlighted = key

    def clear_highlight(self):
        """모든 강조 제거"""
        if self.current_highlighted and self.current_highlighted in self.key_buttons:
            btn = self.key_buttons[self.current_highlighted]
            finger = self.KEY_FINGER_MAP.get(self.current_highlighted, None)
            bg_color = self.FINGER_COLORS.get(finger, '#ECF0F1') if finger else '#ECF0F1'
            btn.config(bg=bg_color, relief=tk.RAISED)
            self.current_highlighted = None

    def switch_language(self, language):
        """언어 전환"""
        self.language = language
        for widget in self.winfo_children():
            widget.destroy()
        self.key_buttons.clear()
        self.current_highlighted = None
        self.create_keyboard()
