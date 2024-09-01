# Elastic-multi-node-cluster (manually mode)

## !! Disclamer !!
```
This branch was created because I have not found a way to automatically initialize a cluster with multiple master nodes using the enrollment token.
To create a token you need at least one elasticsearch node in the cluster to start, from this node you can run the command to generate tokens, but to start a cluster with several master nodes the keys on them must be configured beforehand, otherwise the cluster will not start.
Here I tried to manually configure encryption in the cluster, as well as Encrypt HTTP client communications for Kibana.
I used a cluster of 3 elasticsearch nodes (2 masters and one worker) and a kibana server.
```

## Create vagrant VMs
`vagrant up`

## Create inventory file, generate configs from template, update /etc/hosts
`python ./setup.py`

## Start ansible provisioning (playbook in progress)
`ansible-playbook -i inventory.yaml playbook.yaml`

## Delete infrastructure
`vagrant destroy -f`

## Usi instructions in `certs_manually_setup/setup.sh`

# Go to Kibana
`https://<your_host>/`
### We are using self-signed sertificates, so browser will decline it
### find credentials in `./elasticsearch-master/elasticsearch_password.txt`

## TODO
1. think about JVM setup, swap setup, file descriptor limit (see 4-6 [here](https://prabhjot-singh.medium.com/setup-a-multi-node-production-ready-elasticsearch-cluster-8504955f5d10))
2. update ansoble config for (see script.sh):
    - prepare node for Elastic (see №3 here)
3. add env variable for vagrant VMs number in Vagrantfile
4. add Logstash and some log simulator....
5. add requirements to project