'''A client for reading in archiver files'''

from psconfig.client.psconfig.base_connect import BaseConnect
from psconfig.client.psconfig.archive import Archive

class ArchiveConnect(BaseConnect):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def config_obj(self):
        '''return Archive object'''
        return Archive()
