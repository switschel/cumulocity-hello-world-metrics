# Python Hello-World Metrics Microservice
A hello-world microservice to demonstrate monitoring capabilities with python

# Requirements

* Python3 is installed
* Docker is installed
* zip is installed
* Cumulocity IoT Tenant with Microservice feature enabled

# Build

In a shell of your choice run:

```console
docker build . -t hello-world
docker save hello-world > image.tar
zip hello-world-metrics.zip image.tar cumulocity.json
```

# Deploy

1. Login to your Cumulocity IoT Tenant
2. Go to "Administration" -> "Ecosystem" -> "Microservices" -> "Add microservice" -> Select "hello-world-metrics.zip"

# Usage
After successful installation the following endpoints will be exposed:

`https://{yourC8YTenantURL}/service/hello-world-metrics/prometheus` - Used for prometheus to collect metrics for this microservice

`https://{yourC8YTenantURL}/service/hello-world-metric` - Simulating a device creation and custom metric
