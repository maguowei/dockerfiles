FROM maguowei/python:latest
LABEL maintainer="imaguowei@gmail.com"
LABEL name="maguowei/jupyterlab"
LABEL version="0.1.0"

RUN pip install jupyterlab
WORKDIR /home/jupyterlab

CMD ["jupyter-lab", "--allow-root", "--no-browser", "--ip=0.0.0.0"]
