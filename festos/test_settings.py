from settings import *

MEDIA_ROOT = '/tmp/media'
DOCVIEWER_DOCUMENT_ROOT = join(MEDIA_ROOT, 'docs/')

#STATICFILES_STORAGE = 'django_pipeline_forgiving.storages.PipelineForgivingStorage'
STATICFILES_STORAGE = 'pipeline.storage.NonPackagingPipelineStorage'
PIPELINE_ENABLED = False

#CELERY_EAGER_PROPAGATES_EXCEPTIONS=True
#CELERY_ALWAYS_EAGER=True
#BROKER_BACKEND='default'

#TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'
