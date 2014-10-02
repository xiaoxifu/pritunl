from pritunl.settings.group_base import SettingsGroupBase

from pritunl.constants import *
from pritunl.exceptions import *
from pritunl.descriptors import *

class SettingsGroup(SettingsGroupBase):
    type = 'default'

    def __init__(self):
        self.changed = set()

    def __setattr__(self, name, value):
        if name != 'fields' and name in self.fields:
            self.changed.add(name)
        object.__setattr__(self, name, value)

    def __getattr__(self, name):
        if name in self.fields:
            return self.fields[name]
        raise AttributeError(
            'SettingsGroup instance has no attribute %r' % name)

    def get_commit_doc(self, all_fields):
        doc = {
            '_id': self.group,
        }

        for field in self.fields if all_fields else self.changed:
            doc[field] = getattr(self, field)

        if len(doc) > 1:
            return doc
