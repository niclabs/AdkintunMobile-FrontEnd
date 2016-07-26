server_settings = {
    "server_url": "",
    "antenna_url" : "",
    "report_url" : "",
    "ranking_url" : ""
}


class DefaultConfig(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "this-really-needs-to-be-changed"
    USER = "this-really-needs-to-be-changed"
    SQLALCHEMY_DATABASE_URI = "postgresql://" + USER + ":" + SECRET_KEY + "<database location>"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class AdminUser:
    first_name = "this-really-needs-to-be-changed"
    last_name = "this-really-needs-to-be-changed"
    login = "this-really-needs-to-be-changed"
    email = "this-really-needs-to-be-changed"
    password = "this-really-needs-to-be-changed"
