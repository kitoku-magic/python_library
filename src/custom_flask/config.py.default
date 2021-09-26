from src import logging

class config(object):
    # 共通
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_NAME = 'user_registration_session'
    SESSION_COOKIE_DOMAIN = None
    SESSION_COOKIE_PATH = '/'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_REFRESH_EACH_REQUEST = True
    PERMANENT_SESSION_LIFETIME = 1200
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0
    LOG_MAX_BYTES = 100000
    LOG_BACKUP_COUNT = 10
    LOG_LEVEL = logging.DEBUG
    PG_CHARACTER_SET = 'utf-8'
    MAX_CONTENT_LENGTH = 20 * 1024 * 1024
    MAX_FILE_UPLOAD_SIZE = 10 * 1024 * 1024
    JOB_ID_OTHER = 1
    USER_REGISTRATION_STATUS_REGISTERING = 1
    USER_REGISTRATION_STATUS_REGISTERED = 2
    UTC_DIFF_HOUR = 9
    FILE_UPLOAD_IDENTIFIER_USER_REGISTRATION = 'user_registration'
    APP_FILE_TMP_SAVE_PATH = '/tmp/app'
    APP_FILE_SAVE_PATH = '/upload/app'
    # デフォルトのマジックファイルは/usr/share/misc/magic.mgcだが、ファイルアップロードに失敗する場合は、別途fileコマンドのインストールが必要
    MAGIC_FILE_PATH = '/usr/share/misc/magic.mgc'
    SECRET_TOKEN_BYTE_LENGTH = 96
    SECRET_TOKEN_FOR_URL_BYTE_LENGTH = 96

    # 正規表現パターン
    # 正規表現パターンのUnicodeコードポイント（ひらがな）
    PATTERN_HIRAGANA = '\u3041-\u3096'
    # 正規表現パターンのUnicodeコードポイント（カタカナ）
    PATTERN_KATAKANA = '\u30A1-\u30FA\u31F0-\u31FF\uFF66-\uFF6F\uFF71-\uFF9D'
    # 正規表現パターンのUnicodeコードポイント（濁点・半濁点）
    PATTERN_DAKUTEN = '\u3099\u309A\uFF9E\uFF9F'
    # 正規表現パターンのUnicodeコードポイント（長音）
    PATTERN_CHOON = '\u30FC'
    # 正規表現パターンのUnicodeコードポイント（漢字）(一部の文字は\p{Han}でも良いけど、明示的な方が良いかと)
    PATTERN_KANJI = '[\u2E80-\u2FDF\u3005\u3007\u3021-\u3029\u3038-\u303B\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\u20000-\u2FFFF][\uE0100-\uE01EF\uFE00-\uFE02]'
    # 正規表現パターンのUnicodeコードポイント（全角英数字・半角英数字）
    PATTERN_ALL_WIDTH_ALPHABET_NUMBER = '\u0030-\u0039\u0041-\u005A\u0061-\u007A\uFF10-\uFF19\uFF41-\uFF5A'
    # 正規表現パターンのUnicodeコードポイント（以下の全角記号と全角スペース）
    # ‐ ― ‖ ‘ ’ “ ” ′ ″ ※ 　 、 。 〈 〉 《 》 「 」 『 』 【 】 〒 〔 〕 〖 〗 〜 〝 ！ ＂ ＃ ＄ ％ ＆ ＇ （ ） ＊ ＋ ， － ． ／ ： ； ＜ ＝ ＞ ？ ＠ ［ ＼ ］ ＾ ＿ ｀ ｛ ｜ ｝ ～ ￥
    PATTERN_FULL_WIDTH_SIGN = '\u2010\u2015\u2016\u2018\u2019\u201C-\u201D\u2032\u2033\u203B\u3000-\u3002\u3008-\u3012\u3014-\u3017\u301C-\u301D\uFF01-\uFF0F\uFF1A-\uFF20\uFF3B-\uFF40\uFF5B-\uFF5E\uFFE5'
    # 正規表現パターンのUnicodeコードポイント（全角数字）
    PATTERN_FULL_WIDTH_NUMBER = '\uFF10-\uFF19'
    # 正規表現パターンのUnicodeコードポイント（全角スペース）
    PATTERN_FULL_WIDTH_SPACE = '\u3000'

    # 共通エラーメッセージ
    SHOW_UNEXPECTED_ERROR = '予期しないエラーが発生しました。\nブラウザの戻るボタンで前ページにお戻り下さい。'
    INVALID_REQUEST_ERROR = '不正なリクエストです'
    SHOW_SYSTEM_ERROR = 'システムエラーが発生しました。\n再度、ユーザー登録入力画面から操作をお願いします。'
    TOKEN_NOT_EQUAL_ERROR = 'トークンが一致しません', '不正なリクエストです。'
    TOKEN_NOT_SETTING_ERROR = 'トークンが設定されていません', '不正なリクエストです。'

    # バリデーションエラーメッセージ
    REQUIRED_MESSAGE = '{show_name}は必須項目です'
    NOT_EMPTY_MESSAGE = '{show_name}を入力してください'
    MIN_LENGTH_MESSAGE = '{show_name}は入力必要桁数に足りていません'
    MAX_LENGTH_MESSAGE = '{show_name}は入力可能桁数を超えています'
    MAIL_FORMAT_MESSAGE = '{show_name}の書式が不正です'
    MAIL_DOMAIN_MESSAGE = '{show_name}のドメインが存在しません'
    ALPHA_NUM_MESSAGE = '{show_name}は半角英数字で入力してください'
    JAPANESE_MESSAGE = '{show_name}は日本語で入力してください'
    JAPANESE_EXTEND_MESSAGE = '{show_name}は日本語で入力してください'
    HIRAGANA_MESSAGE = '{show_name}はひらがなで入力してください'
    NUMBER_MESSAGE = '{show_name}は数値を入力してください'
    INTEGER_MESSAGE = '{show_name}は整数を入力してください'
    RANGE_MESSAGE = '{show_name}は有効な値の範囲外です'
    DATE_MESSAGE = '{show_name}は不正な日付です'
    ZIP_CODE_FORMAT_MESSAGE = '{show_name}は不正な郵便番号です'
    TELEPHONE_FORMAT_MESSAGE = '{show_name}は不正な番号です'
    FILE_UPLOAD_NOT_UPLOAD_MESSAGE = 'がアップロードされていません'
    FILE_UPLOAD_FILE_SIZE_OVER_MESSAGE = 'はアップロード可能なファイルサイズを超えています'
    FILE_UPLOAD_BITMAP_MESSAGE = 'はビットマップ画像なのでアップロード出来ません'
    FILE_UPLOAD_NOT_ALLOWED_FILE_TYPE_MESSAGE = 'は許可されていないファイル形式です'
    FILE_UPLOAD_UNKNOWN_EXTENSION_MESSAGE = 'の拡張子が不明です'
    FILE_UPLOAD_UNMATCH_EXTENSION_FILE_TYPE_MESSAGE = 'の拡張子とファイル形式が合っていません'
    FILE_UPLOAD_UNKNOWN_FILE_TYPE_MESSAGE = 'のファイル形式が不明です'
    FILE_UPLOAD_FILE_TYPE_INCONSISTENCY_MESSAGE = 'のファイル形式が矛盾しています'
    FILE_UPLOAD_MAX_CHARACTER_LENGTH_OVER_MESSAGE = 'の長さが最大文字数を超えています'
    FILE_UPLOAD_UNDER_BAR_CONSECUTIVE_MESSAGE = 'にアンダーバーが連続して含まれています'
    FILE_UPLOAD_FIRST_OR_LAST_SPACE_MESSAGE = 'の先頭か末尾に空白が入っています'
    FILE_UPLOAD_RESERVED_WORD_MESSAGE = 'は予約語です'
    FILE_UPLOAD_NOT_ALLOWED_CHARACTER_MESSAGE = 'に許可されていない文字が含まれています'
    FILE_UPLOAD_SAVE_ERROR_MESSAGE = 'アップロードファイルの保存に失敗しました'
    FILE_UPLOAD_SAVE_PATH_OPEN_ERROR_MESSAGE = 'アップロードファイルの保存先パスのオープンに失敗しました'
    FILE_UPLOAD_SHOW_SAVE_ERROR_MESSAGE = 'のアップロードに失敗しました。もう一度アップロードして下さい'

    # ユーザー登録初期入力画面
    USER_REGISTRATION_FIRST_INPUT_TITLE = 'メールアドレス入力'

    # ユーザー登録初期入力完了画面
    USER_REGISTRATION_FIRST_COMPLETE_TITLE = 'メールアドレス入力完了'
    USER_REGISTRATION_FIRST_COMPLETE_REGISTERED_MESSAGE = '''メールアドレスの入力、ありがとうございます。
以下のURLより、登録を継続して下さい。
また、URLの有効期間は１時間となっておりますので、ご注意下さい。

'''
    USER_REGISTRATION_FIRST_COMPLETE_ALREADY_REGISTERED_MESSAGE = '''メール入力画面でメールを入力されましたか？
誰かが、貴方のメールアドレスを入力したかもしれません。
ご注意下さい。'''
    USER_REGISTRATION_FIRST_COMPLETE_MAIL_TITLE = 'メール送信のお知らせ'
    MAIL_SEND_ERROR = 'メールの送信に失敗しました。'
    DB_REGISTRATION_ERROR = 'データベースへの登録に失敗しました。'
    SHOW_FIRST_COMPLETE_ERROR = '登録に失敗しました。\n再度、お手続き下さい。'

    # ユーザー登録入力画面
    USER_REGISTRATION_INPUT_TITLE = 'ユーザー登録'
    USER_REGISTRATION_TIME_LIMIT_SECOND = 3600
    USER_REGISTRATION_URL_EXPIRE_DATE_ERROR = 'URLの有効期限が切れています。'
    SHOW_USER_REGISTRATION_URL_EXPIRE_DATE_ERROR = 'URLの有効期限が切れています。\n再度、メールアドレス入力画面からお手続き下さい。'
    FILE_UPDATE_ERROR = 'ファイル情報の更新に失敗しました'
    SHOW_FILE_UPDATE_SYSTEM_ERROR = 'システムエラーが発生しました。\n再度、ユーザー登録入力画面から操作をお願いします。'

    # ユーザー登録確認画面
    USER_REGISTRATION_CONFIRM_TITLE = 'ユーザー登録確認'
    ZIP_CODE_ERROR = '郵便番号に該当する住所が存在しません'
    ZIP_CODE_CONSISTENCY_ERROR = '郵便番号に対する都道府県が一致していません'
    BIRTH_DAY_NOT_REGISTRATION_ERROR = '登録出来ない誕生日です。'
    MAIL_ADDRESS_REGISTRATIONED_ERROR = '既に該当のメールアドレスでは登録済みです。'
    SHOW_MAIL_ADDRESS_REGISTRATIONED_ERROR = '既に該当のメールアドレスでは登録済みです。\nその他のメールアドレスで、ご登録をお願いします。'
    USER_TEMPORARY_SAVE_ERROR = 'ユーザー情報の一時保存に失敗しました'

    # ユーザー登録完了画面
    USER_REGISTRATION_COMPLETE_TITLE = 'ユーザー登録完了'
    PRE_USER_NOT_EXIST_ERROR = '該当のユーザー事前登録情報が存在しませんでした'
    PRE_USER_DELETE_ERROR = 'ユーザー事前登録情報の削除に失敗しました'
    USER_NOT_EXIST_ERROR = '該当のユーザー情報が存在しませんでした'
    USER_SAVE_ERROR = 'ユーザー情報の保存に失敗しました'
    UPLOAD_FILE_SAVE_DIRECTORY_MAKE_ERROR = 'アップロードファイルの保存先ディレクトリの作成に失敗しました'
    SHOW_USER_REGISTRATION_ERROR = 'ユーザー情報の登録に失敗しました。\n再度、ユーザー登録入力画面から操作をお願いします。'
class testing(config):
    ENV = 'testing'
    TESTING = True

class development(config):
    ENV = 'development'
    DEBUG = True

class production(config):
    ENV = 'production'
    SESSION_COOKIE_SECURE = True
    LOG_MAX_BYTES = 1000000
    LOG_BACKUP_COUNT = 100
    LOG_LEVEL = logging.INFO
