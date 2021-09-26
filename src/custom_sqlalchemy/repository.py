from python_library.src import sa
from python_library.src.custom_sqlalchemy.db_manager import db_manager
from python_library.src.original.util import util

class repository():
    """
    全てのテーブルの基底リポジトリクラス
    """
    __db_manager = None
    def __new__(cls, main_entity):
        cls.__db_manager = db_manager()
        return super().__new__(cls)
    def __init__(self, main_entity):
        self.__main_entity = main_entity
        self.__main_entity_class = self.__main_entity.__class__
        self.__table_name = self.__main_entity.__tablename__
        self.__last_insert_id = None
    def get_db_manager(self):
        return self.__db_manager
    def set_main_entity(self, main_entity):
        self.__main_entity = main_entity
    def get_main_entity(self):
        return self.__main_entity
    def set_main_entity_class(self, main_entity_class):
        self.__main_entity_class = main_entity_class
    def get_main_entity_class(self):
        return self.__main_entity_class
    def select(self, columns, where = '', params = {}, order_by = '', for_update = False):
        """
        SELECT文を作成する
        """
        # TODO: GROUP BYなど足りない分は、必要に応じて追加
        query = self.get_db_manager().get_session().query(*columns)
        if 0 < len(params):
            query = query.filter(sa.text(where)).params(**params)
        if '' != order_by:
            query = query.order_by(sa.text(order_by))
        if True == for_update:
            query = query.with_for_update()
        return query
    def find(self, columns = (), where = '', params = {}, order_by = '', for_update = False):
        """
        該当するデータを１件取得する
        """
        return self.select(columns, where, params, order_by, for_update).first()
    def find_all(self, columns, where = '', params = (), order_by = ''):
        """
        該当するデータを全件取得する
        """
        return self.select(columns, where, params, order_by).all()
    def insert(self, insert_entities, target_column_name_list):
        """
        INSERT文を実行する
        """
        insert_entities = self.set_timestamp('ins', insert_entities)
        insert_list = []
        for insert_entity in insert_entities:
            insert_dict = {}
            for target_column_name in target_column_name_list:
                insert_dict[target_column_name] = getattr(insert_entity, target_column_name)
            insert_list.append(insert_dict)
        result = self.get_db_manager().get_session().execute(self.__main_entity_class.__table__.insert(), insert_list)
        if 'inserted_primary_key_rows' in result.context.__dict__:
            self.__last_insert_id = result.context.inserted_primary_key_rows[-1][0]
            return len(result.context.inserted_primary_key_rows)
        else:
            # 複数行のINSERT時に、挿入件数を取得する方法は無い？
            return len(insert_list)
    def bulk_insert(self, entities):
        """
        BULK INSERT文を実行する
        """
        # ORM機能として、バルクインサート機能は存在しない？（bulk_insert_mappings()も、複数回INSERT文を実行していたので）
        return self.bulk_insert_raw(entities)
    def update(self, columns, where = '', where_params = {}, synchronize_session = False):
        """
        UPDATE文を実行する
        """
        query = self.get_db_manager().get_session().query(self.__main_entity_class)
        if 0 < len(where_params):
            query = query.filter(sa.text(where)).params(**where_params)
        self.set_timestamp_raw('upd', columns)
        update_params = {}
        for column in columns:
            update_params[column] = getattr(self.__main_entity, column)
        row_count = query.update(update_params, synchronize_session = synchronize_session)
        return row_count
    def delete(self, where = '', params = {}, synchronize_session = False):
        """
        DELETE文を実行する
        """
        query = self.get_db_manager().get_session().query(self.__main_entity_class)
        if 0 < len(params):
            query = query.filter(sa.text(where)).params(**params)
        row_count = query.delete(synchronize_session)
        return row_count
    def set_timestamp(self, mode, entities):
        """
        タイムスタンプ値を設定する
        """
        for entity in entities:
            if 'ins' == mode:
                if True == hasattr(entity, 'created_at'):
                    entity.created_at = util.get_current_datetime()
            if True == hasattr(entity, 'updated_at'):
                entity.updated_at = util.get_current_datetime()
        return entities
    def last_insert_id(self):
        """
        直近の主キーの値を取得
        """
        return self.__last_insert_id
    def begin(self, subtransactions = True):
        """
        トランザクション開始
        """
        # session.beginだと、session.executeの更新の管理が出来ない？様なので
        #return self.get_db_manager().get_session().begin(subtransactions)
        # これはこれで、トランザクションの入れ子に未対応なので微妙
        # プリペアドステートメントにするとエラーになるので、単発のクエリで実行
        self.get_db_manager().get_session().connection().connection.cmd_query('START TRANSACTION')
    def commit(self):
        """
        トランザクションコミット
        """
        #self.get_db_manager().get_session().commit()
        self.get_db_manager().get_session().connection().connection.cmd_query('COMMIT')
    def rollback(self):
        """
        トランザクションロールバック
        """
        #self.get_db_manager().get_session().rollback()
        self.get_db_manager().get_session().connection().connection.cmd_query('ROLLBACK')
    # 以下は、ORM機能を用いないでSQLを実行する関数群
    def select_raw(self, columns, where = '', params = (), order_by = '', for_update = False):
        """
        SELECT文を実行する
        """
        # TODO: GROUP BYなど足りない分は、必要に応じて追加
        sql = 'SELECT ' + ', '.join(columns)
        if self.__table_name is not None:
            sql += ' FROM ' + self.__table_name
        if '' != where:
            sql += ' WHERE ' + where
        if '' != order_by:
            sql += ' ORDER BY ' + order_by
        if True == for_update:
            sql += ' FOR UPDATE'
        self.get_db_manager().get_cursor().execute(sql, params)
    def find_raw(self, columns, where = '', params = (), order_by = '', for_update = False):
        """
        該当するデータを１件取得する
        """
        self.select_raw(columns, where, params, order_by, for_update)
        return self.get_db_manager().get_cursor().fetchone()
    def find_all_raw(self, columns, where = '', params = (), order_by = ''):
        """
        該当するデータを全件取得する
        """
        self.select_raw(columns, where, params, order_by)
        return self.get_db_manager().get_cursor().fetchall()
    def insert_raw(self, columns):
        """
        INSERT文を実行する
        """
        self.set_timestamp_raw('ins', columns)
        sql = 'INSERT INTO ' + self.__table_name + '('
        values = ''
        bind_values = list()
        for column in columns:
            sql += column + ', '
            values += '%s, '
            bind_values.append(getattr(self.__main_entity, column))
        sql = sql.rstrip(', ')
        values = values.rstrip(', ')
        sql += ') VALUES(' + values + ');'
        return self.execute_update_raw(sql, bind_values)
    def bulk_insert_raw(self, entities):
        """
        BULK INSERT文を実行する
        """
        sql = 'INSERT INTO '
        table_name = ''
        column_names = ''
        values = ''
        bind_values = list()
        for entity in entities:
            self.__main_entity = entity
            table_name = self.__main_entity.__tablename__
            columns = self.__main_entity.get_insert_column_name_list()
            self.set_timestamp_raw('ins', columns)
            tmp_column_names = ''
            tmp_values = ''
            for column in columns:
                tmp_column_names += column + ', '
                tmp_values += '%s, '
                bind_values.append(getattr(self.__main_entity, column))
            column_names = tmp_column_names
            values += '(' + tmp_values.rstrip(', ') + '),'
        sql += table_name + '('
        column_names = column_names.rstrip(', ')
        values = values.rstrip(',')
        sql += column_names + ') VALUES' + values + ';'
        return self.execute_update_raw(sql, bind_values)
    def update_raw(self, columns, where = '', params = ()):
        """
        UPDATE文を実行する
        """
        self.set_timestamp_raw('upd', columns)
        sql = 'UPDATE ' + self.__table_name + ' SET '
        bind_values = list()
        for column in columns:
            sql += column + ' = %s, '
            bind_values.append(getattr(self.__main_entity, column))
        sql = sql.rstrip(', ')
        if '' != where:
            sql += ' WHERE ' + where
            for value in params:
                bind_values.append(value)
        return self.execute_update_raw(sql, bind_values)
    def delete_raw(self, where = '', params = ()):
        """
        DELETE文を実行する
        """
        sql = 'DELETE FROM ' + self.__table_name
        bind_values = list()
        if '' != where:
            sql += ' WHERE ' + where
            for value in params:
                bind_values.append(value)
        return self.execute_update_raw(sql, bind_values)
    def set_timestamp_raw(self, mode, columns):
        """
        タイムスタンプ値を設定する
        """
        if 'ins' == mode:
            if 'created_at' in columns:
                self.__main_entity.created_at = util.get_current_datetime()
        if 'updated_at' in columns:
            self.__main_entity.updated_at = util.get_current_datetime()
    def execute_update_raw(self, sql, bind_values):
        """
        データを追加・更新・削除する
        """
        self.get_db_manager().get_cursor().execute(sql, tuple(bind_values))
        return self.get_db_manager().get_cursor().rowcount
    def last_insert_id_raw(self):
        """
        直近の主キーの値を取得
        """
        return self.get_db_manager().get_cursor().lastrowid
    def begin_raw(self, consistent_snapshot=False, isolation_level=None, readonly=None):
        """
        トランザクション開始
        """
        self.get_db_manager().get_connection().start_transaction(consistent_snapshot, isolation_level, readonly)
    def commit_raw(self):
        """
        トランザクションコミット
        """
        self.get_db_manager().get_connection().commit()
    def rollback_raw(self):
        """
        トランザクションロールバック
        """
        self.get_db_manager().get_connection().rollback()
