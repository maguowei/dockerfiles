build:
	docker build -t maguowei/base base

build-app:
	docker build -t maguowei/python-app:onbuild app

build-python:
	docker build -t maguowei/python python
