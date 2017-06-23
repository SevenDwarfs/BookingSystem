FROM mysql:5.7

WORKDIR /db-server

COPY ./sql/init_data.sql .
COPY ./init.sh .

CMD ["sh", "init.sh"]

