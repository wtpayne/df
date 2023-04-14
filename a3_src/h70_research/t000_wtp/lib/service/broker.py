# -*- coding: utf-8 -*-
"""
Xact service broker component.

The service broker component is a part of the xact
services infrastructure. The broker acts as an
intermediary between service providers and their
clients.

It matches offers from service providers with
requests from clients, whilst also forwarding and
reformatting messages as required.


Services and the hierarchical resource namespace.
-------------------------------------------------

A service can provide clients with the ability to
subscribe to data from sensors or other parts of
the system. They can also provide clients with the
ability to exert control over effectors, system
outputs, or parts of the system state.

Data sets and controls are all treated as system
"resources", and they are each distinguished from
one another by giving them distinct names in a
hierarchical resource namespace, the structure of
which will be specific to each system or
application.

Using an autonomous fleet as an example, the
engine rev counter for a particular engine on a
particular autonomous boat could be given by
the path:-

    'boat', '01', 'engine', '01', 'data', 'rev_counter'

Similarly, the throttle control on that same
boat can also be given a similar path:-

    'boat', '01', 'engine', '01', 'control', 'throttle'

The set of all resources for that engine can then
be represented by a wildcard:-

    'boat', '01', 'engine', '01', '*'

In this way, each application can organize its
resources in the most appropriate manner,
enabling service clients to access the data and
exert the control that they require.


Offers, requests and responses.
-------------------------------

Service providers may send "offer" messages to the
broker as a way of declaring which resources they
provide access to. Each offer message simply
specifies some subset of the resource namespace
using wildcards. Using the example above, a
service providing data (but no control) for all
engines on boat_01 might use the following
service specification in it's offer message:-

    'boat', '01', 'engine', '*', 'data', '*'

In a similar manner, service clients may send
"request" messages to either obtain data from
some data source, or to attempt to control some
effector. For example, a service client that
is interested in all engine rev counters for
all boats might use the following service
specification in it's request message:-

    'boat', '*', 'engine', '*', 'data', 'rev_counter'

Similarly, a request might be made to set the
throttle of all boats to zero:-

    'boat', '*', 'engine', '*', 'control', 'throttle', 'set', 0'


Matching of offers and requests.
--------------------------------

An offer and a request are said to match if the
parts of the namespace specified by the offer and
the parts of the namespace specified by the
request overlap. (i.e. the intersection between
the two sets is non-empty).

For each request received, the broker will forward
it to all service providers with at least one
matching offer.

After a service provider receives a request, it is
expected to respond with one or more "response"
messages, as appropriate for the resources
specified in the request.

The broker is then responsible for collating and
forwarding the response messages to all service
clients with matching requests.


provider              broker               client
========              ======               ======
   |                    |                    |
   x --> offer -------> x                    |
   |                    x <-- request <----- x
   x <-- request <----- x                    |
   |                    |                    |
   x --> response_1 --> x                    |
   |                    x --> response_1 --> x
   |                    |                    |
   x --> response_2 --> x                    |
   |                    x --> response_2 --> x
   |                    |                    |
   x --> response_3 --> x                    |
   |                    x --> response_3 --> x
   |                    |                    |

        ... and so on ...

It is also possible for the service client to send
its request to the broker before the broker
receives any matching offer. The broker stores
all of the distinct requests that it receives for
some period of time, and it will forward the
request to a service provider upon receipt of a
matching offer.

Response data can be a single value, a finite
collection of values, or some indeterminately
long stream of values (or collections of values).
This means that the offer-request-response pattern
can be used to query one or more databases; to
subscribe to one or more topics from some pub/sub
system, to issue a command, or some mix of the
above.


Hierarchies in the global namespace
-----------------------------------

In order for requests and offers to be matched
with one another, we must necessarily be able to
give names to the sets of data that we want to
match.

By organizing these names hierarchically in some
tree-structured namespace, we can mitigate the
risk of name collisions while also allowing data
to be organized and grouped according to whatever
application-specific criteria are deemed necessary
or appropriate.

It is likely that any sufficiently complex
application will have multiple alternative
organizational schemes in use. In cases like this,
the topmost division of the namespace can be used
to separate the various naming schemes that are
in use.

For example, we might have a maritime autonomy
application where data can be given names either
according to some physical decomposition of the
system, or alternatively according to some
unstructured (flat) collection of ad-hoc tags.

  phy:
    boat1:
      propulsion:
        engine1:
          rpm
    boat2:
      ...

  tag:
    #missionParams
    #safety

Although each name will refer to only
a single specific set of data, any
particular set of data may be referred
to by more than one name at a time.

Names can refer to a single value, a
collection of values, or a series of
such values or collections.


Elementary data set specifications.
-----------------------------------

When an offer message or a request
message specifies some set of data,
it is specifying some subset of the
global namespace. Each set of data
is specified using a path-like data
structure  which we call a "data set
specification".

In it's simplest form, a data set
specification consists of a single
ordered sequence of tokens, where each
token can be a string or a number.
This is termed an "elementary data set
specification", and in Python, it is
represented as a tuple.

  ('phy', 'boat1', 'propulsion', 'engine1', 'rpm')

An elementary data set specification
can be seen as an xpath-like expression
that selects some set of branches and
leaves in our namespace tree.

For example, to select engine1 RPM for
all boats in our fleet, we might use
the following specification:-

  ('phy', '*', 'propulsion', 'engine1', 'rpm')

Alternatively, to select all data
available for boat1, we might use:-

  ('phy', 'boat1', '*')

This is heavily inspired by xpath, and
works in much the same way.


Compound data set specifications.
---------------------------------

Whilst the hierarchical structure of the global
namespace does provide us with the ability to
organize our data in various ways, it is quite
normal for each serice client to have it's own
particular requirements on how the data items
that it consumes should be structured.

It is therefore desirable for service clients to
be able to specify the structure and organization
of the data that they receive.

To support this use-case, we introduce the concept
of a "compound data set specification", which is
merely a collection of elementary data set
specifications organized as the leaves of a tree
of nested dictionaries.

For example, the following compound data set
specification will select the engine RPM and
temperature of all of the boats in the system:-

  {
    '{VEHICLE}': {
      'rpm': ('phy', '{*:VEHICLE}', 'propulsion', 'engine1', 'rpm'),
      'tmp': ('phy', '{*:VEHICLE}', 'propulsion', 'engine1', 'temperature_c')
    }
  }

And the data recieved in response will reflect
both the requested structure and the wildcarded
keys in each elementary data specification.

  { 'boat1': { 'rpm':  0.0,
               'tmp': 45.0 },
    'boat2': { 'rpm':  0.0,
               'tmp': 47.5 } }

TODO: THINK ABOUT HOW QUERIES/VARIABLES
      WILL WORK


Database queries.
-----------------

path1.path2.query

Can be used to write as well as read databases --
the message-brokerage system essentially acts
like a fancy connection string.


Implicit join.
--------------

Timeseries objects - joined on time/simulation step????

Should we look for other natural joins too?
Can queries/requests specify some join?


Conditions and triggers.
------------------------

Service client: condition


Data transforms.
----------------

y = f(x)

"""


