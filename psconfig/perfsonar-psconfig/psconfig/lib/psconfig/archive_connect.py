'''A client for reading in archiver files'''

from ..shared.client.psconfig.base_connect import BaseConnect
from ..shared.client.psconfig.archive import Archive

class ArchiveConnect(BaseConnect):

    def config_obj(self):
        '''return Archive object'''
        return Archive()
