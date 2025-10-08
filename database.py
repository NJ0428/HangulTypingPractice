"""
데이터베이스 관리 모듈
SQLite를 사용한 사용자 정보 관리
"""
import sqlite3
import hashlib
from datetime import datetime


class Database:
    """데이터베이스 관리 클래스"""

    def __init__(self, db_name='typing_practice.db'):
        """데이터베이스 초기화"""
        self.db_name = db_name
        self.init_database()

    def get_connection(self):
        """데이터베이스 연결 생성"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn

    def init_database(self):
        """데이터베이스 테이블 초기화"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 사용자 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                total_score INTEGER DEFAULT 0,
                total_practice_time INTEGER DEFAULT 0
            )
        ''')

        # 연습 기록 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS practice_records (
                record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mode_name TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                accuracy REAL DEFAULT 0,
                speed INTEGER DEFAULT 0,
                practice_time INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # 최고 기록 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                highscore_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                mode_name TEXT NOT NULL,
                high_score INTEGER DEFAULT 0,
                best_accuracy REAL DEFAULT 0,
                best_speed INTEGER DEFAULT 0,
                achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, mode_name)
            )
        ''')

        conn.commit()
        conn.close()

    @staticmethod
    def hash_password(password):
        """비밀번호 해싱"""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, email=None):
        """새 사용자 생성"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            hashed_pw = self.hash_password(password)

            cursor.execute('''
                INSERT INTO users (username, password, email)
                VALUES (?, ?, ?)
            ''', (username, hashed_pw, email))

            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return True, user_id
        except sqlite3.IntegrityError:
            return False, "이미 존재하는 사용자명입니다."
        except Exception as e:
            return False, str(e)

    def verify_user(self, username, password):
        """사용자 인증"""
        conn = self.get_connection()
        cursor = conn.cursor()

        hashed_pw = self.hash_password(password)

        cursor.execute('''
            SELECT user_id, username, total_score
            FROM users
            WHERE username = ? AND password = ?
        ''', (username, hashed_pw))

        user = cursor.fetchone()
        conn.close()

        if user:
            # 마지막 로그인 시간 업데이트
            self.update_last_login(user['user_id'])
            return True, dict(user)
        else:
            return False, None

    def update_last_login(self, user_id):
        """마지막 로그인 시간 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users
            SET last_login = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (user_id,))

        conn.commit()
        conn.close()

    def get_user_info(self, user_id):
        """사용자 정보 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT user_id, username, email, total_score,
                   total_practice_time, created_at, last_login
            FROM users
            WHERE user_id = ?
        ''', (user_id,))

        user = cursor.fetchone()
        conn.close()

        return dict(user) if user else None

    def update_user_score(self, user_id, score_to_add):
        """사용자 점수 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users
            SET total_score = total_score + ?
            WHERE user_id = ?
        ''', (score_to_add, user_id))

        conn.commit()
        conn.close()

    def save_practice_record(self, user_id, mode_name, score, accuracy, speed, practice_time):
        """연습 기록 저장"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO practice_records
            (user_id, mode_name, score, accuracy, speed, practice_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, mode_name, score, accuracy, speed, practice_time))

        # 최고 기록 업데이트
        cursor.execute('''
            INSERT INTO high_scores (user_id, mode_name, high_score, best_accuracy, best_speed)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(user_id, mode_name)
            DO UPDATE SET
                high_score = MAX(high_score, ?),
                best_accuracy = MAX(best_accuracy, ?),
                best_speed = MAX(best_speed, ?),
                achieved_at = CASE
                    WHEN ? > high_score THEN CURRENT_TIMESTAMP
                    ELSE achieved_at
                END
        ''', (user_id, mode_name, score, accuracy, speed,
              score, accuracy, speed, score))

        conn.commit()
        conn.close()

    def get_user_records(self, user_id, limit=10):
        """사용자 연습 기록 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT mode_name, score, accuracy, speed, practice_time, created_at
            FROM practice_records
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        ''', (user_id, limit))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    def get_high_scores(self, user_id):
        """사용자 최고 기록 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT mode_name, high_score, best_accuracy, best_speed, achieved_at
            FROM high_scores
            WHERE user_id = ?
            ORDER BY high_score DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    def get_leaderboard(self, mode_name=None, limit=10):
        """리더보드 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        if mode_name:
            cursor.execute('''
                SELECT u.username, h.high_score, h.best_accuracy, h.best_speed, h.achieved_at
                FROM high_scores h
                JOIN users u ON h.user_id = u.user_id
                WHERE h.mode_name = ?
                ORDER BY h.high_score DESC
                LIMIT ?
            ''', (mode_name, limit))
        else:
            cursor.execute('''
                SELECT u.username, u.total_score, u.total_practice_time
                FROM users u
                ORDER BY u.total_score DESC
                LIMIT ?
            ''', (limit,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]
