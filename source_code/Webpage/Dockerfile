FROM node:6.10.3

WORKDIR /web-server

COPY . .

RUN npm config set registry https://registry.npm.taobao.org \
    && npm config get registry
RUN npm install \
    && npm run build

CMD ["tail", "-f", "/var/log/faillog"]
