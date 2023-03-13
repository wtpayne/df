# -*- coding: utf-8 -*-
"""
"""


SIDEBAR_WIDTH        = 250
SIDEBAR_WIDGET_WIDTH = 100
INDENT               = 7
NODE_WIDGET_WIDTH    = 80


# =============================================================================
class Model():
    """
    Presentation model for the flow_editor application.

    This contains all the logic for updating the
    gui and for keeping the gui and the underlying
    application model updated.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the Diagram presentation model.

        """
        self.sys  = System(      ctx )
        self.host = HostDict(    ctx )
        self.proc = ProcessDict( ctx )
        self.node = NodeDict(    ctx )
        self.edge = EdgeDict(    ctx )
        self.data = DataDict(    ctx )


# =============================================================================
class System():
    """
    Presentation model of system configuration.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the System presentation model.

        """
        self.ctx = ctx
        self.id  = 'id_system'

    # -------------------------------------------------------------------------
    def set_id(self, id_system):
        """
        Set the system id.

        """
        self.id = id_system


# =============================================================================
class HostDict(dict):
    """
    Dict containing system host configuration presentation models.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the HostDict presentation model.

        """
        self.ctx = ctx

    # -------------------------------------------------------------------------
    def set_count(self, count_new):
        """
        Set a new host count, adding or removing hosts as required.

        """
        _set_count_impl(ctx        = self.ctx,
                        count_old  = len(self),
                        count_new  = count_new,
                        fcn_add    = self.add,
                        fcn_remove = self.remove)

    # -------------------------------------------------------------------------
    def add(self):
        """
        Add a host to the collection.

        """
        host = Host(self.ctx)
        self.__setitem__(host.tag, host)
        for proc in self.ctx.pm.proc.values():
            proc.notify_hosts_updated()

    # -------------------------------------------------------------------------
    def remove(self):
        """
        Remove the most recently added host from the collection.

        """

        # The most recently added host will
        # be the last one in the iterable
        # returned by the keys() method.
        #
        list_host = list(self.values())
        host_last = list_host[-1]
        tag_last  = host_last.tag
        self.pop(tag_last)
        self.ctx.ui.delete_item(host_last.tag)
        del host_last
        for proc in self.ctx.pm.proc.values():
            proc.notify_hosts_updated()


# =============================================================================
class Host():
    """
    Presentation model of system host configuration.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the Host presentation model.

        """
        self.ctx = ctx
        self.tag = ctx.ui.generate_uuid()

        idx                = len(ctx.pm.host)
        self.id            = f'host_{idx:02}'
        self.hostname      = f'hostname_{idx:02}'
        self.portnum_min   = 8090
        self.portnum_max   = 8090
        self.dirpath_log   = '/var/log'
        self.launch_cmd    = './da stableflow'
        self.log_level     = 'INFO'

        ctx.ui.add_collapsing_header(
                    tag           = self.tag,
                    label         = self.id,
                    indent        = INDENT,
                    parent        = 'vp.win.main.side.tab.cfg.host',
                    before        = 'vp.win.main.side.tab.cfg.host.separator')

        ctx.ui.add_input_text(
                    default_value = self.id,
                    label         = f'Host ID',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_id,
                    user_data     = ctx)

        ctx.ui.add_input_text(
                    default_value = self.hostname,
                    label         = f'Hostname',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_hostname,
                    user_data     = ctx)

        ctx.ui.add_input_int(
                    default_value = self.portnum_max,
                    label         = f'Min port number',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_portnum_min,
                    user_data     = ctx)

        ctx.ui.add_input_int(
                    default_value = self.portnum_max,
                    label         = f'Max port number',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_portnum_max,
                    user_data     = ctx)

        ctx.ui.add_input_text(
                    default_value = self.dirpath_log,
                    label         = f'Log directory',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_hostname,
                    user_data     = ctx)

        ctx.ui.add_input_text(
                    default_value = self.launch_cmd,
                    label         = f'Launch cmd',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_hostname,
                    user_data     = ctx)

        ctx.ui.add_input_text(
                    default_value = self.log_level,
                    label         = f'Log level',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_hostname,
                    user_data     = ctx)

    # -------------------------------------------------------------------------
    def set_id(self, sender, app_data, ctx):
        """
        Set the id of the current host.

        """
        self.id = app_data
        self.ctx.ui.configure_item(self.tag, label = self.id)
        for proc in self.ctx.pm.proc.values():
            proc.notify_hosts_updated()

    # -------------------------------------------------------------------------
    def set_hostname(self, sender, app_data, ctx):
        """
        Set the hostname of the current host.

        """
        self.hostname = app_data

    # -------------------------------------------------------------------------
    def set_portnum_min(self, sender, app_data, ctx):
        """
        Set the minimum port number to use on the current host.

        """
        self.portnum_min = app_data

    # -------------------------------------------------------------------------
    def set_portnum_max(self, sender, app_data, ctx):
        """
        Set the maximum port number to use on the current host.

        """
        self.portnum_max = app_data


