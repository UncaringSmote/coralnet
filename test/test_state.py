from unittest import TestCase
from state import StateMachine
import os


class Test(TestCase):
    def test_state(self):
        sm = StateMachine("test")
        current = sm.get_state()
        current.lastK=10
        sm.update_state(current)
        sm2 = StateMachine("test")
        assert sm2.get_state().lastK==10

