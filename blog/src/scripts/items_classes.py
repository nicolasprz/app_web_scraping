from __future__ import annotations

import re
import pandas as pd
from dataclasses import dataclass, field
from enum import Enum


class Multiplier(Enum):
    no_multiplier = 1
    K = 1e3
    M = 1e6

    def __str__(self) -> str:
        if self._name_ == 'no_multiplier':
            return ''
        return self._name_


def default_multiplier():
    return Multiplier.no_multiplier


@dataclass(frozen=True)
class NbItems:
    value: float | int
    multiplier: Multiplier = field(default_factory=default_multiplier)

    def __repr__(self) -> str:
        if self.multiplier == Multiplier.no_multiplier:
            return f"{self.value}"
        return f"{self.value}{self.multiplier}"

    def __lt__(self, other: NbItems) -> bool:
        """
        Less than comparison based on as_int property.
        """
        return self.as_int < other.as_int

    @property
    def as_int(self) -> int:
        """
        Takes the NbItems object as a floating value and multiplies it by multiplier value.
        Returns that integer.
        """
        return int(self.value * self.multiplier.value)

    @classmethod
    def from_str(cls: NbItems, cls_string: str) -> NbItems:
        """
        Creates an instance of class NbItems from given string.
        Raises a ValueError if provided string is of wrong format.
        NB: string must either have:
            - a floating part (with optional decimal part), followed by a letter between K and M
            - an integer part, with no decimal part and no letter at the end
        """
        floating_pattern = re.compile(r'^\d+(\.\d+)?[K|M]$')
        int_pattern = re.compile(r'^\d+$')
        if floating_pattern.match(cls_string):
            floating_part = cls_string[:-1]  # Remove last letter, which is multiplier
            return NbItems(float(floating_part), Multiplier[cls_string[-1]])
        elif int_pattern.match(cls_string):
            return NbItems(int(cls_string), Multiplier.no_multiplier)
        else:
            raise ValueError(f'Provided string must be of format {cls.__name__}, {cls_string} was provided')


def generate_nbitems(num_items):
    return [NbItems(value=i, multiplier=Multiplier.K) for i in range(1, num_items + 1)]


if __name__ == "__main__":
    # Tests for classes in this script.
    mult = 'M'
    nb_items = NbItems(3.9, Multiplier[mult])
    nb_items_bis = NbItems(4_000_000)
    print(nb_items)
    print(f"{nb_items.as_int:_}")
    print(nb_items < nb_items_bis)
    print(NbItems.from_str('2.6K'))
    # print(NbItems.from_str('Bonjour'))  # Raises a ValueError
    nb_items_list = generate_nbitems(5)

    # Creating a DataFrame
    print(nb_items_list)
    df = pd.DataFrame(nb_items_list)

    # Displaying the DataFrame
    print(df)
