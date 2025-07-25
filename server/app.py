# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    
    earthquake = Earthquake.query.filter(Earthquake.id == id).first()
    
    
    if not earthquake:
        return {'message': f'Earthquake {id} not found.'}, 404
    
    
    return {
        'id': earthquake.id,
        'location': earthquake.location,
        'magnitude': earthquake.magnitude,
        'year': earthquake.year
    }

@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_min_magnitude(magnitude):
    
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    
    quakes_data = [{
        'id': quake.id,
        'location': quake.location,
        'magnitude': quake.magnitude,
        'year': quake.year
    } for quake in earthquakes]
    
    return {
        'count': len(quakes_data),
        'quakes': quakes_data
    }

if __name__ == '__main__':
    app.run(port=5555, debug=True)
