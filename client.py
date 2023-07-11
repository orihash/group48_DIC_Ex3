import os
import time
import json
import base64
import requests
import argparse


def post_images(input_data, url):
    """
    Makes a post request to the server with the input data.

    Args: input_data(dict): contains list of images as base64
        encoded Strings and timestamp which records the start of uploading time.
        url: host url where to send the request.

    Returns:
        response(json): response as json containing detections boxes, inference time, upload time etc.

    """
    json_data = json.dumps(input_data)
    response = requests.post(url, data=json_data)
    return response


if __name__ == "__main__":
    # Specifying CLI arguments
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument("--images_path", help="Path to image directory or to a single image.")
    parser.add_argument("--host", help="host(url) where to post the images aws http://[pub-ip]:80/endpoint or local(default)", default="http://localhost:5000/api/detect")
    args = parser.parse_args()

    # image array which will be filled with base64 encoded Strings of images
    images_array = []

    # checking if images_path is directory or image file itself
    if os.path.isdir(args.images_path):
        for filename in os.listdir(args.images_path):
            image_path = os.path.join(args.images_path, filename)
            with open(image_path, "rb") as image:
                # encoding images
                converted_string = base64.b64encode(image.read())
                images_array.append(bytes.decode(converted_string))
    else:
        with open(args.images_path, "rb") as image:
            converted_string = base64.b64encode(image.read())
            images_array.append(bytes.decode(converted_string))

    data = {
        'images': images_array,
        'timestamp': time.time()
    }

    res = post_images(data, args.host)
    print(res.json())
