init:
	pipenv install

dev:
	docker-compose up -d

unittests:
	docker-compose up -d nats-streaming
	py.test tests -v --cov worker_images --cov-report term-missing
	rm -rf images_tests