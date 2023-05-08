from ..shared.client.psconfig.addresses.address import Address
from ..shared.client.psconfig.schema import Schema
from ..shared.client.psconfig.base_node import BaseNode
from jsonschema import validate as jsonvalidate

class RequestingAgentConfig(BaseNode):

    def __init__(self):
        self.error = ''
    
    def address(self, field, val=None):
        return self._field_class(field, Address, val)
    
    def address_names(self):
        names = list(self.data)
        return names
    
    def remove_address(self, field):
        if not self.data.get(field):
            return
        del self.data[field]
    
    def validate(self):
        schema = Schema().psconfig_json_schema()
        schema['required'] = ['addresses']
        try:
            #plug-in archive in a way that will validate
            validator = jsonvalidate(instance={'addresses':self.data}, schema=schema)
            return []
        except Exception as e:
            return [e]
        