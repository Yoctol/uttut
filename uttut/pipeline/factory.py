class OperatorFactory:

    _OperatorServiceLocator: dict
    _OperatorServiceLocator = {}

    @classmethod
    def operator_names(cls):
        return list(cls._OperatorServiceLocator.keys())

    @classmethod
    def from_name(cls, name: str):
        if name not in cls._OperatorServiceLocator:
            raise KeyError(f"Operator {name} is not found.")
        return cls._OperatorServiceLocator[name]
