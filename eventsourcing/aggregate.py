class Aggregate:
    def __init__(self):
        self.uncommitted_changes = []

    @classmethod
    def from_events(cls, events):
        aggregate = cls()
        for event in events:
            if hasattr(event, 'apply_changes'):
                event.apply_changes(aggregate)
        aggregate.uncommitted_changes = []
        return aggregate

    def changes_committed(self):
        self.uncommitted_changes = []

    def _apply_changes(self, event):
        self.uncommitted_changes.append(event)
        if hasattr(event, 'apply_changes'):
            event.apply_changes(self)