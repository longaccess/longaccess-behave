from testtools import TestCase
from testtools.matchers import Equals

class UploaTest(TestCase):
    def _makeit(self, *args ,**kw):
        import botofun.provision
        return botofun.provision.Upload(*args, **kw)

    def test_upload(self):
        foo = self._makeit()

    def test_upload_init(self):
        upload = self._makeit()

