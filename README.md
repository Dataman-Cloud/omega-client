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
