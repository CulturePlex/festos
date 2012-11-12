#from celery import Celery
from celery.task import task
from django.core.exceptions import ObjectDoesNotExist

#celery = Celery('tasks', broker='amqp://guest@localhost:5672//')

@task(default_retry_delay=10, max_retries=5)
def task_generate_document(doc_id, task_id=None):
    #import ipdb; ipdb.set_trace()
    from docviewer.helpers import generate_document  
    try:  
        generate_document(doc_id, task_id)
    except ObjectDoesNotExist, e:
        task_generate_document.retry(exc=e)
        

