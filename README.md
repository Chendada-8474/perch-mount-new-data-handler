# Perch Mount New Data Handler

使用須知：

1. 複製一個 upload_example.sh 成 upload.sh 。
2. 把 `SOURCE_DIR` 改成 client 端。
   [perch-mount-data-packer](https://github.com/Chendada-8474/perch-mount-data-packer) 的目的地資料夾。
3. `REMOTE_HOST` 改成你的 Data Handler 。
4. `REMOTE_USER` 改成你在 Data Handler 用的 linux user 。
5. 如果專案不是放在 user home 下面，請記得把 `DEST_DIR` 改到正確的路徑。
6. 設定好與 Data Handler 的 SSH keys.

複製 `upload_example.sh` 成 `upload.sh`， 改成自己需要的參數。
可以在你的 client 上手動執行 `upload.sh`，或者是設定一個 cronjob。
