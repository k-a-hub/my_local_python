# my_local_python

## このプロジェクトをクローン

ターミナルを起動

```sh
# 作業用のディレクトリに移動
cd xxxxx/
git clone https://github.com/k-a-hub/my_local_python.git
```

## dockerコンテナ起動方法

```sh
docker-compose up -d
```

## 玉屋のDocker（mysqlコンテナ）への接続設定

> 玉屋Dockerのネットワーク情報確認

> 「Containers」の中に **saga_tamaya_mysql_1** が含まれているか確認

```sh
docker network inspect saga_tamaya_default

・・・
        "Containers": {
            "d1f279ab46d2cb28c549187d74078134ea7adc621fd27db784fbf2d039b9bf51": {
                "Name": "saga_tamaya_mysql_1",
                "EndpointID": "ef091c4cf083cd2db62e25ceaf373705e602b5aad81a622d92d86b5158aaa537",
                "MacAddress": "02:42:ac:1d:00:05",
                "IPv4Address": "172.29.0.5/16",
                "IPv6Address": ""
            }
        },
・・・
```

> 今回使用するpythonコンテナを **saga_tamaya_default** ネットワークに追加

```sh
# pythonコンテナを「saga_tamaya_default」ネットワークに追加
docker network connect saga_tamaya_default tamaya_python3
```

> 今回使用するpythonコンテナが **saga_tamaya_default** ネットワークに追加されているか確認
>
> 「Containers」の中に **saga_tamaya_mysql_1** と **tamaya_python3** が含まれているか確認

```sh
# 追加されているか確認
docker network inspect saga_tamaya_default

・・・
        "Containers": {
            "d1f279ab46d2cb28c549187d74078134ea7adc621fd27db784fbf2d039b9bf51": {
                "Name": "saga_tamaya_mysql_1",
                "EndpointID": "ef091c4cf083cd2db62e25ceaf373705e602b5aad81a622d92d86b5158aaa537",
                "MacAddress": "02:42:ac:1d:00:05",
                "IPv4Address": "172.29.0.5/16",
                "IPv6Address": ""
            },
            "fcc2bb41efd331d29fa626b04732202f216013f9d37ad8f71526bf69747ba1b3": {
                "Name": "tamaya_python3",
                "EndpointID": "a8213ad7c9b4264e7aee23140db5b24e152d5c4834368035a4bf817adae97fd9",
                "MacAddress": "02:42:ac:1d:00:06",
                "IPv4Address": "172.29.0.6/16",
                "IPv6Address": ""
            }
        },
・・・

```

## コンテナログイン方法

```sh
# python環境
docker exec -it tamaya_python3 /bin/bash
```

## pythonコード実行方法

```sh
$ cd opt
$ python3 main.py 'YYYY-mm-dd HH:MM:SS'
```

## 実行後の後始末

```sh
# pythonコンテナを「saga_tamaya_default」ネットワークから削除
docker network disconnect saga_tamaya_default tamaya_python3
```

```sh
# 削除されているか確認
docker network inspect saga_tamaya_default

・・・
        "Containers": {
            "d1f279ab46d2cb28c549187d74078134ea7adc621fd27db784fbf2d039b9bf51": {
                "Name": "saga_tamaya_mysql_1",
                "EndpointID": "ef091c4cf083cd2db62e25ceaf373705e602b5aad81a622d92d86b5158aaa537",
                "MacAddress": "02:42:ac:1d:00:05",
                "IPv4Address": "172.29.0.5/16",
                "IPv6Address": ""
            }
        },
・・・
```

```sh
# Dockerコンテナの削除
docker-compose down --rmi all --volumes --remove-orphans
```