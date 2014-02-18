all: test

test:
	clear; hr
	coverage run manage.py test

functional_tests:
	hr
	cd functional_tests; py
