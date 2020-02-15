"""
    This file allows for switching between proxy and non-proxy config.
    When working behind a proxy, you can simply configure the
        by editing ONLY THE VALUES for the keys:

         'http': [protocol]://[your-proxy-address]:[port-number]
                                        OR
         'https': [protocol]://[your-proxy-address]:[port-number]

    When you are NOT working behind a proxy, then all is okay. this is the default setting of the ckan-wit
        by editing ONLY THE VALUES for the keys:
         'http': None
            OR
         'https': None
"""


class ProxySetting:
    def __init__(self, ext_http, local_https=None):
        self.http = {'http': ext_http,
                     'https': ext_http}
        self.local_https = local_https

# def proxy_settings():
#     ext_proxy = {
#         'http': 'http://proxy.ciss.de:3128',  # Edit this line if working behind a proxy
#         'https': 'http://proxy.ciss.de:3128'  # Edit this line also if working behind a proxy
#     }
#
#     local_noProxy = {
#         'http': None,
#         'https': None
#     }
#     return ext_proxy, local_noProxy
