from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_, and_, func

def setup_routes(app, db):
    # Models are now imported from app
    from app import Hero, Power, HeroPower
    
    # ==================== HEROES ENDPOINTS ====================
    
    @app.route('/heroes', methods=['GET'])
    def get_heroes():
        """Get all heroes - matches Postman collection"""
        heroes = Hero.query.all()
        heroes_data = []
        for hero in heroes:
            heroes_data.append({
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name
            })
        return jsonify(heroes_data)

    @app.route('/heroes', methods=['POST'])
    def create_hero():
        """Create a new hero"""
        data = request.get_json()
        
        if not data:
            return jsonify({'errors': ['Request body is required']}), 400
        
        required_fields = ['name', 'super_name']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({'errors': [f'Missing required fields: {", ".join(missing_fields)}']}), 400
        
        # Check if hero already exists
        existing_hero = Hero.query.filter(
            or_(Hero.name == data['name'], Hero.super_name == data['super_name'])
        ).first()
        
        if existing_hero:
            return jsonify({'errors': ['Hero with this name or super name already exists']}), 400
        
        try:
            hero = Hero(
                name=data['name'].strip(),
                super_name=data['super_name'].strip()
            )
            
            db.session.add(hero)
            db.session.commit()
            
            response_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                'message': 'Hero created successfully'
            }
            
            return jsonify(response_data), 201
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to create hero: {str(e)}']}), 500

    @app.route('/heroes/<int:id>', methods=['GET'])
    def get_hero(id):
        """Get specific hero with powers - matches Postman collection"""
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({'error': 'Hero not found'}), 404
        
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
        
        return jsonify(hero_data)

    @app.route('/heroes/<int:id>', methods=['PATCH'])
    def update_hero(id):
        """Update a hero's information"""
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({'error': 'Hero not found'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'errors': ['Request body is required']}), 400
        
        try:
            if 'name' in data and data['name']:
                hero.name = data['name'].strip()
            
            if 'super_name' in data and data['super_name']:
                hero.super_name = data['super_name'].strip()
            
            db.session.commit()
            
            response_data = {
                'id': hero.id,
                'name': hero.name,
                'super_name': hero.super_name,
                'message': 'Hero updated successfully'
            }
            
            return jsonify(response_data)
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to update hero: {str(e)}']}), 500

    @app.route('/heroes/<int:id>', methods=['DELETE'])
    def delete_hero(id):
        """Delete a hero and all their power relationships"""
        hero = Hero.query.get(id)
        if not hero:
            return jsonify({'error': 'Hero not found'}), 404
        
        try:
            hero_name = hero.name
            db.session.delete(hero)
            db.session.commit()
            
            return jsonify({
                'message': f'Hero "{hero_name}" deleted successfully'
            }), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to delete hero: {str(e)}']}), 500

    # ==================== POWERS ENDPOINTS ====================
    
    @app.route('/powers', methods=['GET'])
    def get_powers():
        """Get all powers - matches Postman collection"""
        powers = Power.query.all()
        powers_data = []
        for power in powers:
            powers_data.append({
                'id': power.id,
                'name': power.name,
                'description': power.description
            })
        return jsonify(powers_data)

    @app.route('/powers', methods=['POST'])
    def create_power():
        """Create a new power"""
        data = request.get_json()
        
        if not data:
            return jsonify({'errors': ['Request body is required']}), 400
        
        required_fields = ['name', 'description']
        missing_fields = [field for field in required_fields if field not in data or not data[field]]
        
        if missing_fields:
            return jsonify({'errors': [f'Missing required fields: {", ".join(missing_fields)}']}), 400
        
        # Check if power already exists
        existing_power = Power.query.filter(Power.name == data['name']).first()
        if existing_power:
            return jsonify({'errors': ['Power with this name already exists']}), 400
        
        try:
            power = Power(
                name=data['name'].strip(),
                description=data['description'].strip()
            )
            
            db.session.add(power)
            db.session.commit()
            
            response_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description,
                'message': 'Power created successfully'
            }
            
            return jsonify(response_data), 201
        
        except ValueError as e:
            db.session.rollback()
            return jsonify({'errors': [str(e)]}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to create power: {str(e)}']}), 500

    @app.route('/powers/<int:id>', methods=['GET'])
    def get_power(id):
        """Get specific power - matches Postman collection"""
        power = Power.query.get(id)
        if not power:
            return jsonify({'error': 'Power not found'}), 404
        
        power_data = {
            'id': power.id,
            'name': power.name,
            'description': power.description
        }
        return jsonify(power_data)

    @app.route('/powers/<int:id>', methods=['PATCH'])
    def update_power(id):
        """Update power description - matches Postman collection"""
        power = Power.query.get(id)
        if not power:
            return jsonify({'error': 'Power not found'}), 404
        
        data = request.get_json()
        if not data or 'description' not in data:
            return jsonify({'errors': ['validation errors']}), 400
        
        try:
            power.description = data['description']
            db.session.commit()
            
            power_data = {
                'id': power.id,
                'name': power.name,
                'description': power.description
            }
            return jsonify(power_data)
        
        except ValueError as e:
            db.session.rollback()
            return jsonify({'errors': ['validation errors']}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to update power: {str(e)}']}), 500

    @app.route('/powers/<int:id>', methods=['DELETE'])
    def delete_power(id):
        """Delete a power and all its hero relationships"""
        power = Power.query.get(id)
        if not power:
            return jsonify({'error': 'Power not found'}), 404
        
        try:
            power_name = power.name
            db.session.delete(power)
            db.session.commit()
            
            return jsonify({
                'message': f'Power "{power_name}" deleted successfully'
            }), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to delete power: {str(e)}']}), 500

    # ==================== HERO_POWERS ENDPOINTS ====================
    
    @app.route('/hero_powers', methods=['GET'])
    def get_hero_powers():
        """Get all hero-power relationships with filtering"""
        hero_id = request.args.get('hero_id', type=int)
        power_id = request.args.get('power_id', type=int)
        strength = request.args.get('strength', '')
        hero_search = request.args.get('hero_search', '')
        power_search = request.args.get('power_search', '')
        limit = request.args.get('limit', type=int)
        offset = request.args.get('offset', 0, type=int)
        
        query = HeroPower.query.join(Hero).join(Power)
        
        if hero_id:
            query = query.filter(HeroPower.hero_id == hero_id)
        
        if power_id:
            query = query.filter(HeroPower.power_id == power_id)
        
        if strength and strength in ['Strong', 'Weak', 'Average']:
            query = query.filter(HeroPower.strength == strength)
        
        if hero_search:
            query = query.filter(
                or_(
                    Hero.name.ilike(f'%{hero_search}%'),
                    Hero.super_name.ilike(f'%{hero_search}%')
                )
            )
        
        if power_search:
            query = query.filter(
                or_(
                    Power.name.ilike(f'%{power_search}%'),
                    Power.description.ilike(f'%{power_search}%')
                )
            )
        
        if limit:
            query = query.offset(offset).limit(limit)
        
        hero_powers = query.all()
        
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
        
        return jsonify(hero_powers_data)

    @app.route('/hero_powers', methods=['POST'])
    def create_hero_power():
        """Create hero-power relationship - matches Postman collection"""
        data = request.get_json()
        
        if not data:
            return jsonify({'errors': ['validation errors']}), 400
        
        required_fields = ['strength', 'power_id', 'hero_id']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'errors': ['validation errors']}), 400
        
        # Check if hero and power exist
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        
        if not hero or not power:
            return jsonify({'errors': ['validation errors']}), 400
        
        try:
            hero_power = HeroPower(
                strength=data['strength'],
                hero_id=data['hero_id'],
                power_id=data['power_id']
            )
            
            db.session.add(hero_power)
            db.session.commit()
            
            # Return the created hero_power with nested data
            response_data = {
                'id': hero_power.id,
                'hero_id': hero_power.hero_id,
                'power_id': hero_power.power_id,
                'strength': hero_power.strength,
                'hero': {
                    'id': hero.id,
                    'name': hero.name,
                    'super_name': hero.super_name
                },
                'power': {
                    'id': power.id,
                    'name': power.name,
                    'description': power.description
                }
            }
            
            return jsonify(response_data), 201
        
        except ValueError as e:
            db.session.rollback()
            return jsonify({'errors': ['validation errors']}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({'errors': ['validation errors']}), 400

    @app.route('/hero_powers/<int:id>', methods=['GET'])
    def get_hero_power(id):
        """Get a specific hero-power relationship"""
        hero_power = HeroPower.query.get(id)
        if not hero_power:
            return jsonify({'error': 'Hero-Power relationship not found'}), 404
        
        response_data = {
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
        
        return jsonify(response_data)

    @app.route('/hero_powers/<int:id>', methods=['PATCH'])
    def update_hero_power(id):
        """Update a hero-power relationship strength"""
        hero_power = HeroPower.query.get(id)
        if not hero_power:
            return jsonify({'error': 'Hero-Power relationship not found'}), 404
        
        data = request.get_json()
        if not data or 'strength' not in data:
            return jsonify({'errors': ['Strength is required']}), 400
        
        try:
            hero_power.strength = data['strength']
            db.session.commit()
            
            response_data = {
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
                },
                'message': 'Hero-Power relationship updated successfully'
            }
            
            return jsonify(response_data)
        
        except ValueError as e:
            db.session.rollback()
            return jsonify({'errors': [str(e)]}), 400
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to update relationship: {str(e)}']}), 500

    @app.route('/hero_powers/<int:id>', methods=['DELETE'])
    def delete_hero_power(id):
        """Delete a hero-power relationship"""
        hero_power = HeroPower.query.get(id)
        if not hero_power:
            return jsonify({'error': 'Hero-Power relationship not found'}), 404
        
        try:
            hero_name = hero_power.hero.name
            power_name = hero_power.power.name
            
            db.session.delete(hero_power)
            db.session.commit()
            
            return jsonify({
                'message': f'Relationship between "{hero_name}" and "{power_name}" deleted successfully'
            }), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({'errors': [f'Failed to delete relationship: {str(e)}']}), 500

    # ==================== UTILITY ENDPOINTS ====================
    
    @app.route('/search', methods=['GET'])
    def advanced_search():
        """Universal search across all entities"""
        query_text = request.args.get('q', '')
        search_type = request.args.get('type', 'all')
        limit = request.args.get('limit', 10, type=int)
        
        if not query_text:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        results = {
            'query': query_text,
            'search_type': search_type,
            'results': {}
        }
        
        if search_type in ['all', 'heroes']:
            heroes = Hero.query.filter(
                or_(
                    Hero.name.ilike(f'%{query_text}%'),
                    Hero.super_name.ilike(f'%{query_text}%')
                )
            ).limit(limit).all()
            
            results['results']['heroes'] = [
                {
                    'id': hero.id,
                    'name': hero.name,
                    'super_name': hero.super_name,
                    'powers_count': len(hero.hero_powers)
                }
                for hero in heroes
            ]
        
        if search_type in ['all', 'powers']:
            powers = Power.query.filter(
                or_(
                    Power.name.ilike(f'%{query_text}%'),
                    Power.description.ilike(f'%{query_text}%')
                )
            ).limit(limit).all()
            
            results['results']['powers'] = [
                {
                    'id': power.id,
                    'name': power.name,
                    'description': power.description[:100] + '...' if len(power.description) > 100 else power.description,
                    'heroes_count': len(power.hero_powers)
                }
                for power in powers
            ]
        
        if search_type in ['all', 'relationships']:
            hero_powers = HeroPower.query.join(Hero).join(Power).filter(
                or_(
                    Hero.name.ilike(f'%{query_text}%'),
                    Hero.super_name.ilike(f'%{query_text}%'),
                    Power.name.ilike(f'%{query_text}%'),
                    HeroPower.strength.ilike(f'%{query_text}%')
                )
            ).limit(limit).all()
            
            results['results']['relationships'] = [
                {
                    'id': hp.id,
                    'hero_name': hp.hero.name,
                    'hero_super_name': hp.hero.super_name,
                    'power_name': hp.power.name,
                    'strength': hp.strength
                }
                for hp in hero_powers
            ]
        
        return jsonify(results)

    @app.route('/stats', methods=['GET'])
    def get_stats():
        """Get API statistics"""
        stats = {
            'total_heroes': Hero.query.count(),
            'total_powers': Power.query.count(),
            'total_relationships': HeroPower.query.count(),
            'strength_distribution': {
                'Strong': HeroPower.query.filter_by(strength='Strong').count(),
                'Weak': HeroPower.query.filter_by(strength='Weak').count(),
                'Average': HeroPower.query.filter_by(strength='Average').count()
            },
            'most_powerful_heroes': [
                {
                    'name': hero.name,
                    'super_name': hero.super_name,
                    'power_count': len(hero.hero_powers)
                }
                for hero in Hero.query.all()
                if len(hero.hero_powers) > 0
            ][:5],
            'most_popular_powers': [
                {
                    'name': power.name,
                    'hero_count': len(power.hero_powers)
                }
                for power in Power.query.all()
                if len(power.hero_powers) > 0
            ][:5]
        }
        
        return jsonify(stats)

    # ==================== ERROR HANDLERS ====================
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
