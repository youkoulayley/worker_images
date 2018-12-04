init:
	pipenv install

test:
	py.test --cov=worker_images tests/