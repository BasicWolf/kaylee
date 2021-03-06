#pylint: disable-msg=W0212,W0611
#W0212: Access to a protected member
#W0611: Unused import PROJECTS_DIR # FALSE ALARM
###

from kaylee.testsuite import KayleeTest, load_tests, PROJECTS_DIR

import os
from kaylee import loader, Kaylee, KayleeError
from kaylee.errors import SettingsError
from kaylee.contrib import (MemoryTemporalStorage,
                            MemoryPermanentStorage,
                            MemoryNodesRegistry)
from kaylee.session import ClientSessionDataManager
from kaylee.loader import Loader, SettingsValidator
from kaylee.util import generate_sercret_key

_test_REGISTRY = {
    'name' : 'MemoryNodesRegistry',
    'config' : {
        'timeout' : '2s',
        },
}


class TestSettings(object):
    REGISTRY = _test_REGISTRY

    AUTO_GET_ACTION = True

    SECRET_KEY = generate_sercret_key()

    SESSION_DATA_MANAGER = {
        'name' : 'ClientSessionDataManager',
        'config' : {
            'secret_key' : SECRET_KEY
        }
    }


class TestSettingsWithApps(object):
    REGISTRY = _test_REGISTRY

    AUTO_GET_ACTION = True

    SECRET_KEY = generate_sercret_key()

    APPLICATIONS = [
        {
            'name' : 'test.1',
            'description' : 'Test application',
            'project' : {
                'name' : 'AutoTestProject',
            },
            'controller' : {
                'name' :'TestController1',
                'config' : {},
                'temporal_storage' : {
                    'name' : 'MemoryTemporalStorage',
                },
                'permanent_storage' : {
                    'name' : 'MemoryPermanentStorage',
                },
            },
        }
    ]

    PROJECTS_DIR = PROJECTS_DIR


class KayleeLoaderTests(KayleeTest):
    def test_load_settings_class(self):
        kl = loader.load(TestSettings)
        self.assertIsInstance(kl, Kaylee)

    def test_load_settings_dict(self):
        # dict(Class.__dict__) wrapping: __dict__ is a dictproxy,
        kl = loader.load(dict(TestSettings.__dict__))
        self.assertIsInstance(kl, Kaylee)

    def test_load_settings_module(self):
        test_settings = __import__('test_settings')
        kl = loader.load(test_settings)
        self.assertIsInstance(kl, Kaylee)

    def test_load_settings_path(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'test_settings.py'))
        kl = loader.load(path)
        self.assertIsInstance(kl, Kaylee)

    def test_load_applications(self):
        settings = dict(TestSettingsWithApps.__dict__)
        ldr = Loader(settings)
        apps = ldr.applications
        self.assertIsInstance(apps, list)
        self.assertEqual(len(apps), 1)

        app = apps[0]
        self.assertEqual(app.__class__.__name__, 'TestController1')
        self.assertEqual(app.project.__class__.__name__, 'AutoTestProject')
        self.assertIsInstance(app.temporal_storage, MemoryTemporalStorage)
        self.assertIsInstance(app.permanent_storage, MemoryPermanentStorage)
        #self.assertIsInstance(app.project.storage, MemoryPermanentStorage)

    def test_load_registry(self):
        settings = dict(TestSettings.__dict__)
        ldr = Loader(settings)
        reg = ldr.registry
        self.assertIsInstance(reg, MemoryNodesRegistry)

    def test_load_session_data_manager(self):
        settings = dict(TestSettings.__dict__)
        ldr = Loader(settings)
        sdm = ldr.session_data_manager
        self.assertIsInstance(sdm, ClientSessionDataManager)

    def test_load_kaylee(self):
        kl = loader.load(TestSettingsWithApps)
        self.assertIsInstance(kl.registry, MemoryNodesRegistry)

        app = kl.applications['test.1']
        self.assertEqual(app.__class__.__name__, 'TestController1')
        self.assertEqual(app.project.__class__.__name__, 'AutoTestProject')

    def test_kaylee_setup(self):
        from kaylee import setup, kl
        self.assertIsNone(kl._wrapped)
        setup(TestSettingsWithApps)

        self.assertIsNotNone(kl._wrapped)
        self.assertIsInstance(kl.registry, MemoryNodesRegistry)

        app = kl.applications['test.1']
        self.assertEqual(app.__class__.__name__, 'TestController1')
        self.assertEqual(app.project.__class__.__name__, 'AutoTestProject')


    def test_settings_validator(self):
        sv = SettingsValidator
        self.assertRaises(SettingsError, sv.validate_AUTO_GET_ACTION, {'AUTO_GET_ACTION': 10})
        # self.assertRaises(KayleeError, Settings, SECRET_KEY=123)
        # self.assertRaises(KayleeError, Settings, SECRET_KEY='abc')

        # self.assertIsNone(_validate({
        #     'SECRET_KEY': ' ',
        #     'AUTO_GET_ACTION' : True
        # }))


kaylee_suite = load_tests([KayleeLoaderTests])
