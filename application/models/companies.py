from application.models import db
from application.models import ma

class Companies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    code = db.Column(db.String(4), unique=True)

    def __init__(self, name, code):
        self.name = name
        self.code = code

    def __repr__(self):
        return '<User %r>' % self.name

class CompaniesSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('name', 'code')

companies_schema = CompaniesSchema(many=True)