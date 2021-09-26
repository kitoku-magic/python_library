from python_library.src import abc
from python_library.src import re
from python_library.src import sa
from python_library.src import saed
from python_library.src import sao
from python_library.src.custom_sqlalchemy.custom_sql_execution_context import custom_sql_execution_context
from src.application import app

class DeclarativeABCMeta(saed.DeclarativeMeta, abc.ABCMeta):
    """
    SQLAlchemyの基底クラスを抽象クラス化する為の定義
    """
    pass

engine = sa.create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    echo=app.config['SQLALCHEMY_ECHO'],
    connect_args=app.config['SQLALCHEMY_ENGINE_OPTIONS']
)

# セッションの設定
session_options = app.config['SQLALCHEMY_SESSION_OPTIONS']
session_options['bind'] = engine
session = sao.scoped_session(
    sao.sessionmaker(**session_options)
)

db = saed.declarative_base(bind=engine, metaclass=DeclarativeABCMeta)
db.query = session.query_property()

# 静的プリペアドステートメントを使う為に、cursorをカスタマイズする為
engine.dialect.execution_ctx_cls = custom_sql_execution_context

# 何度も実行する為、事前にコンパイル
sql_parameter_replace_pattern = re.compile('%\(.+?\)s')

@sa.event.listens_for(engine, 'before_cursor_execute', retval=True)
def change_prepared_statement(conn, cursor, statement, parameters, context, executemany):
    """
    SQL実行前に静的プリペアドステートメントを実行出来る様にSQLとパラメータを書き換える
    """
    statement = sql_parameter_replace_pattern.sub('%s', statement)
    if isinstance(parameters, tuple):
        # 複数件のINSERTなどは、tupleになっている
        param_list = []
        for dictionary in parameters:
            param_list.append(tuple(dictionary.values()))
        ret = tuple(param_list)
        return statement, ret
    else:
        parameters = tuple(parameters.values())
        return statement, parameters
