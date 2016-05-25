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

import requests
from client import HTTPClient
from jsonschema import SchemaError, ValidationError, validate
import webob
from omageclient.cluster import ClusterAPI
from omageclient.app import AppAPI
from omageclient.project import ProjectAPI
from omageclient.utils import url_maker
import copy

#class OmegaException(Exception):
#    msg = "A unknown exception occurred."
#
#    def __init__(self, message=None, status_code=None):
#        if not message:
#            message = msg
#        self.status_code = status_code
#
#        super(OmegaException, self).__init__(message)
#
#
#def check_return_code(function):
#    def with_code_check(*args, **kwargs):
#        # raise exception when omega get code big than zero;
#        try:
#            rst = function(*args, **kwargs)
#            if 'code' in rst and rst['code'] > 0:
#                raise OmegaException("Calls to Omega got unexpected result: %s" % rst)
#            return rst
#        except Exception as e:
#            raise OmegaException(e)
#
#    return with_code_check


class OmegaClient(object):

    def __init__(self, server_url, email, password):

        self.http = HTTPClient(server_url, email, password)
        self.cluster_api = ClusterAPI(self.http) 
        self.app_api = AppAPI(self.http)
        self.project_api = ProjectAPI(self.http) 

    # Cluster Associated APIS
    # The following apis are cluster associated apis, contains:
    # get_cluster 
    # get_clusters
    # create_cluster
    # delete_cluster
    # get_node_identifier
    # get_cluster_node
    # update_cluster_node
    # get_node_metrics
    # update_node_service
    # post_nodes
    # delete_nodes

    def get_clusters(self):
        """List all clusters"""

        return self.cluster_api.index()

    def create_cluster(self, name, cluster_type, group_id):
        """
        Create new cluster.
       
        :param name: cluster name
        :param cluster_type: cluster type, current support values are: 1_master, 3_masters, 5_masters
        :param group_id: the group which the new cluster belong to
        """
        body = {
            "name": name,
            "clusterType": cluster_type,
            "groupId": group_id,
        }

        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "clusterType": {"type": "string"},
                "groupId": {"type": "number"},
            },
            "required": ["name", "clusterType", "groupId"]
        }
        return self.cluster_api.create(body=body)

    def get_cluster(self, cluster_id):

        return self.cluster_api.show(cluster_id)

    def delete_cluster(self, cluster_id):

        return self.cluster_api.delete(cluster_id)

    def get_node_identifier(self, cluster_id):

        return self.cluster_api.identifier(cluster_id)

    def get_cluster_node(self, cluster_id, node_id):
        """List node information for specified cluster"""

        return self.cluster_api.node(cluster_id, node_id)

    def update_cluster_node(self, cluster_id, node_id, **kwargs):
        """Updated node information for specified cluster"""

        return self.cluster_api.update_node(cluster_id, node_id, **kwargs)

    def get_node_metrics(self, cluster_id, node_id):
        """List metrics for node of specified cluster"""
        return self.cluster_api.metrics(cluster_id, node_id)

    def update_node_service(self, cluster_id, node_id, service_name, **kwargs):
        """Reset or restart service on speicified node"""
        return self.cluster_api.service(cluster_id, node_id, service_name,
                                        **kwargs)

    def post_nodes(self, cluster_id, **kwargs):
        """Add new node for cluster identified by `cluster_id`"""

        return self.cluster_api.create_node(cluster_id, **kwargs)

    def delete_nodes(self, cluster_id, *args):

        return self.cluster_api.delete_nodes(cluster_id, *args)

    # APP Associated APIS

    def get_cluster_apps(self, cluster_id, **kwargs):
        """List all apps for speicified cluster"""

        kwargs['cluster_id'] = cluster_id
        return self.app_api.index(**kwargs)

    def create_cluster_apps(self, cluster_id, **kwargs):
        """Create app under speicified cluster"""

        # NOTE(mgniu): `deep copy or shadow copy? i'm confused.
        body = copy.deepcopy(kwargs)

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
            validate(body, schema)
        except (SchemaError, ValidationError):
            raise webob.exc.HTTPBadRequest(explanation="Bad Paramaters")

        return self.app_api.create(cluster_id, body=body)

    def get_cluster_app(self, cluster_id, app_id):
        """List specified app information under specified cluster"""

        return self.app_api.show(cluster_id, app_id)

    def delete_cluster_app(self, cluster_id, app_id):
        """Delete speicified app under specified cluster"""

        self.app_api.delete(cluster_id, app_id)

    def get_user_apps(self, **kwargs):
        """List all apps belong to specified user."""

        return self.app_api.index(**kwargs)


    def get_user_apps_status(self):
        """
        APP_STATUS_MAPPING = {
             '1': "部署中",
             '2': "运行中",
             '3': "已停止",
             '4': "停止中 ",
             '5': "删除中",
             '6': "扩展中",
             '7': "启动中",
             '8': "撤销中",
             '9': "失联",
             '10': "异常"
         }
         """
        return self.app_api.status()

    def get_app_versions(self, cluster_id, app_id):
        """Get app's histroy versions."""

        #try:
        #    return GET(self.client.clusters[cluster_id].apps[app_id].versions)
        #except BeanBagException as exc:
        #    raise OmegaException(message=exc.msg, status_code=exc.response.status_code)
        return self.app_api.versions(cluster_id, app_id)

    def delete_app_version(self, cluster_id, app_id, version_id):
        """Delete app version according `cluster_id` `app_id` and `version_id`."""

        #try:
        #    return DELETE(self.client.clusters[cluster_id].apps[app_id].versions[version_id])
        #except BeanBagException as exc:
        #    raise OmegaException(message=exc.msg, status_code=exc.response.status_code)
        return self.app_api.delete(cluster_id, app_id, version_id)

    def update_cluster_app(self, cluster_id, app_id, **kwargs):
        """Update app's status"""

        #try:
        #    return PATCH(self.client.clusters[cluster_id].apps[app_id], kwargs)
        #except BeanBagException as exc:
        #    raise OmegaException(message=exc.msg, status_code=exc.response.status_code)
        self.app_api.update(cluster_id, app_id, **kwargs)

    def get_app_instances(self, cluster_id, app_id):
        """Get all instances belong to the app"""

        return self.app_api.instancs(cluster_id, app_id)

    def get_app_events(self, cluster_id, app_id, **kwargs):
        """
        Get app events total `page` pages perpage `per_page` entries.
        For example get the first two page and 50 items perpage.
        """
        return self.app_api.events(cluster_id, app_id)

    def get_projects(self):
        """List all projects(images) for user."""
        return self.http.get("/projects")

    # Project Associated APIS

    def create_project(self, uid, project_name, image_name, desc,
                             repo, branch, active, period, trigger_type):
        """Create new project.

        :param uid: user id
        :param project_name: project name the image belong to
        :param image_name: image name to build
        :param desc: image description 
        :param repo: the repository url contains the Dockerfile for building
        :param branch: the repository's branch. eg. master.
        :param active: whether switch on the automatic build. true or false.
        :param period: the aotomatic build period. unit is minute.
        :param trigger_type: automatic build conditions. 1 means tag. 2 means branch. 3 means tag and branch.
        """
        body = {
            "uid": uid,
            "name": project_name,
            "imageName": image_name,
            "description": desc,
            "repoUri": repo,
            "branch": branch,
            "active": active,
            "period": period,
            "triggerType": trigger_type,
        }
        schema = {  
            "type": "object",
            "properties": {
                "uid": {"type": "number"},
                "name": {"type": "string"},
                "imageName": {"type": "string"},
                "description": {"type": "string"},
                "repoUri": {"type": "string"},
                "branch": {"type": "string"},
                "active": {"type": "boolean"},
                "period": {"type": "number"},
                "triggerType": {"type": "number"},
            },
            "required": ["uid", "name", "imageName", "description", "repoUri", "branch", "active", "period", "triggerType"]
        }
       
        try:
            validate(body, schema)
        except (SchemaError, ValidationError):
            raise webob.exc.HTTPBadRequest(explanation="Bad Paramaters")

        return self.project_api.create(body=body)

    def delete_project(self, project_id):

        return self.project_api.delete(project_id)

    def get_project(self, project_id):

        return self.project_api.show(project_id) 

    def update_project(self, project_id, uid, active, period, trigger_type):
        """Update project's partial infomation"""
        body = {
            "uid": uid,
            "active": active,
            "period": period,
            "trigger_type": trigger_type
        }
  
        schema = {
            "type": "object",
            "properties": {
                "uid": {"type": "number"},
                "active": {"type": "boolean"},
                "period": {"type": "number"},
                "trigger_type": {"type": "number"},
            },
            "required": ["uid", "active", "period", "trigger_type"]
        }
             
        try:
            validate(body, schema)
        except (SchemaError, ValidationError):
            raise webob.exc.HTTPBadRequest(explanation="Bad Paramaters")

        return self.project_api.update(project_id, body)

    def get_project_builds(self, project_id):
        """List all builds for a project."""

        return self.project_api.builds(project_id)

    def get_project_build_log(self, project_id, build_num, job_id):

        return self.project_api.logs(project_id, build_num, job_id)

    def get_project_build_stream(self, project_id, build_num, job_id):

        return self.project_api.stream(project_id, build_num, job_id)
