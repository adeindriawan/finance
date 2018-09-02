from flask import jsonify
from application.models.companies import Companies
from application.models.companies import companies_schema

def companies():
	query = Companies.query.all()
	result = companies_schema.dump(query)
	return jsonify(result.data)