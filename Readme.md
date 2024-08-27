# Elastic-multi-node-cluster

## Create vagrant VMs
`vagrant up`

## Create inventory file
`python ./setup.py`

## Start ansible provisioning (playbook in progress)
`ansible-playbook -i inventory.yaml playbook.yaml`

## Delete infrastructure
`vagrant destroy -f`

# Go to Kibana
`http://192.168.56.12:5601/`
### find credentials in `./elasticsearch-master/elasticsearch_password.txt`

## TODO
1. create and test with more than 1 worker cluster
2. think about additionall Elastic node setup in config, [example](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html)
3. think about JVM setup, swap setup, file descriptor limit (see 4-6 [here](https://prabhjot-singh.medium.com/setup-a-multi-node-production-ready-elasticsearch-cluster-8504955f5d10))
4. update ansoble config for (see script.sh):
    - prepare node for Elastic (see №3 here)
5. add env variable for vagrant VMs number in Vagrantfile
6. add Logstash and some log simulator....
7. add requirements to project
8. Add Nginx server for Kibana, setup domain using /etc/hosts