cdef class Entity:

    def __init__(
            self,
            int label,
            str value,
            int start,
            int end,
            replacements = None,
        ) -> None:

        """

        replacements: List[str]
        """

        self.label = label
        self.value = value
        self.start = start
        self.end = end
        cdef list _replacements = [] if replacements is None else list(replacements)
        self.replacements = set(_replacements)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError('can only compare entity to entity')
        cdef bint same_label = self.label == other.label
        cdef bint same_value = self.value == other.value
        cdef bint same_position = (self.start == other.start) and (self.end == other.end)
        cdef bint same_replacements = self.replacements == other.replacements
        return same_label and same_value and same_position and same_replacements

    def __repr__(self):
        return "<Entity {}: {} at {} - {}, with replacements: {}>".format(
            self.label,
            self.value,
            self.start,
            self.end,
            ', '.join(list(self.replacements)),
        )

    def no_replacements(self) -> bool:
        return len(self.replacements) == 0

    def n_replacements(self):
        return len(self.replacements) + 1

    def to_dict(self) -> dict:
        result = {
            'label': self.label,
            'start': self.start,
            'end': self.end,
        }
        if not self.no_replacements():
            result['replacements'] = list(self.replacements)
        return result

    @classmethod
    def from_dict(cls, dict entity, str utterance):
        new_end = entity['end']
        entity_value = utterance[entity['start']: new_end]
        replacements = entity.get('replacements')
        return cls(
            label=entity['label'],
            value=entity_value,
            start=entity['start'],
            end=new_end,
            replacements=[] if replacements is None else replacements,
        )
