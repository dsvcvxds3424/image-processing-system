from . import celery, db
from .models import Request, Product
from PIL import Image
import requests
from io import BytesIO
import csv
import os

@celery.task
def process_images(csv_data, request_id):
    csv_reader = csv.reader(csv_data.splitlines())
    next(csv_reader)  # Skip header

    for row in csv_reader:
        serial_number, product_name, input_image_urls = row
        output_image_urls = []

        for url in input_image_urls.split(','):
            response = requests.get(url.strip())
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                image = image.resize((image.width // 2, image.height // 2))
                output_path = f"processed_images/{os.path.basename(url)}"
                image.save(output_path)
                output_image_urls.append(f"http://localhost:5000/{output_path}")

        # Save product to database
        product = Product(
            serial_number=serial_number,
            product_name=product_name,
            input_image_urls=input_image_urls,
            output_image_urls=','.join(output_image_urls),
            request_id=request_id
        )
        db.session.add(product)

    # Update request status
    req = Request.query.filter_by(request_id=request_id).first()
    req.status = 'Completed'
    db.session.commit()