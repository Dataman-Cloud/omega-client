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

from omegaclient.utils import url_maker
from omegaclient.client import OmegaClient


class AppAPI(OmegaClient):

    def __init__(self, http):
        self.http = http

    def index(self, **kwargs):
        """
        While cluster_id is None, list all apps belong to specified users;
        other wise list all apps belongs to specified users and specified
        clusters.
        """
        if 'cluster_id' in kwargs:
            cluster_id = kwargs['cluster_id']
            del kwargs['cluster_id']
            return self.http.get(url_maker("/clusters", cluster_id, "apps"),
                                 **kwargs)
        return self.http.get("/apps", **kwargs)

    def show(self, cluster_id, app_id):
        """List specified app"""
        return self.http.get(url_maker("/clusters", cluster_id,
                                       "apps", app_id))

    def create(self, cluster_id, body):
        """Create new app"""
        return self.http.post(url_maker("/clusters", cluster_id, "apps"),
                              data=body)

    def delete(self, cluster_id, app_id, version_id=None):
        """
        While version_id is none, delete specified app; other wise delete
        specified versions for specified app
        """
        if version_id is not None:
            return self.http.delete(url_maker("/clusters", cluster_id,
                                              "apps", app_id))
        return self.http.delete(url_maker("/clusters", cluster_id, "apps",
                                          app_id, "versions", version_id))

    def update(self, cluster_id, app_id, **kwargs):
        """
        While kwargs contains `method`, updated app's status(such as stop.
        start. etc.); other wise updated app's information(such as name. etc.)
        """
        if 'method' in kwargs:
            return self.http.patch(url_maker("/clusters", cluster_id,
                                             "apps", app_id),
                                   data=kwargs)
        return self.http.put(url_maker("/clusters", cluster_id, "apps",
                                       app_id), data=kwargs)

    def events(self, cluster_id, app_id):
        """List all operation logs for specfied app"""
        return self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "events"))

    def instances(self, cluster_id, app_id):
        """List all instances for specified app"""
        return self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "tasks"))

    def versions(self, cluster_id, app_id):
        """List all history versions for specified app"""
        return self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "versions"))

    def status(self):
        """List status for all apps of specified users"""
        return self.http.get("/app/status")
