from flask import Flask, make_response, jsonify, abort,request
from models import db, Hero, Power, HeroPower
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    response = make_response(
        '<h1>Welcome to the heroes directory!!</h1>', 200
    )
    return response

### GET /heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes_list = Hero.query.all()

    if heroes_list:
        heroes_data = [
            {"id": hero.id, "name": hero.name, "super_name": hero.super_name}
            for hero in heroes_list
        ]
        return jsonify(heroes_data)
    else:
        return jsonify([]), 404

### GET /heroes/:id
@app.route('/heroes/<int:id>', methods=['GET'])
def heroes_id(id):
    hero = Hero.query.filter(Hero.id == id).first()

    if hero:
        powers_data = [
            {"id": power.id, "name": power.name, "description": power.description}
            for power in hero.powers
        ]
        response_body = {
            'id': hero.id,
            'name': hero.name,
            'super_name': hero.super_name,
            'powers': powers_data,
        }
        response = make_response(jsonify(response_body), 200)
    else:
        response = make_response(jsonify({"error": "Hero not found"}), 404)

    return response

### GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    power_list = Power.query.all()

    if power_list:
        power_data = [
            {"id": power.id, "name": power.name, "description": power.description}
            for power in power_list
        ]
        return jsonify(power_data)
    else:
        return jsonify([]), 404
    
    
    
### GET /powers/:id
@app.route('/powers/<int:id>')
def power_id(id):
    power = Power.query.filter(Power.id == id).first()
    
    if power:
        response_body = {
            'id': power.id,
            'name': power.name,
            'description': power.description,
        }
        response = make_response(jsonify(response_body), 200)
    else:
        response = make_response(jsonify({"error": "Power not found"}), 404)
    
    return response

@app.route('/powers/<int:power_id>', methods=['PATCH'])
def patch_power():
    power = Power.query.get(power_id)
    
    if not power:
        abort(404, {'error': 'Power not found'})
    
    try:
        dt = request.get_json()
        power.description = dt['description']
        db.session.commit()
        return jsonify({'id': power.id, 'name': power.name, 'description' : power.description})
    except KeyError:
        abort(400, {'error':['Invalid data format']})
@app.route("/hero_powers",  methods=["POST"])
def add_authors():
    # print("Name ", request.json.name)

    data = request.get_json()
    new_hero = HeroPower(**data)
    db.session.add(new_hero)
    db.session.commit()
    return jsonify({"success": "hero added successfully!"}), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
