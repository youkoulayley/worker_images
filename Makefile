init:
	pipenv install

unittests:
	py.test tests/ -v --cov worker_images --cov-report term-missing