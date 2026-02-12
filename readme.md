### Senario 1

* python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000

* curl http://127.0.0.1:8000/process

* docker run --rm ab-tester -n 100 -c 10 http://host.docker.internal:8000/process


### Senario 2

* python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000 --workers 4

* docker run --rm ab-tester -n 100 -c 10 http://host.docker.internal:8000/process


### Senaryo 3: Load Balancer (NGINX) ile Farklı Portlara Dağıtım

Bu senaryoda, uygulamanızı aynı makinede farklı portlarda birden fazla kez başlatıp, bir load balancer (ör. NGINX) ile gelen istekleri bu portlara dağıtacaksınız. Böylece kullanıcı sadece load balancer'ın portuna istek atar, yük arka planda çalışan uygulamalara dağıtılır.

#### 1. Uygulamayı Farklı Portlarda Başlatın

Her biri ayrı terminalde aşağıdaki komutları çalıştırın:

```
python.exe -m uvicorn app:app --host 127.0.0.1 --port 8001
python.exe -m uvicorn app:app --host 127.0.0.1 --port 8002
python.exe -m uvicorn app:app --host 127.0.0.1 --port 8003
```

#### 2. NGINX Kurulumu ve Konfigürasyonu

**a) NGINX'i kurun:**
- Windows için: [https://nginx.org/en/download.html](https://nginx.org/en/download.html) adresinden indirin ve kurun.
- Linux için: `sudo apt install nginx` veya `sudo yum install nginx` komutunu kullanabilirsiniz.

**b) NGINX konfigürasyon dosyasını düzenleyin:**
Örneğin, `nginx.conf` dosyanıza aşağıdaki bölümü ekleyin:

```
upstream app_servers {
	server 127.0.0.1:8001;
	server 127.0.0.1:8002;
	server 127.0.0.1:8003;
}

server {
	listen 8080;
	location / {
		proxy_pass http://app_servers;
	}
}
```

**c) NGINX'i başlatın veya yeniden başlatın:**
- Windows: Komut satırında NGINX klasörüne gidip `nginx.exe` çalıştırın.
- Linux: `sudo systemctl restart nginx` veya `sudo service nginx restart`

#### 3. Yük Testi

Artık sadece load balancer'ın portuna istek atmanız yeterli:

```
docker run --rm ab-tester -n 100 -c 10 http://host.docker.internal:8080/process
```

Bu şekilde, NGINX gelen istekleri arka planda çalışan uygulama instance'larına dağıtır ve ölçeklenebilirliği test edebilirsiniz.

