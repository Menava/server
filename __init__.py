from flask import Flask
from flask_cors import CORS
from .config import ApplicationConfig

from .extensions import db

from .models import *
from .routes import *
from .Google import google_route


def create_app():
    app=Flask(__name__)
    CORS(app,resources={r"/*":{"origins":"*"}},supports_credentials=True)
    #app config
    app.config.from_object(ApplicationConfig)

    # jwt.init_app(app)
    db.init_app(app)
    # socketio.init_app(app)
    # socketio.init_app(app,cors_allowed_origins="*")
    # sess.init_app(app)
    
    #registering routes
    app.register_blueprint(app_route)

    app.register_blueprint(customer_route)
    app.register_blueprint(car_route)
    app.register_blueprint(damagetype_route)
    app.register_blueprint(customercar_route)
    app.register_blueprint(framecomponent_route)
    app.register_blueprint(carframe_route)

    app.register_blueprint(supplier_route)
    app.register_blueprint(item_route)
    app.register_blueprint(itempayments_route)
    app.register_blueprint(itempurchases_route)
    app.register_blueprint(service_route)
    app.register_blueprint(serviceitem_route)

    app.register_blueprint(employee_route)
    app.register_blueprint(employeepayrolls_route)

    app.register_blueprint(initcheck_route)
    app.register_blueprint(initialimage_route)
    app.register_blueprint(finalcheck_route)
    app.register_blueprint(finalImage_route)

    app.register_blueprint(serviceplace_route)
    app.register_blueprint(serviceplaceEmployee_route)
    app.register_blueprint(serviceplaceServiceItem_route)

    app.register_blueprint(voucher_route)
    app.register_blueprint(voucherPayment_route)
    app.register_blueprint(voucheremployee_route)
    app.register_blueprint(voucherServiceItem_route)
    app.register_blueprint(voucherOutsources_route)

    app.register_blueprint(generalpurchase_route)
    app.register_blueprint(googleService_route)
    app.register_blueprint(notification_route)

    return app 