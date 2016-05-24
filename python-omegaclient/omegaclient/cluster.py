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
        self.http.get(self.path)

    def show(self, id):
        """List specified cluster"""
        self.http.get(url_maker(self.path, id))

    def create(self, body):
        """Create new cluster"""
        self.http.post(self.path, body=body)

    def delete(self, id):
        """Delete specified cluster"""
        self.http.delete(url_maker(self.path, id))

    def update(self, id, body):
        """Update cluster partial"""
        self.http.patch(url_maker(self.path, id), body=body)
    
    def versions(self, 
