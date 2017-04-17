from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

migrate = Migrate(app, db)
manager = Manager(app)

from manage_commands import Populate, DeleteDb,\
    MonthlyImport, ExampleAntennas, CityAntennas,\
    GeneralImport, RefreshQueries

manager.add_command('db', MigrateCommand)
manager.add_command('populate', Populate())
manager.add_command('delete', DeleteDb())
manager.add_command('monthly_import', MonthlyImport())
manager.add_command('city_antennas', CityAntennas())
manager.add_command('example_antennas', ExampleAntennas())
manager.add_command('general_import_example', GeneralImport())
manager.add_command('refresh', RefreshQueries)

if __name__ == '__main__':
    manager.run()
