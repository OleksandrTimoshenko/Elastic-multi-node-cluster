# Elastic-multi-node-cluster

## Requirements
- `ansible [core 2.14.1]`
- `Vagrant 2.4.1 (Configured)`
- `Python3, pip3`

## Install required Python libs
`pip3 install -r ./requirements.txt`

## Create vagrant VMs
`vagrant up`

## Create inventory file, generate configs from template, update /etc/hosts
`python ./setup.py`

## Start ansible provisioning
`ansible-playbook -i inventory.yaml playbook.yaml`

## Delete infrastructure
`vagrant destroy -f`

# Go to Kibana
`https://<your_host>/`
### We are using self-signed sertificates, so browser will decline it
### find credentials in `./elasticsearch-master/elasticsearch_password.txt`

## TODO
1. add env variable for vagrant VMs number in Vagrantfile
2. add Logstash and some log simulator

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
