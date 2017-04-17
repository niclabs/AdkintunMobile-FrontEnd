from datetime import datetime
from app.importation import reportLogger
from app.importation.general_importation import import_all


def monthly_import():
    actual_month = datetime.now().month
    actual_year = datetime.now().year
    month_new_import = actual_month - 1
    year_new_import = actual_year

    if month_new_import == 0:
        month_new_import = 12
        year_new_import = year_new_import - 1

    year = year_new_import
    month = month_new_import
    reportLogger.info("Initiating monthly report import for {}/{}".format(month, year))
    import_all(year, month)
