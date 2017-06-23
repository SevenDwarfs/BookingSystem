# copy static file
if [ -d "/data" ]; then
    echo "[success]: dir /data exist"
else
    mkdir /data
    echo "[success]: make dir /data"
fi

if [ -d "/data/webpage" ]; then
    echo "[success]: dir /data/webpage exist"
else
    mkdir /data/webpage
    echo "[success]: make dir /data/webpage"
fi

cp -R ./Webpage/dist /data/webpage
echo "[success]: store static resources in /data/webpage/dist"
# config nginx
cp ./Webpage/nginx.conf /etc/nginx/nginx.conf
nginx -s reload
echo "[success]: config nginx.conf"

# docker

# database server
docker build -t db-server ./DatabaseServer
docker run -d --name db db-server

# web service server
docker build -t kinpzz/restful-server ./WebService
docker run -d -p 127.0.0.1:8082:8082 --name restful-server --link db:db-server kinpzz/restful-server
