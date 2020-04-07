build:
	docker build -t maguowei/base base

build-go-app:
	docker build -t maguowei/go-app:onbuild go/app

build-go-builder:
	docker build -t maguowei/go-builder:onbuild go/builder

build-python:
	docker build -t maguowei/python python

build-python-app:
	docker build -t maguowei/python-app:onbuild python-app

build-surge-snell:
	docker build -t maguowei/surge-snell surge-snell

build-v2ray:
	docker build -t maguowei/v2ray v2ray

build-frp:
	docker build -t maguowei/frp frp
