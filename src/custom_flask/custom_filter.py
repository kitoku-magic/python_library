from python_library.src import markupsafe

# テンプレートファイルから呼び出すfilter関数群
def nl2br(value):
    """
    改行コードを、HTMLの改行に変換する
    """
    value = value.__str__().replace('\n', '<br />')
    return markupsafe.Markup(value)