import collections
import pickle

import xact.util
import xact.lib.service.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Service broker coroutine.

    """

    signal       = None
    set_id_inout = xact.lib.service.util.get_inout_ids(inputs, outputs)
    xact.lib.service.util.reset_outputs(
                            set_id_port = set_id_inout,
                            outputs     = outputs)

    ddict        = collections.defaultdict
    ddict_list   = lambda: ddict(list)
    ddict_set    = lambda: ddict(set)
    map_template = ddict_set()   # Compound spec template
    map_offer    = ddict_set()   # Service offer.
    map_request  = ddict_set()   # Service request (elementary spec -> node)

    # Remember the set of requests already made
    set_requested = set()

    while True:

        inputs = yield (outputs, signal)

        xact.lib.service.util.reset_outputs(
                            set_id_port  = set_id_inout,
                            outputs      = outputs)

        if cfg['do_validate']:
            _validate_inputs(set_id_port = set_id_inout,
                             inputs      = inputs)

        (map_response,
         has_offer_change,
         has_request_change) = _group_messages_by_type(
                            set_id_port   = set_id_inout,
                            inputs        = inputs,
                            map_template  = map_template,
                            map_offer     = map_offer,
                            map_request   = map_request)

        map_route = _match_offers_and_requests(
                            map_offer     = map_offer,
                            map_request   = map_request)

        map_match = _match_responses_and_requests(
                            map_response  = map_response,
                            map_route     = map_route)

        map_compiled = _assemble_compound_messages(
                            map_match     = map_match,
                            map_template  = map_template)

        _forward_requests_to_services(
                            map_route     = map_route,
                            set_requested = set_requested,
                            outputs       = outputs)

        _forward_responses_to_clients(
                            map_compiled  = map_compiled,
                            outputs       = outputs)


# -----------------------------------------------------------------------------
def _validate_inputs(set_id_port, inputs):
    """
    Raise a RuntimeError if any of the input messages are invalid.

    """
    for (id_port, msg) in xact.lib.service.util.iter_msg(set_id_port, inputs):

        if '_spec' not in msg.keys():
            raise RuntimeError('No _spec field in message: ' + repr(msg))

        if '_node' not in msg.keys():
            raise RuntimeError('No _node field in message: ' + repr(msg))


# -----------------------------------------------------------------------------
def _group_messages_by_type(set_id_port,
                            inputs,
                            map_template,
                            map_offer,
                            map_request):
    """
    Group messages into offer, request and response sets.

    For each of the input ports specified by
    set_id_port, read all available messages and
    group them into offer, request and response
    (all other message type) sets.

    map_offer maps from elementary data set
    specification to a set of service provider
    node identifiers.

    map_request maps from an elementary data
    set specification to a set of service client
    node identifiers.

    map_template maps from a pair of identifiers
    (The specified node id, and the elementary
    spec). to a set of pairs (the message ID and
    the path in the template).

    map_response maps from the service provider
    node identifier to a list of response
    messages.

    """
    map_response       = collections.defaultdict(list)
    has_offer_change   = False
    has_request_change = False

    for (id_port, msg) in xact.lib.service.util.iter_msg(set_id_port, inputs):

        try:
            if msg['_type'] == 'offer':
                if _add_offer_to_map(msg, map_offer):
                    has_offer_change = True

            elif msg['_type'] == 'request':
                if _add_request_to_map(msg          = msg,
                                       map_request  = map_request,
                                       map_template = map_template):
                    has_request_change = True

            else:
                map_response[id_port].append(msg)

        except KeyError:
            map_response[id_port].append(msg)


    return (map_response, has_offer_change, has_request_change)


# -----------------------------------------------------------------------------
def _add_offer_to_map(msg, map_offer):
    """
    Add an offer message to map_offer.

    """
    spec = msg['_spec']
    node = msg['_node']
    has_change = ((spec not in map_offer) or (node not in map_offer[spec]))
    if has_change:
        map_offer[spec].add(node)

    return has_change


# -----------------------------------------------------------------------------
def _add_request_to_map(msg, map_request, map_template):
    """
    Add a request message to map_request and map_template.

    """
    spec = msg['_spec']
    node = msg['_node']

    if isinstance(spec, tuple):
        has_change = (    (spec not in map_request)
                       or (node not in map_request[spec]))
        if has_change:
            map_request[spec].add(node)
            map_template[(node, spec)].add((None, None))


    elif isinstance(spec, dict):

        has_change = False

        for pair in xact.lib.service.util.iter_elementary_spec(
                                                        spec_compound = spec):
            (path_template, spec_elementary) = pair

            if (    (spec_elementary not in map_request)
                 or (node not in map_request[spec_elementary])):

                has_change = True
                map_request[spec_elementary].add(node)
                map_template[(node, spec_elementary)].add(
                                                (msg['_id'], path_template))

    else:
        has_change = False
        raise RuntimeError('Could not determine type of spec: ' + repr(spec))

    return has_change


# -----------------------------------------------------------------------------
def _match_offers_and_requests(map_offer, map_request):
    """
    Return a map of id_provider to spec to set(id_client).

    This will be replaced with a more efficient
    algorithm in due course.

    """
    map_route = collections.defaultdict(lambda: collections.defaultdict(set))

    for (spec_offer, set_id_provider) in map_offer.items():

        for (spec_request, set_id_client) in map_request.items():

            if not xact.lib.service.util.is_match(spec_offer, spec_request):
                continue

            for id_provider in set_id_provider:
                for id_client in set_id_client:
                    map_route[id_provider][spec_request].add(id_client)

    return map_route


# -----------------------------------------------------------------------------
def _match_responses_and_requests(map_response, map_route):
    """
    Match responses to requests.

    """
    map_match = collections.defaultdict(list)

    for (id_provider, msg_response) in _iter_response(map_response):

        for (spec_request, set_id_out) in map_route[id_provider].items():
            if not xact.lib.service.util.is_match(
                                    spec_request, msg_response['_spec']):
                continue

            for id_out in set_id_out:
                map_match[id_out].append((spec_request, msg_response))

    return map_match


# -----------------------------------------------------------------------------
def _iter_response(map_response):
    """
    Yield (id_provider, response) pairs in map_response

    """
    for (id_provider, list_msg_response) in map_response.items():
        for msg_response in list_msg_response:
            yield (id_provider, msg_response)


# -----------------------------------------------------------------------------
def _assemble_compound_messages(map_match, map_template):
    """
    Assemble compound messages ready to be output.

    map_match    -- map from output port id to a list
                    of (spec_request, msg_response)
                    pairs.

    map_template -- map from the pair (id_out,
                    spec_request) to

    """
    map_compiled       = collections.defaultdict(xact.util.PathDict)
    tup_filter_routing = ('_id', '_type', '_node', '_spec')
    tup_filter_none    = tuple()

    id_msg_auto   = 0

    for (id_out, spec_request, msg_response) in _iter_match(map_match):

        for (id_msg, path_output) in map_template[(id_out, spec_request)]:

            if id_msg is None:
                id_msg_auto = id_msg_auto + 1
                id_msg      = str(id_msg_auto)
            key_msg = (id_out, id_msg)

            is_elementary = path_output is None
            if is_elementary:
                tup_filter = tup_filter_none
            else:
                tup_filter = tup_filter_routing

            payload = dict()
            for (key, value) in msg_response.items():
                if key not in tup_filter:
                    payload[key] = value

            if path_output is None:
                map_compiled[key_msg] = payload
            else:
                map_compiled[key_msg][path_output] = payload

    return map_compiled


# -----------------------------------------------------------------------------
def _iter_match(map_match):
    """
    Yield all response messages in map_match.

    Each response is yielded as a triple (id_out,
    spec_requet, msg_response).

    """
    for (id_out, list_response) in map_match.items():
        for (spec_request, msg_response) in list_response:
            yield (id_out, spec_request, msg_response)


# -----------------------------------------------------------------------------
def _forward_requests_to_services(map_route, set_requested, outputs):
    """
    Update outputs with requests to the relevant service provider.

    """
    for (id_provider, spec_request, id_client) in _iter_routes(map_route):

        key = (id_provider, spec_request, id_client)
        if key not in set_requested:
            set_requested.add(key)
            outputs[id_provider]['ena'] = True
            outputs[id_provider]['list'].append({
                '_type': 'request',
                '_spec': spec_request,
                '_node': id_client})


# -----------------------------------------------------------------------------
def _iter_routes(map_route):
    """
    Yield id_provider, spec_request, id_client triples from map_route.

    """
    for (id_provider, map_request) in map_route.items():
        for (spec_request, set_id_client) in map_request.items():
            for id_client in set_id_client:
                yield (id_provider, spec_request, id_client)


# -----------------------------------------------------------------------------
def _forward_responses_to_clients(map_compiled, outputs):
    """
    Assign compiled messages to output ports.

    """
    for (key, msg) in map_compiled.items():
        (id_out, id_msg) = key
        outputs[id_out]['ena'] = True
        outputs[id_out]['list'].append(msg)

