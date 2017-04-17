from config import Files
from logging.handlers import RotatingFileHandler
import os
import logging

reportLogger = logging.getLogger(__name__)

log_folder = Files.LOGS_FOLDER
log_filename = Files.IMPORT_LOG_FILE
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

file_handler = RotatingFileHandler(log_folder + "/" + log_filename, maxBytes=50 * 1024 * 1024)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"))
reportLogger.setLevel(logging.INFO)
file_handler.setLevel(logging.INFO)
reportLogger.addHandler(file_handler)
reportLogger.info("Report Importer log start")

from app.importation import general_importation
from app.importation import monthly_importation
