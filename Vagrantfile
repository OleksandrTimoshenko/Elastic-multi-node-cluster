Vagrant.configure("2") do |config|
  num_workers = 3

  config.vm.define "elasticsearch-master" do |master|
    master.vm.box = "bento/ubuntu-22.04"
    master.vm.hostname = "elasticsearch-master"
    master.vm.network "private_network", ip: "192.168.56.11"
    master.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
  end

  # Master node
  config.vm.define "kibana" do |master|
    master.vm.box = "bento/ubuntu-22.04"
    master.vm.hostname = "kibana"
    master.vm.network "private_network", ip: "192.168.56.12"
    master.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
  end

  # Worker nodes loop
  (1..num_workers).each do |i|
    config.vm.define "elasticsearch-worker-#{i}" do |worker|
      worker.vm.box = "bento/ubuntu-22.04"
      worker.vm.hostname = "elasticsearch-worker-#{i}"
      worker.vm.network "private_network", ip: "192.168.56.1#{i+2}"
      worker.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2
      end
    end
  end
end