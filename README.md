# omega-Client


## Install

``` 
git clone https://github.com/Dataman-Cloud/omega-client.git
   
    
cd omega-client/python-omegaclient/ 
   
    
pip3 install -r requirements.txt
    
    
python3 setup.py install
```   
    
## Use

```
>> from omegaclient import OmegaClient
>> client = OmegaClient(server_url, email, password)
>> client.get_clusters()
>> ...
```
## APIS

* ### get_clusters

 ```
  List all clusters for specified user

  arguments: None

  returns: clusters list
```

* ### get_cluster

```
  List single cluster's information

  arguments: cluster_id

  returns: cluster dictionary

* ### delete_cluster

```
  Delete specified cluster

  arguments: cluster_id

  returns: None

* ### create_cluster

```
  Create new cluster.

  arguments: name: cluster name - string
             cluster_type: cluster type - 1_master or 3_masters or 5_masters
             group_id: - int 

  returns: None

* ### get_node_identifier

```
  Generated new node identifier. this identifier will be used for add new node.

  arguments: cluster_id

  returns: {
               "code": 0,
               "data": {
                   "identifier": "string"
               }
           }
```

* ### get_cluster_node

```
  List node information for specified cluster.

  arguments:
           cluster_id
           node_id

  returns:
          {
            "code": 0,
            "data": {
              "cluster": {
                "id": 0,
                "name": "string",
                "cluster_type": "string"
              },
              "id": "string",
              "name": "string",
              "status": "string",
              "created_at": "string",
              "ip": "string",
              "services": [
                {
                  "name": "string",
                  "status": "string"
                }
              ]
            }
          }
```

* ### update_cluster_node

```
  Updated node information for specified cluster

  arguments:
           cluster_id
           node_id
           kwargs

  returns: 
          {
            "code": 0
          }
 
  status: 200
          401
```

* ### get_node_metrics

```
  Retrive metrics for node 

  arguments:
            cluster_id
            node_id

  returns:
          {
            "code": 0,
            "data": [
                {}
            ]
          } 
```

* ### update_node_service

```
  Reset or restart service on speicified node

  arguments:
           cluster_id
           node_id
           service_name
           kwargs

  returns: { "code": 0 }
```

* ### create_node

```
  Add new node for cluster identified by `cluster_id`
  
  arguments: `cluster_id` `kwargs`

  returns: { "code": 0 }
```

* ### delete_nodes

```
  Delete single node or multiple nodes

  arguments: `cluster_id` `args`

  returns: { "code": 0 }
```
            


