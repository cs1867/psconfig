'''
Utilities for running JQ.
'''

import pyjq

def jq(jq, json_obj, formatting_params, timeout):

    #initialize formatting params
    try:
        value = pyjq.all(jq, json_obj)
        return value
    except Exception as e:
        raise Exception('jq error: {}'.format(e))
