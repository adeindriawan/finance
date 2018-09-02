from flask import Flask
from application.routes.web import main
from application.config.db import connect
from application.models import db
from application.models import ma

def launch_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = connect
	# https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
	
	#initialize SQLAlchemy
	db.init_app(app)

	#initialize Marshmallow
	ma.init_app(app)

	# register the blueprints
	app.register_blueprint(main)

	return app	