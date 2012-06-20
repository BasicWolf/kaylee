# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod
from datetime import datetime

from .errors import KayleeError
from .node import Node, NodeID
from .util import parse_timedelta

class NodesStorage(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add(self, node):
        """TODO: Add node to storage"""

    @abstractmethod
    def clean(self, node):
        """Removes the obsolete nodes from the storage"""

    @abstractmethod
    def __delitem__(self, node):
        """Removes the node from the storage"""

    @abstractmethod
    def __getitem__(self, node_id):
        """TODO: Returns a node with requested id"""

    @abstractmethod
    def __contains__(self, node):
        """TODO: Check if storage contains the node"""


class MemoryNodesStorage(NodesStorage):
    def __init__(self, timeout, *args, **kwargs):
        self._d = {}
        self.timeout = parse_timedelta(timeout)
        super(MemoryNodesStorage, self).__init__(*args, **kwargs)

    def add(self, node):
        self._d[node.id] = node

    def clean(self):
        nodes_to_clean = [node for node in self._d.iteritems()
                          if datetime.now() - node.id.timestamp > self.timeout]
        for node in nodes_to_clean:
            del self._d[node]

    def __delitem__(self, node):
        node_id = NodeID.from_object(node)
        try:
            del self._d[node_id]
        except KeyError:
            pass

    def __getitem__(self, node_id):
        node_id = NodeID.from_object(node_id)
        return self._d[node_id]

    def __contains__(self, node):
        node_id = NodeID.from_object(node)
        return node_id in self._d


class ControllerResultsStorage(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, node_id, task_id, result):
        """Stores results from particular node associated with task_id to the
        storage.
        """

    @abstractmethod
    def remove(self, node_id, task_id):
        """Removes result recieved from particular node associated with task_id
        from the storage.
        """

    @abstractmethod
    def clear(self):
        """ """

    @abstractmethod
    def __setitem__(self, task_id, results):
        """Stores results associated with task_id to the storage."""

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

    @abstractmethod
    def __delitem__(self, task_id):
        """Removes all results associated with task_id from the storage."""

    @abstractmethod
    def __contains__(self, task_id):
        """ """


class MemoryControllerResultsStorage(ControllerResultsStorage):
    def __init__(self):
        self._d = {}

    def add(self, node_id, task_id, result):
        d = self._d.get(task_id, {})
        d[node_id] = result
        self._d[task_id] = d

    def remove(self, node_id, task_id):
        del self._d[task_id][node_id]

    def clear(self):
        self._d = {}

    def __getitem__(self, task_id):
        try:
            return self._d[task_id]
        except KeyError:
            return []

    def __setitem__(self, task_id, val):
        self._d[task_id] = val

    def __delitem__(self, task_id):
        del self._d[task_id]

    def __contains__(self, task_id):
        return task_id in self._d


class ProjectResultsStorage(object):
    """Applications results holder object. This class is an interface for
    objects which should hold the final results of an application. """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __len__(self):
        """ """

    @abstractmethod
    def __getitem__(self, task_id):
        """ """

    @abstractmethod
    def __setitem__(self, task_id, result):
        """ """

    @abstractmethod
    def __contains__(self, task_id):
        """ """

    @abstractmethod
    def __iter__(self):
        """ """

    @abstractmethod
    def keys(self):
        """ """

    @abstractmethod
    def values(self):
        """ """


class MemoryProjectResultsStorage(ProjectResultsStorage):
    def __init__(self):
        self._d = {}

    def __len__(self):
        return len(self._d)

    def __getitem__(self, task_id):
        return self_d[task_id]

    def __setitem__(self, task_id, result):
        self._d[task_id] = result

    def __contains__(self, task_id):
        return task_id in self._d

    def __iter__(self):
        return iter(self._d)

    def keys(self):
        return self._d.iterkeys()

    def values(self):
        return self._d.itervalues()
