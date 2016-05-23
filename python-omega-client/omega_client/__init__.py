# -*- coding: utf-8 -*-

from beanbag.v2 import BeanBag, GET, POST, DELETE, PUT, PATCH, BeanBagException
import requests
from client import HTTPClient 
from jsonschema import SchemaError, ValidationError, validate
import webob


BASE_URL = '/api/v3'


class OmegaException(Exception):
    msg = "A unknown exception occurred."

    def __init__(self, message=None, status_code=None):
        if not message:
            message = msg
        self.status_code = status_code

        super(OmegaException, self).__init__(message)


def check_return_code(function):
    def with_code_check(*args, **kwargs):
        # raise exception when omega get code big than zero;
        try:
            rst = function(*args, **kwargs)
            if 'code' in rst and rst['code'] > 0:
                raise OmegaException("Calls to Omega got unexpected result: %s" % rst)
            return rst
        except Exception as e:
            raise OmegaException(e)

    return with_code_check


class OmegaClient(object):

    def __init__(self, server_url, email, password):
        self.session = requests.session()
        self.client = BeanBag(server_url + BASE_URL, session=self.session, use_attrdict=True)

        token = self.get_token(email, password)
        self.session.headers["Authorization"] = token

        self.http = HTTPClient(server_url + BASE_URL, token)

    def get_token(self, email, password):
        try:
            return POST(self.client.auth, {'email': email, 'password': password})['data']['token']
        except BeanBagException as e:
            raise

    def __call__(self, *args, **kwargs):
        return self.client(*args, **kwargs)

    def __getattr__(self, name):
        return self.client.__getattr__(name)

    def __getitem__(self, *args, **kwargs):
        return self.client.__getitem__(*args, **kwargs)

    @check_return_code
    def get_auth(self):
        return GET(self.client.auth)

    @check_return_code
    def post_auth(self, email, password):
        return POST(self.client.auth, {'email': email, 'password': password})

    @check_return_code
    def get_clusters(self):
        return GET(self.client.clusters)

    @check_return_code
    def post_clusters(self, **kwargs):
        return POST(self.client.clusters, kwargs)

    @check_return_code
    def get_cluster(self, cluster_id):
        return GET(self.client.clusters[cluster_id])

    @check_return_code
    def delete_cluster(self, cluster_id):
        return DELETE(self.client.clusters[cluster_id])

    @check_return_code
    def get_node_identifier(self, cluster_id):
        return GET(self.client.clusters[cluster_id].new_node_identifier)

    @check_return_code
    def get_cluster_apps(self, cluster_id):
        return GET(self.client.clusters[cluster_id].apps)

    @check_return_code
    def post_cluster_apps(self, cluster_id, **kwargs):
        return POST(self.client.clusters[cluster_id].apps, kwargs)

    @check_return_code
    def get_cluster_app(self, cluster_id, app_id):
        return GET(self.client.clusters[cluster_id].apps[app_id])

    @check_return_code
    def delete_cluster_app(self, cluster_id, app_id):
        return DELETE(self.client.clusters[cluster_id].apps[app_id])

    @check_return_code
    def post_nodes(self, cluster_id, **kwargs):
        return POST(self.client.clusters[cluster_id].nodes, kwargs)

    @check_return_code
    def delete_nodes(self, cluster_id, *args):
        return DELETE(self.client.clusters[cluster_id].nodes, args)

    @check_return_code
    def get_user_apps(self, **kwargs):
        return GET(self.client.apps, kwargs)

    @check_return_code
    def get_cluster_matrix(self, cluster_id, **kwargs):
        return GET(self.client.clusters[cluster_id].metrics, kwargs)

    @check_return_code
    def get_user_apps_status(self):
        # APP_STATUS_MAPPING = {
        #     '1': "部署中",
        #     '2': "运行中",
        #     '3': "已停止",
        #     '4': "停止中 ",
        #     '5': "删除中",
        #     '6': "扩展中",
        #     '7': "启动中",
        #     '8': "撤销中",
        #     '9': "失联",
        #     '10': "异常"
        # }
        return GET(self.client.apps.status)

    def get_app_versions(self, cluster_id, app_id):
        """Get app's histroy versions."""

        try:
            return GET(self.client.clusters[cluster_id].apps[app_id].versions)
        except BeanBagException as exc:
            raise OmegaException(message=exc.msg, status_code=exc.response.status_code)

    def delete_app_version(self, cluster_id, app_id, version_id):
        """Delete app version according `cluster_id` `app_id` and `version_id`."""

        try:
            return DELETE(self.client.clusters[cluster_id].apps[app_id].versions[version_id])
        except BeanBagException as exc:
            raise OmegaException(message=exc.msg, status_code=exc.response.status_code)

    def update_cluster_app(self, cluster_id, app_id, **kwargs):
        """Update app's status"""

        try:
            return PATCH(self.client.clusters[cluster_id].apps[app_id], kwargs)
        except BeanBagException as exc:
            raise OmegaException(message=exc.msg, status_code=exc.response.status_code)


    def modified_cluster_app(self, cluster_id, app_id, **kwargs):
        """Modified app configuration."""

        try:
            return PUT(self.client.clusters[cluster_id].apps[app_id], kwargs)
        except BeanBagException as exc:
            raise OmegaException(message=exc.msg, status_code=exc.response.status_code)

    def get_app_instance(self, cluster_id, app_id):
        """Get all instances belong to the app"""

        try:
            return GET(self.client.clusters[cluster_id].apps[app_id].tasks)
        except BeanBagException as exc:
            raise OmegaException(message=exc.msg, status_code=exc.response.status_code)

    def get_app_events(self, cluster_id, app_id, **kwargs):
	"""
        Get app events total `page` pages perpage `per_page` entries.
        For example get the first two page and 50 items perpage.
        """
        try:
            return GET(self.client.clusters[cluster_id].apps[app_id].events, kwargs)
        except BeanBagException as exc:
            raise OmegaException(message=exc.msg, status_code=exc.response.status_code)

    def get_projects(self):
        """List all projects(images) for user."""
        return self.http.get("/projects")

    def create_project(self, uid, project_name, image_name,desc,
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

        return self.http.post("/projects", body=body)

    def delete_project(self, project_id):
        return self.http.delete("/projects/{}".format(project_id))

    def get_project(self, project_id):
        return self.http.get("/projects/{}".format(project_id))

    def put_project(self, project_id, uid, active, period, trigger_type):
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

        return self.http.put("/projects/{}".format(project_id), body=body)

    def get_project_builds(self, project_id):
        """List all builds for a project."""
        return self.http.get("/projects/{}/builds".format(project_id)) 

    def get_project_build_log(self, project_id, build_id, job_id):
        return self.http.get("/projects/{}/builds/{}/{}/logs".format(project_id,build_id,job_id))

    def get_project_build_stream(self, project_id, build_id, job_id):
        return self.http.get("/projects/{}/builds/{}/{}/logs".format(project_id,build_id,job_id))
