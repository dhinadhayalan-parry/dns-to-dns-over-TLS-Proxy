FROM python:2.7
RUN apt-get install openssl
WORKDIR /usr/local/bin
COPY proxy.py .
EXPOSE 53/tcp
CMD ["python","proxy.py"]
