# python_library
Pythonにおいて、様々なアプリケーションで共通して使う処理をまとめたライブラリです。

現状では、Flaskにかなり依存してしまっていますが、

将来的には、各プログラムの独立性を高めていく方向性で考えています。

また、各ファイルの説明として、

拡張子が「.default」となっているファイルは、

以下の通り、各アプリケーションへファイルを移動（移動後、拡張子defaultを外す）して、

場合によってはファイル内の記述を各アプリケーション毎に修正する必要があります。

- src/custom_flask/.app_env.default → 「アプリケーションの基底ディレクトリ」配下に移動して中身修正
- src/custom_flask/application.py.default → 「アプリケーションの基底ディレクトリ/src」配下に移動して中身修正
- src/custom_flask/config.py.default → 「アプリケーションの基底ディレクトリ/src/config」配下に移動して中身修正
- src/custom_flask/index.py.default → 「アプリケーションの基底ディレクトリ」配下に移動
- src/custom_flask/instance.py.default → 「アプリケーションの基底ディレクトリ/src/instance」配下に移動して中身修正
- src/custom_jinja/error.html.default → 「アプリケーションの基底ディレクトリ/template」配下に移動
- src/custom_jinja/layout.html.default → 「アプリケーションの基底ディレクトリ/template」配下に移動
- src/custom_jinja/on_load.html.default → 「アプリケーションの基底ディレクトリ/template」配下に移動
- src/custom_uwsgi/uwsgi.ini.default → 「アプリケーションの基底ディレクトリ」配下に移動して中身修正

上記のファイルの移動などに対応した、

本ライブラリを実際に導入しているアプリケーションが、以下になりますので、

ご参考下さい。

https://github.com/kitoku-magic/user_registration_form/tree/master/python

# 免責事項
実際の業務でも使う事を意識して作っていますが、

当然、業務によって仕様なども違うことや、

また、不具合もあるかもしれませんので、

テストを入念に行うなど、ご注意下さい。
