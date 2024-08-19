Vagrant.configure("2") do |config|

  # Master node
  config.vm.define "elasticsearch-master" do |master|
    master.vm.box = "bento/ubuntu-22.04"
    master.vm.hostname = "elasticsearch-master"
    master.vm.network "private_network", ip: "192.168.56.11"
    master.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
    master.vm.provision "file", source: "./scripts/install_elastic.sh", destination: "/home/vagrant/install_elastic.sh"
    master.vm.provision "shell", inline: "bash /home/vagrant/install_elastic.sh"
  end

  # Worker node
  config.vm.define "elasticsearch-worker" do |worker|
    worker.vm.box = "bento/ubuntu-22.04"
    worker.vm.hostname = "elasticsearch-worker"
    worker.vm.network "private_network", ip: "192.168.56.12"
    worker.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
    worker.vm.provision "file", source: "./scripts/install_elastic.sh", destination: "/home/vagrant/install_elastic.sh"
    worker.vm.provision "shell", inline: "bash /home/vagrant/install_elastic.sh"
  end

end