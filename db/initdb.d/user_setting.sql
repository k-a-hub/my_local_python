-- 外部のpython環境からアクセスするための設定
-- mysql.connectorが「caching_sha2_password」の認証方式を採用してないので
-- 「mysql_native_password」の認証方式に変更
alter user 'test'@'%' identified with mysql_native_password by 'password';