import duckdb
from datetime import datetime

# 全局實例
_chat_history = None

def get_chat_history():
    global _chat_history
    if _chat_history is None:
        _chat_history = MemoryChatHistory()
    return _chat_history

class MemoryChatHistory:
    def __init__(self):
        self.db = duckdb.connect(':memory:')  # 使用內存數據庫
        self._init_db()
        self.TIMEOUT = 300  # 5分鐘無活動自動結束對話
        print("初始化 MemoryChatHistory")  # 調試日誌

    def _init_db(self):
        """初始化數據庫表"""
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS chat_history (
                user_id VARCHAR,
                message TEXT,
                response TEXT,
                timestamp TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS chat_status (
                user_id VARCHAR PRIMARY KEY,
                is_chatting BOOLEAN,
                last_activity TIMESTAMP
            );
        """)

    def start_chat(self, user_id):
        """開始對話模式"""
        self.db.execute("""
            INSERT OR REPLACE INTO chat_status (user_id, is_chatting, last_activity)
            VALUES (?, TRUE, CURRENT_TIMESTAMP)
        """, [user_id])

    def end_chat(self, user_id):
        """結束對話模式"""
        self.db.execute("""
            INSERT OR REPLACE INTO chat_status (user_id, is_chatting, last_activity)
            VALUES (?, FALSE, NULL)
        """, [user_id])

    def is_chatting(self, user_id):
        """檢查是否在對話模式"""
        result = self.db.execute("""
            SELECT is_chatting, last_activity 
            FROM chat_status 
            WHERE user_id = ?
        """, [user_id]).fetchone()

        if not result:
            return False

        is_chatting, last_activity = result

        if not is_chatting:
            return False

        # 檢查超時
        if last_activity:
            try:
                # 只取前19個字符，去掉毫秒部分
                last_active_str = str(last_activity)[:19]
                last_active = datetime.strptime(last_active_str, '%Y-%m-%d %H:%M:%S')
                if (datetime.now() - last_active).total_seconds() > self.TIMEOUT:
                    self.end_chat(user_id)
                    return False
            except Exception as e:
                print(f"時間解析錯誤: {e}, 原始值: {last_activity}")
                return False

        return True

    def update_activity(self, user_id):
        """更新最後活動時間"""
        self.db.execute("""
            UPDATE chat_status 
            SET last_activity = CURRENT_TIMESTAMP
            WHERE user_id = ?
        """, [user_id])

    def add_history(self, user_id, message, response):
        """添加新的對話記錄"""
        try:
            self.db.execute("""
                INSERT INTO chat_history (user_id, message, response, timestamp)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, [user_id, message, response])
            
            # 驗證插入
            result = self.db.execute("""
                SELECT COUNT(*) FROM chat_history WHERE user_id = ?
            """, [user_id]).fetchone()[0]
            
            print(f"已存儲對話記錄，用戶 {user_id} 當前有 {result} 條記錄")  # 調試日誌
            
            # 清理舊記錄
            self.db.execute("""
                DELETE FROM chat_history 
                WHERE user_id = ? 
                AND timestamp NOT IN (
                    SELECT timestamp 
                    FROM chat_history 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT 30
                )
            """, [user_id, user_id])
            
        except Exception as e:
            print(f"存儲對話記錄失敗: {e}")  # 調試日誌

    def get_recent_history(self, user_id, limit=5):
        """獲取最近的對話記錄"""
        result = self.db.execute("""
            SELECT message, response
            FROM chat_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, [user_id, limit]).fetchall()
        
        return [(msg, resp) for msg, resp in reversed(result)]