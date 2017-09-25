
class EverythingEquals:
    def __eq__(self, other):
        return True


everything_equals = EverythingEquals()


def hello(event, context):
    return "hello " + event['arg1']


def to_upper(event, context):
    return event['greeting'].upper()


def workflow_one_step():
    return {
        "comment": "A simple minimal example of the States language",
        "name": "placement_engine",

        "start_at": "hello world",
        "states": {
            "hello world": {
                "type": "python_method",
                "function_to_exec": "tests.unit.util.hello",
                "end": True,
                "result_path": 'greeting',

            }
        }
    }


def workflow_two_step():
    wf = workflow_one_step()
    wf['states']['hello world']["end"] = False
    wf['states']['hello world']["next"] = 'hello world2'
    wf['states']['hello world2'] = {
        "type": "python_method",
        "function_to_exec": "tests.unit.util.to_upper",
        "result_path": 'greeting',
        "end": True
    }
    return wf
