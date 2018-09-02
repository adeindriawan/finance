from flask import Blueprint
from application.controllers.home import home
from application.controllers.companies import companies
from application.controllers.beta import calculate

main = Blueprint('main', __name__)

@main.route('/')
def home_page():
	response = home()
	return response

@main.route('/companies')
def companies_page():
	response = companies()
	return response

@main.route('/beta/<code>/<start>/<end>')
def beta_page(code, start, end):
	response = calculate(code, start, end)
	return response