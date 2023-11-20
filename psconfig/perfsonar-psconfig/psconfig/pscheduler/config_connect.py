'''A client for interacting pSConfig pScheduler agent configuration file
'''

from ..client.psconfig.base_connect import BaseConnect
from .config import Config

class ConfigConnect(BaseConnect):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def config_obj(self):
        '''Overridden method that returns psconfig.pscheduler.config.Config instance'''
        return Config()