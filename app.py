from PIL import Image
import time
import numpy as np
import io
import tensorflow_hub as hub
from flask import Flask, request, Response, jsonify, make_response
import tensorflow as tf
import base64


# loading the pre-trained model mobilenet_v2 from tensorflow
module_handle = "https://tfhub.dev/google/openimages_v4/ssd/mobilenet_v2/1"
tf_detector = hub.load(module_handle).signatures['default']


def detection_loop(images, detector, upload_time_start):
    """
    Runs tensorflow mobilenet_v2 pre-trained model against an array of images.
    Args:
        images: list containing images as numpy array
        detector: tensorflow pre-trained mobilenet_v2
        upload_time_start: start time of post request

    Returns:
        data(dict): dictionary containing a list of num images * 100 bounding boxes,
        list of inference time for each image, average inference time, upload time and average upload time.

    """
    bounding_boxes = []
    inf_times = []

    for image in images:
        # fixing array size for grayscale images
        if len(image.shape) == 2:
            image = np.expand_dims(image, axis=-1)
            image = np.repeat(image, 3, axis=-1)

        converted_img = tf.image.convert_image_dtype(image, tf.float32)[tf.newaxis, ...]

        start_time = time.time()
        # using the pre-trained model to make predictions
        result = detector(converted_img)
        end_time = time.time()

        # We are saving the results (which are dictionary)
        result = {key: value.numpy() for key, value in result.items()}

        # inference time for one detected picture is end time - start time
        inf_time = end_time - start_time

        print("Found %d objects." % len(result["detection_scores"]))
        print("Inference time: ", inf_time)

        # Saving 100 borders, classes names and scores for each detection
        bboxes = result['detection_boxes'].tolist()

        # appending inference time per image and bboxes per image in inf_times and bounding_boxes lists
        inf_times.append(inf_time)
        bounding_boxes.append(bboxes)

    upload_time_end = time.time()

    # calculating upload time (run time from posting the request to getting the response back)
    upload_times = upload_time_end - upload_time_start

    # average upload time total upload time divided per number of images
    avg_upload_time = upload_times / len(images)
    avg_inf_time = sum(inf_times) / len(inf_times)

    data = {
        "status": 200,
        "bounding_boxes": bounding_boxes,
        "inf_time": inf_times,
        "avg_inf_time": str(avg_inf_time),
        "upload_time": upload_times,
        "avg_upload_time": str(avg_upload_time)

    }
    return make_response(jsonify(data), 200)


# initializing the flask app
app = Flask(__name__)


# routing http posts to this method
@app.route('/api/detect', methods=['POST', 'GET'])
def main():
    # getting the data(images,timestamp) from server
    data = request.get_json(force=True)

    # get the array of images and the upload start time from the json body
    response_images = data['images']
    upload_time_start = data["timestamp"]

    images = []
    for img in response_images:
        # preparing images for object detection by decoding them
        images.append((np.array(Image.open(io.BytesIO(base64.b64decode(img))), dtype=np.float32)))

    return detection_loop(images, tf_detector, upload_time_start)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
