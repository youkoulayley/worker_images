FROM python:3.7 as base

FROM base as builder

ENV PYTHONPATH=/install/lib/python3.7/site-packages

RUN mkdir /install
WORKDIR /install

COPY . /app
WORKDIR /app

RUN pip install --install-option="--prefix=/install" -r requirements.txt
RUN python setup.py install --prefix="/install"

FROM base

RUN useradd -ms /bin/bash worker_images
RUN mkdir /app
RUN mkdir /etc/worker_images

COPY --from=builder /install /usr/local

COPY . /app
RUN chown -R worker_images:worker_images /app /etc/worker_images
USER worker_images
COPY config.ini /etc/worker_images
WORKDIR /app/worker_images

CMD ["python", "__init__.py", "--config-file", "/etc/worker_images/config.ini"]