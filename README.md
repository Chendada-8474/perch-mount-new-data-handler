# Perch Mount New Data Handler

使用須知：

1. 複製一個 upload_example.sh 成 upload.sh 。
2. 把 `SOURCE_DIR` 改成 client 端。
   [perch-mount-data-packer](https://github.com/Chendada-8474/perch-mount-data-packer) 的目的地資料夾。
3. `REMOTE_DEST` 改成 `"<username>@<host>:<where ever you put repo>/perch-mount-new-data-handler/new-data/"` 格式。
4. 設定好與 Data Handler 的 SSH connection 。

複製 `upload_example.sh` 成 `upload.sh`， 改成自己需要的參數。
可以在你的 client 上手動執行 `upload.sh`，或者是設定一個 cronjob。

Install ffmpeg on Service

Ubuntu

```sh
sudo apt update && sudo apt install ffmpeg
```
