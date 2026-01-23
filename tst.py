from enum import Enum

class Status(Enum):
    NEU = 1
    IN_BEARBEITUNG = 2
    ABGESCHLOSSEN = 3

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        if value == 1:
            obj.description = "Status ist neu."
        elif value == 2:
            obj.description = "Status wird bearbeitet."
        elif value == 3:
            obj.description = "Status ist abgeschlossen."
        return obj

# Testen
x = Status(1)
print(Status.NEU.description)  # Ausgabe: Status ist neu.
print(Status.ABGESCHLOSSEN.description)  # Ausgabe: Status ist abgeschlossen.
