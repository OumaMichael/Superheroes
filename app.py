import os
from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)

# Database configuration with absolute path
db_path = os.path.abspath(os.path.join(os.getcwd(), "Superheroes", "superheroes.db"))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

# Helper function to handle JSON requests - FIXED VERSION
def get_json_data():
    try:
        # Try to get JSON data regardless of content type
        data = request.get_json(force=True)
        if data is None:
            # If that fails, try to parse manually
            raw_data = request.get_data(as_text=True)
            if raw_data:
                import json
                data = json.loads(raw_data)
            else:
                return None, "No data provided"
        return data, None
    except Exception as e:
        return None, f"JSON parsing error: {str(e)}"

# GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    try:
        heroes = Hero.query.all()
        heroes_data = []
        
        for hero in heroes:
            heroes_data.append({
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            })
        
        return make_response(jsonify(heroes_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': f'Database error: {str(e)}'}), 500)

# POST /heroes
@app.route('/heroes', methods=['POST'])
def create_hero():
    try:
        data, error = get_json_data()
        if error:
            return make_response(jsonify({'errors': [error]}), 400)
        
        # Validate required fields
        name = data.get('name', '').strip()
        super_name = data.get('super_name', '').strip()
        
        if not name:
            return make_response(jsonify({'errors': ['name is required and cannot be empty']}), 400)
        
        if not super_name:
            return make_response(jsonify({'errors': ['super_name is required and cannot be empty']}), 400)
        
        # Create new hero
        new_hero = Hero(name=name, super_name=super_name)
        
        db.session.add(new_hero)
        db.session.commit()
        
        hero_data = {
            'id': new_hero.id,
            'name': new_hero.name,
            'super_name': new_hero.super_name
        }
        
        return make_response(jsonify(hero_data), 201)
        
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [f'Error creating hero: {str(e)}']}), 400)

# GET /heroes/<int:id>
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    try:
        hero = Hero.query.get(id)
        
        if not hero:
            return make_response(jsonify({'error': 'Hero not found'}), 404)
        
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'hero_powers': []
        }
        
        for hero_power in hero.hero_powers:
            hero_power_data = {
                'id': hero_power.id,
                'hero_id': hero_power.hero_id,
                'power_id': hero_power.power_id,
                'strength': hero_power.strength,
                'power': {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                }
            }
            hero_data['hero_powers'].append(hero_power_data)
        
        return make_response(jsonify(hero_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': f'Database error: {str(e)}'}), 500)

# PATCH /heroes/<int:id>
@app.route('/heroes/<int:id>', methods=['PATCH'])
def update_hero(id):
    try:
        hero = Hero.query.get(id)
        
        if not hero:
            return make_response(jsonify({'error': 'Hero not found'}), 404)
        
        data, error = get_json_data()
        if error:
            return make_response(jsonify({'errors': [error]}), 400)
        
        if 'name' in data:
            hero.name = data['name'].strip()
        if 'super_name' in data:
            hero.super_name = data['super_name'].strip()
        
        db.session.commit()
        
        hero_data = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name
        }
        
        return make_response(jsonify(hero_data), 200)
        
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [f'Error updating hero: {str(e)}']}), 400)

