FROM python:3.10.7

COPY ./start.sh /start.sh
COPY ./wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh
RUN chmod +x /start.sh

# set the working directory in the container
WORKDIR /usr/src/app

# copy the content of the local src directory to the working directory
COPY . .

# install depenencies from requirements.txt file in working directory
RUN pip install -r requirements.txt

# expose application port
EXPOSE 5000

# Run application
ENV PYTHONPATH=/usr/src/app
CMD ["/wait-for-it.sh", "-t", "120", "cassandra:9042", "--", "/start.sh"]