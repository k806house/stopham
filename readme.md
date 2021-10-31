# CeleBlur

### Запуск локально

1. В `cicd/` положить файл .env, где указать `S3_ACCESS_KEY`, `S3_SECRET_KEY`
2.
```bash
cd cicd && ./run_dev.sh
```
3. Положить файлы `dump_encodings`, `dump_names` в директорию, которая маунтится к контейнеру storage

4. После старта контейнера storage выполнить
```
curl --data '{"filename": "/opt/dump"}' --header 'Content-Type: application/json' http://localhost:5000/load
```
