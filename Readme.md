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
1. think about JVM setup, swap setup, file descriptor limit (see 4-6 [here](https://prabhjot-singh.medium.com/setup-a-multi-node-production-ready-elasticsearch-cluster-8504955f5d10))
2. update ansoble config for (see script.sh):
    - prepare node for Elastic (see №1 here)
3. add env variable for vagrant VMs number in Vagrantfile
4. add Logstash and some log simulator