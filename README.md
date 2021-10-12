
# MusicIDs 
  
MusicIDs is a Django web app to share personal music ideas and creations with other musicians.
In the first phase, the app is mostly focused on guitarists. You can upload your music idea through an audio file and
join music sheets, tabs, or ableton project so that other musicians can modify your creation.
  
## Getting Started  
  
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
  
### Prerequisites  
  
To run the project you will need:
* [Docker](https://www.docker.com/get-started) & [Docker Compose](https://docs.docker.com/compose/install/)
  
### Installing  
  
A step by step series of examples that tell you how to get a development env running
Fyi the project contains two containers, one for the application itself and another one for the database (only used for
dev environment).
  
Clone the repo:
```
git clone https://github.com/Sebastien-M/music_ids.git
```  

At the root of the repository, create a file named `.env` containing the settings described below:
```
DEBUG=TRUE
SECRET_KEY=<your secret key>
ALLOWED_HOSTS=[*]
DB_NAME=<Your database name>
DB_USER=<Your database user>
DB_PASSWORD=<Your database password>
DB_HOST=db
DB_PORT=<Your database port>
MEDIA_ROOT_FOLDER=media
STATIC_ROOT_FOLDER=static
APPLICATION_PORT=8080
```
  
Run the web and db containers:
```
docker-compose up
```  

Run Django migrations
```
docker-compose run web python manage.py migrate
```


Create a user to have access to the admin panel:
```
docker-compose run web python manage.py createsuperuser 
```

Once done the command `docker-compose up` should be okay and should launch the application connected to the database.

## Running the tests

Lol tests?


## Deployment
  TODO

## Versioning

I use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/Sebastien-M/music_ids/releases).

## Authors

* **Sébastien Mandaba** - *Initial work* - [github](https://github.com/Sebastien-M)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details
