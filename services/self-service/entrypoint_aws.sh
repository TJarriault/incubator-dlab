#!/bin/sh
# *****************************************************************************
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
# ******************************************************************************

/bin/mkdir -p /root/keys

/usr/bin/aws s3 cp s3://${SSN_BUCKET_NAME}/dlab/certs/ssn/ssn.keystore.jks /root/keys/ssn.keystore.jks
/usr/bin/aws s3 cp s3://${SSN_BUCKET_NAME}/dlab/certs/ssn/ssn.crt /root/keys/ssn.crt
/usr/bin/aws s3 cp s3://${SSN_BUCKET_NAME}/dlab/certs/endpoint/endpoint.crt /root/keys/endpoint.crt

/usr/bin/keytool -importcert -trustcacerts -alias dlab -file /root/keys/ssn.crt -noprompt -storepass changeit -keystore /usr/lib/jvm/java-1.8-openjdk/jre/lib/security/cacerts
/usr/bin/keytool -importcert -trustcacerts -file /root/keys/endpoint.crt -noprompt -storepass changeit -keystore /usr/lib/jvm/java-1.8-openjdk/jre/lib/security/cacerts

/usr/bin/java -Xmx1024M -jar -Duser.timezone=UTC -Dfile.encoding=UTF-8 -DDLAB_CONF_DIR=/root/ /root/self-service-2.1.jar server /root/self-service.yml