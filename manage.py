from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Server

migrate = Migrate(app, db)
manager = Manager(app)

from manage_commands import PopulateAntennas, Populate, PopulateCities, PopulateRegions, DeleteDb, ExampleReport, \
    ExampleRanking, MonthlyImport

manager.add_command('db', MigrateCommand)
manager.add_command('populate', Populate())
manager.add_command('populate_antennas', PopulateAntennas())
manager.add_command('populate_cities', PopulateCities())
manager.add_command('populate_regions', PopulateRegions())
manager.add_command('delete', DeleteDb())
manager.add_command('example_report', ExampleReport())
manager.add_command('example_ranking', ExampleRanking())
manager.add_command('monthly_import', MonthlyImport())

if __name__ == '__main__':
    manager.run()
