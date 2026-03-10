from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask import Flask # type: ignore

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    scientific_name = db.Column(db.String(100), nullable=False)
    common_names = db.Column(db.String(200))
    habitat = db.Column(db.String(500))
    medicinal_uses = db.Column(db.String(500))
    cultivation = db.Column(db.String(500))
    image = db.Column(db.String(500))
    wikipedia = db.Column(db.String(500))
    model = db.Column(db.String(500))

# Run this script once to create the database
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Database created successfully!")
