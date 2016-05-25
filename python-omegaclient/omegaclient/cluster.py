# Copyright (c) 2016 Dataman Cloud
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from omageclient.utils import url_maker 

class ClusterAPI(object):
      
    path = "/clusters"

    def __init__(self, http):
        self.http = http

    def index(self):
        """List all clusters"""
        return self.http.get(self.path)

    def show(self, id):
        """List specified cluster"""
        return self.http.get(url_maker(self.path, id))

    def create(self, body):
        """Create new cluster"""
        return self.http.post(self.path, body=body)

    def create_node(self, cluster_id, **kwargs):
        """Add new node for cluster identified by `cluster_id`"""
        return self.http.post(url_maker(self.path, cluster_id, "nodes"),
                              body=kwargs)

    def delete(self, cluster_id):
        """Delete specified cluster"""
        return self.http.delete(url_maker(self.path, cluster_id))

    def delete_nodes(self, cluster_id, *args):
        """Delete nodes for cluster identified by `cluster_id`"""
        return self.http.delete(url_maker(self.path, cluster_id, "node"),
                                body=args)

    def update(self,  body):
        """Update cluster partial"""
        return self.http.patch(url_maker(self.path, id), body=body)
    
    def versions(self):
        pass

    def identifier(self, cluster_id):
        """Generated new node uuid belong to specified cluster"""
        return self.http.get(url_maker(self.path, cluster_id,
                                       "new_node_identifier"))
    
    def node(self, cluster_id, node_id):
        """List node information for specified cluster"""
        return self.http.get(url_maker(self.path, cluster_id, "nodes",
                                       node_id))
    
    def update_node(self, cluster_id, node_id, **kwargs):
        """Updated node information for speicified cluster"""
        return self.http.patch(url_maker(self.path, cluster_id,
                                         "nodes", node_id), **kwargs)

    def metrics(self, cluster_id, node_id):
        """List metrics for node of specified cluster"""
        return self.http.get(url_maker(self.path, cluster_id, "nodes",
                                       node_id))

    def service(self, cluster_id, node_id, service_name, **kwargs):
        """Reset or Restart specified service"""
        return self.http.patch(url_maker(self.path, cluster_id, "nodes",
                                         node_id, "services", service_name),
                               **kwargs)
