# rm static file
if [ -d "/data" ]; then
    if [ -d "/data/webpage" ]; then
        rm -rf /data/webpage
        echo "[success]: rm dir /data/webpage"
    else
        echo "[success]: make dir /data/webpage"
    fi
else
    echo "[success]: dir /data/webpage is not exist"
fi

# database server
docker stop db
docker rm db
docker rmi db-server

# web service server
docker stop restful-server
docker rm restful-server
docker rmi kinpzz/restful-server
