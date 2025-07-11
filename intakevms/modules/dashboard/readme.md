# Prometheus install

1. Download tar.gz file from [Prometheus](https://prometheus.io/download/)

        An example: prometheus-2.37.4.linux-amd64.tar.gz

2. Unzip the downloaded archive
    ```bash
	tar -xvf prometheus-2.37.4.linux-amd64.tar.gz 
    ```

3. Create two directories:
    - folder1 `/var/db/prometheus` the prometheus database will be stored
    - folder2 `/etc/prometheus` prometheus configuration files will be stored

    ```bash
    sudo mkdir -p /var/db/prometheus /etc/prometheus
    ```

4. Go to the folder with the unpacked Prometheus:
    ```bash
    cd prometheus-2.37.4.linux-amd64
    ```

5. Move prometheus and promtool files to /usr/lib/bin
    ```bash
    sudo mv prometheus promtool /usr/local/bin/
    ```

6. Moving folders console/ console_libraries/ to /etc/prometheus/
    ```bash
    sudo mv consoles console_libraries /etc/prometheus/
    ```

7. Move the prometheus.yaml file to /etc/prometheus/
    ```bash
    sudo mv prometheus.yml /etc/prometheus/
    ```

8. Adding rights to the folder for our user virtman
    ```bash
    sudo chown -R virtman:virtman /etc/prometheus/ /var/db/prometheus 
    ```

9. The archive and the unpacked folder can be deleted:
    ```bash
    cd ..
    rm -rf prometheus*
    ```

10. Checking the Prometheus version:
    ```bash
    prometheus --version
    ```

11. Let's create a demon for Prometheus:
    ```bash
    sudo vim /etc/systemd/system/prometheus.service
    ```

    and write the data there:
```
[Unit]
Description=Prometheus
Wants=network-online.target
After=network-online.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=virtman
group=virtman
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/db/prometheus \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090 \
  --web.enable-lifecycle

[Install]
WantedBy=multi-user.target
```

12. Adding autostart daemon:
    ```bash
    sudo systemctl enable prometheus.service
    ```

13. Launching the service:
    ```bash
    sudo systemctl start prometheus.service
    ```

14. Let's check that everything worked.:
    ```bash
    sudo systemctl status prometheus.service
    ```

    We'll also check the webcam: [0.0.0.0:9090](http://0.0.0.0:9090)

---

# Node_exporter install

1. Download node_exporter from the same [site](https://prometheus.io/download/)
        
        An example: node_exporter-1.4.0.linux-amd64.tar.gz

2. Unpack the downloaded archive:
    ```bash
    tar -xvf node_exporter-1.4.0.linux-amd64.tar.gz
    ```

3. Go to the unpacked folder
    ```bash
    cd node_exporter-1.4.0.linux-amd64
    ```

4. Moving the folder node_exporter в /etc/local/bin/
    ```bash
    sudo mv node_exporter /usr/local/bin 
    ```

5. Let's check that everything works:
    ```bash
    node_exporter --help
    ```

6. Let's create a daemon for this service:
    ```bash
    sudo vim /etc/systemd/system/node_exporter.service
    ```

    and we'll write it there:
```
[Unit]
Description=Node Exporter
Wants=network-online.target
After=network-online.target

StartLimitIntervalSec=500
StartLimitBurst=5

[Service]
User=virtman
group=virtman
Type=simple
Restart=on-failure
RestartSec=5s
ExecStart=/usr/local/bin/node_exporter \
  --collector.logind

[Install]
WantedBy=multi-user.target
```

7. Adding a service to startup:
    ```bash
    sudo systemctl enable node_exporter.service
    ```

8. We start a service:
    ```bash
    sudo systemctl start node_exporter.service
    ```

9. Add job_name to prometheus:
    ```bash
    sudo vim /etc/prometheus/prometheus.yml
    ```

    we add a new job_name at the end of the file:
```bash
  - job_name: "node_exporter"
    static_configs:
      - targets: ["localhost:9100"]
```

10. Check that prometheus.yaml config is working:
    ```bash
    promtool check config /etc/prometheus/prometheus.yml
    
    # SUCCESS: /etc/prometheus/prometheus.yml is valid prometheus config file syntax
    ```

11. Rebooting Prometheus:
    ```bash
    curl -X POST http://localhost:9090/-/reload
    ```
    
    Now in Status \-\> Targets Prometheus will have, in addition to the standard, node_exporter, which will return metrics.


