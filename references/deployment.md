# Docker image

The Docker image structure is designed so that minimal configuration changes are needed between development and production environments.

Following are some details around the setup of the app in the Docker image.

### App location
`/usr/salary_prediction`

### Files and directories copied
Only the files directly related to the api or front-end are copied into the image. (i.e. any notebooks or unnecessary source code are not included.)

These are:
- Python requirements file
- Flask api directory, located at `./api/`
- React build distribution directory, located at `./front-end/build/`
- Pickled model located at `./models/<filename>`

The Flask API expects to serve static files from the `./front-end/build/` folder.
-  [(i.e. refer here)](../api/app.py#L10)

---

# Building and deploying to Heroku


### 1. Make sure the React build is up-to-date with latest changes
From the main project directory, change to `./front-end` directory and run build script.

```shell
cd front-end
npm run build
```

### 2. Build docker image
In main project directory:  
`docker build -t <image-name> .`

* _Not required for Heroku deployment, since it will build an image before pushing_ 

### 3. Push to Heroku
Using [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

In main project directory:
```shell
heroku login
heroku container:login
heroku container:push web -a <app-name>
heroku container:release web -a <app-name>
```