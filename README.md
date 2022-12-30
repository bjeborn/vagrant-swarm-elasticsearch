# vagrant-swarm-elasticsearch
Configuration and scripts for deploying elasticsearch in docker swarm in vagrant

## Instruction
`vagrant up` will deploy the following

```
3 Rocky Linux VMs in libvirt
|-Docker Swarm with 1 manager and 2 worker nodes
  |-2 ES master nodes. Locked to worker01 and worker02
  |-3 ES data nodes. One on each swarm node
  |-1 ES ingest node. Port 9200 exposed (https)
  |-1 Kibana. Port 5601 exposed (https)
```

Kibana: https://192.168.50.100:5601  
ES API: https://192.168.50.100:9200  
Username: elastic  
Password: elasticelastic

## Details
VM specifications are in Vagrantfile  
Swarm is constructed in Vagrantfile  
Swarm join token is shared to workers via Vagrant NFS share  
ES certificates are generated from Vagrantfile by letting the manager node call generate-certs-and-docker-configs.sh  
ES certificates are stored as Docker configs for availability on all nodes  
ES cluster specification is generated from template and saved in mycluster/mycluster.yml  

## Modifications
### Disable TLS between Kibana and browser
__On manager VM__
* Set `SERVER_SSL_ENABLED: "false"` on the kibana service in /vagrant/stacks/mycluster.yml
* Redeploy stack with `docker stack deploy -c /vagrant/stacks/mycluster.yml mycluster`

## Stack generator
To generate stack configs, stack_generator.py can be used on manager VM
```
/venv/bin/python /vagrant/stack_generator.py \
 --elastic_password elasticelastic \
 --elastic_port=9210 \
 --kibana_password=kibanakibana \
 --kibana_port=5611 \
 cluster2
```
Deploy (on manager VM) with `docker stack deploy /vagrant/stacks/cluster2.yml cluster2`