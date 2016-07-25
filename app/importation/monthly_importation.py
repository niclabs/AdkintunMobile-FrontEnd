from datetime import datetime
from app.importation.general_importation import report_import, ranking_import


def monthly_import():
    actual_month = datetime.now().month
    actual_year = datetime.now().year
    month_new_import = actual_month - 1
    year_new_import = actual_year
    if month_new_import == 0:
        month_new_import = 12
        year_new_import = year_new_import - 1

    year = str(year_new_import)
    month = str(month_new_import)
    report_import(year,month)
    ranking_import(year,month)
