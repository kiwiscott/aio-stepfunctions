from typing import List
from enum import Enum
from aiostepfunctions.state_types import factory
from aiostepfunctions.util import unique_key
from datetime import datetime

"""
{
   "executionArn": "string",
   "input": "string",
   "name": "string",
   "output": "string",
   "startDate": number,
   "uuid": "string",
   "status": "string",
   "stopDate": number
}



Steps
1. Create the object
    return a uuid identifying the machine // this validates the syntax etc

2. execute the wf

"""


class StateMachine:
    def __init__(self, id, name, comment, start_at):
        self.machine_id = id
        self.name = name
        self.comment = comment
        self.start_at = start_at
        self.current_state = None

        self.states = []

    def execution_state(self):
        print(self.current_state, list(str(s) for s in self.states))
        current = next(s for s in self.states if s.name == self.current_state)
        return current

    def start(self):
        self.current_state = self.start_at

    def transition(self):
        current = next(
            (s for s in self.states if s.name == self.current_state))
        self.current_state = current.next

    @classmethod
    def from_dict(cls, state_dict):
        machine_id = state_dict['machine_id'] if 'machine_id' in state_dict \
            else unique_key('m_')

        state_machine = cls(
            machine_id, state_dict['name'], state_dict['comment'],
            state_dict['start_at'])

        for k, v in state_dict['states'].items():
            state = factory(k, v)
            state_machine.states.append(state)

        return state_machine

    def to_dict(self):
        copied = self.__dict__.copy()
        del copied['states']
        states = {}
        for state in self.states:
            states[state.name] = state.__dict__.copy()
            del states[state.name]['name']
        copied['states'] = states
        return copied


class State(Enum):
    Red = 1
    Blue = 2
    Green = 3


class Executor:
    def __init__(self, state_machine):
        self.state_machine = state_machine
        self.input = None
        self.result = None

    def _build_context(self):
        return {
            "machine_id":  self.state_machine.machine_id,
            "name": self.state_machine.name,
            "machine_start": datetime.utcnow()
        }

    def execute(self, input=None):
        self.input = input
        self.result = input.copy()
        self.context = self._build_context()

        self.state_machine.start()
        while True:
            try:
                state = self.state_machine.execution_state()
            except:
                # end of wf
                break

            print('execution' + str(state))
            a_result = state.execute(self.result, self.context)

            if state.result_path is not None:
                self.result[state.result_path] = a_result
            self.state_machine.transition()
        return input
