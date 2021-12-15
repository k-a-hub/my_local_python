# my_local_python


## このプロジェクトをクローン

`ターミナルを起動`

```sh
# 作業用のディレクトリに移動
cd xxxxx/
git clone https://github.com/k-a-hub/my_local_python.git
cd my_local_python/
```


## dockerコンテナ起動時、DBにデータを登録する方法

> 商用、検証環境のDBからdumpデータを取得

```sh
# dump取得方法
mysqlduymp -u user -p sagatamaya_ec1 | gzip > 0_sagatamaya.sql.gz
```

> **dumpファイルのみ** を **./mysql/initdb.d** ディレクトリに配置

```sh
ls -l mysql/initdb.d/
total XXXXXX
-rw-r--r--  1 user  user  62376139 XX XX XX:XX 0_sagatamaya.sql.gz
```


## dockerコンテナ起動方法

```sh
docker-compose up -d
```

 ※コンテナは直ぐに起動しますが、DBへのデータ登録には少々時間がかかります。


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
# Dockerコンテナの削除
docker-compose down --rmi all --volumes --remove-orphans
```

---

## DBにテストデータを登録する方法

> 一度コンテナを作成済みの場合は、mysqlのコンテナとボリュームを削除

```sh
# mysqlコンテナのみを止める
docker container stop tamaya_mysql

# mysqlコンテナを削除
docker container rm tamaya_mysql

# mysqlボリュームを削除
docker volume rm my_local_python_mysql-data
```

> テストデータのgzファイルが **./mysql/initdb.d** ディレクトリあるか確認

```sh
ls -l mysql/initdb.d/
total XXXXX
-rw-r--r--  1 user  user  XXXXXX XX XX XX:XX 0_sagatamaya.sql.gz
-rw-r--r--  1 user  user  XXXXXX XX XX XX:XX 1_testdata.sql.gz
```

> コンテナを起動

```sh
docker-compose up -d
```

 ※コンテナは直ぐに起動しますが、DBへのデータ登録には少々時間がかかります。