# DELETE /heroes/<int:id>
@app.route('/heroes/<int:id>', methods=['DELETE'])
def delete_hero(id):
    try:
        hero = Hero.query.get(id)
        
        if not hero:
            return make_response(jsonify({'error': 'Hero not found'}), 404)
        
        db.session.delete(hero)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Hero deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': f'Error deleting hero: {str(e)}'}), 500)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    try:
        powers = Power.query.all()
        powers_data = []
        
        for power in powers:
            powers_data.append({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        
        return make_response(jsonify(powers_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': f'Database error: {str(e)}'}), 500)

# POST /powers
@app.route('/powers', methods=['POST'])
def create_power():
    try:
        data, error = get_json_data()
        if error:
            return make_response(jsonify({'errors': [error]}), 400)
        
        # Validate required fields
        name = data.get('name', '').strip()
        description = data.get('description', '').strip()
        
        if not name:
            return make_response(jsonify({'errors': ['name is required and cannot be empty']}), 400)
        
        if not description:
            return make_response(jsonify({'errors': ['description is required and cannot be empty']}), 400)
        
        if len(description) < 20:
            return make_response(jsonify({'errors': ['description must be at least 20 characters long']}), 400)
        
        # Create new power
        new_power = Power(name=name, description=description)
        
        db.session.add(new_power)
        db.session.commit()
        
        power_data = {
            'id': new_power.id,
            'name': new_power.name,
            'description': new_power.description
        }
        
        return make_response(jsonify(power_data), 201)
        
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [str(e)]}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [f'Error creating power: {str(e)}']}), 400)

# GET /powers/<int:id>
@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    try:
        power = Power.query.get(id)
        
        if not power:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        
        return make_response(jsonify(power_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': f'Database error: {str(e)}'}), 500)

# PATCH /powers/<int:id> - FIXED
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    try:
        power = Power.query.get(id)
        
        if not power:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        
        data, error = get_json_data()
        if error:
            return make_response(jsonify({'errors': [error]}), 400)
        
        if 'description' in data:
            description = data['description'].strip()
            if len(description) < 20:
                return make_response(jsonify({'errors': ['description must be at least 20 characters long']}), 400)
            power.description = description
            
        if 'name' in data:
            power.name = data['name'].strip()
        
        db.session.commit()
        
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        
        return make_response(jsonify(power_data), 200)
        
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [str(e)]}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [f'Error updating power: {str(e)}']}), 400)

# DELETE /powers/<int:id>
@app.route('/powers/<int:id>', methods=['DELETE'])
def delete_power(id):
    try:
        power = Power.query.get(id)
        
        if not power:
            return make_response(jsonify({'error': 'Power not found'}), 404)
        
        db.session.delete(power)
        db.session.commit()
        
        return make_response(jsonify({'message': 'Power deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': f'Error deleting power: {str(e)}'}), 500)

# GET /hero_powers
@app.route('/hero_powers', methods=['GET'])
def get_hero_powers():
    try:
        hero_powers = HeroPower.query.all()
        hero_powers_data = []
        
        for hero_power in hero_powers:
            hero_power_data = {
                'id': hero_power.id,
                'hero_id': hero_power.hero_id,
                'power_id': hero_power.power_id,
                'strength': hero_power.strength,
                'hero': {
                    'id': hero_power.hero.id,
                    'name': hero_power.hero.name,
                    'super_name': hero_power.hero.super_name
                },
                'power': {
                    'id': hero_power.power.id,
                    'name': hero_power.power.name,
                    'description': hero_power.power.description
                }
            }
            hero_powers_data.append(hero_power_data)
        
        return make_response(jsonify(hero_powers_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': f'Database error: {str(e)}'}), 500)

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    try:
        data, error = get_json_data()
        if error:
            return make_response(jsonify({'errors': [error]}), 400)
        
        # Validate required fields
        strength = data.get('strength', '').strip()
        hero_id = data.get('hero_id')
        power_id = data.get('power_id')
        
        if not strength:
            return make_response(jsonify({'errors': ['strength is required']}), 400)
        
        if strength not in ['Strong', 'Weak', 'Average']:
            return make_response(jsonify({'errors': ['strength must be one of: Strong, Weak, Average']}), 400)
        
        if not hero_id:
            return make_response(jsonify({'errors': ['hero_id is required']}), 400)
        
        if not power_id:
            return make_response(jsonify({'errors': ['power_id is required']}), 400)
        
        # Check if hero and power exist
        hero = Hero.query.get(hero_id)
        power = Power.query.get(power_id)
        
        if not hero:
            return make_response(jsonify({'errors': [f'Hero with id {hero_id} not found']}), 400)
        
        if not power:
            return make_response(jsonify({'errors': [f'Power with id {power_id} not found']}), 400)
        
        # Create new hero power
        new_hero_power = HeroPower(
            strength=strength,
            hero_id=hero_id,
            power_id=power_id
        )
        
        db.session.add(new_hero_power)
        db.session.commit()
        
        hero_power_data = {
            'id': new_hero_power.id,
            'hero_id': new_hero_power.hero_id,
            'power_id': new_hero_power.power_id,
            'strength': new_hero_power.strength,
            'hero': {
                'id': new_hero_power.hero.id,
                'name': new_hero_power.hero.name,
                'super_name': new_hero_power.hero.super_name
            },
            'power': {
                'id': new_hero_power.power.id,
                'name': new_hero_power.power.name,
                'description': new_hero_power.power.description
            }
        }
        
        return make_response(jsonify(hero_power_data), 201)
        
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [str(e)]}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [f'Error creating hero power: {str(e)}']}), 400)

