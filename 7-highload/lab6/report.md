# 7-Highload. Lab6.
Mykhailo Koreshkov, FI-91

## 1. Cluster setup
```
(sci) PS C:\Windows\system32> docker run --name mongo-primary -d --net mongonet mongo --replSet "rs0"
Unable to find image 'mongo:latest' locally
latest: Pulling from library/mongo
ef773e84b43a: Pull complete
2bfad1efb664: Pull complete
84e59a6d63c9: Pull complete
d2f00ac700e0: Pull complete
96d33bf42f45: Pull complete
ebaa69d77b61: Pull complete
aa77b709a7d6: Pull complete
245bd0c9ace2: Pull complete
Digest: sha256:c015870b10451c414911aff5648495bd3fcc9fe0cec340f46bb852706697a72f
Status: Downloaded newer image for mongo:latest
d306ca7a7d51f81cf5e0a072f4e34c1347886c1ee7a8c84cd524c29c34bb9f80
(sci) PS C:\Windows\system32> docker run --name mongo-1 -d --net mongonet mongo --replSet "rs0"
3947a26f3844011962e0b1cc7af5e1c8d1ba13cd737dd3697f247deb85aa0599
(sci) PS C:\Windows\system32> docker run --name mongo-2 -d --net mongonet mongo --replSet "rs0"
a18c5e25713e9d45c5784acda32c9643ae8890fbca854955f2b01377998a48e3
(sci) PS C:\Windows\system32> docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED          STATUS          PORTS       NAMES
a18c5e25713e   mongo     "docker-entrypoint.s…"   6 seconds ago    Up 4 seconds    27017/tcp   mongo-2
3947a26f3844   mongo     "docker-entrypoint.s…"   12 seconds ago   Up 10 seconds   27017/tcp   mongo-1
d306ca7a7d51   mongo     "docker-entrypoint.s…"   43 seconds ago   Up 39 seconds   27017/tcp   mongo-primary
(sci) PS C:\Windows\system32> docker run --name mongo-client -d --net mongonet mongoclient/mongoclient
Unable to find image 'mongoclient/mongoclient:latest' locally
latest: Pulling from mongoclient/mongoclient
290431e50016: Pull complete
6d69d403d242: Pull complete
66a5bb5b2377: Pull complete
814c8cc3a6fa: Pull complete
9f2c20557b72: Pull complete
4e4768f54d55: Pull complete
0312d8fbddab: Pull complete
7e87bd0aff9b: Pull complete
Digest: sha256:ca98c95de349493fab630ca3fae6e611e27e392ebc59f14d7dd73580c045927a
Status: Downloaded newer image for mongoclient/mongoclient:latest
6ea68ab3fdcfc1db33be7c889e762dba1070533bfe93fa374b69075a31f070f1
```
