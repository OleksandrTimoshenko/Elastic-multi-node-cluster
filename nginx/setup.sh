# in host mashine all `192.168.56.12   kibana.com` to /etc/hosts/
sudo apt install nginx -y
cd /etc/nginx/sites-available/
sudo nano kibana.conf
sudo ln -s /etc/nginx/sites-available/kibana.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx