### Senario 1

* python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000

* curl http://127.0.0.1:8000/process

* docker run --rm ab-tester -n 100 -c 10 http://host.docker.internal:8000/process


### Senario 2

* python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000 --workers 4

* docker run --rm ab-tester -n 100 -c 10 http://host.docker.internal:8000/process


### Senario 3

