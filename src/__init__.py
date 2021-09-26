# 標準ライブラリ
import abc
import datetime as dt
import hashlib
import inspect
import os
import re
import secrets
import sys
import time
import traceback
import unicodedata
import uuid

# サードパーティライブラリ（アプリケーションによっては使わないライブラリもあるはずなので、アプリのPipfileと合わせて適時修正する）
import dns.resolver as dns_resolver
import flask
import flask_mail
import jinja2
import magic
import markupsafe
import requests
import sqlalchemy as sa
import sqlalchemy.dialects.mysql as sadm
import sqlalchemy.dialects.mysql.base as sadmb
import sqlalchemy.ext.automap as saea
import sqlalchemy.ext.declarative as saed
import sqlalchemy.inspection as sai
import sqlalchemy.orm as sao
import sqlalchemy.orm.relationships as saor
import sqlalchemy.sql.functions as sasf
import sqlalchemy.sql.schema as sassc
import sqlalchemy.sql.sqltypes as sasst
import sqlalchemy.types as sat
import werkzeug
