from prometheus_client import start_http_server, Gauge, REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR
import threading
import subprocess
import sys
import time

systemd_service_status = Gauge("systemd_service_status", "Service's status", ['service'])

def get_service_status(service_name):
    status = subprocess.call(["systemctl", "is-active", "--quiet", service_name])
    if status == 0:
        systemd_service_status.labels(service_name).set(1.0)
    else:
        systemd_service_status.labels(service_name).set(0.0)
#    return status

def service_threads(service_name):
    while True:
        t = threading.Thread(target=get_service_status,args=(service_name,))
        t.setDaemon(True)
        t.start()
        time.sleep(10)

def get_services_list(filepath):
    with open(filepath) as f:
        service_list = [line.rstrip() for line in f]
    return service_list

if __name__ == '__main__':
    service_list = get_services_list(sys.argv[1])

    start_http_server(9091)

    [REGISTRY.unregister(c) for c in [PROCESS_COLLECTOR, PLATFORM_COLLECTOR, GC_COLLECTOR]]

    threads = []
    for service_name in service_list:
        t = threading.Thread(target=service_threads,args=(service_name,))
        threads.append(t)
    for thread in threads:
        thread.setDaemon(True)
        thread.start()
    thread.join()
