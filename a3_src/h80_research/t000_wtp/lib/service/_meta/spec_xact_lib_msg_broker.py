# -*- coding: utf-8 -*-
"""
Functional specification for the xact messaging system data broker.

"""


import xact.lib.test.component
import xact.cli.util


# =============================================================================
class SpecifyBroker:
    """
    Spec for broker module.

    """

    #--------------------------------------------------------------------------
    def it_forwards_messages_to_the_specified_ports(self):
        """
        Request and response forwarding to specified producers and consumers.

        """
        cfg = xact.lib.test.component.scripted(
            module = 'xact.lib.service.broker',
            config = dict(),
            script = [
                {

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'offer',
                                      '_spec': ('multi','a','b'),
                                      '_node': 'producer_b'}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'offer',
                                      '_spec': ('multi','c','d'),
                                      '_node': 'producer_a'}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_id':   1,
                                      '_spec': {'foo': ('multi','a','b'),
                                                'bar': ('multi','c','d')},
                                      '_node': 'consumer_a'}]}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_spec': ('multi','c','d'),
                                      '_node': 'consumer_a'}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_spec': ('multi','a','b'),
                                      '_node': 'consumer_a'}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('multi','c','d'),
                                      'value': 100}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('multi','a','b'),
                                      'value': 200}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  True,
                            'list': [{ 'foo':   { 'value': 200 },
                                       'bar':   { 'value': 100 }}]},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('multi','c','d'),
                                      'value': 101}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('multi','a','b'),
                                      'value': 201}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  True,
                            'list': [{ 'foo':   { 'value': 201 },
                                       'bar':   { 'value': 101 } }]},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                }])

        xact.cli.util.run_test(cfg,
                               expected_exit_code = 0,
                               do_expect_stdout   = False,
                               do_expect_stderr   = False)


    #--------------------------------------------------------------------------
    def it_handles_wildcards(self):
        """
        Request and response forwarding to specified producers and consumers.

        """
        cfg = xact.lib.test.component.scripted(
            module = 'xact.lib.service.broker',
            config = dict(),
            script = [
                {

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'offer',
                                      '_spec': ('boat1', '*'),
                                      '_node': 'producer_b'}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'offer',
                                      '_spec': ('boat2', '*'),
                                      '_node': 'producer_a'}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_id':   1,
                                      '_spec': {'rpm':  ('*','engine','rpm'),
                                               'temp': ('*','engine','temp')},
                                      '_node': 'consumer_a'}]}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_spec': ('*','engine','temp'),
                                      '_node': 'consumer_a'},
                                     {'_type': 'request',
                                      '_spec': ('*','engine','rpm'),
                                      '_node': 'consumer_a'}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_spec': ('*','engine','temp'),
                                      '_node': 'consumer_a'},
                                     {'_type': 'request',
                                      '_spec': ('*','engine','rpm'),
                                      '_node': 'consumer_a'}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('boat2','engine','rpm'),
                                      'value': 100}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('boat1','engine','temp'),
                                      'value': 200}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  True,
                            'list': [{ 'temp': { 'value': 200 },
                                       'rpm':  { 'value': 100 } }]},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                }])

        xact.cli.util.run_test(cfg,
                               expected_exit_code = 0,
                               do_expect_stdout   = False,
                               do_expect_stderr   = False)


    #--------------------------------------------------------------------------
    def it_handles_elementary_request_specs(self):
        """
        Handling of requests that consist only of elementary specs.

        """
        cfg = xact.lib.test.component.scripted(
            module = 'xact.lib.service.broker',
            config = dict(),
            script = [
                {

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'offer',
                                      '_spec': ('boat1', '*'),
                                      '_node': 'producer_b'}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'offer',
                                      '_spec': ('boat2', '*'),
                                      '_node': 'producer_a'}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_id':   1,
                                      '_spec': ('*','engine','rpm'),
                                      '_node': 'consumer_a'}]}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_spec': ('*','engine','rpm'),
                                      '_node': 'consumer_a'}]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'request',
                                      '_spec': ('*','engine','rpm'),
                                      '_node': 'consumer_a'}]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                },{

                    'in':  {
                        'producer_a': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('boat2','engine','rpm'),
                                      'value': 100 }]},
                        'producer_b': {
                            'ena':  True,
                            'list': [{'_type': 'response',
                                      '_spec': ('boat1','engine','temp'),
                                      'value': 200 }]},
                        'consumer_a': {
                            'ena':  False,
                            'list': []},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    },
                    'out': {
                        'producer_a': {
                            'ena':  False,
                            'list': []},
                        'producer_b': {
                            'ena':  False,
                            'list': []},
                        'consumer_a': {
                            'ena':  True,
                            'list': [{ 'value': 100 }]},
                        'consumer_b': {
                            'ena':  False,
                            'list': []}
                    }

                }])

        xact.cli.util.run_test(cfg,
                               expected_exit_code = 0,
                               do_expect_stdout   = False,
                               do_expect_stderr   = False)


