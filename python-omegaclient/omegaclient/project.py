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

from omegaclient.utils import url_maker

class ProjectAPI(object):
    """Project controllers for response projects apis."""

    prefix = "/projects"

    def __init__(self, http):
        self.http = http

    def index(self):
        """list all projects."""
        return self.http.get(self.prefix)

    def show(self, id):
        """show project details."""
        return self.http.get(url_maker(self.prefix, id))

    def create(self, body):
        """create new project."""
        return self.http.post(self.prefix, data=body)

    def update(self, id, body):
        """update project information."""
        return self.http.patch(url_maker(self.prefix, id), data=body)

    def delete(self, id):
        """delete project"""
        return self.http.delete(url_maker(self.prefix, id))

    def builds(self, id):
        """list all builds for project"""
        return self.http.get(url_maker(self.prefix, id, "builds"))

    def logs(self, id, build_num, job_id):
        """list all build logs for project"""
        return self.http.get(url_maker(self.prefix, id, "builds",
                                       build_num, job_id))

    def stream(self, id, build_num, job_id):
        """list all build text stream for project"""
        return self.http.get(url_maker(self.prefix, id, "builds",
                                       build_num, job_id))
