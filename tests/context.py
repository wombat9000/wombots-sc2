import os
import sys
from unittest.mock import Mock

from sc2.unit import Unit

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# noinspection PyUnresolvedReferences
from wombots.zerg_bot import *


async def async_mock(val):
    return val


def unit_mock_of(type_id: UnitTypeId):
    unit: Unit = Mock()
    unit.is_mine = Mock(return_value=True)
    unit.type_id = type_id
    return unit
