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

import copy
from jsonschema import SchemaError, ValidationError, validate
from omegaclient.utils import url_maker
import webob


class AppAPI(object):
    """App associated APIs"""

    def get_cluster_apps(self, cluster_id, **kwargs):
        """List all apps for speicified cluster"""
        return self.http.get(url_maker("/clusters", cluster_id, "apps"),
                             **kwargs)

    def create_cluster_apps(self, cluster_id, **kwargs):
        """Create app under speicified cluster

        :param cluster_id: Cluster identifier
        :param data: Dictionary to send in the body of the request.

        """

        # NOTE(mgniu): `deep copy or shallow copy? i'm confused.
        data = copy.deepcopy(kwargs)

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "instances": {"type": "number"},
                "volumes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "hostPath": {"type": "string"},
                            "containerPath": {"type": "string"},
                         },
                     },
                 },
                "portMappings": {
                     "type": "array",
                     "items": {
                         "type": "object",
                         "properties": {
                             "appPort": {"type": "number"},
                             "protocol": {"type": "number"},
                             "isUri": {"type": "number"},
                             "type": {"type": "number"},
                             "mapPort": {"type": "number"},
                             "uri": {"type": "string"},
                          },
                      },
                   },
                "cpus": {"type": "number"},
                "mem": {"type": "number"},
                "cmd": {"type": "string"},
                "envs": {
                       "type": "array",
                       "items": {
                           "type": "object",
                           "properties": {
                               "key": {"type": "string"},
                               "value": {"type": "string"},
                            },
                        },
                   },
                "imageName": {"type": "string"},
                "imageVersion": {"type": "string"},
                "forceImage": {"type": "boolean"},
                "network": {"type": "string"},
                "constraints": {
                       "type": "array",
                       "items": {
                           "type": "array",
                           "items": {"type": "string"},
                       },
                   },
                "parameters": {
                       "type": "array",
                       "items": {
                           "type": "object",
                           "properties": {
                               "key": {"type": "string"},
                               "value": {"type": "string"},
                           },
                       },
                   }
            }
        }
        try:
            validate(data, schema)
        except (SchemaError, ValidationError):
            raise webob.exc.HTTPBadRequest(explanation="Bad Paramaters")

        return self.http.post(cluster_id, data=data)

    def get_cluster_app(self, cluster_id, app_id):
        """List specified app information under specified cluster"""

        return self.http.get(url_maker("/clusters", cluster_id,
                                       "apps", app_id))

    def delete_cluster_app(self, cluster_id, app_id):
        """Delete speicified app under specified cluster"""

        return self.http.delete(url_maker("/clusters", cluster_id,
                                          "apps", app_id))

    def get_user_apps(self, **kwargs):
        """List all apps belong to specified user."""

        return self.http.get("/apps", **kwargs)

    def get_user_apps_status(self):
        """List all app's status"""

        return self.http.get("/app/status")

    def get_app_versions(self, cluster_id, app_id):
        """List all history versions for app"""

        return self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "versions"))

    def delete_app_version(self, cluster_id, app_id):
        """Delete app version"""

        return self.http.delete(url_maker("/clusters", cluster_id,
                                          "apps", app_id))

    def update_cluster_app(self, cluster_id, app_id, **kwargs):
        """Updated app configuration"""

        if 'method' in kwargs:
            return self.http.patch(url_maker("/clusters", cluster_id,
                                             "apps", app_id),
                                   data=kwargs)
        return self.http.put(url_maker("/clusters", cluster_id, "apps",
                                       app_id), data=kwargs)

    def get_app_instances(self, cluster_id, app_id):
        """List all app instances"""

        return self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "tasks"))

    def get_app_events(self, cluster_id, app_id):
        """List all app events"""

        return self.http.get(url_maker("/clusters", cluster_id, "apps", app_id,
                                       "events"))
