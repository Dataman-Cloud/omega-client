# -*- coding: utf-8 -*-

from beanbag.v2 import BeanBag, GET, POST, DELETE, BeanBagException
import requests


BASE_URL = '/api/v3'


class OmegaException(Exception):
    pass


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
        self.client = BeanBag(server_url + BASE_URL, session=self.session)

        token = self.get_token(email, password)
        self.session.headers["Authorization"] = token

    def get_token(self, email, password):
        try:
            return POST(self.client.auth, {'email': email, 'password': password})['data']['token']
        except BeanBagException, e:
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
