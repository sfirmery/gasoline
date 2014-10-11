PYTHON=`which python`
NAME=`python setup.py --name`
VERSION=`python setup.py --version`
SDIST=dist/$(NAME)-$(VERSION).tar.gz
VENV=/tmp/venv



check:
	find . -name \*.py | grep -v "^test_" | xargs pylint --errors-only --reports=n
	# pep8
	# pyntch
	# pyflakes
	# pychecker
	# pymetrics

clean:
	rm -rf MANIFEST dist build my_program.egg-info deb_dist
	find . -name '*.pyc' -delete

clean-coffee:
	find gasoline/static/js/backbone/ -name '*.js' -delete

clean-assets: clean-coffee
	rm -rf bower_components/*
	rm -rf gasoline/static/.webassets-cache
	rm -rf gasoline/static/assets/*
	rm -rf gasoline/static/vendors/*
	rm -rf gasoline/static/js/backbone/*

clean-all: clean clean-assets

test:
	python tests

assets: clean-assets
	grunt
	python manager.py assets build

watch:
	grunt watch

build-coffee: clean-coffee
	grunt coffee

routes:
	python manager.py routes

update-pot:
	pybabel extract -F babel.cfg -k _l -o gasoline/translations/messages.pot .
	pybabel update -i gasoline/translations/messages.pot -d gasoline/translations

compile-pot:
	pybabel compile -d gasoline/translations

