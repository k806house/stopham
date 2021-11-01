# CeleBlur

### Запуск локально

1. В `cicd/` положить файл .env, где указать `S3_ACCESS_KEY`, `S3_SECRET_KEY`
2. В docker-compose.dev.yml заменить все пути `/Users/a19179021` на любой другой путь. Важно, чтобы директория шарилась между всеми контейнерами
3.
```bash
cd cicd && ./run_dev.sh
```
4. Положить файлы `dump_encodings`, `dump_names` из `data/` в директорию, которая маунтится к контейнеру storage

5. После старта контейнера storage выполнить
```
curl --data '{"filename": "/opt/dump"}' --header 'Content-Type: application/json' http://localhost:5000/load
```

### Деплой на виртуалку

1. Зайти на гитхабе в Actions
2. Слева в Workflows выбрат Run server deploy
3. Справа нажать Run workflow
4. Нажать на зеленую кнопку Run workflow
5. После успешного завершения деплоя выполнить

```
curl --data '{"filename": "/opt/dump"}' --header 'Content-Type: application/json' http://46.243.143.125:5000/load
```
