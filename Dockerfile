# Docker image creation. The image will
#   - Setup python
#   - Tell the client/user of container what prt flask is runninhg on (here 5000)
#   - Install flask
#   - Run the flask app 

FROM python:3.12
# EXPOSE 5000
# Copy app.py into the image so that we can then run it 
WORKDIR /app            
# Copy requirements.txt into the current folder ('.') which is /app
COPY ./requirements.txt requirements.txt
RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt 
# Copy everything ('.') into the current directory ('/app' or '.' since we are currently in /app) 
COPY . .          
# Need to tell what command should run when this image starts app as a container
# "--host", "0.0.0.0" --> allows an external client to the container to make a request to the flask app running in the container

# To deploy code locally
#CMD ["flask", "run", "--host", "0.0.0.0"]      # To run the pp with the flask build in dev server

# To deploy code with gunicorn
#CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]    


CMD ["/bin/bash", "docker-entrypoint.sh"]


# Then in terminal:
# 'docker build -t image_name .'

# To run a container in the terminal
# docker run -p host_port:docker_img_port image_name -->ex: docker run -p 5005:5000 rest-apis-flask-python
# To run a container in the terminal and we want to use the terminal:
# docker run -d -p host_port:docker_img_port image_name -->ex: docker run -d -p 5005:5000 rest-apis-flask-python


# To create a volume
# docker run -dp 5005:5000 -w /app -v "$(pwd):/app" flask-smorest-api
# This creates a volume (= mapping of a directory between my local file system and the container file system) 
# allowng the code folder to be sync with the containers folder --> let us work with the modified code everytime
# Only use volume for local development, not when we want to deploy our app