import csv

def validate_csv(csv_data):
    try:
        csv_reader = csv.reader(csv_data.splitlines())
        header = next(csv_reader)
        if header != ['Serial Number', 'Product Name', 'Input Image Urls']:
            return False
        return True
    except Exception:
        return False