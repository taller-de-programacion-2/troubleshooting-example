start_api:
	docker-compose up -d --build
stop_api:
	docker-compose down
start_traffic:
	locust -f ./load_test/locusfile.py