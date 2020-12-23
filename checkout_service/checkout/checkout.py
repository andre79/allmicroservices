from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import requests
import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@checkout-mysql/maccshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
db = SQLAlchemy(app)


class Checkout(db.Model):
    __tablename__ = "checkout"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idFkOrder = db.Column(db.Integer)
    idUserOrder = db.Column(db.Integer)
    dateOrder = db.Column(db.String(100))
    statusOrder = db.Column(db.String(100))
    productOrder = db.Column(db.String(255))
    quantityOrder = db.Column(db.Integer)
    amountOrder = db.Column(db.String(100))
    forecastOrder = db.Column(db.String(100))
    dateDelivery = db.Column(db.String(100))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, idFkOrder, idUserOrder, dateOrder, statusOrder, productOrder, quantityOrder, amountOrder,
                 forecastOrder,
                 dateDelivery):
        self.idFkOrder = idFkOrder
        self.idUserOrder = idUserOrder
        self.dateOrder = dateOrder
        self.statusOrder = statusOrder
        self.productOrder = productOrder
        self.quantityOrder = quantityOrder
        self.amountOrder = amountOrder
        self.forecastOrder = forecastOrder
        self.dateDelivery = dateDelivery

    def __repr__(self):
        return '' % self.id


class CheckoutOrder(db.Model):
    __tablename__ = 'checkoutOrder'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    idUser = db.Column(db.Integer)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, idUser):
        self.idUser = idUser

    def __repr__(self):
        return '' % self.id


db.create_all()


class CheckoutSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Checkout
        sqla_session = db.session

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    numFkOrder = fields.Number(required=True)
    idUserOrder = fields.Number(required=True)
    dateOrder = fields.String(required=True)
    statusOrder = fields.String(required=True)
    productOrder = fields.String(required=True)
    quantityOrder = fields.String(required=True)
    amountOrder = fields.String(required=True)
    forecastOrder = fields.String(required=True)
    dateDelivery = fields.String(required=True)


class CheckoutOrderScheme(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = CheckoutOrder
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    idUser = fields.Number(required=True)


@app.route('/checkout', methods=['GET'])
def index():
    get_checkout = Checkout.query.all()
    checkout_schema = CheckoutSchema(many=True)
    checkout = checkout_schema.dump(get_checkout)

    fk = 0
    valor = ""
    productsList = list()
    allOrder = list()
    data = dict()
    for i in checkout:
        if i['idFkOrder'] == fk:
            productsList.append({"name": i['productOrder'], "quantity": i['quantityOrder']})
        elif i['idFkOrder'] != fk:
            productsList.append({"name": i['productOrder'], "quantity": i['quantityOrder']})
            data = {"order": i['idFkOrder'],
                    "dateOrder": i['dateOrder'],
                    "statusOrder": i['statusOrder'],
                    "amount": i['amountOrder'],
                    "products": productsList,
                    "forecastOrder": i['forecastOrder'],
                    "dateDelivery": i['dateDelivery']
                    }
            fk = i['idFkOrder']

    allOrder.append(data)

    return make_response(jsonify({"checkout": allOrder}))


@app.route('/checkout/<id>', methods=['GET'])
def get_checkout_by_id(id):
    checkout_schema = CheckoutSchema(many=True)
    get_checkout = Checkout.query.filter(Checkout.idUserOrder == id).all()
    checkout = checkout_schema.dump(get_checkout)

    fk = 0
    valor = ""
    productsList = list()
    allOrder = list()
    data = dict()
    for i in checkout:
        if i['idFkOrder'] == fk:
            productsList.append({"name": i['productOrder'], "quantity": i['quantityOrder']})
        elif i['idFkOrder'] != fk:
            data.clear()
            productsList.clear()
            productsList.append({"name": i['productOrder'], "quantity": i['quantityOrder']})
            data = {"order": i['idFkOrder'],
                    "dateOrder": i['dateOrder'],
                    "statusOrder": i['statusOrder'],
                    "amount": i['amountOrder'],
                    "products": productsList,
                    "forecastOrder": i['forecastOrder'],
                    "dateDelivery": i['dateDelivery']
                    }
            fk = i['idFkOrder']

    allOrder.append(data)

    return make_response(jsonify({"checkout": allOrder}))


@app.route('/checkout/<id>', methods=['PUT'])
def update_checkout_by_id(id):
    data = request.get_json()
    get_checkout = Checkout.query.get(id)
    if data.get('numCard'):
        get_checkout.numCard = data['numCard']
    if data.get('numVenc'):
        get_checkout.numVenc = data['numVenc']
    db.session.add(get_checkout)
    db.session.commit()
    checkout_schema = CheckoutSchema(only=['id', 'numCard', 'numVenc'])
    checkout = checkout_schema.dump(get_checkout)
    return make_response(jsonify({"checkout": checkout}))


@app.route('/checkout/<id>', methods=['DELETE'])
def delete_checkout_by_id(id):
    get_checkout = Checkout.query.get(id)
    db.session.delete(get_checkout)
    db.session.commit()
    return make_response("", 204)


@app.route('/checkout', methods=['POST'])
def create_checkout():
    request.is_json
    content = request.get_json()
    path = 'http://a8518e99d0f4.ngrok.io'

    # Verifica cartão de credito
    cardNumber = content['card']['card-number']
    cardTotal = content['card']['total']
    url = path + "/payment/" + cardNumber
    headers = {'content-type': 'application/json'}
    r = requests.get(url, headers=headers)
    value = r.json()
    if not value:
        response = jsonify({'message': '(Cartão de Credito inválido ou Não Autorizado)'})
        return response, 401

    # Verifica quantidade de produtos
    for i in content['products']:
        item = str(i['id'])
        quantity = i['quantity']
        url = path + "/products/" + item
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers)
        productItem = r.json()
        if productItem['product']['quantity'] > 0:
            if 1000 - productItem['product']['quantity'] > 0:
                text = "Compra approved"
            else:
                response = jsonify({'message': 'Produto Indisponivel: ' + productItem['product']['name']})
                return response, 401

    # Cria a Ordem de Pagamento
    data = content['user']
    order_schema = CheckoutOrderScheme()
    order = order_schema.load(data)
    resultOrder = order_schema.dump(order.create())

    productsList = list()
    x = datetime.datetime.now()
    dataOrder = x.strftime('%d/%m/%Y')
    dataForecast = "28/12/2020"
    for c in content['products']:
        checkout = Checkout(resultOrder['id'], content['user']['idUser'], dataOrder, 'confirmed', c['name'],
                            c['quantity'],
                            cardTotal, '5',
                            dataForecast)
        productsList.append({"name": c['name'], "quantity": c['quantity']})
        db.session.add(checkout)
        db.session.commit()

    data = {"order": resultOrder['id'],
            "dateOrder": dataOrder,
            "statusOrder": 'confirmed',
            "amount": cardTotal,
            "products": productsList,
            "forecastOrder": dataForecast,
            "dateDelivery": dataForecast
            }

    return make_response(jsonify({"checkout": data}), 200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
