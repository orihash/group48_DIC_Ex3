# Project 3
app.py - contains code base for running the mobilenet_v2 pre-trained model for object detection in one image or
           a list of images that we get from the flask server.
client.py - contains code base for posting the images to the server (can post one image or a folder of images) `run client.py --help for more`
requirement.txt - file with libraries needed to run the program
Dockerfile - file with specifications to build a docker container
object-detection-SMALL - directory that holds 4 images for testing purposes

# Part 1
to run locally:
    1. `run`: app.py
    2. `run`: client.py


# Part 2
#Build docker image from Dockerfile
docker build -t dic-assignment .

# Run docker container locally
docker run -d -p 5000:5000 dic-assignment

# Part 3
