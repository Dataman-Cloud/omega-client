import unittest
import pprint
from __init__ import OmegaClient



class OmegaClientTest(unittest.TestCase):

    def setUp(self):
        self.client = OmegaClient('http://devforward.dataman-inc.net',
                                  'mgniu@dataman-inc.com', 'do-not-tell-you')
        self.pp = pprint.PrettyPrinter(indent=4)

    def tearDown(self):
        pass

    def test_get_clusters(self):
        self.pp.pprint(self.client.get_clusters())

    def test_get_cluster(self):
        self.client.get_cluster(695)

    def test_delete_cluster(self):
        self.client.delete_cluster(695)
     
    def test_post_clusters(self):
        self.client.post_clusters(name='test', clusterType='1_master')

    def test_get_node_identifier(self):
        self.pp.pprint(self.client.get_node_identifier(698))

    def test_get_cluster_apps(self):
        self.pp.pprint(self.client.get_cluster_apps(699))

    def test_get_cluster_app(self):
        self.client.get_cluster_app(695, 1001)

    def test_post_cluster_apps(self):
        pass

    def test_delete_cluster_app(self):
        pass

    def test_post_nodes(self):
        pass

    def test_delete_nodes(self):
        pass

    def test_get_user_apps(self):
        pass

    def test_get_user_apps_status(self):
        pass

    def test_get_app_version(self):
        self.pp.pprint(self.client.get_app_versions(699, 967)) 

    def test_delete_app_version(self):
        self.client.delete_app_version(699,967,1133)

    def test_update_cluster_app(self):
        self.client.update_cluster_app(699,967,method="stop")

    def test_modified_cluster_app(self):
        self.client.modified_cluster_app(699,967,mem=32)

    def test_get_app_instance(self):
        self.pp.pprint(self.client.get_app_instance(699,967))
   
    def test_get_app_events(self):
        self.pp.pprint(self.client.get_app_events(699,967,page=1))
    
if __name__ =='__main__':
    unittest.main()
