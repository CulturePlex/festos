from settings import *

MEDIA_ROOT = '/tmp/media'
DOCVIEWER_DOCUMENT_ROOT = join(MEDIA_ROOT, 'docs/')

CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
CELERY_ALWAYS_EAGER=True
BROKER_BACKEND='memory'

#TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
