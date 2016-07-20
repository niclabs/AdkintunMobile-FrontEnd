from flask_migrate import Migrate, MigrateCommand

from flask import g
from flask_script import Manager, Server

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

from manage_commands import PopulateAntennas, Populate, PopulateCities,PopulateRegions, DeleteDb, ExampleReport, ExampleRanking
manager.add_command('runserver', Server(host="0.0.0.0", port=9000))
manager.add_command('db', MigrateCommand)
manager.add_command('populate', Populate())
manager.add_command('populate_antennas', PopulateAntennas())
manager.add_command('populate_cities', PopulateCities())
manager.add_command('populate_regions', PopulateRegions())
manager.add_command('delete', DeleteDb())
manager.add_command('example_report', ExampleReport())
manager.add_command('example_ranking', ExampleRanking())

if __name__ == '__main__':
    manager.run()
