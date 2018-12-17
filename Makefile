init:
	pipenv install

dev:
	docker-compose up -d

unittests:
	docker-compose -f tests/docker/docker-compose.yml up -d
	docker-compose -f tests/docker/docker-compose-tls.yml up -d
	py.test tests -v --cov worker_images --cov-report term-missing
	rm -rf images_tests