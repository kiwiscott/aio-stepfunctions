import pytest
from .util import workflow_one_step, workflow_two_step
from aiostepfunctions.executor import Executor, StateMachine


def test_single_step():
    wf = workflow_one_step()
    state_machine = StateMachine.from_dict(wf)
    the_executor = Executor(state_machine)
    the_executor.execute({'arg1': 'world'})
    assert the_executor.result['greeting'] == 'hello world'


def test_two_steps():
    wf = workflow_two_step()
    state_machine = StateMachine.from_dict(wf)
    the_executor = Executor(state_machine)
    the_executor.execute({'arg1': 'world awesome!'})

    assert the_executor.result['greeting'] == 'HELLO WORLD AWESOME!'
