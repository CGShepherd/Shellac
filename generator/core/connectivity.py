from dataclasses import dataclass, field

@dataclass(frozen=True)
class Net:
    name: str
    net_class: str = "Default"

@dataclass
class PinRef:
    component_ref: str
    pin: str

@dataclass
class Connection:
    net: Net
    pins: list[PinRef] = field(default_factory=list)

    def add(self, component_ref: str, pin: str):
        self.pins.append(PinRef(component_ref, pin))
        return self
