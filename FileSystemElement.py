
class File:
    def __init__(self, type, permissions, hard_links, owner, group, size, date, name):
        self.type = type
        self.permissions = permissions
        self.hard_links = hard_links
        self.owner = owner
        self.group = group
        self.size = size
        self.date = date
        self.name = name

    def get_name(self):
        return self.name

    def __str__ (self):
        return f'File(type={self.type}, permissions={self.permissions}, hard_links={self.hard_links}, owner={self.owner}, group={self.group}, size={self.size}, date={self.date}, name={self.name})'