# =============================================================================
class ProcessDict(dict):
    """
    Dict containing system process configuration presentation models.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the ProcessDict presentation model.

        """
        self.ctx = ctx

    # -------------------------------------------------------------------------
    def set_count(self, count_new):
        """
        Set a new process count, adding or removing processes as required.

        """
        _set_count_impl(ctx        = self.ctx,
                        count_old  = len(self),
                        count_new  = count_new,
                        fcn_add    = self.add,
                        fcn_remove = self.remove)

    # -------------------------------------------------------------------------
    def add(self):
        """
        Add a process to the collection.

        """
        proc = Process(self.ctx)
        self.__setitem__(proc.tag, proc)
        for node in self.ctx.pm.node.values():
            node.notify_processes_updated()

    # -------------------------------------------------------------------------
    def remove(self):
        """
        Remove the most recently added process from the collection.

        """

        # The most recently added process
        # will be the last one in the
        # iterable returned by the keys()
        # method.
        #
        list_proc = list(self.values())
        proc_last = list_proc[-1]
        tag_last  = proc_last.tag
        self.pop(tag_last)
        self.ctx.ui.delete_item(proc_last.tag)
        del proc_last
        for node in self.ctx.pm.node.values():
            node.notify_processes_updated()


# =============================================================================
class Process():
    """
    Presentation model of system process configuration.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the Process presentation model.

        """
        self.ctx = ctx
        self.tag = ctx.ui.generate_uuid()

        idx     = len(ctx.pm.proc)
        self.id = f'proc_{idx:02}'

        assert len(ctx.pm.host) > 0
        self.list_id_host = list((it.id for it in self.ctx.pm.host.values()))
        self.idx_host     = 0
        self.host         = self.list_id_host[self.idx_host]

        ctx.ui.add_collapsing_header(
                    tag           = self.tag,
                    label         = self.id,
                    indent        = INDENT,
                    parent        = 'vp.win.main.side.tab.cfg.proc',
                    before        = 'vp.win.main.side.tab.cfg.proc.separator')

        ctx.ui.add_input_text(
                    default_value = self.id,
                    label         = f'Process ID',
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_id,
                    user_data     = ctx)

        self._tag_host_combo = ctx.ui.add_combo(
                    items         = self.list_id_host,
                    label         = f'Host ID',
                    default_value = self.host,
                    indent        = INDENT,
                    width         = SIDEBAR_WIDGET_WIDTH,
                    parent        = self.tag,
                    callback      = self.set_host,
                    user_data     = ctx)

    # -------------------------------------------------------------------------
    def set_id(self, sender, app_data, ctx):
        """
        Set the id of the current process.

        """
        self.id = app_data
        self.ctx.ui.configure_item(self.tag, label = self.id)
        for node in self.ctx.pm.node.values():
            node.notify_processes_updated()

    # -------------------------------------------------------------------------
    def set_host(self, sender, app_data, ctx):
        """
        Set the host of the current process.

        """
        self.host     = app_data
        self.idx_host = self.list_id_host.index(self.host)

    # -------------------------------------------------------------------------
    def notify_hosts_updated(self):
        """
        Notify the process that the list of hosts has been updated.

        """
        self.list_id_host = list((it.id for it in self.ctx.pm.host.values()))
        self.ctx.ui.configure_item(self._tag_host_combo,
                                   items = self.list_id_host)

        # If the currently configured host
        # had it's ID changed, then we need
        # to update self.host and self.idx_host
        # and the value of the combo box.
        #
        if self.host not in self.list_id_host:

            try:
                self.host = self.list_id_host[self.idx_host]
            except IndexError:
                self.idx_host = 0
                self.host = self.list_id_host[self.idx_host]

            self.ctx.ui.set_value(self._tag_host_combo,
                                  value = self.host)


