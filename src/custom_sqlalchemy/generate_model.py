# -*- coding: utf-8 -*-↲

# モデルのエンティティクラスを自動生成するプログラム

from python_library.src import os
from python_library.src import sa
from python_library.src import saea
from python_library.src import sai
from python_library.src import sys
from src.instance.instance import development

if len(sys.argv) < 2:
    print('引数の数が不足しています')
    exit()

if os.path.isdir(sys.argv[1]) == False:
    print('引数に指定したディレクトリが存在しません')
    exit()

app_base_dir = sys.argv[1]

Base = saea.automap_base()

engine = sa.create_engine(development.SQLALCHEMY_DATABASE_URI)
Base.prepare(engine, reflect=True)

column_data_type_import_name_mappings = {
    'sqlalchemy.sql.sqltypes': 'sasst',
    'sqlalchemy.dialects.mysql.types': 'sadm',
}

# 1ファイル、1テーブルの関係
for table in sorted(Base.classes.items()):
    # エンティティ基底クラスの作成
    inspect_table = sai.inspect(table[1])
    local_table_name = inspect_table.persist_selectable.name
    # 自動生成するファイル名とクラス名は、オリジナルから変えておく
    local_class_name = local_table_name + '_entity_base'
    base_path = app_base_dir + '/src/model/entity/generate/'
    base_path += local_class_name + '.py'
    file_handler = open(base_path, mode='w')
    require_import_list = [
        'from src import typing'
    ]
    sqlalchemy_import_list = [
        'from python_library.src import saed',
        'from python_library.src import sassc'
    ]
    custom_data_type_import_list = list()
    entity_class_import_list = [
        'from python_library.src.custom_sqlalchemy.entity import entity'
    ]
    length_body = ''
    length_property_body = ''
    property_body = ''
    created_at_body = ''
    updated_at_body = ''
    insert_column_name_list_body = '    def get_insert_column_name_list(self: typing.Type[T]) -> typing.List[str]:\n'
    insert_column_name_list_body += '        return ['
    update_column_name_list_body = '    def get_update_column_name_list(self: typing.Type[T]) -> typing.List[str]:\n'
    update_column_name_list_body += '        return ['
    is_use_timestamp_mixin = False
    timestamp_column_data_types = list()
    columns = inspect_table.persist_selectable.columns._all_columns
    # 1カラムずつ処理
    for column in columns:
        column_attr_list = []
        # データ型の設定
        data_type_name = column.type.__class__.__name__
        # BLOB系は、独自の拡張型にする
        if 'BLOB' in data_type_name:
            data_type_name = 'custom_blob'
        # VARBINARYは、独自の拡張型にする
        elif 'VARBINARY' == data_type_name:
            data_type_name = 'custom_varbinary'
        else:
            if column.type.__class__.__module__ in column_data_type_import_name_mappings:
                data_type_name = column_data_type_import_name_mappings[column.type.__class__.__module__] + '.' + data_type_name
        data_type = data_type_name + '('
        data_type_attr_list = []
        if hasattr(column.type, 'unsigned') and column.type.unsigned is not None:
            data_type_attr_list.append('unsigned = ' + str(column.type.unsigned))
        if hasattr(column.type, 'length') and column.type.length is not None:
            # 桁数の数値は、定数にする
            upper_column_name = column.name.upper()
            data_type_attr_list.append(local_class_name + '.__' + upper_column_name + '_LENGTH')
            length_body += '    __' + upper_column_name + '_LENGTH: int = ' + str(column.type.length) + '\n'
            length_property_body += '    def get_' + column.name + '_length(cls: typing.Type[T]) -> int:\n'
            length_property_body += '        return ' + local_class_name + '.__' + upper_column_name + '_LENGTH\n'
        data_type += ', '.join(data_type_attr_list) + ')'
        column_attr_list.append(data_type)
        # 外部キーの設定
        if hasattr(column, 'foreign_keys') and len(column.foreign_keys) > 0:
            for foreign_key in column.foreign_keys:
                column_attr_list.append("sa.ForeignKey('" + foreign_key._colspec + "')")
            if 'from python_library.src import sa' not in sqlalchemy_import_list:
                sqlalchemy_import_list.append('from python_library.src import sa')
        # NULLの設定
        if hasattr(column, 'nullable') and column.nullable is not None:
            column_attr_list.append('nullable = ' + str(column.nullable))
        # DEFAULTの設定（クラスの中の値に入っている）
        if hasattr(column, 'server_default') and \
           column.server_default is not None and \
           hasattr(column.server_default, 'arg') and \
           'TextClause' == column.server_default.arg.__class__.__name__:
            column_attr_list.append('server_default = ' + str(column.server_default.arg.text))
        # AUTO_INCREMENTの設定
        if hasattr(column, 'autoincrement') and column.autoincrement is True:
            column_attr_list.append('autoincrement = ' + str(column.autoincrement))
        # PRIMARY KEYの設定
        if hasattr(column, 'primary_key') and column.primary_key is True:
            column_attr_list.append('primary_key = ' + str(column.primary_key))
        # UNIQUE KEYの設定
        if hasattr(column, 'unique') and column.unique is True:
            column_attr_list.append('unique = ' + str(column.unique))
        # INDEXの設定
        if hasattr(column, 'index') and column.index is True:
            column_attr_list.append('index = ' + str(column.index))
        # コメントの設定
        if hasattr(column, 'comment') and column.comment is not None:
            column_attr_list.append("comment = '" + str(column.comment) + "'")
        # created_atとupdated_atが両方存在する場合は、専用のmixinを使うので、ここではまだ設定しない
        if 'created_at' == column.name:
            created_at_body += '    ' + column.name + ' = sassc.Column(' + ', '.join(column_attr_list) + ')\n'
            timestamp_column_data_types.append(column.type.__class__.__module__)
        elif 'updated_at' == column.name:
            updated_at_body += '    ' + column.name + ' = sassc.Column(' + ', '.join(column_attr_list) + ')\n'
            timestamp_column_data_types.append(column.type.__class__.__module__)
        else:
            property_body += '    @saed.declared_attr\n'
            property_body += '    def ' + column.name + '(cls: typing.Type[T]) -> sassc.Column:\n'
            property_body += '        return sassc.Column(' + ', '.join(column_attr_list) + ')\n'
            if data_type_name.startswith('custom_') == True:
                import_str = 'from python_library.src.custom_sqlalchemy.' + data_type_name + ' import ' + data_type_name
                if import_str not in custom_data_type_import_list:
                    custom_data_type_import_list.append(import_str)
            else:
                if column.type.__class__.__module__ in column_data_type_import_name_mappings:
                    import_str = 'from python_library.src import ' + column_data_type_import_name_mappings[column.type.__class__.__module__]
                    if import_str not in sqlalchemy_import_list:
                        sqlalchemy_import_list.append(import_str)
        # 追加・更新可能カラムのリストを作成
        if hasattr(column, 'autoincrement') and column.autoincrement is True:
            continue
        insert_column_name_list_body += "'" + column.name + "', "
        if 'created_at' != column.name:
            update_column_name_list_body += "'" + column.name + "', "
    if len(timestamp_column_data_types) == 1:
        if timestamp_column_data_types[0] in column_data_type_import_name_mappings:
            import_str = 'from python_library.src import ' + column_data_type_import_name_mappings[timestamp_column_data_types[0]]
            if import_str not in sqlalchemy_import_list:
                sqlalchemy_import_list.append(import_str)
    # リレーションの設定
    relation_body = ''
    many_variables_suffix = '_collection'
    for key in dir(inspect_table.relationships):
        # keyが「_」から始まらない場合は、リレーションプロパティ名が入っている
        if True == key.startswith('_'):
            continue
        prop = getattr(inspect_table.relationships, key)
        foreign_table_name = prop.mapper.persist_selectable.name
        foreign_class_name = foreign_table_name + '_entity'
        # リレーションが複数カラムかどうか
        if True == hasattr(prop.primaryjoin, 'clauses'):
            primaryjoin = "primaryjoin='" + prop.primaryjoin.operator.__name__ + "("
            for clause in prop.primaryjoin.clauses:
                primaryjoin += local_table_name + "_entity." + clause.left.key + " == " + foreign_class_name + "." + clause.right.key + ", "
            primaryjoin = primaryjoin.rstrip(', ') + ")', "
        else:
            primaryjoin = ''
        cascade = ",".join([x for x in sorted(prop._cascade)])
        # TODO: 1対1の場合、これでは動かなさそう
        relation_body += '    @saed.declared_attr\n'
        if prop.backref is None:
            relation_body += '    def ' + foreign_table_name + many_variables_suffix + '(cls: typing.Type[T]) -> saor.RelationshipProperty:\n'
            relation_body += "        return sao.relationship('" + foreign_class_name + "', " + primaryjoin + "back_populates='" + local_table_name + "', cascade='" + cascade + "', uselist=True)\n"
        else:
            relation_body += '    def ' + foreign_table_name + '(cls: typing.Type[T]) -> saor.RelationshipProperty:\n'
            relation_body += "        return sao.relationship('" + foreign_class_name + "', " + primaryjoin + "back_populates='" + local_table_name + many_variables_suffix + "', cascade='" + cascade + "', uselist=False)\n"
        if 'from python_library.src import sao' not in sqlalchemy_import_list:
            sqlalchemy_import_list.append('from python_library.src import sao')
        if 'from python_library.src import saor' not in sqlalchemy_import_list:
            sqlalchemy_import_list.append('from python_library.src import saor')
    timestamp_mixin_body = ''
    # created_atとupdated_atが両方存在するか調べる
    if '' != created_at_body:
        if '' != updated_at_body:
            timestamp_mixin_body += 'timestamp_mixin_entity, '
            is_use_timestamp_mixin = True
            entity_class_import_list.append('from python_library.src.custom_sqlalchemy.timestamp_mixin_entity import timestamp_mixin_entity')
        else:
            property_body += created_at_body
    elif '' != updated_at_body:
        property_body += updated_at_body
    body = ''
    body += '\n'.join(sorted(require_import_list)) + '\n'
    body += '\n'.join(sorted(sqlalchemy_import_list)) + '\n'
    body += '\n'.join(sorted(custom_data_type_import_list)) + '\n'
    body += '\n'.join(sorted(entity_class_import_list)) + '\n'
    body += '\n'
    body += "T = typing.TypeVar('T', bound='" + local_class_name + "')\n"
    body += '\n'
    body += 'class ' + local_class_name + '('
    body += timestamp_mixin_body
    body += 'entity):\n'
    body += '    """\n'
    body += '    ' + inspect_table.persist_selectable.comment + 'テーブルエンティティの基底クラス\n'
    body += '    """\n'
    body += "    __abstract__: bool = True\n"
    body += length_body + '\n'
    if '' != length_property_body:
        body += length_property_body + '\n'
    body += property_body
    body += relation_body + '\n'
    # コンストラクタの設定
    body += '    def __init__(self: typing.Type[T]) -> None:\n'
    if True == is_use_timestamp_mixin:
        super_class_name = 'timestamp_mixin_entity'
    else:
        super_class_name = 'entity'
    body += '        ' + super_class_name + '.__init__(self)\n'
    body += '    def set_validation_setting(self: typing.Type[T]) -> None:\n'
    body += '        pass\n'
    body += insert_column_name_list_body.rstrip(', ') + ']\n'
    body += update_column_name_list_body.rstrip(', ') + ']\n'
    file_handler.write(body)
    file_handler.close()

    # エンティティクラスの存在確認と作成
    local_class_name = local_table_name + '_entity'
    base_path = app_base_dir + '/src/model/entity/'
    base_path += local_class_name + '.py'
    if os.path.isfile(base_path) == False:
        file_handler = open(base_path, mode='w')
        body = ''
        body += '\n'.join(sorted(require_import_list)) + '\n'
        body += 'from src.model.entity.generate.' + local_class_name + '_base import ' + local_class_name + '_base\n'
        body += '\n'
        body += "T = typing.TypeVar('T', bound='" + local_class_name + "')\n"
        body += '\n'
        body += 'class ' + local_class_name + '(' + local_class_name + '_base):\n'
        body += '    """\n'
        body += '    ' + inspect_table.persist_selectable.comment + 'テーブルのエンティティクラス\n'
        body += '    """\n'
        # コンストラクタの設定
        body += '    def __init__(self: typing.Type[T]) -> None:\n'
        body += '        super().__init__()\n'
        file_handler.write(body)
        file_handler.close()

    # リポジトリクラスの存在確認と作成
    local_repository_class_name = local_table_name + '_repository'
    base_path = app_base_dir + '/src/model/repository/'
    base_path += local_repository_class_name + '.py'
    if os.path.isfile(base_path) == False:
        file_handler = open(base_path, mode='w')
        body = ''
        body += 'from python_library.src.custom_sqlalchemy.repository import repository\n'
        body += '\n'.join(sorted(require_import_list)) + '\n'
        body += 'from src.model.entity.' + local_class_name + ' import ' + local_class_name + '\n'
        body += '\n'
        body += "T = typing.TypeVar('T', bound='" + local_repository_class_name + "')\n"
        body += '\n'
        body += 'class ' + local_repository_class_name + '(repository):\n'
        body += '    """\n'
        body += '    ' + inspect_table.persist_selectable.comment + 'テーブルのリポジトリクラス\n'
        body += '    """\n'
        # コンストラクタの設定
        body += '    def __init__(self: typing.Type[T], ' + local_class_name + ': ' + local_class_name + ') -> None:\n'
        body += '        super().__init__(' + local_class_name + ')\n'
        file_handler.write(body)
        file_handler.close()
