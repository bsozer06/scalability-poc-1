### Scenario 1: Single Instance (Direct Access)

* Start the application:
  
	```bash
	python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
	```

* Send a test request:
  
	```bash
	curl http://127.0.0.1:8000/process
	```

* Load test:
  
	```bash
	docker run --rm ab-tester -n 250 -c 50 http://host.docker.internal:8000/process
	```

#### Mermaid Diagram of the Architecture

```mermaid
flowchart LR
		Client((Client))
		Client -- HTTP --> FastAPI["FastAPI Application<br>127.0.0.1:8000"]
```


### Scenario 2: Single Instance, Multiple Workers

* Start the application with multiple workers:
  
	```bash
	python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000 --workers 4
	```

* Load test:
  
	```bash
	docker run --rm ab-tester -n 100 -c 50 http://host.docker.internal:8000/process
	```

#### Mermaid Diagram of the Architecture

```mermaid
flowchart LR
		Client((Client))
		Client -- HTTP --> FastAPI["FastAPI Application<br>127.0.0.1:8000"]
		subgraph Uvicorn
				Worker1((Worker 1))
				Worker2((Worker 2))
				Worker3((Worker 3))
				Worker4((Worker 4))
		end
		FastAPI -- Task Distribution --> Worker1
		FastAPI -- Task Distribution --> Worker2
		FastAPI -- Task Distribution --> Worker3
		FastAPI -- Task Distribution --> Worker4
```


### Scenario 3: NGINX + Multiple FastAPI Instances (Each with 2 Workers)

In this scenario, multiple FastAPI instances (app1, app2, app3) and NGINX are started together using Docker Compose. Each FastAPI instance is started with 2 workers. NGINX load balances incoming requests across the backend application containers.

#### 1. Required Files

- `Dockerfile` (for the application)
- `docker-compose.yml`
- `nginx/default.conf` (NGINX configuration)
- `start.sh` (Uvicorn starter)
- `requirements.txt`

#### 2. Start with Docker Compose

Run the following command in the project folder:

```bash
docker compose up --build
```

* Load test:

```bash
docker run --rm ab-tester -n 300 -c 50 http://host.docker.internal:8888/process
```

#### Mermaid Diagram of the Architecture

```mermaid
flowchart TD
	Client((Client))
	Client -- HTTP --> NGINX["NGINX<br>localhost:8888"]
	NGINX -- Load Balancing --> App1["FastAPI Instance 1<br>app1:8001"]
	NGINX -- Load Balancing --> App2["FastAPI Instance 2<br>app2:8002"]
	NGINX -- Load Balancing --> App3["FastAPI Instance 3<br>app3:8003"]
	subgraph app1:8001
		W1a((Worker 1))
		W1b((Worker 2))
	end
	subgraph app2:8002
		W2a((Worker 1))
		W2b((Worker 2))
	end
	subgraph app3:8003
		W3a((Worker 1))
		W3b((Worker 2))
	end
	App1 -- Task Distribution --> W1a
	App1 -- Task Distribution --> W1b
	App2 -- Task Distribution --> W2a
	App2 -- Task Distribution --> W2b
	App3 -- Task Distribution --> W3a
	App3 -- Task Distribution --> W3b
```
