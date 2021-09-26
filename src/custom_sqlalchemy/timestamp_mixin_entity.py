from python_library.src import sa
from python_library.src import saed
from python_library.src import sasf
from python_library.src import sassc
from python_library.src import sasst
from python_library.src.custom_sqlalchemy.entity import entity

class timestamp_mixin_entity(entity):
    """
    タイムスタンプを設定するエンティティのミックスイン
    """
    __abstract__ = True
    def __init__(self):
        super().__init__()
        self.created_at = sasf.current_timestamp()
        self.updated_at = sasf.current_timestamp()

    @saed.declared_attr
    def created_at(cls):
        return sassc.Column(sasst.DATETIME, nullable = False, server_default = sa.text('CURRENT_TIMESTAMP'), comment = '作成日時')
    @saed.declared_attr
    def updated_at(cls):
        return sassc.Column(sasst.DATETIME, nullable = False, server_default = sa.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment = '更新日時')
