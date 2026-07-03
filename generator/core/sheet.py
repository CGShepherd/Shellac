from dataclasses import dataclass, field
from .components import Component

@dataclass
class Sheet:
    title: str
    filename: str
    components: list[Component] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def add_component(self, component):
        self.components.append(component)
        return component

    def add_note(self, note):
        self.notes.append(note)