# =============================================================================
class NodeDict(dict):
    """
    Dict containing system node configuration presentation models.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the NodeDict presentation model.

        """
        self.ctx = ctx

        # We create a special no-op node so that
        # we do not need to check if any nodes
        # are selected each time we want to do
        # something.
        #
        self._NOOP_NODE = Node(ctx = self.ctx, is_noop = True)

    # -------------------------------------------------------------------------
    def selected(self):
        """
        Return the first selected Node or _NOOP_NODE if no nodes are selected.

        """
        list_tag = self.ctx.ui.get_selected_nodes('vp.win.main.nodeeditor')
        if list_tag:
            return self.get(list_tag[0])
        else:
            return self._NOOP_NODE

    # -------------------------------------------------------------------------
    def add(self, pos = None):
        """
        Add a new node to the dict.

        """
        node = Node(self.ctx, pos)
        self.__setitem__(node.tag, node)

    # -------------------------------------------------------------------------
    def update_selected_nodes(self):
        """
        Update nodes which are selected in the nodeeditor.

        """
        self.selected().sync_to_sidebar()


# =============================================================================
class Node():
    """
    Presentation model of system node configuration.

    """
    _SIDEBAR_PREFIX = 'vp.win.main.side.tab.cfg.node'
    _SIDEBAR_TABLE  = (( 'id',         '', True,  ),
                       ( 'proc',       '', True,  ),
                       ( 'func',       '', True,  ),
                       ( 'state',      '', True,  ),
                       ( 'cfg',        '', True,  ),
                       ( 'countin',     0, False, ),
                       ( 'countout',    0, False, ))

    # -------------------------------------------------------------------------
    def __init__(self, ctx, pos = None, is_noop = False):
        """
        Return an instance of the Node presentation model.

        """
        self.ctx = ctx

        # Set default properties for noop node.
        self.is_noop = is_noop
        if self.is_noop:
            self.id              = ''
            self._tag_proc_combo = 'vp.win.main.side.tab.cfg.node.proc'
            self._list_id_proc   = ['']
            self._idx_proc       = 0
            self.proc            = ''
            self.func            = ''
            self.state           = ''
            self.cfg             = ''
            self.countin         = 0
            self.countout        = 0
            return

        self.tag = ctx.ui.generate_uuid()
        idx      = len(ctx.pm.node)
        self.id  = f'node_{idx:02}'

        # Setup initial items list for the proc combo box.
        assert len(ctx.pm.proc) > 0
        self._tag_proc_combo = 'vp.win.main.side.tab.cfg.node.proc'
        self._list_id_proc   = list((it.id for it in self.ctx.pm.proc.values()))
        self._idx_proc       = 0
        self.proc            = self._list_id_proc[self._idx_proc]
        self.ctx.ui.configure_item(self._tag_proc_combo,
                                   items = self._list_id_proc)

        # Simple attributes.
        #
        self.func  = '_spec::noop'
        self.state = 'dict'
        self.cfg   = '{}'

        self.list_input  = []
        self.list_output = []

        if pos is None:
            pos = [0, 0]

        self.ctx.ui.add_node(
                label  = self.id,
                pos    = pos,
                tag    = self.tag,
                parent = 'vp.win.main.nodeeditor')

    # -------------------------------------------------------------------------
    def set_id(self, str_id):
        """
        Set the node id.

        """
        if self.is_noop:
            return
        self.id = str_id
        self.sync_to_nodeeditor()

    # -------------------------------------------------------------------------
    def set_proc(self, str_proc):
        """
        Set the node process.

        """
        if self.is_noop:
            return
        self.proc     = str_proc
        self._idx_proc = self._list_id_proc.index(self.proc)
        self.sync_to_nodeeditor()

    # -------------------------------------------------------------------------
    def notify_processes_updated(self):
        """
        Notify the node that the list of processes has been updated.

        """
        self._list_id_proc = list((it.id for it in self.ctx.pm.proc.values()))
        self.ctx.ui.configure_item(self._tag_proc_combo,
                                   items = self._list_id_proc)

        # If the currently configured process
        # had it's ID changed, then we need
        # to update self.proc and self._idx_proc
        # and the value of the combo box.
        #
        if self.proc not in self._list_id_proc:

            try:
                self.proc = self._list_id_proc[self._idx_proc]
            except IndexError:
                self._idx_proc = 0
                self.proc = self._list_id_proc[self._idx_proc]

            self.ctx.ui.set_value(self._tag_proc_combo,
                                  value = self.proc)

    # -------------------------------------------------------------------------
    def set_func(self, str_func):
        """
        Set the node functionality implementation.

        """
        if self.is_noop:
            return
        self.func = str_func
        self.sync_to_nodeeditor()

    # -------------------------------------------------------------------------
    def set_state(self, str_state):
        """
        Set the data type for the node state.

        """
        if self.is_noop:
            return
        self.state = str_state
        self.sync_to_nodeeditor()

    # -------------------------------------------------------------------------
    def set_cfg(self, str_cfg):
        """
        Set the node configuration.

        """
        if self.is_noop:
            return
        self.cfg = str_cfg
        self.sync_to_nodeeditor()

    # -------------------------------------------------------------------------
    @staticmethod
    def clear_sidebar(ctx):
        """
        Clear all node related information from the side tab.

        """
        for (name, value, _) in Node._SIDEBAR_TABLE:
            tag = '.'.join((Node._SIDEBAR_PREFIX, name))
            ctx.ui.set_value(tag, value)

    # -------------------------------------------------------------------------
    def sync_to_sidebar(self):
        """
        """
        for (name, value, is_attrib) in Node._SIDEBAR_TABLE:
            tag = '.'.join((Node._SIDEBAR_PREFIX, name))
            if is_attrib:
                self.ctx.ui.set_value(tag, getattr(self, name))
        self.ctx.ui.configure_item('vp.win.main.side.tab.cfg.node.proc',
                                   items = self._list_id_proc)

    # -------------------------------------------------------------------------
    def sync_to_nodeeditor(self):
        """
        """
        if self.is_noop:
            return
        self.ctx.ui.configure_item(self.tag, label = self.id)

    # -------------------------------------------------------------------------
    def set_input_count(self, count_new):
        """
        """
        if self.is_noop:
            return
        _set_count_impl(ctx        = self.ctx,
                        count_old  = len(self.list_input),
                        count_new  = count_new,
                        fcn_add    = self.add_input,
                        fcn_remove = self.remove_input)

    # -------------------------------------------------------------------------
    def add_input(self):
        """
        Add an input to the node.

        """
        # TODO: CREATE AN INPUT PORT CLASS?
        if self.is_noop:
            return
        port = InputPort(ctx      = self.ctx,
                         tag_node = self.tag)
        self.list_input.append(port)

    # -------------------------------------------------------------------------
    def remove_input(self):
        """
        Remove an input from the node.

        """
        pass

    # -------------------------------------------------------------------------
    def set_output_count(self, count_new):
        """
        """
        if self.is_noop:
            return
        _set_count_impl(ctx        = self.ctx,
                        count_old  = len(self.list_output),
                        count_new  = count_new,
                        fcn_add    = self.add_output,
                        fcn_remove = self.remove_output)

    # -------------------------------------------------------------------------
    def add_output(self):
        """
        Add an output to the node.

        """
        if self.is_noop:
            return
        port = OutputPort(ctx      = self.ctx,
                          tag_node = self.tag)
        self.list_output.append(port)

    # -------------------------------------------------------------------------
    def remove_output(self):
        """
        Remove an output from the node.

        """
        if self.is_noop:
            return
        pass


