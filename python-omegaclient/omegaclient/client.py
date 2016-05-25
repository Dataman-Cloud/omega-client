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
import json

API_VERSION = "/api/v3"


class HTTPClient(object):
    """Http client for send http requests"""

    def __init__(self, server_url, email, password):
        self._base_url = "{}/{}".format(server_url, API_VERSION)
        self._email = email
        self._password = password
        self._token = self.get_token()
        self._session = None
        self.timeout = 86400

    def get_session(self):
        """Get request session"""

        if not self._session:
            self._session = requests.Session()
        return self._session

    def get_token(self):
        """Get user auth token"""

        resp = self.post("/auth", data={'email': self._email,
                                        'password': self._password})

        return resp.json()['data']['token']

    def request(self, url, method, **kwargs):
        """Send request"""

        kwargs.setdefault('headers', kwargs.get('headers', {}))
        kwargs['headers']['User-Agent'] = "API-CLIENT"
        kwargs['headers']['Accept'] = 'application/json'
        kwargs['headers']['Authorization'] = self._token

        if 'data' in kwargs:
            kwargs['headers']['Content-Type'] = 'application/json'
            kwargs['data'] = json.dumps(kwargs['data'])

        if 'param' in kwargs:
            kwargs['params'] = json.dumps(kwargs['params'])

        if self.timeout is not None:
            kwargs.setdefault('timeout', self.timeout)

        with self.get_session() as session:
            resp = session.request(method, self._base_url + url, **kwargs)

        return resp

    def get(self, url, **kwargs):
        """Send a GET request. Returns :class:`requests.Response` object"""

        return self.request(url, 'GET', **kwargs)

    def post(self, url, **kwargs):
        """Send a POST request. Returns :class:`requests.Response` object"""

        return self.request(url, 'POST', **kwargs)

    def options(self, url, **kwargs):
        """Send a OPTIONS request. Returns :class:`requests.Response` object"""

        raise NotImplementedError()

    def put(self, url, data=None, **kwargs):
        """Send a PUT request. Returns :class:`requests.Response` object"""

        return self.request(url, 'PUT', data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """Send a PATCH request. Returns :class:`requests.Response` object"""

        return self.request(url, 'PATCH', data=data, **kwargs)

    def delete(self, url, **kwargs):
        """Send a DELETE request. Returns :class:`requests.Response` object"""

        return self.request(url, 'DELETE', **kwargs)
