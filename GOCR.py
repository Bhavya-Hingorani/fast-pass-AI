from google.cloud import vision
import io
import os
import re

credential_path = "D:/Google_cloud_vision/fast-pass-381106-1560d8f380d2.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def clean_plate(input_str):
    input_str = input_str.upper()
    cleaned_str = re.sub(r'[^a-zA-Z0-9]', '', input_str)
    
    return cleaned_str

def convert_to_valid(input_str):
    match = re.search(r"[A-Z]{2}\d{2}", input_str)
    if match is None:
        return ""

    # Extract the matched substring and everything after it as the valid number plate
    valid_number_plate = input_str[match.start():]

    return valid_number_plate


def detect_text(path):
    """Detects text in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # print("Number plate: " + str(texts[0].description))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    else:
        try:
            text = str(texts[0].description)
            text = clean_plate(text)
            # text = convert_to_valid(text)
            return text
        except IndexError:
                return ""

# detect_text("./8.jpg")