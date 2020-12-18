from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@user-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.String(255))
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, user, password, name, email):
        self.user = user
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return '' % self.id


db.create_all()


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    user = fields.String(required=True)
    password = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)


@app.route('/user', methods=['GET'])
def index():
    get_user = User.query.all()
    user_schema = UserSchema(many=True)
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/user/<id>', methods=['GET'])
def get_user_by_id(id):
    get_user = User.query.get(id)
    user_schema = UserSchema()
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))

@app.route('/user/auth', methods=['POST'])
def get_user_by_login():
    email = request.json["email"]
    if not email:
        response = jsonify({'message': '(Unauthorized)'})
        return response, 401
    password = request.json["password"]
    if not email:
        response = jsonify({'message': '(Unauthorized)'})
        return response, 401

    get_user = User.query.filter_by(email=email, password=password).first()
    user_schema = UserSchema(exclude=['password'])
    userReturn = user_schema.dump(get_user)
    if not userReturn:
        response = jsonify({'message': '(Unauthorized)'})
        return response, 401
    return make_response(jsonify({"user": userReturn}))


@app.route('/user/<id>', methods=['PUT'])
def update_user_by_id(id):
    data = request.get_json()
    get_user = User.query.get(id)
    if data.get('user'):
        get_user.user = data['user']
    if data.get('password'):
        get_user.password = data['password']
    if data.get('name'):
        get_user.name = data['name']
    if data.get('email'):
        get_user.email = data['email']
    db.session.add(get_user)
    db.session.commit()
    user_schema = UserSchema(only=['id', 'user', 'password', 'name', 'email'])
    user = user_schema.dump(get_user)
    return make_response(jsonify({"user": user}))


@app.route('/user/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    get_user = User.query.get(id)
    db.session.delete(get_user)
    db.session.commit()
    return make_response("", 204)


@app.route('/user', methods=['POST'])
def create_user():
    email = request.json["email"]
    get_user = User.query.filter_by(email=email).first()

    if get_user:
        response = jsonify({'message': '(E-mail already registered)'})
        return response, 406

    data = request.get_json()
    user_schema = UserSchema()
    user = user_schema.load(data)
    result = user_schema.dump(user.create())
    return make_response(jsonify({"user": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
