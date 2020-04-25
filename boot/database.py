#!/usr/bin/env python
#
# Copyright 2015-2016 zephyr
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


class DatabaseBoot(object):

    def __init__(self, options=None):
        self.config(options)

    def config(self, options=None):
        options = options or self.options
        with options.group("DB settings") as group:
            group.define('--mysql.db', default='amazsic', help='The database name (default %(default)r)')
            group.define('--mysql.host', default='localhost', help='The host of the database (default %(default)r)')
            group.define('--mysql.user', default='root', help='The user of the database (default %(default)r)')
            group.define('--mysql.passwd', default='amazsic', help='The password of the database (default %(default)r)')
            group.define('--mysql.port', default=3306, help='The port of the database (default %(default)r)', type=int)
