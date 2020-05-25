#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    七牛云 > SSL证书服务 > 更新自有证书
"""

import qiniu
from qiniu import DomainManager
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    filename='/var/log/qiniu/update_sslcert.log',
                    filemode='a')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)

# 配置七牛云的AK/SK
access_key = '*****************************'
secret_key = '*****************************'

auth = qiniu.Auth(access_key=access_key, secret_key=secret_key)
domain_manager = DomainManager(auth)

# 配置域名名称
domain_name = 'yourdomain.com'
privatekey = "/etc/letsencrypt/live/%s/privkey.pem" % domain_name
ca = "/etc/letsencrypt/live/%s/fullchain.pem" % domain_name

with open(privatekey, 'r') as f:
    privatekey_str = f.read()

with open(ca, 'r') as f:
    ca_str = f.read()

ret, info = domain_manager.create_sslcert(
    domain_name, domain_name, privatekey_str, ca_str)
logging.info('Post sslcert: %s' % ret['certID'])
logging.info(info)

ret, info = domain_manager.put_httpsconf('.' + domain_name, ret['certID'], False)
logging.info(info)

