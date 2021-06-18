run-rasa-server:
	clean ;\
	clear ;\
	rasa run \
    --enable-api \
    -vv \
    --log-file out.log

train-model:
	clean ;\
	clear ;\
    rasa train

clean: clean-build clean-pyc clean-logs; clear

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*.pyo" -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test:
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr app.egg-info/

clean-logs:
	rm -f .logs/*