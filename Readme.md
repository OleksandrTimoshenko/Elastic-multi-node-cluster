# Elastic-multi-node-cluster

## Create vagrant VMs
`vagrant up`

## Create inventory file
`python ./create_inventory.py`

## Start ansible provisioning (playbook in progress)
`ansible-playbook -i inventory.yaml playbook.yml`

## Delete infrastructure
`vagrant destroy -f`

## TODO
1. create and test with more than 1 worker cluster
2. think about additionall Elastic node setup in config, [example](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.html)
3. think about JVM setup, swap setup, file descriptor limit (see 4-6 [here](https://prabhjot-singh.medium.com/setup-a-multi-node-production-ready-elasticsearch-cluster-8504955f5d10))
4. automate config`s creation for N worker nodes
5. update ansoble config for (see script.sh):
    - prepare node for Elastic (see №3 here)
    - copy config to master node
    - start master node
    - create new password for elastic
    - create token for connecting to cluster
    - copy config to worker node
    - connect worker node to cluster using enrollment-token
    - start worker node
6. add env variable for vagrant VMs number in Vagrantfile
7. add Kibana, Logstash and some log simulator....