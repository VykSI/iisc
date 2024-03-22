# iisc

## open 2 terminals

### frontend

build docker:
`docker build -t vue-app .`
run docker:
`docker run -p 8000:8080 vue-app`
Your server must be running on localhost:8000

### backend

build docker:
`docker build -t flask-app .`
run docker:
`docker run -p 5000:5000 flask-app`
Your server must be running on localhost:5000
