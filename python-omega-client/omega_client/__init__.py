from beanbag.v2 import BeanBag, GET, POST, DELETE, BeanBagException
import requests


BASE_URL = '/api/v3'


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

    def get_auth(self):
        return GET(self.client.auth)

    def post_auth(self, email, password):
        return POST(self.client.auth, {'email': email, 'password': password})

    def get_clusters(self):
        return GET(self.client.clusters)

    def post_clusters(self, **kwargs):
        return POST(self.client.clusters, kwargs)

    def get_cluster(self, cluster_id):
        return GET(self.client.clusters[cluster_id])

    def delete_cluster(self, cluster_id):
        return DELETE(self.client.clusters[cluster_id])

    def get_node_identifier(self, cluster_id):
        return GET(self.client.clusters[cluster_id].new_node_identifier)

    def get_apps(self, cluster_id):
        return GET(self.client.clusters[cluster_id].apps)

    def post_apps(self, cluster_id, **kwargs):
        return POST(self.client.clusters[cluster_id].apps, kwargs)

    def get_app(self, cluster_id, app_id):
        return GET(self.client.clusters[cluster_id].apps[app_id])

    def delete_app(self, cluster_id, app_id):
        return DELETE(self.client.clusters[cluster_id].apps[app_id])

    def post_nodes(self, cluster_id, **kwargs):
        return POST(self.client.clusters[cluster_id].nodes, kwargs)

    def delete_nodes(self, cluster_id, *args):
        return DELETE(self.client.clusters[cluster_id].nodes, args)
