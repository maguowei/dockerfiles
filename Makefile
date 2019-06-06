build:
	docker build -t maguowei/base base

build-python:
	docker build -t maguowei/python python

build-python-app:
	docker build -t maguowei/python-app:onbuild python-app

build-surge-snell:
	docker build -t maguowei/surge-snell surge-snell
