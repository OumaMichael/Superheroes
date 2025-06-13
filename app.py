from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define models directly in app.py to avoid circular imports
class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'
    
    serialize_rules = ('-hero_powers.hero',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)
    
    # Relationship
    hero_powers = db.relationship('HeroPower', back_populates='hero', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Hero {self.name}>'

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'
    
    serialize_rules = ('-hero_powers.power',)
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Relationship
    hero_powers = db.relationship('HeroPower', back_populates='power', cascade='all, delete-orphan')
    
    @validates('description')
    def validate_description(self, key, description):
        if not description or len(description) < 20:
            raise ValueError("Description must be present and at least 20 characters long")
        return description
    
    def __repr__(self):
        return f'<Power {self.name}>'

class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    
    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')
    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)
    
    # Relationships
    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')
    
    @validates('strength')
    def validate_strength(self, key, strength):
        valid_strengths = ['Strong', 'Weak', 'Average']
        if strength not in valid_strengths:
            raise ValueError(f"Strength must be one of: {', '.join(valid_strengths)}")
        return strength
    
    def __repr__(self):
        return f'<HeroPower {self.hero_id}-{self.power_id}>'

# Import routes after models are defined
from routes import setup_routes

# Setup routes
setup_routes(app, db)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5555)
