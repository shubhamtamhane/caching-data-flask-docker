# caching-data-flask-docker


For running the file locally, run the command "python api.py" in your terminal when in the working directory and it should work. Details regarding the code in "api.py" can be found in the comments of the file

Port number can be changed in the "app.run(host=YOUR PORT)"

Change the username and password of configfile.ini as per requirement.

Some packages and their working is dependent on the python version. For the code to work as expected, please run it on python 3.9.12 / 3.9.16

requirements.txt has some of the libraries commented out on purpose as they serve other versions of python.

Dockerfile consists of the required steps to create the image. 

For creating image and running container, execute the following steps

1) docker image build -t YOUR_IMAGE_NAME .
2) docker run -p 5000:5000 -d YOUR_IMAGE_NAME
3) Check localhost:5000 on your machine to see it's working.
