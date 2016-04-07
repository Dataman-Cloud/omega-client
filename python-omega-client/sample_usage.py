# coding: utf-8
from omega_client import OmegaClient

clt = OmegaClient('http://offlineforward.dataman-inc.net', 'admin@shurenyun.com', 'Dataman1234')

print clt.get_clusters()
print clt.get_cluster(630)
print clt.get_node_identifier(630)
print clt.post_nodes(630, id='83ec44c13e2a482aa4645713d3857ff6', name='test_node')
print clt.get_apps(630)
print clt.get_app(627, 750)
