from unittest import mock

from ulauncher.api.shared.action.ActionList import ActionList
from ulauncher.api.shared.action.BaseAction import BaseAction


class EmptyAction(BaseAction):
    def __init__(self, keep_app_open):
        self.keep_app_open = keep_app_open

    def run(self):
        pass


class TestActionList:
    def test_keep_app_open(self):
        assert ActionList().keep_app_open
        assert ActionList([EmptyAction(False), EmptyAction(True), EmptyAction(False)]).keep_app_open
        assert ActionList(["kw val", False, EmptyAction(False)]).keep_app_open
        assert not ActionList([EmptyAction(False), EmptyAction(False), False]).keep_app_open

    def test_run(self):
        alist = ActionList([mock.create_autospec(BaseAction), mock.create_autospec(BaseAction)])
        alist.run()

        alist[0].run.assert_called_with()
        alist[1].run.assert_called_with()
