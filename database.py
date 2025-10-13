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
                last_practice_date DATE,
                total_score INTEGER DEFAULT 0,
                total_practice_time INTEGER DEFAULT 0,
                login_streak INTEGER DEFAULT 0,
                theme TEXT DEFAULT 'light'
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

        # 업적 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS achievements (
                achievement_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                achievement_name TEXT NOT NULL,
                achievement_description TEXT,
                achieved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, achievement_name)
            )
        ''')

        # 일일 목표 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_goals (
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_date DATE DEFAULT CURRENT_DATE,
                target_time INTEGER DEFAULT 30,
                target_score INTEGER DEFAULT 100,
                achieved_time INTEGER DEFAULT 0,
                achieved_score INTEGER DEFAULT 0,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, goal_date)
            )
        ''')

        # 키 통계 테이블 생성
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS key_statistics (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                key_char TEXT NOT NULL,
                total_presses INTEGER DEFAULT 0,
                correct_presses INTEGER DEFAULT 0,
                incorrect_presses INTEGER DEFAULT 0,
                avg_time REAL DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, key_char)
            )
        ''')

        # 사용자 정의 단어 리스트 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS custom_word_lists (
                list_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                list_name TEXT NOT NULL,
                words TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

        # 설정 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_settings (
                setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                sound_enabled INTEGER DEFAULT 1,
                volume INTEGER DEFAULT 50,
                font_size INTEGER DEFAULT 12,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id)
            )
        ''')

        # 레벨 시스템 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_levels (
                level_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                current_level INTEGER DEFAULT 1,
                current_exp INTEGER DEFAULT 0,
                total_exp INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id)
            )
        ''')

        # 친구 시스템 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS friendships (
                friendship_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                friend_id INTEGER NOT NULL,
                status TEXT DEFAULT 'pending',
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                accepted_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                FOREIGN KEY (friend_id) REFERENCES users (user_id),
                UNIQUE(user_id, friend_id)
            )
        ''')

        # 클랜/그룹 시스템 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clans (
                clan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                clan_name TEXT UNIQUE NOT NULL,
                description TEXT,
                leader_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_members INTEGER DEFAULT 1,
                FOREIGN KEY (leader_id) REFERENCES users (user_id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clan_members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                clan_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                role TEXT DEFAULT 'member',
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                contribution INTEGER DEFAULT 0,
                FOREIGN KEY (clan_id) REFERENCES clans (clan_id),
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id)
            )
        ''')

        # 시즌 패스 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS season_pass (
                pass_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                season_number INTEGER NOT NULL,
                tier INTEGER DEFAULT 0,
                season_exp INTEGER DEFAULT 0,
                is_premium INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, season_number)
            )
        ''')

        # 손가락별 통계 테이블
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS finger_statistics (
                stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                finger_name TEXT NOT NULL,
                total_presses INTEGER DEFAULT 0,
                correct_presses INTEGER DEFAULT 0,
                avg_speed REAL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (user_id),
                UNIQUE(user_id, finger_name)
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

    # ========== 업적 관련 메서드 ==========
    def unlock_achievement(self, user_id, achievement_name, description):
        """업적 해제"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO achievements (user_id, achievement_name, achievement_description)
                VALUES (?, ?, ?)
            ''', (user_id, achievement_name, description))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False  # 이미 해제된 업적

    def get_achievements(self, user_id):
        """사용자 업적 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT achievement_name, achievement_description, achieved_at
            FROM achievements
            WHERE user_id = ?
            ORDER BY achieved_at DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()
        return [dict(record) for record in records]

    def check_achievements(self, user_id):
        """업적 달성 조건 체크 및 자동 해제"""
        user_info = self.get_user_info(user_id)
        if not user_info:
            return []

        unlocked = []

        # 첫 발자국
        if user_info['total_practice_time'] > 0:
            if self.unlock_achievement(user_id, "첫 발자국", "첫 연습을 완료하였습니다"):
                unlocked.append("첫 발자국")

        # 타자 초보
        if user_info['total_score'] >= 1000:
            if self.unlock_achievement(user_id, "타자 초보", "총 점수 1000점 달성"):
                unlocked.append("타자 초보")

        # 타자 고수
        if user_info['total_score'] >= 10000:
            if self.unlock_achievement(user_id, "타자 고수", "총 점수 10000점 달성"):
                unlocked.append("타자 고수")

        # 타자 마스터
        if user_info['total_score'] >= 50000:
            if self.unlock_achievement(user_id, "타자 마스터", "총 점수 50000점 달성"):
                unlocked.append("타자 마스터")

        # 연습벌레
        if user_info['total_practice_time'] >= 60:  # 1시간
            if self.unlock_achievement(user_id, "연습벌레", "총 1시간 이상 연습"):
                unlocked.append("연습벌레")

        # 끈기왕
        if user_info['total_practice_time'] >= 600:  # 10시간
            if self.unlock_achievement(user_id, "끈기왕", "총 10시간 이상 연습"):
                unlocked.append("끈기왕")

        # 연속 로그인
        if user_info['login_streak'] >= 7:
            if self.unlock_achievement(user_id, "일주일 연속", "7일 연속 로그인"):
                unlocked.append("일주일 연속")

        if user_info['login_streak'] >= 30:
            if self.unlock_achievement(user_id, "한 달 연속", "30일 연속 로그인"):
                unlocked.append("한 달 연속")

        return unlocked

    # ========== 일일 목표 관련 메서드 ==========
    def get_daily_goal(self, user_id):
        """오늘의 목표 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT goal_id, target_time, target_score, achieved_time, achieved_score, completed
            FROM daily_goals
            WHERE user_id = ? AND goal_date = DATE('now')
        ''', (user_id,))

        goal = cursor.fetchone()

        if not goal:
            # 오늘의 목표가 없으면 생성
            cursor.execute('''
                INSERT INTO daily_goals (user_id, goal_date, target_time, target_score)
                VALUES (?, DATE('now'), 30, 100)
            ''', (user_id,))
            conn.commit()

            cursor.execute('''
                SELECT goal_id, target_time, target_score, achieved_time, achieved_score, completed
                FROM daily_goals
                WHERE user_id = ? AND goal_date = DATE('now')
            ''', (user_id,))
            goal = cursor.fetchone()

        conn.close()
        return dict(goal) if goal else None

    def update_daily_goal(self, user_id, time_to_add=0, score_to_add=0):
        """일일 목표 진행도 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE daily_goals
            SET achieved_time = achieved_time + ?,
                achieved_score = achieved_score + ?,
                completed = CASE
                    WHEN achieved_time + ? >= target_time AND achieved_score + ? >= target_score THEN 1
                    ELSE 0
                END
            WHERE user_id = ? AND goal_date = DATE('now')
        ''', (time_to_add, score_to_add, time_to_add, score_to_add, user_id))

        conn.commit()
        conn.close()

    def set_daily_goal_targets(self, user_id, target_time, target_score):
        """일일 목표 설정"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT OR REPLACE INTO daily_goals
            (user_id, goal_date, target_time, target_score, achieved_time, achieved_score)
            VALUES (?, DATE('now'), ?, ?,
                COALESCE((SELECT achieved_time FROM daily_goals WHERE user_id = ? AND goal_date = DATE('now')), 0),
                COALESCE((SELECT achieved_score FROM daily_goals WHERE user_id = ? AND goal_date = DATE('now')), 0))
        ''', (user_id, target_time, target_score, user_id, user_id))

        conn.commit()
        conn.close()

    # ========== 키 통계 관련 메서드 ==========
    def update_key_stat(self, user_id, key_char, is_correct, press_time=0):
        """키 통계 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO key_statistics (user_id, key_char, total_presses, correct_presses, incorrect_presses, avg_time)
            VALUES (?, ?, 1, ?, ?, ?)
            ON CONFLICT(user_id, key_char)
            DO UPDATE SET
                total_presses = total_presses + 1,
                correct_presses = correct_presses + ?,
                incorrect_presses = incorrect_presses + ?,
                avg_time = (avg_time * total_presses + ?) / (total_presses + 1),
                last_updated = CURRENT_TIMESTAMP
        ''', (user_id, key_char, 1 if is_correct else 0, 0 if is_correct else 1, press_time,
              1 if is_correct else 0, 0 if is_correct else 1, press_time))

        conn.commit()
        conn.close()

    def get_key_statistics(self, user_id, limit=None):
        """키 통계 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        query = '''
            SELECT key_char, total_presses, correct_presses, incorrect_presses, avg_time,
                   ROUND(100.0 * correct_presses / total_presses, 2) as accuracy
            FROM key_statistics
            WHERE user_id = ?
            ORDER BY total_presses DESC
        '''

        if limit:
            query += f' LIMIT {limit}'

        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    def get_weak_keys(self, user_id, limit=10):
        """약한 키 분석 (정확도 낮은 키)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT key_char, total_presses, correct_presses, incorrect_presses,
                   ROUND(100.0 * correct_presses / total_presses, 2) as accuracy,
                   avg_time
            FROM key_statistics
            WHERE user_id = ? AND total_presses >= 5
            ORDER BY accuracy ASC, avg_time DESC
            LIMIT ?
        ''', (user_id, limit))

        records = cursor.fetchall()
        conn.close()
        return [dict(record) for record in records]

    def get_slow_keys(self, user_id, limit=10):
        """느린 키 분석 (평균 시간 긴 키)"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT key_char, total_presses, avg_time,
                   ROUND(100.0 * correct_presses / total_presses, 2) as accuracy
            FROM key_statistics
            WHERE user_id = ? AND total_presses >= 5
            ORDER BY avg_time DESC
            LIMIT ?
        ''', (user_id, limit))

        records = cursor.fetchall()
        conn.close()
        return [dict(record) for record in records]

    # ========== 스트릭 관련 메서드 ==========
    def update_login_streak(self, user_id):
        """로그인 스트릭 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT last_practice_date, login_streak FROM users WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()
        if result:
            last_date = result['last_practice_date']
            current_streak = result['login_streak']

            from datetime import datetime, timedelta
            today = datetime.now().date()

            if last_date:
                last_date_obj = datetime.strptime(last_date, '%Y-%m-%d').date()

                if last_date_obj == today:
                    # 오늘 이미 로그인함
                    pass
                elif last_date_obj == today - timedelta(days=1):
                    # 어제 로그인 -> 스트릭 증가
                    current_streak += 1
                    cursor.execute('''
                        UPDATE users
                        SET login_streak = ?, last_practice_date = DATE('now')
                        WHERE user_id = ?
                    ''', (current_streak, user_id))
                else:
                    # 스트릭 끊김
                    cursor.execute('''
                        UPDATE users
                        SET login_streak = 1, last_practice_date = DATE('now')
                        WHERE user_id = ?
                    ''', (user_id,))
            else:
                # 첫 로그인
                cursor.execute('''
                    UPDATE users
                    SET login_streak = 1, last_practice_date = DATE('now')
                    WHERE user_id = ?
                ''', (user_id,))

        conn.commit()
        conn.close()

    # ========== 사용자 정의 단어 리스트 ==========
    def create_custom_word_list(self, user_id, list_name, words):
        """사용자 정의 단어 리스트 생성"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 리스트를 쉼표로 구분된 문자열로 저장
        words_str = ','.join(words) if isinstance(words, list) else words

        cursor.execute('''
            INSERT INTO custom_word_lists (user_id, list_name, words)
            VALUES (?, ?, ?)
        ''', (user_id, list_name, words_str))

        conn.commit()
        conn.close()

    def get_custom_word_lists(self, user_id):
        """사용자의 커스텀 단어 리스트 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT list_id, list_name, words, created_at
            FROM custom_word_lists
            WHERE user_id = ?
            ORDER BY created_at DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()

        result = []
        for record in records:
            data = dict(record)
            data['words'] = data['words'].split(',')
            result.append(data)

        return result

    def delete_custom_word_list(self, list_id):
        """커스텀 단어 리스트 삭제"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM custom_word_lists WHERE list_id = ?', (list_id,))

        conn.commit()
        conn.close()

    # ========== 테마 설정 ==========
    def update_theme(self, user_id, theme):
        """사용자 테마 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE users SET theme = ? WHERE user_id = ?
        ''', (theme, user_id))

        conn.commit()
        conn.close()

    def get_user_theme(self, user_id):
        """사용자 테마 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT theme FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        conn.close()

        return result['theme'] if result else 'light'

    # ========== 사용자 설정 ==========
    def get_user_settings(self, user_id):
        """사용자 설정 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT sound_enabled, volume, font_size
            FROM user_settings
            WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()

        if not result:
            # 기본 설정 생성
            cursor.execute('''
                INSERT INTO user_settings (user_id, sound_enabled, volume, font_size)
                VALUES (?, 1, 50, 12)
            ''', (user_id,))
            conn.commit()

            cursor.execute('''
                SELECT sound_enabled, volume, font_size
                FROM user_settings
                WHERE user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()

        conn.close()
        return dict(result) if result else None

    def update_user_settings(self, user_id, sound_enabled=None, volume=None, font_size=None):
        """사용자 설정 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if sound_enabled is not None:
            updates.append('sound_enabled = ?')
            params.append(sound_enabled)
        if volume is not None:
            updates.append('volume = ?')
            params.append(volume)
        if font_size is not None:
            updates.append('font_size = ?')
            params.append(font_size)

        if updates:
            params.append(user_id)
            query = f"UPDATE user_settings SET {', '.join(updates)} WHERE user_id = ?"
            cursor.execute(query, params)
            conn.commit()

        conn.close()

    # ========== 통계 대시보드용 데이터 ==========
    def get_practice_history(self, user_id, days=7):
        """최근 N일간의 연습 기록"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DATE(created_at) as practice_date,
                   COUNT(*) as session_count,
                   SUM(score) as total_score,
                   AVG(accuracy) as avg_accuracy,
                   AVG(speed) as avg_speed,
                   SUM(practice_time) as total_time
            FROM practice_records
            WHERE user_id = ? AND created_at >= DATE('now', '-' || ? || ' days')
            GROUP BY DATE(created_at)
            ORDER BY practice_date DESC
        ''', (user_id, days))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    def get_mode_distribution(self, user_id):
        """모드별 연습 분포"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT mode_name, COUNT(*) as count, SUM(practice_time) as total_time
            FROM practice_records
            WHERE user_id = ?
            GROUP BY mode_name
            ORDER BY count DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    # ========== 레벨 시스템 ==========
    def get_user_level(self, user_id):
        """사용자 레벨 정보 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT current_level, current_exp, total_exp
            FROM user_levels
            WHERE user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()

        if not result:
            # 레벨 정보가 없으면 생성
            cursor.execute('''
                INSERT INTO user_levels (user_id, current_level, current_exp, total_exp)
                VALUES (?, 1, 0, 0)
            ''', (user_id,))
            conn.commit()

            cursor.execute('''
                SELECT current_level, current_exp, total_exp
                FROM user_levels
                WHERE user_id = ?
            ''', (user_id,))
            result = cursor.fetchone()

        conn.close()
        return dict(result) if result else None

    def add_exp(self, user_id, exp_amount):
        """경험치 추가 및 레벨업 처리"""
        level_info = self.get_user_level(user_id)
        if not level_info:
            return None

        current_level = level_info['current_level']
        current_exp = level_info['current_exp']
        total_exp = level_info['total_exp']

        new_current_exp = current_exp + exp_amount
        new_total_exp = total_exp + exp_amount

        # 레벨업 계산 (각 레벨당 필요 경험치: level * 100)
        leveled_up = False
        new_level = current_level

        while new_current_exp >= new_level * 100:
            new_current_exp -= new_level * 100
            new_level += 1
            leveled_up = True

        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE user_levels
            SET current_level = ?, current_exp = ?, total_exp = ?
            WHERE user_id = ?
        ''', (new_level, new_current_exp, new_total_exp, user_id))

        conn.commit()
        conn.close()

        return {
            'leveled_up': leveled_up,
            'new_level': new_level,
            'new_exp': new_current_exp,
            'total_exp': new_total_exp
        }

    def get_level_leaderboard(self, limit=10):
        """레벨 리더보드"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.username, l.current_level, l.total_exp
            FROM user_levels l
            JOIN users u ON l.user_id = u.user_id
            ORDER BY l.current_level DESC, l.total_exp DESC
            LIMIT ?
        ''', (limit,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    # ========== 친구 시스템 ==========
    def send_friend_request(self, user_id, friend_username):
        """친구 요청 보내기"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # 친구 ID 찾기
        cursor.execute('SELECT user_id FROM users WHERE username = ?', (friend_username,))
        friend = cursor.fetchone()

        if not friend:
            conn.close()
            return False, "사용자를 찾을 수 없습니다."

        friend_id = friend['user_id']

        if friend_id == user_id:
            conn.close()
            return False, "자기 자신에게 친구 요청을 보낼 수 없습니다."

        try:
            cursor.execute('''
                INSERT INTO friendships (user_id, friend_id, status)
                VALUES (?, ?, 'pending')
            ''', (user_id, friend_id))
            conn.commit()
            conn.close()
            return True, "친구 요청을 보냈습니다."
        except sqlite3.IntegrityError:
            conn.close()
            return False, "이미 친구 요청을 보냈거나 친구입니다."

    def accept_friend_request(self, user_id, friend_id):
        """친구 요청 수락"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE friendships
            SET status = 'accepted', accepted_at = CURRENT_TIMESTAMP
            WHERE friend_id = ? AND user_id = ? AND status = 'pending'
        ''', (user_id, friend_id))

        # 양방향 친구 관계 생성
        try:
            cursor.execute('''
                INSERT INTO friendships (user_id, friend_id, status, accepted_at)
                VALUES (?, ?, 'accepted', CURRENT_TIMESTAMP)
            ''', (user_id, friend_id))
        except:
            pass

        conn.commit()
        conn.close()

    def get_friends(self, user_id):
        """친구 목록 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.user_id, u.username, u.total_score, f.accepted_at
            FROM friendships f
            JOIN users u ON f.friend_id = u.user_id
            WHERE f.user_id = ? AND f.status = 'accepted'
            ORDER BY f.accepted_at DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    def get_friend_requests(self, user_id):
        """받은 친구 요청 목록"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.user_id, u.username, u.total_score, f.requested_at
            FROM friendships f
            JOIN users u ON f.user_id = u.user_id
            WHERE f.friend_id = ? AND f.status = 'pending'
            ORDER BY f.requested_at DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    # ========== 클랜 시스템 ==========
    def create_clan(self, clan_name, description, leader_id):
        """클랜 생성"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO clans (clan_name, description, leader_id)
                VALUES (?, ?, ?)
            ''', (clan_name, description, leader_id))

            clan_id = cursor.lastrowid

            # 리더를 멤버로 추가
            cursor.execute('''
                INSERT INTO clan_members (clan_id, user_id, role)
                VALUES (?, ?, 'leader')
            ''', (clan_id, leader_id))

            conn.commit()
            conn.close()
            return True, clan_id
        except sqlite3.IntegrityError:
            return False, "이미 존재하는 클랜 이름이거나 이미 클랜에 소속되어 있습니다."

    def join_clan(self, clan_id, user_id):
        """클랜 가입"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO clan_members (clan_id, user_id, role)
                VALUES (?, ?, 'member')
            ''', (clan_id, user_id))

            cursor.execute('''
                UPDATE clans
                SET total_members = total_members + 1
                WHERE clan_id = ?
            ''', (clan_id,))

            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_clan(self, user_id):
        """사용자가 속한 클랜 정보"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT c.clan_id, c.clan_name, c.description, c.total_members,
                   cm.role, cm.contribution
            FROM clan_members cm
            JOIN clans c ON cm.clan_id = c.clan_id
            WHERE cm.user_id = ?
        ''', (user_id,))

        result = cursor.fetchone()
        conn.close()

        return dict(result) if result else None

    def get_clan_members(self, clan_id):
        """클랜 멤버 목록"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT u.username, cm.role, cm.contribution, cm.joined_at
            FROM clan_members cm
            JOIN users u ON cm.user_id = u.user_id
            WHERE cm.clan_id = ?
            ORDER BY cm.contribution DESC
        ''', (clan_id,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]

    # ========== 시즌 패스 ==========
    def get_season_pass(self, user_id, season_number=1):
        """시즌 패스 정보 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT tier, season_exp, is_premium
            FROM season_pass
            WHERE user_id = ? AND season_number = ?
        ''', (user_id, season_number))

        result = cursor.fetchone()

        if not result:
            # 시즌 패스 정보가 없으면 생성
            cursor.execute('''
                INSERT INTO season_pass (user_id, season_number, tier, season_exp)
                VALUES (?, ?, 0, 0)
            ''', (user_id, season_number))
            conn.commit()

            cursor.execute('''
                SELECT tier, season_exp, is_premium
                FROM season_pass
                WHERE user_id = ? AND season_number = ?
            ''', (user_id, season_number))
            result = cursor.fetchone()

        conn.close()
        return dict(result) if result else None

    def add_season_exp(self, user_id, exp_amount, season_number=1):
        """시즌 경험치 추가"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE season_pass
            SET season_exp = season_exp + ?,
                tier = (season_exp + ?) / 100
            WHERE user_id = ? AND season_number = ?
        ''', (exp_amount, exp_amount, user_id, season_number))

        conn.commit()
        conn.close()

    # ========== 손가락별 통계 ==========
    def update_finger_stat(self, user_id, finger_name, is_correct, press_time=0):
        """손가락별 통계 업데이트"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO finger_statistics (user_id, finger_name, total_presses, correct_presses, avg_speed)
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT(user_id, finger_name)
            DO UPDATE SET
                total_presses = total_presses + 1,
                correct_presses = correct_presses + ?,
                avg_speed = (avg_speed * total_presses + ?) / (total_presses + 1)
        ''', (user_id, finger_name, 1 if is_correct else 0, press_time,
              1 if is_correct else 0, press_time))

        conn.commit()
        conn.close()

    def get_finger_statistics(self, user_id):
        """손가락별 통계 조회"""
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT finger_name, total_presses, correct_presses, avg_speed,
                   ROUND(100.0 * correct_presses / total_presses, 2) as accuracy
            FROM finger_statistics
            WHERE user_id = ?
            ORDER BY total_presses DESC
        ''', (user_id,))

        records = cursor.fetchall()
        conn.close()

        return [dict(record) for record in records]
