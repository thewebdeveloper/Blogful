import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from getpass import getpass
from werkzeug.security import generate_password_hash

from blog.database import Base
from blog import app
manager = Manager(app)


from blog.database import session, Entry, User # blog in the same directory


@manager.command
def run():
	port = int(os.environ.get('PORT', 8080))
	app.run(host='0.0.0.0', port=port)
	
	
@manager.command
def seed():
	content = """ Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. """
	
	for i in range(20):
		entry = Entry(
			title = "Test entry #{}".format(i),
			content = content
		)
		session.add(entry)
	session.commit()
	
	
@manager.command
def addUser():
	name = input("Name: ")
	email = input("Email: ")
	if session.query(User).filter_by(email=email).first():
		print("User with that email already exists")
		return
	
	password = ""
	password_2 = ""
	while len(password) < 8 or password != password_2:
		password = getpass("Password: ")
		password_2 = getpass("Re-enter Password: ")
	user = User(name=name, email=email, 
				password=generate_password_hash(password))
	session.add(user)
	session.commit()
	
	
class DB(object):
	def __init__(self, metadata):
		self.metadata = metadata


migrate = Migrate(app, DB(Base.metadata))
manager.add_command('db', MigrateCommand)



if __name__ == "__main__":
	manager.run()