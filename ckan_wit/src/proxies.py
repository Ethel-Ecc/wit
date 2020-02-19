"""
    This file allows for switching between proxy and non-proxy config.
    When working behind a proxy, you can simply configure the environmental variables of your system
        by using these variables as keys

         HTTP_PROXY=[protocol]://[your-proxy-address]:[port-number]
                                        OR
         HTTPS_PROXY=[protocol]://[your-proxy-address]:[port-number]

"""
import os


class ProxySetting:
    http_proxy = os.environ['HTTP_PROXY']
    https_proxy = os.environ['HTTPS_PROXY']

    def __init__(self, http_proxy=http_proxy, https_proxy=https_proxy):
        self.http_proxy = http_proxy
        self.https_proxy = https_proxy