# =============================================================================
class InputPort():
    """
    Presentation model of an input port on a node.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx, tag_node):
        """
        Return an instance of the InputPort presentation model.

        """
        self.ctx             = ctx
        self.tag_node        = tag_node
        self.tag_side_parent = 'vp.win.main.side.tab.cfg.node'
        self.tag_side_end    = 'vp.win.main.side.tab.cfg.node.countout'
        self.tag_side_input  = ctx.ui.generate_uuid()
        self.tag_node_input  = ctx.ui.generate_uuid()
        self.tag_node_attrib = ctx.ui.generate_uuid()

        DEFAULT_PORT_NAME    = 'input_01'

        self.ctx.ui.add_input_text(
                        parent        = self.tag_side_parent,
                        tag           = self.tag_side_input,
                        before        = self.tag_side_end,
                        default_value = DEFAULT_PORT_NAME,
                        label         = f'Input ID',
                        indent        = INDENT,
                        width         = SIDEBAR_WIDGET_WIDTH,
                        # callback      = self.set_input_id,
                        user_data     = self.ctx)

        self.ctx.ui.add_node_attribute(
                        tag            = self.tag_node_attrib,
                        parent         = self.tag_node,
                        attribute_type = self.ctx.ui.mvNode_Attr_Input)

        self.ctx.ui.add_input_text(
                        parent        = self.tag_node_attrib,
                        tag           = self.tag_node_input,
                        width         = NODE_WIDGET_WIDTH,
                        default_value = DEFAULT_PORT_NAME)

    

# =============================================================================
class OutputPort():
    """
    Presentation model of an output port on a node.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx, tag_node):
        """
        Return an instance of the OutputPort presentation model.

        """
        self.ctx             = ctx
        self.tag_node        = tag_node
        self.tag_side_parent = 'vp.win.main.side.tab.cfg.node'
        self.tag_side_end    = 'vp.win.main.side.tab.cfg.node.separator'
        self.tag_side_input  = ctx.ui.generate_uuid()
        self.tag_node_input  = ctx.ui.generate_uuid()
        self.tag_node_attrib = ctx.ui.generate_uuid()

        DEFAULT_PORT_NAME    = 'output_01'

        self.ctx.ui.add_input_text(
                        parent        = self.tag_side_parent,
                        tag           = self.tag_side_input,
                        before        = self.tag_side_end,
                        default_value = DEFAULT_PORT_NAME,
                        label         = f'Output ID',
                        indent        = INDENT,
                        width         = SIDEBAR_WIDGET_WIDTH,
                        # callback      = self.set_input_id,
                        user_data     = self.ctx)

        self.ctx.ui.add_node_attribute(
                        tag            = self.tag_node_attrib,
                        parent         = self.tag_node,
                        attribute_type = self.ctx.ui.mvNode_Attr_Output)

        self.ctx.ui.add_input_text(
                        parent        = self.tag_node_attrib,
                        tag           = self.tag_node_input,
                        width         = NODE_WIDGET_WIDTH,
                        default_value = DEFAULT_PORT_NAME)



