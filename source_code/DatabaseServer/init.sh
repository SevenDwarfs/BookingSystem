
service mysql start
mysql << EOF
CREATE DATABASE movie;
use movie
source init_data.sql
CREATE USER 'movie_database'@'%' IDENTIFIED BY 'movie_database';
GRANT ALL ON movie.* TO 'movie_database'@'%';
EOF
service mysql restart
tail -f /var/log/mysql/error.log

