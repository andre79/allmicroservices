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


class Auth(db.Model):
    __tablename__ = "auth"
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


class AuthSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Auth
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    user = fields.String(required=True)
    password = fields.String(required=True)
    name = fields.String(required=True)
    email = fields.String(required=True)


@app.route('/auth', methods=['GET'])
def index():
    get_auth = Auth.query.all()
    auth_schema = AuthSchema(many=True)
    auth = auth_schema.dump(get_auth)
    return make_response(jsonify({"auth": auth}))


@app.route('/auth/<id>', methods=['GET'])
def get_product_by_id(id):
    get_auth = Auth.query.get(id)
    auth_schema = AuthSchema()
    auth = auth_schema.dump(get_auth)
    return make_response(jsonify({"auth": auth}))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
