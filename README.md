# Hits

REST API providing endpoints with (mock) list of radio hits (and artists performing them).

Endpoins path:

```sh
/api/v1/hits
```

To run application on your local machine, enter the application directory and use command:
```sh
flask run
```
or

```sh
python3 main.py
```

To run application using containers:

 - open terminal in the directory with Docker file and type command:
 ```sh
docker build -t <chosen-image-name> .
```
Example:
```sh
docker build -t hits_app .
```
- Run container using command:
```sh
docker run --rm <chosen-image-name>
```

To populate database with additional fake data:

- Run application
- Use URL path:
```sh
/populate/<int: artists>/<int: hits>
```
Where "artists" is a number of of artists you want to add and "hits" is a number of hits you want to add. Hits will be automatically assigned to random artists in the database.

To execute tests, run nose in application directory:
```sh
nose2 -v
```

