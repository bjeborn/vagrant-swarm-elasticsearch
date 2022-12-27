# vagrant-swarm-elasticsearch
Configuration and scripts for deploying elasticsearch in docker swarm in vagrant

## Instruction
`vagrant up` will deploy the following

```
3 Rocky Linux VMs in libvirt
|-Docker Swarm with 1 manager and 2 worker nodes
  |-2 ES master nodes. Locked to worker nodes
  |-3 ES data nodes. One on each node
  |-1 ES ingest node. Port 9200 exposed
  |-1 Kibana. Port 5601 exposed
```

Kibana: http://192.168.50.100:5601  
ES API: https://192.168.50.100:9200  
Username: elastic  
Password: elasticelastic

## Details
VM specifications are in Vagrantfile  
Swarm is constructed in Vagrantfile  
Swarm join token is shared to workers via Vagrant NFS share  
ES certificates are generated from Vagrantfile by letting the manager node call certs/generate-certs-and-docker-configs.sh  
ES certificates are stored as Docker configs for availability on all nodes  
ES cluster specification is in mycluster/mycluster.yml  