$install_docker_script = <<SCRIPT
rm /vagrant/worker_token
echo Installing Docker...
dnf config-manager --set-enabled crb
dnf -y install epel-release
dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
dnf -y install docker-ce docker-ce-cli containerd.io docker-compose-plugin
echo "vm.max_map_count=262144" >> /etc/sysctl.conf
sysctl -w vm.max_map_count=262144
systemctl --now enable docker
sleep 5
docker run --rm hello-world
usermod -a -G docker vagrant
zcat /vagrant/elasticsearch-8.5.3.docker.gz | docker load
zcat /vagrant/kibana-8.5.3.docker.gz | docker load
zcat /vagrant/rockylinux-9.docker.gz | docker load
mkdir -m 777 /tank
SCRIPT

$manager_script = <<SCRIPT
echo Swarm Init...
docker swarm init --listen-addr 192.168.50.100:2377 --advertise-addr 192.168.50.100:2377
sleep 5
docker swarm join-token --quiet worker > /vagrant/worker_token
until [ "`docker node ls -q 2>/dev/null | wc -l`" -eq "3" ]; do
  echo "Waiting for nodes..."
  sleep 1
done
sleep 5
echo "Adding node labels"
docker node update --label-add rack=rack1 manager
docker node update --label-add rack=rack2 worker01
docker node update --label-add rack=rack3 worker02
pushd /vagrant
./generate-certs-and-docker-configs.sh
popd
pushd /vagrant
python -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python stack_generator.py \
 --elastic_password elasticelastic \
 --elastic_port=9200 \
 --kibana_password=kibanakibana \
 --kibana_port=5601 \
 mycluster
docker stack deploy -c stacks/mycluster.yml mycluster
popd
SCRIPT

$worker_script = <<SCRIPT
echo Swarm Join...
until [ -s /vagrant/worker_token ]; do
  echo "Waiting for token..."
  sleep 1
  ls -la /vagrant/ > /dev/null 2>&1
done
docker swarm join --token $(cat /vagrant/worker_token) 192.168.50.100:2377
SCRIPT

Vagrant.configure('2') do |config|
  vm_box = 'rockylinux/9'

  config.vm.provider :libvirt do |libvirt|
    libvirt.qemu_use_session = false
  end

  config.vm.define :manager, primary: true  do |manager|
    manager.vm.box = vm_box
    manager.vm.box_check_update = false
    manager.vm.network :private_network, :ip => "192.168.50.100"
    manager.vm.hostname = "manager"
    manager.vm.synced_folder ".", "/vagrant", type: "nfs", nfs_udp: false
    manager.vm.provision "shell", inline: $install_docker_script, privileged: true
    manager.vm.provision "shell", inline: $manager_script, privileged: true
    manager.vm.provider "libvirt" do |v|
      v.cpus = 4
      v.memory = "3000"
    end
  end
  
  (1..2).each do |i|
    config.vm.define "worker0#{i}" do |worker|
      worker.vm.box = vm_box
      worker.vm.box_check_update = false
      worker.vm.network :private_network, :ip => "192.168.50.10#{i}"
      worker.vm.hostname = "worker0#{i}"
      worker.vm.synced_folder ".", "/vagrant", type: "nfs", nfs_udp: false
      worker.vm.provision "shell", inline: $install_docker_script, privileged: true
      worker.vm.provision "shell", inline: $worker_script, privileged: true
      worker.vm.provider "libvirt" do |v|
        v.cpus = 4
        v.memory = "3000"
      end
    end
  end
end
