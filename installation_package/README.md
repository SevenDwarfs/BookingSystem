# 《安装部署说明》

## 安装环境

下面的环境依赖说明的是运行安装包所需要的依赖，而非构建源代码所需要的依赖。

安装环境为：Ubuntu 16.04 LTS、Ubuntu 14.04 64位系统

- curl
- Docker
- Nginx

### Docker 安装

先安装curl，若未安装则使用命令安装

```shell
$ sudo apt-get update
$ sudo apt-get install curl
```

Docker 官方为了简化安装流程，提供了一套安装脚本，用户可以使用下面的脚本进行安装，由于墙内原因安装可能会比较慢。所以这里使用国内的镜像进行安装，这里使用的是17.04.0版本，安装脚本不同版本可见https://github.com/gitlawr/install-docker

```shell
$ export DOCKER_VERSION=17.04.0 && curl -sSL https://raw.githubusercontent.com/gitlawr/install-docker/master/${DOCKER_VERSION}.sh | sh
```

安装完成之后，通过下列命令可以查看docker运行状态。

```shell
$ systemctl status docker
```

显示Active: active(running)即安装成功。

参考：[Docker安装](https://blog.kinpzz.com/2017/05/16/docker-ci-cd/#Docker-安装)

### Docker 配置（可选）

在国内直接使用Docker官方的镜像源下载速度非常慢，所以这里需要手动改成阿里云的镜像地址。如果可以接受较慢的速度，或者不受国内网络环境影响，可以忽略此步骤。

需要注册自己的阿里云账户，阿里云会对每个账户分配一个专属的加速地址。在https://cr.console.aliyun.com/#/accelerator可以查看。获取到加速地址之后执行下面命令进行修改即可。注: 此处需要将`your-accelerator-address`换为你的docker加速地址，演示安装过程的时候默认已经修改好，此处不再显示加速地址。

```shell
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["your-accelerator-address"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

参考：[Docker镜像加速器](http://blog.csdn.net/hyzhou33550336/article/details/58033405)

### Nginx

直接通过apt-get安装nginx

```shell
$ sudo apt-get install nginx
```



## 安装步骤

**安装**

```shell
$ cd installation_package
$ sudo sh install.sh
```

**重启**

```shell
$ sudo sh restart.sh
```

**卸载**

```shell
$ sudo sh uninstall.sh
```

## 安装成功

命令行可以见Sucessfully built 即安装成功。

```shell
sudo sh install.sh
[success]: dir /data exist
[success]: make dir /data/webpage
[success]: store static resources in /data/webpage/dist
[success]: config nginx.conf
Sending build context to Docker daemon   27.3MB
Step 1/5 : FROM mysql:5.7
 ---> e799c7f9ae9c
Step 2/5 : WORKDIR /db-server
 ---> 157f9dc04b35
Removing intermediate container b148bed7c9c5
Step 3/5 : COPY ./sql/init_data.sql .
 ---> 3bb15b00763d
Removing intermediate container 60998d282044
Step 4/5 : COPY ./init.sh .
 ---> ced327b5e2f7
Removing intermediate container 7df458d72c29
Step 5/5 : CMD sh init.sh
 ---> Running in 7804feaf1541
 ---> b7775f46f2e3
Removing intermediate container 7804feaf1541
Successfully built b7775f46f2e3
74b6cdb62e70904cf4f079d4028f962df33e1c53a781f44de4cfd4957e832f09
Sending build context to Docker daemon  33.22MB
Step 1/4 : FROM java:8
 ---> d23bdf5b1b1b
Step 2/4 : VOLUME /tmp
 ---> Running in 8fab1ed5e202
 ---> f7aa701e6210
Removing intermediate container 8fab1ed5e202
Step 3/4 : COPY target/movie-booking.war .
 ---> 8a15625b6d07
Removing intermediate container 617230869bc6
Step 4/4 : CMD java -jar movie-booking.war
 ---> Running in e30678b30dcf
 ---> 95db408cb927
Removing intermediate container e30678b30dcf
Successfully built 95db408cb927
f37df54f98fa1b143f20452de091077729402c9babb52d5338d0dea808ddb64d
```

浏览器访问`127.0.0.1:8000`或者`localhost:8000`或本机ip的8000端口即可以看到页面。若页面可以正常显示、使用即运行正常。

## 常见问题

1. 进行`sudo apt-get update`失败，错误提示Unable to lock the administration directory (/var/lib/dpkg/), is another process using it?

   解决办法：执行

   ```
   sudo rm /var/lib/apt/lists/lock
   sudo rm /var/cache/apt/archives/lock
   sudo rm /var/lib/dpkg/lock
   ```

   参考：https://askubuntu.com/questions/15433/unable-to-lock-the-administration-directory-var-lib-dpkg-is-another-process

2. 为什么不直接将Docker镜像发布在阿里云镜像仓库上安装的时候直接下载即可呢？

   因为这里模拟了多个节点，涉及多个Docker镜像，每一个镜像都单独下载可能会花费较多的时间，所以这里就考虑直接在本地构建Docker镜像。

3. 出现没有权限`Permission Denied`

   docker、nginx的使用需要root权限，所以请使用root用户，或者在命令前面加上sudo指令。