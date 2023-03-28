#!flask/bin/python
import os
import time
from threading import Thread

import flask
import prometheus_client
import psutil
from flask import Flask
from prometheus_client import generate_latest
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)

UPDATE_PERIOD = 5
SYSTEM_USAGE = prometheus_client.Gauge('system_usage',
                                       'Hold current system resource usage',
                                       ['resource_type'])
PROCESS_USAGE = prometheus_client.Gauge('process_usage',
                                        'Hold current process resource usage',
                                        ['resource_type'])
DEVICE_COUNTER = prometheus_client.Counter('devices_created', 'Simulates a counter to count created devices')


# Hello world endpoint
@app.route('/')
def hello():
    DEVICE_COUNTER.inc()
    return 'Hello world!'

# Verify the status of the microservice
@app.route('/health')
def health():
    response = flask.Response('{ "status" : "UP" }')
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/prometheus')
def metrics():
    response = flask.Response(generate_latest())
    response.headers["Content-Type"] = "text/plain"
    return response

def system_metrics():
    process = psutil.Process(os.getpid())
    process.cpu_percent()
    while True:
        # print('Updating system metrics...')
        SYSTEM_USAGE.labels('cpu_usage').set(psutil.cpu_percent())
        SYSTEM_USAGE.labels('cpu_count').set(psutil.cpu_count())
        SYSTEM_USAGE.labels('memory_total').set(psutil.virtual_memory()[0])
        SYSTEM_USAGE.labels('memory_available').set(psutil.virtual_memory()[1])
        SYSTEM_USAGE.labels('memory_usage').set(psutil.virtual_memory()[2])
        SYSTEM_USAGE.labels('memory_used').set(psutil.virtual_memory()[3])
        SYSTEM_USAGE.labels('memory_free').set(psutil.virtual_memory()[4])
        PROCESS_USAGE.labels('cpu_usage').set(process.cpu_percent())
        if (hasattr(process, "cpu_num")):
            PROCESS_USAGE.labels('cpu_count').set(process.cpu_num())
        PROCESS_USAGE.labels('thread_count').set(len(process.threads()))
        PROCESS_USAGE.labels('memory_rss').set(process.memory_info().rss)
        PROCESS_USAGE.labels('memory_vms').set(process.memory_info().vms)
        PROCESS_USAGE.labels('memory_uss').set(process.memory_full_info().uss)
        if (hasattr(process, "pss")):
            PROCESS_USAGE.labels('memory_pss').set(process.memory_full_info().pss)
        if (hasattr(process, "swap")):
            PROCESS_USAGE.labels('memory_swap').set(process.memory_full_info().swap)
        time.sleep(UPDATE_PERIOD)

if __name__ == '__main__':
    daemon = Thread(target=system_metrics, daemon=True, name='Background')
    daemon.start()
    app.run(host='0.0.0.0', port=80)