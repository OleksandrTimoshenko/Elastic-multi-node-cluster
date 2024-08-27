Vagrant.configure("2") do |config|
  num_masters = 3
  num_workers = 3

  # Kibana node
  config.vm.define "kibana" do |kibana|
    kibana.vm.box = "bento/ubuntu-22.04"
    kibana.vm.hostname = "kibana"
    kibana.vm.network "private_network", ip: "192.168.56.11"
    kibana.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end
  end

  # Masters nodes loop
  (1..num_masters).each do |i|
    config.vm.define "elasticsearch-master-#{i}" do |master|
      master.vm.box = "bento/ubuntu-22.04"
      master.vm.hostname = "elasticsearch-worker-#{i}"
      master.vm.network "private_network", ip: "192.168.56.1#{i + 1}"
      master.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2
      end
    end
  end

  # Workers nodes loop
  (1..num_workers).each do |i|
    config.vm.define "elasticsearch-worker-#{i}" do |worker|
      worker.vm.box = "bento/ubuntu-22.04"
      worker.vm.hostname = "elasticsearch-worker-#{i}"
      worker.vm.network "private_network", ip: "192.168.56.1#{i + num_masters + 1}"
      worker.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2
      end
    end
  end
end