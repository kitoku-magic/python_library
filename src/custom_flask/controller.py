from python_library.src import abc
from python_library.src import flask
from python_library.src import secrets
from python_library.src import traceback
from python_library.src.original.custom_exception import custom_exception
from python_library.src.original.util import util
from src.application import app

class controller:
    """
    基底コントローラークラス
    """
    __abstract__ = True
    def __init__(self):
        self.__request = flask.request
        self.__response_data = {}
        self.__template_file_name = ''
        self.__ajax_flag = False
        self.__status_code = 200
    @abc.abstractmethod
    def execute(self):
        pass
    def get_request(self):
        return self.__request
    def add_response_data(self, name, value):
        self.__response_data[name] = value
    def set_template_file_name(self, template_file_name):
        self.__template_file_name = template_file_name
    def run(self):
        """
        処理実行
        """
        r = None
        try:
            if 'X-Requested-With' in self.get_request().headers:
                if 'fm_xml_http_request' == self.get_request().headers['X-Requested-With']:
                    self.__ajax_flag = True
            # サブクラスでオーバーライドしている
            self.execute()
        except custom_exception as e:
            app.logger.exception('{}'.format(e))
            if 2 <= len(e.args):
                show_error_message = e.args[1]
            else:
                show_error_message = app.config['SHOW_UNEXPECTED_ERROR']
            r = self.make_error_response(show_error_message)
            if True == self.__ajax_flag:
                self.__status_code = 500
        except Exception as e:
            app.logger.exception('{}'.format(e))
            show_error_message = app.config['SHOW_UNEXPECTED_ERROR']
            r = self.make_error_response(show_error_message)
            if True == self.__ajax_flag:
                self.__status_code = 500
        except:
            app.logger.exception(traceback.format_exc())
            show_error_message = app.config['SHOW_UNEXPECTED_ERROR']
            r = self.make_error_response(show_error_message)
            if True == self.__ajax_flag:
                self.__status_code = 500
        finally:
            # レスポンスヘッダーに必ず追加したい内容を設定する
            require_response_headers = {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0',
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                # ここは特に、サイトの作りによってマチマチなので、 https://inside.pixiv.blog/kobo/5137 等、その他の参考ページも参照
                'Content-Security-Policy': "default-src 'none'; style-src 'self'; script-src 'self' 'unsafe-inline'; object-src 'none'; base-uri 'none'; connect-src 'self';",
            }
            if 'https' == app.config['URI_SCHEME']:
                require_response_headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            if r is None:
                if True == self.__ajax_flag:
                    require_response_headers['Content-Type'] = 'application/json; charset=' + app.config['PG_CHARACTER_SET']
                    r = flask.make_response()
                    r.status_code = self.__status_code
                    r.data = flask.json.dumps(self.__response_data)
                else:
                    # テンプレートにデータを渡して、レスポンスを返す
                    template = app.jinja_environment.get_template(self.__template_file_name + '.html')
                    http_response = template.render({'res': self.__response_data})

                    r = flask.make_response(http_response)
                    require_response_headers['Content-Type'] = 'text/html; charset=' + app.config['PG_CHARACTER_SET']
            return self.set_response_headers(r, require_response_headers)
    def make_error_response(self, show_error_message):
        """
        エラー用のレスポンス
        """
        self.add_response_data('title', 'エラー')
        self.add_response_data('show_error_message', show_error_message)
        template = app.jinja_environment.get_template('error.html')
        http_response = template.render({'res': self.__response_data})
        return flask.make_response(http_response)
    def set_response_headers(self, response, params):
        for key, val in params.items():
            response.headers[key] = val
        return response
    def create_csrf_token(self):
        csrf_token = util.get_token(app.config['SECRET_TOKEN_BYTE_LENGTH'])
        flask.session['csrf_token'] = csrf_token
        self.add_response_data('csrf_token', csrf_token)
    def check_csrf_token(self):
        post_csrf_token = self.get_request().form.get('csrf_token', default=None, type=str)
        session_csrf_token = flask.session.get('csrf_token')
        # 取得したトークンはすぐに削除
        flask.session.pop('csrf_token', None)
        if post_csrf_token is not None and session_csrf_token is not None:
            # タイミング攻撃を考慮した比較方法
            if True == secrets.compare_digest(post_csrf_token, session_csrf_token):
                return True
            else:
                raise custom_exception(app.config['TOKEN_NOT_EQUAL_ERROR'])
        else:
            raise custom_exception(app.config['TOKEN_NOT_SETTING_ERROR'])
    def set_template_common_data(self, title, template_file_name):
        """
        全てのテンプレートの表示で行う処理
        """
        self.add_response_data('title', title)
        self.set_template_file_name(template_file_name)
