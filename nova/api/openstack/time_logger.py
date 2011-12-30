# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""Utility that returns the api response time in response header"""
import time
import webob.dec

from nova import wsgi


class TimeLogger(wsgi.Middleware):
    """Helper class for measuring API performance.

    Can be inserted into any WSGI application chain to return the api response
    time in response header.
    """

    @classmethod
    def factory(cls, global_config, **local_config):
        def _factory(app):
            return cls(app, **local_config)
        return _factory

    def __init__(self, application, **kwargs):
        self.application = application

    @webob.dec.wsgify
    def __call__(self, req):

        start_time = time.time()
        resp = req.get_response(self.application)
        end_time = time.time()

        resp.headers['response_time'] = str("%.3f" % (end_time - start_time))
        return resp
