build:
	docker build -f Dockerfile.dev . --rm -t app
start:
	docker run --rm -it -e PORT=3000 --name app -p 3000:3000 app
test:
	docker build  -f Dockerfile.test . --rm  -t app-test
	docker run --rm -it app-test