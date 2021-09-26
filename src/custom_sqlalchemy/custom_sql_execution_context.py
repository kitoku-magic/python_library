from python_library.src import sadmb

class custom_sql_execution_context(sadmb.MySQLExecutionContext):
    """
    SQLの実行コンテキストクラス（静的プリペアドステートメントにする為にカスタマイズ）
    """
    def create_cursor(self):
        self._is_server_side = False
        return self._dbapi_connection.cursor(prepared=True)
    def get_lastrowid(self):
        return self.cursor.lastrowid
