# -*- coding: utf-8 -*-
"""
File browser UI component.

"""


import urllib.parse
import pprint

import imgui
import imgui.core


# -----------------------------------------------------------------------------
def coro_frontend(inputs, outputs):

    cache = dict()

    while True:

        cache_path = ('media/wtp/Data',)
        url_path   = 'media/wtp/Data'
        url        = urllib.parse.urlunparse(
                                urllib.parse.ParseResult(
                                                scheme   = 'stableflow-file',
                                                netloc   = 'url',
                                                path     = url_path,
                                                params   = None,
                                                query    = None,
                                                fragment = None))

        # outputs['request']['ena'] = True
        # outputs['request']['list'].clear()
        # outputs['request']['list'].append({'id':   url,
        #                                    'url':  url,
        #                                    'path': cache_path})

        (inputs, context) = yield (outputs)

        # pd_cache = stableflow.util.PathDict(cache)

        # if url in inputs['response']:
        #     for item in inputs['response'][url]:
        #         pd_cache[item['path']] = item['url']

        # import pprint
        # pprint.pprint(pd_cache.data)

        # imgui.begin("Data view", True)
        # _ply(cursor = pd_cache.data)
        # imgui.end()


# -----------------------------------------------------------------------------
def coro_backend(request, response):
    """
    """

    PATHSEP_RFC3986 = '/'

    while True:

        (request) = yield (response)

        if not request['ena']:
            continue

        for item in request['list']:

            id_item = item['id']
            url     = urllib.parse.urlsplit(item['url'])
            # if url.scheme == 'stableflow-file':
            path = os.path.join(os.sep, *url.path.split(PATHSEP_RFC3986))

            response[id_item] = list()
            for name in os.listdir(path):
                url = PATHSEP_RFC3986.join((item['url'], name))
                response[id_item].append({
                                    'id':   url,
                                    'url':  url,
                                    'path': (*item['path'], name)})

                # import pprint
                # pprint.pprint(outputs['data'])


# -----------------------------------------------------------------------------
def _ply(cursor):
    """
    """
    for (key, value) in cursor.items():
        if imgui.core.tree_node(key, 0):
            if isinstance(value, str):
                imgui.text(value)
            else:
                _ply(cursor = value)
            imgui.tree_pop()
