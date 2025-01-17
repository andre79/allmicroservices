from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@stock-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Stock(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quantity = db.Column(db.Integer)


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, quantity):
        self.quantity = quantity

    def __repr__(self):
        return '' % self.id


db.create_all()


class StockSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Stock
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    quantity = fields.Number(required=True)


@app.route('/stock', methods=['GET'])
def index():
    get_stock = Stock.query.all()
    stock_schema = StockSchema(many=True)
    stock = stock_schema.dump(get_stock)
    return make_response(jsonify({"stock": stock}))


@app.route('/stock/<id>', methods=['GET'])
def get_stock_by_id(id):
    get_stock = Stock.query.get(id)
    stock_schema = StockSchema()
    stock = stock_schema.dump(get_stock)
    return make_response(jsonify({"stock": stock}))


@app.route('/stock/<id>', methods=['PUT'])
def update_stock_by_id(id):
    data = request.get_json()
    get_stock = Stock.query.get(id)
    if data.get('quantity'):
        get_stock.address = data['quantity']
    db.session.add(get_stock)
    db.session.commit()
    stock_schema = StockSchema(only=['id', 'quantity'])
    stock = stock_schema.dump(get_stock)
    return make_response(jsonify({"stock": stock}))


@app.route('/stock/<id>', methods=['DELETE'])
def delete_stock_by_id(id):
    get_stock = Stock.query.get(id)
    db.session.delete(get_stock)
    db.session.commit()
    return make_response("", 204)


@app.route('/stock', methods=['POST'])
def create_stock():
    data = request.get_json()
    stock_schema = StockSchema()
    stock = stock_schema.load(data)
    result = stock_schema.dump(stock.create())
    return make_response(jsonify({"stock": result}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
