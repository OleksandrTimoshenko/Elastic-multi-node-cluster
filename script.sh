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








## legacy:
# this is really interesting - https://discuss.elastic.co/t/elasticsearch-create-enrollment-token-using-ip-from-wrong-ethernet-adaptor/320999/3
# тобто тут проблема
# я роблю sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
# потім беру токет, роблю 
encode = base64.b64decode("<token>")
# і отримую токен, в якому стоїть неправильна IP (тобто не та, яку я поставив в )
# b'{"ver":"8.14.0","adr":["10.0.2.15:9200"],.......
# потім взяв цей вивід, поміняв у ньому IP і задекодив внову
# text = b'{"ver":"8.14.0","adr":["192.168.56.11:9200"],.......
# token = base64.b64encode(text)
# і тільки потім .....