# GET /hero_powers/<int:id>
@app.route('/hero_powers/<int:id>', methods=['GET'])
def get_hero_power_by_id(id):
    try:
        hero_power = HeroPower.query.get(id)
        
        if not hero_power:
            return make_response(jsonify({'error': 'HeroPower not found'}), 404)
        
        hero_power_data = {
            'id': hero_power.id,
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength,
            'hero': {
                'id': hero_power.hero.id,
                'name': hero_power.hero.name,
                'super_name': hero_power.hero.super_name
            },
            'power': {
                'id': hero_power.power.id,
                'name': hero_power.power.name,
                'description': hero_power.power.description
            }
        }
        
        return make_response(jsonify(hero_power_data), 200)
    except Exception as e:
        return make_response(jsonify({'error': f'Database error: {str(e)}'}), 500)

# PATCH /hero_powers/<int:id>
@app.route('/hero_powers/<int:id>', methods=['PATCH'])
def update_hero_power(id):
    try:
        hero_power = HeroPower.query.get(id)
        
        if not hero_power:
            return make_response(jsonify({'error': 'HeroPower not found'}), 404)
        
        data, error = get_json_data()
        if error:
            return make_response(jsonify({'errors': [error]}), 400)
        
        if 'strength' in data:
            strength = data['strength'].strip()
            if strength not in ['Strong', 'Weak', 'Average']:
                return make_response(jsonify({'errors': ['strength must be one of: Strong, Weak, Average']}), 400)
            hero_power.strength = strength
        
        db.session.commit()
        
        hero_power_data = {
            'id': hero_power.id,
            'hero_id': hero_power.hero_id,
            'power_id': hero_power.power_id,
            'strength': hero_power.strength,
            'hero': {
                'id': hero_power.hero.id,
                'name': hero_power.hero.name,
                'super_name': hero_power.hero.super_name
            },
            'power': {
                'id': hero_power.power.id,
                'name': hero_power.power.name,
                'description': hero_power.power.description
            }
        }
        
        return make_response(jsonify(hero_power_data), 200)
        
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [str(e)]}), 400)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'errors': [f'Error updating hero power: {str(e)}']}), 400)

# DELETE /hero_powers/<int:id>
@app.route('/hero_powers/<int:id>', methods=['DELETE'])
def delete_hero_power(id):
    try:
        hero_power = HeroPower.query.get(id)
        
        if not hero_power:
            return make_response(jsonify({'error': 'HeroPower not found'}), 404)
        
        db.session.delete(hero_power)
        db.session.commit()
        
        return make_response(jsonify({'message': 'HeroPower deleted successfully'}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({'error': f'Error deleting hero power: {str(e)}'}), 500)

# Debug route
@app.route('/debug', methods=['POST'])
def debug():
    return jsonify({
        'content_type': request.content_type,
        'headers': dict(request.headers),
        'data': request.get_data(as_text=True),
        'json': request.get_json(force=True, silent=True)
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)
