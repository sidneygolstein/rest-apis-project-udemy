# CONTRIBUTING

## How to run the docker file locally

```
docker run -dp 5005:5000 -w /app -v "$(pwd):/app" IMAGE_NAME sh -c "flask run --host 0.0.0.0"
```


## How to re-create the image of a databse
```
docker compose up --build --force-recreate --no-deps db
```



## How to connect with a client database
Create a new conection to the following URL:
```
postgres://USER:PASSWORD@INTERNAL_HOST:PORT/DATABASE
```
Where USER, PASSWORD, INTERNAL_HOST, PORT, and DATABASE depend on the client database
 