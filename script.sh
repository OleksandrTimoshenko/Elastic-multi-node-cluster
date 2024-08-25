# in master node

sudo rm -rf /etc/elasticsearch/elasticsearch.yml
sudo nano /etc/elasticsearch/elasticsearch.yml
# copy your config from ./config/elastic_master.yaml to /etc/elasticsearch/elasticsearch.yml
# start elastic
sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service

# create new password for elastic user
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -bs -u elastic
# test
# curl -ku elastic:<pass> https://<ip>:9200/_cluster/health?pretty

# create token for connecting to cluster
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node

# in worker node

sudo /usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <token>

# copy your config from ./config/elastic_worker.yaml to /etc/elasticsearch/elasticsearch.yml

sudo systemctl daemon-reload
sudo systemctl enable elasticsearch.service
sudo systemctl start elasticsearch.service

# test: you should have more than 1 node in cluster
curl -ku elastic:<pass> https://<ip>:9200/_cat/nodes


# setup kibana
# in elastic - generate kibana token
curl -X POST -ku elastic:<pass> https://192.168.56.11:9200/_security/service/elastic/kibana/credential/token/kibana_token

curl -X DELETE -ku elastic:dXCrxrKFMBIxX8xlZQd5 https://192.168.56.11:9200/_security/service/elastic/kibana/credential/token/kibana_token
dXCrxrKFMBIxX8xlZQd5

# in kibana -
1. nano /etc/kibana/kibana.yml
2. /usr/share/kibana/bin/kibana-keystore add elasticsearch.serviceAccountToken
    <set kibana token>
3. cd /etc/kibana && chown -R kibana:kibana /etc/kibana
4. далі треба буде погратися з сертифікатами... 
5. але після запуску kibana працює....