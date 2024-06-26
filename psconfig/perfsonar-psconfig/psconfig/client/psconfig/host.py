from .base_meta_node import BaseMetaNode

class Host(BaseMetaNode):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def archive_refs(self, val=None):
        '''Gets/sets archives as a list'''
        return self._field_refs('archives', val)
    
    def add_archive_ref(self, val):
        '''Adds an archive'''
        self._add_field_ref('archives', val)
    
    def tags(self, val=None):
        '''Gets/sets tags as a list'''
        return self._field('tags', val)
    
    def add_tag(self, val):
        '''Adds tag'''
        self._add_list_item('tags', val)
    
    def disabled(self, val=None):
        '''Gets/sets disabled'''
        return self._field_bool('disabled', val)

    def no_agent(self, val=None):
        '''Gets/sets no-agent'''
        return self._field_bool('no-agent', val)

