from python_library.src import abc
from python_library.src import hashlib
from python_library.src import inspect
from python_library.src import magic
from python_library.src import os
from python_library.src import re
from python_library.src import saed
from python_library.src import werkzeug
from python_library.src.custom_sqlalchemy.database import db
from python_library.src.original.util import util
from src.application import app

class entity(db):
    """
    全てのエンティティの基底クラス
    """
    __abstract__ = True
    def __init__(self):
        self.__validation_settings = {}
        self.__is_any_item = False
        property_dict = self.get_all_properties()
        for field, value in property_dict.items():
            setattr(self, field, value)
    @abc.abstractmethod
    def set_validation_setting(self):
        # TODO: raiseした方が良いか？
        pass
    @saed.declared_attr
    def __tablename__(cls):
        return cls.__name__.lower().replace('_entity', '')
    def validate(self):
        """
        バリデーションを行う
        """
        result = True
        for name, validation_setting in self.__validation_settings.items():
            # 項目毎に初期化して、前回の状態を引き継がないようにする
            self.__is_any_item = False
            for rule_name, options in validation_setting['rules'].items():
                options['name'] = name
                method_name = 'is_' + rule_name
                ret = getattr(self, method_name)(getattr(self, name), options)
                if False == ret:
                    result = False
                    if 'message' in options:
                        message = options['message']
                    else:
                        message_format = app.config[rule_name.upper() + '_MESSAGE']
                        message = message_format.replace('{show_name}', validation_setting['show_name']);
                    # エラーメッセージを設定
                    setattr(self, name + '_error', message)
                    # チェックを継続する設定になっていなければ、次の項目へ
                    if 'is_next' not in options or True != options['is_next']:
                        break
        return result
    def is_required(self, value, options):
        """
        必須項目チェック
        """
        return value is not None
    def is_not_empty(self, value, options):
        """
        未入力チェック
        """
        return '' != value and [] != value
    def is_allow_empty(self, value, options):
        """
        未入力を許可する
        """
        self.__is_any_item = True
    def is_min_length(self, value, options):
        """
        最小桁数チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return util.check_min_length(value, options['value'])
        else:
            return True
    def is_max_length(self, value, options):
        """
        最大桁数チェック
        """
        return util.check_max_length(value, options['value'])
    def is_mail_format(self, value, options):
        """
        メール書式チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            r = util.check_mail_format(value)
            return r
        else:
            return True
    def is_mail_domain(self, value, options):
        """
        メールドメインチェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            r = util.check_mail_domain(value)
            return r
        else:
            return True
    def is_alpha_num(self, value, options):
        """
        半角英数字チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return re.match('\A[a-zA-Z0-9]+\Z', value) is not None
        else:
            return True
    def is_japanese(self, value, options):
        """
        日本語（ひらがな、カタカナ、漢字）チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return re.match('\A(?:[' + app.config['PATTERN_HIRAGANA'] + app.config['PATTERN_KATAKANA'] + '][' + app.config['PATTERN_DAKUTEN'] + ']?|' + app.config['PATTERN_CHOON'] + '|' + app.config['PATTERN_KANJI'] + '?)+\Z', value) is not None
        else:
            return True
    def is_japanese_extend(self, value, options):
        """
        日本語（ひらがな、カタカナ、漢字、全角数字、全角スペース）チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return re.match('\A(?:[' + app.config['PATTERN_HIRAGANA'] + app.config['PATTERN_KATAKANA'] + '][' + app.config['PATTERN_DAKUTEN'] + ']?|' + app.config['PATTERN_CHOON'] + '|' + app.config['PATTERN_KANJI'] + '?|[' + app.config['PATTERN_FULL_WIDTH_NUMBER'] + ']|' + app.config['PATTERN_FULL_WIDTH_SPACE'] + ')+\Z', value) is not None
        else:
            return True
    def is_hiragana(self, value, options):
        """
        ひらがなチェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return re.match('\A(?:[' + app.config['PATTERN_HIRAGANA'] + '][' + app.config['PATTERN_DAKUTEN'] + ']?)+\Z', value) is not None
        else:
            return True
    def is_number(self, value, options):
        """
        半角数字チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            if True == isinstance(value, list):
                result = True
                for val in value:
                    result = self.is_number(val, options)
                    if False == result:
                        break
                return result
            else:
                value = self.get_entity_field_value(value, options)
                return re.match('\A[0-9]+\Z', value) is not None
        else:
            return True
    def is_integer(self, value, options):
        """
        整数チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            if True == isinstance(value, list):
                result = True
                for val in value:
                    result = self.is_number(val, options)
                    if False == result:
                        break
                return result
            else:
                r = None
                value = self.get_entity_field_value(value, options)
                try:
                    r = float(value)
                except ValueError:
                    return False
                else:
                    return r.is_integer()
        else:
            return True
    def is_range(self, value, options):
        """
        数値の範囲チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            if True == isinstance(value, list):
                result = True
                for val in value:
                    result = self.is_range(val, options)
                    if False == result:
                        break
                return result
            else:
                r = None
                value = self.get_entity_field_value(value, options)
                try:
                    r = float(value)
                except ValueError:
                    return False
                else:
                    return options['min'] <= r and r <= options['max']
        else:
            return True
    def is_date(self, value, options):
        """
        日付チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return util.check_date(value, options['format'])
        else:
            return True
    def is_zip_code_format(self, value, options):
        """
        郵便番号書式チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return util.check_zip_code(value, options['is_include_hyphen'])
        else:
            return True
    def is_telephone_format(self, value, options):
        """
        電話番号書式チェック
        """
        is_check = self.is_check(value)
        if True == is_check:
            return util.check_telephone(value, options['is_include_hyphen'])
        else:
            return True
    def is_file_upload(self, value, options):
        """
        ファイルアップロードをチェックする
        """
        magic_obj = magic.Magic(mime=True, magic_file=app.config['MAGIC_FILE_PATH'])
        # TODO: forになってはいるが、複数ファイルがアップロードされる前提の処理にはなっていない
        for key, upload_file in enumerate(value):
            stream = upload_file.stream.read()
            # 任意項目で且つ、ファイルがアップロードされていない時はチェックしない
            if False == options['required'] \
            and '' == upload_file.filename \
            and 0 == len(stream):
                continue
            # TODO: options['message']への代入は参照になっている
            if '' == upload_file.filename \
            or 0 == len(stream):
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_NOT_UPLOAD_MESSAGE']
                return False
            if app.config['MAX_FILE_UPLOAD_SIZE'] < len(stream):
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_FILE_SIZE_OVER_MESSAGE']
                return False
            mime_type = magic_obj.from_buffer(stream)
            if 'image/bmp' == mime_type:
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_BITMAP_MESSAGE']
                return False
            if mime_type not in options['allow_mime_types']:
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_NOT_ALLOWED_FILE_TYPE_MESSAGE']
                return False
            file_info = os.path.splitext(upload_file.filename)
            extension = file_info[1][1:]
            if '' == extension:
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_UNKNOWN_EXTENSION_MESSAGE']
                return False
            if mime_type not in options['allow_extensions'] \
            or extension.lower() not in options['allow_extensions'][mime_type]:
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_UNMATCH_EXTENSION_FILE_TYPE_MESSAGE']
                return False
            if True == util.is_empty(upload_file.content_type) or True == util.is_empty(upload_file.mimetype):
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_UNKNOWN_FILE_TYPE_MESSAGE']
                return False
            if mime_type != upload_file.content_type or mime_type != upload_file.mimetype:
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_FILE_TYPE_INCONSISTENCY_MESSAGE']
                return False
            if True == options['is_file_name_check']:
                if options['max_length'] < len(upload_file.filename):
                    options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_MAX_CHARACTER_LENGTH_OVER_MESSAGE']
                    return False
                if '__' in upload_file.filename:
                    options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_UNDER_BAR_CONSECUTIVE_MESSAGE']
                    return False
                if ' ' == file_info[0][0] \
                or ' ' == file_info[0][-1] \
                or '　' == file_info[0][0] \
                or '　' == file_info[0][-1]:
                    options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_FIRST_OR_LAST_SPACE_MESSAGE']
                    return False
                reserved_words = {
                    'CON': True,
                    'PRN': True,
                    'AUX': True,
                    'NUL': True,
                    'CLOCK$': True,
                    'COM0': True,
                    'COM1': True,
                    'COM2': True,
                    'COM3': True,
                    'COM4': True,
                    'COM5': True,
                    'COM6': True,
                    'COM7': True,
                    'COM8': True,
                    'COM9': True,
                    'LPT0': True,
                    'LPT1': True,
                    'LPT2': True,
                    'LPT3': True,
                    'LPT4': True,
                    'LPT5': True,
                    'LPT6': True,
                    'LPT7': True,
                    'LPT8': True,
                    'LPT9': True,
                };
                if upload_file.filename in reserved_words or file_info[0] in reserved_words:
                    options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_RESERVED_WORD_MESSAGE']
                    return False
                # 許容する文字
                white_list = '\A(?:['
                # ひらがな
                white_list += app.config['PATTERN_HIRAGANA']
                # カタカナ
                white_list += app.config['PATTERN_KATAKANA']
                white_list += ']['
                # 濁点・半濁点
                white_list += app.config['PATTERN_DAKUTEN']
                white_list += ']?|'
                # 長音
                white_list += app.config['PATTERN_CHOON']
                white_list += '|'
                # 漢字
                white_list += app.config['PATTERN_KANJI']
                white_list += '?|['
                # 全角英数字・半角英数字
                white_list += app.config['PATTERN_ALL_WIDTH_ALPHABET_NUMBER']
                white_list += ']|['
                # 全角記号と全角スペース
                white_list += app.config['PATTERN_FULL_WIDTH_SIGN']
                white_list += ']|['
                # アンダーバー・半角スペース
                white_list += '_ '
                white_list += '])+\Z'
                if re.match(white_list, file_info[0]) is None:
                    options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_NOT_ALLOWED_CHARACTER_MESSAGE']
                    return False
            log_error_message = ''
            current_datetime = util.utc_to_other_timezone(util.get_current_datetime())
            file_path = app.config['APP_FILE_TMP_SAVE_PATH'] + '/' + options['save_path_identifier'] + '/' + current_datetime.strftime('%Y%m%d')
            r = util.make_directory(file_path)
            if False == r:
                log_error_message = app.config['UPLOAD_FILE_SAVE_DIRECTORY_MAKE_ERROR']
            if '' == log_error_message:
                os.chmod(file_path, 0o700)
                if True == options['is_secret']:
                    token = util.get_token(app.config['SECRET_TOKEN_BYTE_LENGTH'])
                else:
                    token = ''
                file_name = hashlib.sha512(str(token + werkzeug.utils.secure_filename(file_info[0]) + util.get_unique_id()).encode(app.config['PG_CHARACTER_SET'])).hexdigest() + '.' + extension
                full_file_path = file_path + '/' + file_name
                try:
                    with open(file = full_file_path, mode = 'xb') as fp:
                        write_byte = fp.write(stream)
                        if 0 < write_byte:
                            os.chmod(full_file_path, 0o600)
                        else:
                            log_error_message = app.config['FILE_UPLOAD_SAVE_ERROR_MESSAGE']
                except OSError:
                    log_error_message = app.config['FILE_UPLOAD_SAVE_PATH_OPEN_ERROR_MESSAGE']
            if '' == log_error_message:
                setattr(self, options['name'], upload_file.filename)
                setattr(self, options['path'], full_file_path)
            else:
                options['message'] = self.__validation_settings[options['name']]['show_name'] + app.config['FILE_UPLOAD_SHOW_SAVE_ERROR_MESSAGE']
                app.logger.error(log_error_message)
                return False
        return True
    def is_required_file(self, value, options):
        """
        必須項目チェック（ファイル）
        """
        for f in value:
            if '' == f.filename:
                return False
        return True
    def is_check(self, value):
        """
        チェックをするかどうかを調べる
        """
        result = True
        # 任意項目で且つ、値が空の時はチェックしない
        if True == self.__is_any_item and True == util.is_empty(value):
            result = False
        return result
    def get_entity_field_value(self, value, options):
        """
        エンティティの指定されたフィールドの値を取得する
        """
        result = value
        if 'field' in options:
            result = getattr(value, options['field'], None)
        return result
    def set_request_to_entity(self, request_data):
        """
        リクエストされたフォームデータを、対応するエンティティに設定する
        """
        properties = self.get_all_properties()
        request_data = request_data.to_dict()
        for field, value in properties.items():
            is_exist = False
            for k, v in request_data.items():
                if field == k:
                    is_exist = True
                    if True == isinstance(v, str) and True == v.isdecimal():
                        v = int(v)
                    setattr(self, field, v)
                    break
            if False == is_exist and [] != value:
                setattr(self, field, None)
    def trim_all_data(self):
        """
        エンティティに設定されている文字列データの空白を削除する
        """
        properties = self.get_all_properties()
        for field, value in properties.items():
            if True == isinstance(value, str):
                # 改行コードはtrimしない
                setattr(self, field, util.mb_trim(value, '\u0020\u0009\u0000\u000b\u3000'))
    def get_all_properties(self):
        """
        エンティティに存在する全てのプロパティデータを取得する
        """
        attributes = inspect.getmembers(self, lambda a:not(inspect.isroutine(a)))
        property_dict = {}
        for attribute in attributes:
            # 不要なプロパティはスルー
            if 'metadata' == attribute[0] or 'query' == attribute[0] or 'query_class' == attribute[0]:
                continue
            if True == attribute[0].startswith('_'):
                continue
            property_dict[attribute[0]] = attribute[1]
        return property_dict
    def add_validation_settings(self, name, show_name, validation_rules):
        """
        バリデーション設定を追加する
        """
        self.__validation_settings[name] = {'show_name': show_name, 'rules': validation_rules}
