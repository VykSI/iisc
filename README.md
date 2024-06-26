# IISC Assignment

demo of website is available in demo folder

```bash
git clone https://github.com/VykSI/iisc.git
```

Place yolov3.weights in backend folder after downloading from below link:


Download Yolov3.weights : https://github.com/patrick013/Object-Detection---Yolov3/raw/master/model/yolov3.weights?download=


Copy the file to backend folder


## Docker-compose Method:

open a terminal at current dir:
```bash
docker-compose up --build
```

This should run your web app and you will be able to access frontend on localhost:8000 and backend on localhost:5000

## Docker Method:

Open 2 terminals

### frontend

build docker:
```bash
cd frontend
docker build -t vue-app .
```
run docker:
```bash
docker run -p 8000:8080 vue-app
```
Your server must be running on localhost:8000

### backend

build docker:
```bash
cd backend
docker build -t flask-app .
```
run docker:
```bash
docker run -p 5000:5000 flask-app
```
Your server must be running on localhost:5000

## No Docker Method:

Open 2 terminals

### Frontend

```bash
cd frontend
npm init
npm install
npm install axios
npm install file-saver
npm install xlsx
npm run serve -- --port 8000
```

Should run your server in localhost:8000

### backend

```bash
cd backend
pip install -r requirements.txt
python server.py
```

Should run the server on localhost:5000

