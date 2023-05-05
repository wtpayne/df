# -*- coding: utf-8 -*-
"""
MIL (Model-In-the-Loop) simulator module.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2019 High Integrity Artificial Intelligence Systems"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."

requirements:
    "This design document may contain any number of requirements
    items embedded in comment blocks. Each requirements item
    that is present shall have one formal requirement statement
    with one modal verb. The modal verb shall be interpreted
    in accordance with iso29148:2011

    SHALL indicates a mandatory binding provision, the fulfillment
    of which must be proven through an appropriate test.

    WILL indicates a statement of fact; futurity; a declaration
    of purpose; or to establish a context or a limitation of use.
    These statements are not manadatory and not binding.

    SHOULD indicates a preference; a goal or an advantageous
    quality. These statements are not mandatory and not binding.

    MAY is used to grant permission or to make a suggestion.
    These statements are not mandatory and not binding."
...
"""


import runtime.mil


# -----------------------------------------------------------------------------
def _build(cfg, graph):
    """
    Return a dict of instantiated and configured data-flow vertices.

    ---
    type:   function
    ...

    """
    # Allocate and reset data structures for each vertex.
    vertices = dict()
    for (name, data) in graph.items():
        vertices[name] = runtime.mil.Vertex(cfg, data['logic'])

    # Connect vertices with edges. (Set pointers in data structures).
    for (name, data) in graph.items():
        self_vtx = vertices[name]
        for (self_path_str, other_path_str) in data['edges']:

            other_path = other_path_str.split('.')
            other_vtx  = vertices[other_path[0]]
            other_path = other_path[1:]

            self_path  = self_path_str.split('.')
            self_ref   = self_vtx.get_ref(self_path[:-1])

            self_ref[self_path[-1]] = other_vtx.get_ref(other_path)

    return vertices


# -----------------------------------------------------------------------------
def _schedule(graph):
    """
    Plan the order of evaluation.

    Exeuction order is currently manually configured.
    we can add an automatic scheduler when maintaining
    this becomes a burden.

    ---
    type:   function
    ...

    """
    return tuple(
        name for (name, _) in sorted(graph.items(),
                                     key = lambda it: it[1]['order']))


# -----------------------------------------------------------------------------
def _run(vertices, sequence):
    """
    Run simulation.

    ---
    type:   function
    ...

    """
    # while True:
    for i in range(100):
        print(i)
        for name in sequence:
            try:
                vertices[name].step()
            except StopIteration:
                return


# -----------------------------------------------------------------------------
def main(graph, cfg):
    """
    Configure and run the simulation.

    ---
    type:   function
    ...

    """
    _run(
        vertices = _build(cfg, graph),  # Allocate and configure vertices.
        sequence = _schedule(graph))    # Work out run order.