# =============================================================================
class EdgeDict(dict):
    """
    Dict containing system edge configuration presentation models.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the EdgeDict presentation model.

        """
        self.ctx = ctx

    # -------------------------------------------------------------------------
    def update_selected_edges(self):
        """
        Update edges which are selected in the nodeeditor.

        """
        pass
        # list_tag = self.ctx.ui.get_selected_links('vp.win.main.nodeeditor')
        # if not list_tag:
        #     Edge.clear_sidebar(ctx)
        # else:
        #     edge = self.get(list_tag[0])
        #     edge.sync_to_sidebar()


# =============================================================================
class Edge():
    """
    Presentation model of system edge configuration.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the Edge presentation model.

        """
        self.ctx = ctx


# =============================================================================
class DataDict(dict):
    """
    Dict containing system data item configuration presentation models.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the DataDict presentation model.

        """
        self.ctx = ctx


# =============================================================================
class Data():
    """
    Presentation model of system data item configuration.

    """

    # -------------------------------------------------------------------------
    def __init__(self, ctx):
        """
        Return an instance of the Data presentation model.

        """
        self.ctx = ctx


# -----------------------------------------------------------------------------
def _set_count_impl(ctx, count_old, count_new, fcn_add, fcn_remove):
    """
    Generic implementation for 'set count' functions.

    """
    is_fewer = count_new < count_old
    is_same  = count_new == count_old
    is_more  = count_new > count_old

    if is_fewer:
        count = count_old - count_new
        fcn   = fcn_remove
    elif is_same:
        count = 0
    elif is_more:
        count = count_new - count_old
        fcn   = fcn_add

    for _ in range(count):
        fcn()
