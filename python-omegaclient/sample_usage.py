# coding: utf-8
import sys
import time
from omega_client import OmegaClient
from omega_client import OmegaException

CLT = OmegaClient('http://devforward.dataman-inc.net', 'mgniu@dataman-inc.com', 'Nmg1769815')


### get_clusters
sys.stdout.write('get_clusters')
try:
    clusters = CLT.get_clusters()
    sys.stdout.write('        OK\n')
except OmegaException as exc:
    sys.stdout.write('    {}\n'.format(exc))

time.sleep(0.5)

### get_cluster
sys.stdout.write('get_cluster')
try:
    cluster_id = clusters['data'][0]['id']
    try:
        cluster = CLT.get_cluster(cluster_id)
        sys.stdout.write('        OK\n')
    except OmegaExcepthion as exc:
        sys.stdout.write('        FAILED')
        sys.stdout.write('    {}\n'.format(exc))
except IndexError:
    sys.stdout.write('        OK\n')

### delete_cluster
sys.stdout.write('delete_cluster')
try:
    cluster_id = clusters['data'][0]['id']
    try:
        CLT.delete_cluster(cluster_id)
        sys.stdout.write('        OK\n')
    except OmegaExcepthion as exc:
        sys.stdout.write('        FAILED')
        sys.stdout.write('    {}\n'.format(exc))
except IndexError:
    sys.stdout.write('        OK\n')

### post_clusters
sys.stdout.write('post_clusters')
try:
    CLT.post_clusters(name='test', clusterType='1_master')
    sys.stdout.write('        OK\n')
except OmegaExcepthion as exc:
    sys.stdout.write('        FAILED')
    sys.stdout.write('    {}\n'.format(exc))

### get_cluster_apps
sys.stdout.write('get_cluster_apps')
try:
    cluster_id = clusters['data'][0]['id']
    try:
        apps = CLT.get_cluster_apps(cluster_id)
        sys.stdout.write('        OK\n')
    except OmegaException as exc:
        sys.stdout.write('        FAILED')
        sys.stdout.write('    {}\n'.format(exc))
except IndexError:
    sys.stdout.write('        OK\n')


#print clt.get_node_identifier(630)
#print clt.post_nodes(630, id='83ec44c13e2a482aa4645713d3857ff6', name='test_node')
#print clt.get_apps(630)
#print clt.get_app(627, 750)
