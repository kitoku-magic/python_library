from python_library.src import dns_resolver
from python_library.src import dt
from python_library.src import os
from python_library.src import re
from python_library.src import requests
from python_library.src import secrets
from python_library.src import time
from python_library.src import unicodedata
from python_library.src import uuid
from src.application import app

class util:
    """
    汎用処理を集めたクラス
    """
    @classmethod
    def check_mail_format(cls, value):
        """
        メールフォーマットをチェック
        """
        return '@' in value
    @classmethod
    def check_mail_domain(cls, value):
        """
        メールドメインの存在チェック
        """
        ret = True
        tmp = value.split('@')
        mail_domain = tmp[-1]
        try:
            dns_resolver_answer  = dns_resolver.resolve(mail_domain, 'MX')
        except Exception as exc:
            ret = False
        return ret
    @classmethod
    def replace_hyphen(cls, value, replace):
        """
        ハイフン文字を置換する
        """
        return re.sub('\u002D|\uFE63|\uFF0D|\u2010|\u2011|\u2043|\u02D7|\u2212|\u2012|\u2013|\u2014|\u2015|\uFE58|\u23AF|\u23E4|\u268A|\u2500|\u1173|\u2F00|\u30FC|\u3161|\u31D0|\u4E00|\uFF70|\uFFDA', replace, value)
    @classmethod
    def mb_trim(cls, value, character_mask):
        """
        空白文字などを削除する
        """
        return value.strip(character_mask)
    @classmethod
    def join_diacritic(cls, value, mode='NFC'):
        """
        基底文字と濁点・半濁点を結合する
        @see https://qiita.com/syamamura/items/13c0825282415e2e360d
        """
        bytes_value = value.encode()

        # 濁点Unicode結合文字置換
        bytes_value = re.sub(b"\xe3\x82\x9b", b'\xe3\x82\x99', bytes_value)
        bytes_value = re.sub(b"\xef\xbe\x9e", b'\xe3\x82\x99', bytes_value)

        # 半濁点Unicode結合文字置換
        bytes_value = re.sub(b"\xe3\x82\x9c", b'\xe3\x82\x9a', bytes_value)
        bytes_value = re.sub(b"\xef\xbe\x9f", b'\xe3\x82\x9a', bytes_value)

        value = bytes_value.decode()

        return unicodedata.normalize(mode, value)
    @classmethod
    def is_empty(cls, value):
        """
        空かどうかのチェック
        """
        return value is None or '' == value
    @classmethod
    def check_min_length(cls, value, length):
        """
        最小桁数のチェック
        """
        return len(value.encode(app.config['PG_CHARACTER_SET'])) >= length
    @classmethod
    def check_max_length(cls, value, length):
        """
        最大桁数のチェック
        """
        return len(value.encode(app.config['PG_CHARACTER_SET'])) <= length
    @classmethod
    def check_date(cls, date, date_format = '%Y-%m-%d %H:%M:%S'):
        """
        日付が妥当かどうかのチェック
        """
        try:
            dt.datetime.strptime(date, date_format)
            return True
        except ValueError:
            return False
    @classmethod
    def check_zip_code(cls, value, is_include_hyphen = False):
        """
        郵便番号が妥当かどうかのチェック
        """
        pattern = '\A[0-9]{3}'
        if True == is_include_hyphen:
            pattern += '-'
        pattern += '[0-9]{4}\Z'
        return re.match(pattern, value) is not None
    @classmethod
    def check_telephone(cls, value, is_include_hyphen = False):
        """
        電話番号が妥当かどうかのチェック
        """
        pattern = '\A0[1-9][0-9]{0,3}'
        if True == is_include_hyphen:
            pattern += '-'
        pattern += '[0-9]{1,4}'
        if True == is_include_hyphen:
            pattern += '-'
        pattern += '[0-9]{4}\Z'
        return re.match(pattern, value) is not None
    @classmethod
    def make_directory(cls, path):
        """
        ディレクトリを作成する（makedirsのラッパー）
        """
        try:
            if False == os.path.isdir(path):
                os.makedirs(path)
        except FileExistsError as fee:
            # 同時に同名のディレクトリを作るアクセスがあった時のチェック用
            if False == os.path.isdir(path):
                # ディレクトリ作成に失敗
                return False
        return True
    @classmethod
    def get_token(cls, byte_length):
        """
        第三者が知り得ない秘密情報(トークン)の値を取得する
        """
        return secrets.token_hex(byte_length)
    @classmethod
    def get_token_for_url(cls, byte_length):
        """
        第三者が知り得ない秘密情報(トークン)の値を取得する（URL文字列用）
        """
        return secrets.token_urlsafe(byte_length)
    @classmethod
    def get_unique_id(cls):
        """
        ユニークなIDを取得する（推測可能なので注意）
        """
        return str(uuid.uuid4())
    @classmethod
    def call_http_request(cls, url, timeout, modify_encoding_flag = True, headers = {}, wait_seconds = 0):
        """
        HTTPリクエストを実行する
        """
        time.sleep(wait_seconds)
        http_response = requests.get(url, timeout=timeout, headers=headers)
        if modify_encoding_flag == True:
            http_response.encoding = http_response.apparent_encoding
        return http_response
    @classmethod
    def get_current_datetime(cls, timezone = dt.timezone.utc):
        """
        現在日時のdatetimeオブジェクトを取得する
        """
        return dt.datetime.now(timezone)
    @classmethod
    def utc_to_other_timezone(cls, datetime, utc_diff_hours = app.config['UTC_DIFF_HOUR']):
        """
        UTCから任意の他のタイムゾーンに変換する
        """
        return datetime.astimezone(dt.timezone(dt.timedelta(hours = utc_diff_hours)))
