# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.discord.client

"""


import inspect
import time

import psutil
import pytest


STR_TOKEN = 'MTExNzg4MzU0MTUxNTE1NzYyNQ.GA5OxH.wB_-NWRVOWZTcTnrEQDewDGkyiIvMthu0XsSfY'


# =============================================================================
class SpecifyFlNetDiscordClient:
    """
    Spec for the fl.net.discord.client module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_net_discord_client(self):
        """
        fl.net.discord.client can be imported.

        """
        import fl.net.discord.client


# =============================================================================
class SpecifyFlNetDiscordClientCoro:
    """
    Spec for the fl.net.discord.client.coro coroutine function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_run(self):
        """
        fl.net.discord.client.coro can be initialized as a generator.

        """
        import fl.net.discord.client

        # client.coro is a generator function, and
        # when we run it it spawns a subprocess.
        #
        proc_child_before = psutil.Process().children()
        client            = fl.net.discord.client.coro({
                                'str_token':       STR_TOKEN,
                                'secs_interval':   0.1,
                                'debug':           False })
        assert inspect.isgenerator(client)
        for _ in range(40):
            time.sleep(0.05)
            proc_child_after = psutil.Process().children()
            if proc_child_after != proc_child_before:
                break
        assert proc_child_after != proc_child_before

        # Sending nothing gets nothing back.
        #
        list_msg_to_bot = []
        list_cmd_to_bot = []

        (list_msg_from_bot,
         list_cmd_from_bot,
         list_log_from_bot) = client.send((list_msg_to_bot,
                                           list_cmd_to_bot))

        assert list_msg_from_bot == []
        assert list_cmd_from_bot == []
        # assert list_log_from_bot == []
