# CONTRIBUTING

## How to run the docker file locally

```
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```

## How to run the docker file with gunicorn (for deployment)
```
CMD ["gunicorn", "--bind", "0.0.0.0:80", "app:create_app()"]    
```

## How to re-create the image of a database
```
docker compose up --build --force-recreate --no-deps web
```


## How to connect with a client database
Create a new conection to the following URL, in '.env':
```
postgres://USER:PASSWORD@INTERNAL_HOST:PORT/DATABASE
```
Where USER, PASSWORD, INTERNAL_HOST, PORT, and DATABASE depend on the client database
