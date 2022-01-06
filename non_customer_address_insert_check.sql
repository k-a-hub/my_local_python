MariaDB [sagatamaya_ec1]> SELECT * FROM dtb_customer_address;
+---------+-------------+------------+---------+------------+------------+-----------------+-----------+-----------------------------+-------------+--------------------------------+---------+--------------+---------------------+---------------------+--------------------+----------+-------+-----------+---------+-------------------+
| id      | customer_id | country_id | pref_id | name01     | name02     | kana01          | kana02    | company_name                | postal_code | addr01                         | addr02  | phone_number | create_date         | update_date         | discriminator_type | position | title | accept_no | page_no | delete_end_season |
+---------+-------------+------------+---------+------------+------------+-----------------+-----------+-----------------------------+-------------+--------------------------------+---------+--------------+---------------------+---------------------+--------------------+----------+-------+-----------+---------+-------------------+
|  999950 |   999999950 |       NULL |       5 | 会員1      | ユーザ1    | カイイン        | ユーザ    | （株）会社                  | 0100001     | 秋田市中通                     | 1-1-1   | 090987654322 | 2022-01-03 05:15:27 | 2022-01-03 05:30:09 | customeraddress    | 肩書     | NULL  |  15000255 |    NULL |                 0 |
| 1000119 |   999999950 |       NULL |       5 | 会員1      | ユーザ2    | カイイン        | ユーザ    | （株）会社                  | 0100002     | 秋田市東通仲町                 | 1-1-1   | 0100002      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000255 |       1 |                 0 |
| 1000120 |  1000000006 |       NULL |       1 | 非会員1    | ユーザ1    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0010011     | 札幌市北区北十一条西           | 1-1-1   | 0010011      | 2022-01-06 10:28:00 | 2022-01-03 05:05:12 | customeraddress    | 肩書     | NULL  |  15000254 |       1 |                 0 |
| 1000121 |  1000000007 |       NULL |       3 | 非会員2    | ユーザ1    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000002     | パターン7                      | 受注3   | 0000002      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000258 |       1 |                 0 |
| 1000122 |  1000000007 |       NULL |       4 | 非会員2    | ユーザ2    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000003     | パターン7                      | 受注3   | 0000003      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000258 |       2 |                 0 |
| 1000123 |  1000000007 |       NULL |       5 | 非会員2    | ユーザ3    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000004     | パターン7                      | 受注3   | 0000004      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000258 |       3 |                 0 |
| 1000124 |  1000000008 |       NULL |       9 | 非会員3    | 新規1      | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000008     | パターン9                      | 受注1   | 0000008      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000259 |       1 |                 0 |
| 1000125 |  1000000008 |       NULL |      10 | 非会員3    | 新規2      | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000009     | パターン9                      | 受注1   | 0000009      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000259 |       2 |                 0 |
| 1000126 |  1000000008 |       NULL |      11 | 非会員3    | 新規3      | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000010     | パターン9                      | 受注2   | 0000010      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000260 |       3 |                 0 |
| 1000127 |  1000000008 |       NULL |      12 | 非会員3    | 新規4      | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000011     | パターン9                      | 受注2   | 0000011      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000260 |       4 |                 0 |
| 1000128 |  1000000008 |       NULL |       6 | 非会員3    | ユーザ1    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000005     | パターン9                      | 受注3   | 0000005      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000261 |       5 |                 0 |
| 1000129 |  1000000008 |       NULL |       7 | 非会員3    | ユーザ2    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000006     | パターン9                      | 受注3   | 0000006      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000261 |       6 |                 0 |
| 1000130 |  1000000008 |       NULL |       8 | 非会員3    | ユーザ3    | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000007     | パターン9                      | 受注3   | 0000007      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000261 |       7 |                 0 |
| 1000131 |  1000000008 |       NULL |      13 | 非会員3    | 新規5      | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000012     | パターン9                      | 受注3   | 0000012      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000261 |       8 |                 0 |
| 1000132 |  1000000008 |       NULL |      14 | 非会員3    | 新規6      | ヒカイイン      | ユーザ    | （株）ローカル環境          | 0000013     | パターン9                      | 受注3   | 0000013      | 2022-01-06 10:28:00 | 2022-01-03 05:30:21 | customeraddress    | 肩書     | NULL  |  15000261 |       9 |                 0 |
+---------+-------------+------------+---------+------------+------------+-----------------+-----------+-----------------------------+-------------+--------------------------------+---------+--------------+---------------------+---------------------+--------------------+----------+-------+-----------+---------+-------------------+
15 rows in set (0.002 sec)
