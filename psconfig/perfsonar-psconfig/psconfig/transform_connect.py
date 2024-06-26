'''
A client for reading in JQTransform files
'''

from .client.psconfig.base_connect import BaseConnect
from .client.psconfig.jq_transform import JQTransform

class TransformConnect(BaseConnect):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def config_obj(self):
        '''return jqtransform object'''
        return JQTransform()
