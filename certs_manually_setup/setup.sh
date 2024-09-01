#!/bin/bash

###############################################
# Set up basic security for the Elastic Stack #
###############################################

# on master #
sudo /usr/share/elasticsearch/bin/elasticsearch-certutil ca
# set file location /etc/elasticsearch/certs/elastic-stack-ca.p12
# set empty password (for now)

# original file permissions
# -rw------- 1 root root 2672 Aug 31 11:22 elastic-stack-ca.p12

sudo chown elasticsearch:elasticsearch /etc/elasticsearch/certs/elastic-stack-ca.p12

sudo cp ./elastic-stack-ca.p12 /etc/elasticsearch/certs/
sudo chown elasticsearch:elasticsearch /etc/elasticsearch/certs/elastic-stack-ca.p12

sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --ca /etc/elasticsearch/certs/elastic-stack-ca.p12
# set file location /etc/elasticsearch/certs/elastic-certificates.p12
# set empty password (for now)

# for vagrant scp only
sudo cp /etc/elasticsearch/certs/elastic-certificates.p12 /home/vagrant/
sudo chown vagrant:vagrant /home/vagrant/elastic-certificates.p12

# on host #
vagrant scp elasticsearch-master-1:/home/vagrant/elastic-certificates.p12 ./certs_manually_setup/
vagrant scp ./certs_manually_setup/elastic-certificates.p12 elasticsearch-master-2:~
vagrant scp ./certs_manually_setup/elastic-certificates.p12 elasticsearch-worker-1:~

# on every elasticsearch node #
sudo cp /home/vagrant/elastic-certificates.p12 /etc/elasticsearch/
sudo chown elasticsearch:elasticsearch /etc/elasticsearch/elastic-certificates.p12
sudo rm -rf /etc/elasticsearch/elasticsearch.yml && sudo nano /etc/elasticsearch/elasticsearch.yml
# copy config from ./certs_manually_setup/{hostname}.yaml

# even with EMPTY PASSWORD (y, pass)
sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
sudo systemctl start elasticsearch

# reset password
sudo /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic

# test:
curl -ku elastic:<pass> https://192.168.56.12:9200/_cat/nodes
```
192.168.56.14 49 96 0 0.00 0.04 0.07 d - elasticsearch-worker-1
192.168.56.13 39 92 0 0.14 0.18 0.12 m * elasticsearch-master-2
192.168.56.12 47 95 0 0.00 0.03 0.06 m - elasticsearch-master-1
```

# instructions: https://elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup.html



##########################################################################
# Set up basic security for the Elastic Stack plus secured HTTPS traffic #
##########################################################################

# on every node #
sudo systemctl stop elasticsearch

# on master #
sudo /usr/share/elasticsearch/bin/elasticsearch-certutil http
```
n
y
/etc/elasticsearch/certs/elastic-stack-ca.p12
Enter
Enter
y
elasticsearch-master-1 (node name)

kibana
elasticsearch-master-1
elasticsearch-master-2
elasticsearch-worker-1

y

192.168.56.11
192.168.56.12
192.168.56.13
192.168.56.14

y
N
n
/home/vagrant/elasticsearch-ssl-http.zip
```
sudo chown vagrant:vagrant /home/vagrant/elasticsearch-ssl-http.zip 

# in host #
vagrant scp elasticsearch-master-1:/home/vagrant/elasticsearch-ssl-http.zip ./
vagrant scp ./elasticsearch-ssl-http.zip elasticsearch-master-1:~
vagrant scp ./elasticsearch-ssl-http.zip elasticsearch-masrer-2:~
vagrant scp ./elasticsearch-ssl-http.zip elasticsearch-worker-1:~


# in every node #
sudo apt install unzip
unzip /home/vagrant/elasticsearch-ssl-http.zip
sudo mv /etc/elasticsearch/certs/http.p12 /etc/elasticsearch/certs/http.p12_backup
sudo cp /home/vagrant/elasticsearch/http.p12 /etc/elasticsearch/certs/http.p12

sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
sudo systemctl start elasticsearch



#################################################
# Encrypt HTTP client communications for Kibana #
#################################################
# on master #
# create kibana_token
curl -u elastic:<pass> -X POST "https://192.168.56.12:9200/_security/service/elastic/kibana/credential/token/kibana_token" -k

# on host #
vagrant scp ./elasticsearch-ssl-http.zip kibana:~

# on kibana VM #
sudo apt install unzip
unzip /home/vagrant/elasticsearch-ssl-http.zip
sudo cp ./kibana/elasticsearch-ca.pem /etc/kibana/
sudo rm -rf /etc/kibana/kibana.yml && sudo nano /etc/kibana/kibana.yml
# copy kibana config (and set created on master token)

sudo chown -R kibana:kibana /etc/kibana
sudo systemctl start kibana

# instruction: https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html