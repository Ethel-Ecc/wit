
"""
    This file allows for switching between proxy and non-proxy config.

    When working behind a proxy, you can simply configure the
    :param - ext_proxy
        by editing ONLY THE VALUES for the keys:

         'http': [protocol]://[your-proxy-address]:[port-number]
                                        OR
         'https': [protocol]://[your-proxy-address]:[port-number]

    When you are NOT working behind a proxy, then all is okay. this is the default setting of the ckan-wit
    :param - local_noProxy
        by editing ONLY THE VALUES for the keys:
         'http': None
            OR
         'https': None
"""


def proxy_settings():
    ext_proxy = {
        'http': 'http://proxy.ciss.de:3128',  # Edit this line if working behind a proxy
        'https': 'http://proxy.ciss.de:3128'  # Edit this line also if working behind a proxy
    }

    local_noProxy = {
        'http': None,
        'https': None
    }

    return local_noProxy['https']