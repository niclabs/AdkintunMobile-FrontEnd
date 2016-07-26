import flask_login as login
from app import db
from app.admin import admin
from app.models.antenna import Antenna
from app.models.carrier import Carrier
from app.models.region import Region
from app.models.city import City
from app.models.report import Report
from app.models.ranking import Ranking
from flask_admin.contrib.sqla import ModelView


class StandardView(ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated

    column_display_pk = True
    can_delete = True
    can_create = False
    can_edit = True
    can_export = True


# Add views
# admin.add_view(UserView(User, db.session))

admin.add_view(StandardView(Antenna, db.session))
admin.add_view(StandardView(Carrier, db.session))
admin.add_view(StandardView(Region, db.session))
admin.add_view(StandardView(City, db.session))
admin.add_view(StandardView(Report, db.session))
admin.add_view(StandardView(Ranking, db.session))
