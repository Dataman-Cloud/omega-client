








from omeageclient.utils import url_maker


class AppAPI(object):
    
    def __init__(self, http):
        self.http = http

    def index(self, cluster_id):
        """List all apps"""
        self.http.get(url_maker("/clusters", cluster_id, "apps"))
   
    def show(self, cluster_id, app_id):
        """List specified app"""
        self.http.get(url_maker("/clusters", cluster_id, "apps", app_id))

    def create(self, cluster_id, body):
        """Create new app"""
        self.http.post(url_maker("/clusters", cluster_id, "apps"), body=body) 
