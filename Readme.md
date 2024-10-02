# Elastic-multi-node-cluster

## Requirements
- `ansible [core 2.14.1]`
- `Vagrant 2.4.1 (Configured)`
- `Python3, pip3`
- `GNU Make 4.3 (if you want use installation with Makefile)`

## Setup with make
- `make help`

## Or manual setup

## Install required Python libs
`pip3 install -r ./requirements.txt`

## Create vagrant VMs
`NUM_WORKERS=3 vagrant up`

## Create inventory file, generate configs from template, update /etc/hosts
`python ./setup.py`

## Start ansible provisioning
`ansible-playbook -i inventory.yaml playbook.yaml`

## Delete infrastructure
`vagrant destroy -f`

# Go to Kibana
`https://<your_host>/`
### We are using self-signed sertificates, so browser will decline it
### find credentials in `./elasticsearch-master/elasticsearch_password.txt`,

## Working with data in Kibana:
```
Go to "Discover" -> "Click on existing index (if exist)" -> "Create a data view" -> setup regex for index
Create data streams
    - elasticsearch
    - nginx
    - kibana
Import dashboards from ./kibana_dashboards folder
```

## Elasticsearch JVM setup
### elastik usually sets the best values based on the node characteristics.
### but if you know what you're doing...
1. add `bootstrap.memory_lock: true` to `/etc/elasticsearch/elasticsearch.yml`
2. create file `/etc/elasticsearch/jvm.options.d/custom.options` (see [this](https://www.elastic.co/guide/en/elasticsearch/reference/8.15/advanced-configuration.html#set-jvm-options) for more info)
```
-Xms1g
-Xmx1g
```
3. add `MAX_LOCKED_MEMORY=unlimited` to `/etc/default/elasticsearch`
4. add this lines to `/etc/security/limits.conf`
```
- nofile 65536
elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
```
5. add `session required pam_limits.so` to  `/etc/pam.d/common-session`
6. Update elasticsearch service settings (add this to file):
`sudo systemctl edit elasticsearch.service`
```
[Service]
LimitMEMLOCK=infinity
```
7. Restart servive `sudo systemctl daemon-reload && sudo systemctl restart elasticsearch`
