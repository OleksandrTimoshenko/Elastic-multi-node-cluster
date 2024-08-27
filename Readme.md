# Elastic-multi-node-cluster

## Create vagrant VMs
`vagrant up`

## Create inventory file, generate configs from template, update /etc/hosts
`python ./setup.py`

## Start ansible provisioning (playbook in progress)
`ansible-playbook -i inventory.yaml playbook.yaml`

## Delete infrastructure
`vagrant destroy -f`

# Go to Kibana
`https://<your_host>/`
### We are using self-signed sertificates, so browser will decline it
### find credentials in `./elasticsearch-master/elasticsearch_password.txt`

## TODO
1. think about additionall Elastic node setup in config, [example](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html)
2. think about JVM setup, swap setup, file descriptor limit (see 4-6 [here](https://prabhjot-singh.medium.com/setup-a-multi-node-production-ready-elasticsearch-cluster-8504955f5d10))
3. update ansoble config for (see script.sh):
    - prepare node for Elastic (see №3 here)
4. add env variable for vagrant VMs number in Vagrantfile
5. add Logstash and some log simulator....
6. add requirements to project
7. Add Nginx server for Kibana, setup domain using /etc/hosts