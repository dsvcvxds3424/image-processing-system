from flask import Blueprint, request, jsonify
from .models import Request, Product, db
from .tasks import process_images
import uuid

main = Blueprint('main', __name__)

@main.route('/upload', methods=['POST'])
def upload_csv():
    if 'csv' not in request.files:
        return jsonify({'error': 'No CSV file provided'}), 400

    csv_file = request.files['csv']
    request_id = str(uuid.uuid4())

    # Save request to database
    new_request = Request(request_id=request_id, status='Pending')
    db.session.add(new_request)
    db.session.commit()

    # Trigger image processing
    process_images.delay(csv_file.read().decode('utf-8'), request_id)

    return jsonify({'request_id': request_id, 'status': 'Pending'})

@main.route('/status', methods=['GET'])
def get_status():
    request_id = request.args.get('request_id')
    if not request_id:
        return jsonify({'error': 'request_id is required'}), 400

    req = Request.query.filter_by(request_id=request_id).first()
    if not req:
        return jsonify({'error': 'Request not found'}), 404

    return jsonify({'request_id': request_id, 'status': req.status})