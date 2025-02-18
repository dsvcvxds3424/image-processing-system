from . import db

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(100), nullable=False)
    input_image_urls = db.Column(db.Text, nullable=False)
    output_image_urls = db.Column(db.Text)
    request_id = db.Column(db.String(50), db.ForeignKey('request.request_id'))