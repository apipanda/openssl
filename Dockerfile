FROM tiangolo/uwsgi-nginx:python3.6

MAINTAINER Bernard Ojengwa <bernard@verifi.ng>


RUN pip install flask


ENV NGINX_MAX_UPLOAD 0
ENV PYSPARK_PYTHON=python3
ENV LISTEN_PORT 80
ENV UWSGI_INI /var/sslme/.bin/uwsgi.ini
ENV STATIC_URL /static
ENV STATIC_PATH /var/sslme/static
ENV STATIC_INDEX 0
ENV PYTHONPATH=/var/sslme
ENV FLASK_SETTINGS_MODULE=app.config.ProdConfig
ENV NAMEKO_AMQP_URI=amqp:///
ENV REDIS_URL=redis:///
ENV MONGO_URI=mongodb:///
ENV SSL_DISABLE=True

COPY ./ /var/sslme
RUN chmod +x /var/sslme/entrypoint.sh
RUN chmod +x /var/sslme/run.sh

WORKDIR /var/sslme
RUN pip install -r requirements.txt

ENTRYPOINT ["entrypoint.sh"]
CMD ["run.sh"]