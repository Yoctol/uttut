from typing import List, Callable

import json

from .step import Step
from .factory import OperatorFactory


class Pipe:

    def __init__(self):
        self._steps = []
        self._step_info = []

    def add(self, op_name: str, op_kwargs=None):
        """Add steps based on the operation name.

        This method creates a step, which has an op. The op
        is created.

        Args:
            op_name:
            op_kwargs,

        Raises:
            KeyError

        """
        if op_kwargs is None:
            op_kwargs = {}

        op = OperatorFactory.from_name(op_name)(**op_kwargs)
        step = Step(op)

        self._validate_steps(step)

        self.update_steps(step)
        self.update_step_info(op_name, op_kwargs)

    def _validate_steps(self, step):
        if len(self._steps) > 0:
            target_type = self._steps[-1].output_type
            in_type = step.input_type
            if in_type != target_type:
                raise TypeError(
                    "InputType of the step op is not valid."
                    f"Got {in_type}, but requires {target_type}")

    def update_steps(self, step: Step):
        self._steps.append(step)

    def update_step_info(self, name, kwargs):
        self._step_info.append(
            {  # for serialization
                'op_name': name,
                'op_kwargs': kwargs,
            },
        )

    def transform(self, input_sequence, labels: List[int]):
        """Process data based on Steps(Ops).

        This method processes input sequence according to the Pipe's steps.

        Args:
            input_sequence: string or list of strings (tokens)

        Returns:
            output_sequence: transfromed sequence
            labels: updated labels
            realigners: list of Realigners
        """
        realigners = Realigners()
        for step in self._steps:
            input_sequence, labels, realigner = step.transform(input_sequence, labels)
            realigners.add(realigner)
        return input_sequence, labels, realigners

    def serialize(self, path):
        with open(path, 'wb') as fw:
            json.dump(self.step_info, fw)

    @classmethod
    def restore_from_json(cls, path: str):
        pipe = cls()
        with open(path, 'rb') as f:
            step_infos = json.load(f)

        # restore steps
        for step_info in step_infos:
            pipe.add(
                op_name=step_info['op_name'],
                op_kwargs=step_info['op_kwargs'],
            )
        return pipe


class Realigners:

    def __init__(self):
        self.collections = []

    def add(self, realigner: Callable[[List[int]], List[int]]):
        self.collections.append(realigner)

    def __call__(self, labels: List[int]) -> List[int]:
        for realigner in self.collections[::-1]:
            labels = realigner(labels)
        return labels
