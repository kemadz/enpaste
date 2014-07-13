clean:
	rm -f *.pyc
	rm -f enpaste/*.pyc
	rm -f tests/*.pyc
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist

dep:
	pip install -r requirements.txt

test:
	python setup.py test

install:
	pip install .

upgrade:
	pip install --upgrade .
