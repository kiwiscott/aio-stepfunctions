import pytest
from .util import workflow_one_step, workflow_two_step, everything_equals
from aiostepfunctions.executor import Executor, StateMachine


def test_build_state_machine_id():
    wf = workflow_one_step()
    _id = 'M_1234456'
    wf['machine_id'] = _id
    state_machine = StateMachine.from_dict(wf)
    assert state_machine.machine_id == _id


def test_build_state_machine():
    wf = workflow_one_step()
    state_machine = StateMachine.from_dict(wf)
    assert state_machine.name == wf['name']
    assert state_machine.comment == wf['comment']
    assert hasattr(state_machine, 'machine_id')
    assert len(state_machine.states) == 1


def test_to_dict_ids():
    wf = workflow_one_step()
    wf['machine_id'] = 'M_123455'
    wf['current_state'] = None

    counter = 1

    for name, parameters in wf['states'].items():
        parameters['state_id'] = 'S_122200' + str(counter)
        parameters['end'] = True
        parameters['next'] = None
        counter += 1

    state_machine = StateMachine.from_dict(wf)
    d = state_machine.to_dict()

    assert wf == d


def test_to_dict():
    wf = workflow_one_step()
    state_machine = StateMachine.from_dict(wf)
    wf['machine_id'] = everything_equals
    wf['current_state'] = None

    for name, parameters in wf['states'].items():
        parameters['state_id'] = everything_equals
        parameters['end'] = True
        parameters['next'] = None

    d = state_machine.to_dict()

    assert wf == d


@pytest.mark.parametrize("active_state", [
    'hello world2',
    'hello world'
])
def test_correct_state_active(active_state):
    wf = workflow_two_step()
    wf['start_at'] = active_state

    state_machine = StateMachine.from_dict(wf)
    state_machine.start()

    assert state_machine.current_state == active_state
    assert len(state_machine.states) == 2
