class ServerSettings:
    urls = {
    "server_url": "http://dev.niclabs.cl",
    "antenna_url" : "antenna",
    "report_url" : "reports",
    "ranking_url" : "reports",
    "network_url" : "reports",
    "signal_url" : "reports"
    }


class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "1234"
    USER = "cris"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "@localhost/visualization"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class AppTokens:
    tokens = {
        "server" : "sKjCLst1xNJhPVKgqCLWBCbZ1CSRGYscGWXnWoZMVbNoCVlmiQ"
    }


class AdminUser:
    first_name = "Cristian"
    last_name = "Parra"
    login = "cris"
    email = "cris@example.cl"
    password = "1234"
