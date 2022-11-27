# Test project with prometheus_client python module

node_exporter has ability to export systemd services status so it is better to use that one.

This project is just for fun)

Run script and print metrics:

```
[root@test systemd_exporter]# nohup python3 services_status_exporter.py services_list.txt &
[1] 1840

[root@test systemd_exporter]# ss -tnlp | grep python
LISTEN     0      5            *:9091                     *:*                   users:(("python3",pid=1840,fd=3))

[root@test systemd_exporter]# curl -s 127.0.0.1:9091
# HELP systemd_service_status Service's status
# TYPE systemd_service_status gauge
systemd_service_status{service="sshd"} 1.0
systemd_service_status{service="docker"} 1.0

```

