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

#### Build docker image from Dockerfile
docker build -t dic-assignment .

#### Run docker container locally
docker run -d -p 5000:5000 dic-assignment

#### Run client.py script after docker container is up


# Part 3

1. Launch an EC2 instance (AWS LINUX, 64-bit(Arm), 18gb RAM or 8GB RAM, 16GB storage, allow ssh and http trafic from anywhere)
2. Connect to EC2 instance by SSH `ssh -i labsuser.pem ec2-user@[pub-ip]`
3. Configure instance like below:
### remote pre-setup: 

sudo yum install git docker
ssh-keygen
cat /home/ec2-user/.ssh/id_rsa.pub
# copy key to github ssh keys 
# then get ssh link for repo
git clone git@github.com:orihash/grou48_DIC_Ex3.git

cd grou48_DIC_Ex3
sudo systemctl start docker

Before building the image we had to make changes to requirements file by adding
`tensorflow-io==0.25.0`
and to app.py 
by specifying the `port=80`

### setup docker image

# Create the container:
sudo docker build -t dic .

#Run the container
sudo docker run -p 80:80 dic

Then from local machine you run the client.py passing the arguments for images folder and host 

example for one image:
`python client.py --host http://[pub-ip]:80/api/detect  --images_path /Users/orahashani/Documents/group48_DIC_Ex3/object-detection-SMALL/000000146486.jpg`

