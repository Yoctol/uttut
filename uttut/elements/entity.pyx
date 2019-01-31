cdef class Entity:

    def __cinit__(
            self,
            unsigned int label,
            str value,
            unsigned int start,
            unsigned int end,
            object replacements = None,
        ) -> None:

        self.label = label
        self.value = value
        self.start = start
        self.end = end
        cdef list _replacements = [] if replacements is None else list(replacements)
        self.replacements = set(_replacements)

    def __eq__(self, Entity other):
        cdef tuple self_attrs, other_attrs
        self_attrs = (self.label, self.value, self.start, self.end, self.replacements)
        other_attrs = (other.label, other.value, other.start, other.end, other.replacements)
        return self_attrs == other_attrs

    def __repr__(self):
        return "<Entity {}: {} at {} - {}, with replacements: {}>".format(
            self.label,
            self.value,
            self.start,
            self.end,
            ', '.join(list(self.replacements)),
        )

    cpdef bint no_replacements(self):
        return len(self.replacements) == 0

    cpdef unsigned int n_replacements(self):
        return len(self.replacements) + 1

    cpdef dict to_dict(self):
        cdef dict result
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
