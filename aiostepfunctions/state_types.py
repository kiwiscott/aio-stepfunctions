from abc import ABC, abstractmethod
import importlib
from aiostepfunctions.util import unique_key, load_func


def factory(name, state_dict):
    copied_state_dict = state_dict.copy()
    state_id = None
    if 'state_id' in copied_state_dict:
        state_id = copied_state_dict['state_id']
        del copied_state_dict['state_id']
    else:
        state_id = unique_key('s_')

    state_type = copied_state_dict['type']
    del copied_state_dict['type']

    if state_type is PythonMethodStateType.NAME:
        return PythonMethodStateType.from_dict(state_id, name, **copied_state_dict)
    raise AttributeError(name + ':' + state_type)


class StateType(ABC):
    def __init__(self,  state_id, name, type, **kwargs):
        self.name = name
        self.type = type
        self.state_id = state_id
        self.next = kwargs.get('next', None)
        self.end = kwargs.get('end', None)
        self.result_path = kwargs.get('result_path', None)

    @classmethod
    @abstractmethod
    def from_dict(cls, state_id, name, **kwargs):
        pass

    @abstractmethod
    def execute(self, event, context):
        pass

    def __str__(self):
        return "{0}:{1}:{2}".format(self.type, self.name, self.state_id)


class PythonMethodStateType(StateType):
    NAME = 'python_method'

    def __init__(self, state_id, name, **kwargs):
        super(PythonMethodStateType, self).__init__(
            state_id, name, PythonMethodStateType.NAME, **kwargs)
        self.function_to_exec = kwargs.get('function_to_exec')

    @classmethod
    def from_dict(cls, state_id, name, **kwargs):
        state = cls(state_id, name, **kwargs)
        return state

    def execute(self,  event, context):
        func = load_func(self.function_to_exec)
        return func(event, context)
