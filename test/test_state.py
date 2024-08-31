from unittest import TestCase
from state import StateMachine
import os


class Test(TestCase):
    def test_state(self):
        sm = StateMachine("test")
        current = sm.get_state()
        current.deploy_started=True
        sm.update_state(current)
        sm2 = StateMachine("test")
        assert sm2.get_state().deploy_started==True

