# Movie Recommendation System

## How to start the project

## Models and Server
### Installation
First, go to MovieRec directory.
Follow [this guide](https://code.visualstudio.com/docs/remote/containers) to open a development docker container in VSCode.
The docker file and post-installation command will prepare for the enviromnet automatically.

### Train models
```
python main.py
```
### Inferencing
```
python inference.py
```

### Start up the server
Place the built website (the folder named build) under MovieRec directory.
Download MovieLens 20M posters' images from [here](https://www.kaggle.com/datasets/ghrzarea/movielens-20m-posters-for-machine-learning), and place all the images under a directory named MLP-20M.
Change BERT's trained model weight's directory to yours in server.py.
```
python server.py
```
The config is described in server.conf.

## Website
Please make sure you install the latest node.js.
Go to movie-rec-web directory.

### Installation
```
npm install
```

## Start up website
```
npm start
```

## Build website
```
npm run build
```

Due to CORS issue, please place the folder named build under MovieRec directory and access the website from the port number opend by the server (http://localhost:3500/index.html).