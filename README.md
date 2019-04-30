# Eska_2

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
python eska.py
```

To run application using Containers:

 - enter application directory and build docker container by typing command:
 ```sh
docker build -t <name-of-your-container> .
```
Example:
```sh
docker build -t eska_app .
```
- Run container using command:
```sh
docker docker run -p 5000:5000 -rm <name-of-your-container>
```

To populate database with additional fake data:

- Run application
- Use URL path:
```sh
/populate/<int: artists>/<int: hits>
```
Where "artists" is a number of of artists you want to add and "hits" is a number of hits you want to add. Hits will be automatically assigned to random artists in the database.

If you want to execute tests on the API, use nose or nose2:
```sh
nose2 -v
```
or run tests.py in application directory.

