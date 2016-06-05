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

from omegaclient.client import HTTPClient
from omegaclient.project import ProjectMixin
from omegaclient.app import AppMixin
from omegaclient.cluster import ClusterMixin
from omegaclient.logs import LogMixin
from omegaclient.alert import AlertMixin
from omegaclient.metrics import MetricsMixin


class OmegaClient(ProjectMixin, AppMixin, ClusterMixin, LogMixin, AlertMixin,
                  MetricsMixin):
    """
    Client for user to use Dataman Cloud.
    """

    def __init__(self, server_url, email, password):

        self.http = HTTPClient(server_url, email, password)

        super(OmegaClient, self).__init__()

    @staticmethod
    def process_data(resp):
        """Processing data response from Omega API."""

        data = resp.json()

        if 'data' in data:
            return data['data']

        return data
