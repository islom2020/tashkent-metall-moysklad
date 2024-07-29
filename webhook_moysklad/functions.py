from barcode import EAN13

def create_barcode(number, barcode_type, file_path):
    # Get the barcode class for the specified format
    barcode_class = barcode.get_barcode_class(barcode_type)

    # Create the barcode with ImageWriter to get an image file
    my_barcode = barcode_class(number, writer=ImageWriter())

    # Save the barcode image
    my_barcode.save(file_path)


# Example usage
if __name__ == "__main__":
    number_to_encode = '123456789012'  # Your barcode data
    barcode_type = 'ean13'  # Type of the barcode, e.g., 'ean13', 'code39', 'code128'
    file_path = 'my_barcode'  # Output filename without extension

    create_barcode(number_to_encode, barcode_type, file_path)
