# -*- coding: utf-8 -*-
"""
Exception classes for da systems.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2023 William Payne"

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


# =============================================================================
class PreconditionViolation(RuntimeError):
    """
    Exception to be raised when a precondition is violated.

    """

    pass


# =============================================================================
class SystemPreconditionViolation(PreconditionViolation):
    """
    Exception to be raised when a unit precondition is violated.

    """

    pass


# =============================================================================
class UnitPreconditionViolation(PreconditionViolation):
    """
    Exception to be raised when a unit precondition is violated.

    """

    pass


# =============================================================================
class DesignNonconformity(RuntimeError):
    """
    Exception to be raised when a design nonconformity is encountered.

    This exception is intended to be raised when a
    design nonconformity (bug) is encountered.

    Specifically, this exception indicates that the
    system is in a state which should be impossible
    if the design were internally consistent and
    conformant with expections.

    """

    pass


# =============================================================================
class ImplementationNotPresentError(DesignNonconformity):
    """
    Exception to be raised when a feature is not yet implemented.

    We allow features to be introduced incrementally
    to production software, disabled or enabled by
    suitable runtime configuration.

    This exception serves both as a searchable
    indicator of unfinished work and also as an
    indicator of configuration errors during
    testing.

    The Python built-in exception NotImplementedError
    is not suitable as it is intended for a different
    use-case. Its' documentation explicitly states
    that it is intended to be used (only?) for abstract
    methods in a base class that need to be overridden.

    """

    pass


# =============================================================================
class AbortSilently(Exception):
    """
    Exception to be raised when the display of a message is undesirable.

    This exception is raised when we have already displayed an error
    message and just need the program to abort.

    """

    pass


# =============================================================================
class AbortWithoutStackTrace(Exception):
    """
    Exception to be raised when the display of a stack trace is undesirable.

    Raising this exception will not result in a
    stack trace in the CLI, so it should not be
    used to indicate errors in running components
    of the build system, but should instead be
    used to indicate incorrect or invalid input
    being provided to the build. E.g. bad parameters,
    bad configuration files or other build input
    file errors.

    ---
    type: class
    attributes:
        message:
            Human readable string describing the
            reason for the abort.
        filepath:
            If specified, this is a string holding
            the fully qualified path to the file
            within which a fault was found.
            Otherwise None.
        line_number:
            If specified, this is an integer
            indicating the line number in
            filepath where a fault was found.
            Otherwise None.
    ...
    """

    def __init__(self, message, filepath = None, line_number = None):
        """
        Return a new instance of the AbortWithoutStackTrace Exception class.

        ---
        type: constructor
        args:
            message:
                Human readable string describing
                the reason for the abort.
            filepath:
                If specified, this is a string
                holding the fully qualified path
                to the file within which a fault
                was found. Otherwise None.
            line_number:
                If specified, this is an integer
                indicating the line number in
                filepath where a fault was found.
                Otherwise None.
        ...

        """
        # We need to be careful to call the base
        # class with the parameters that it needs
        # - as we will have difficulty unpickling
        # it otherwise.
        #
        super(AbortWithoutStackTrace, self).__init__(message)
        self.message     = message
        self.filepath    = filepath
        self.line_number = line_number
