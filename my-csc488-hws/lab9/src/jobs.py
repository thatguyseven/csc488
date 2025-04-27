import uuid
from hotqueue import HotQueue
import redis
import os

redisIP = os.environ.get('REDIS_IP', '172.17.0.1')
q = HotQueue("queue", host=redisIP, port=6379, db=1) 
rd = redis.StrictRedis(host=redisIP, port=6379, db=0) 

def generate_jid(): 
    """ 
    Generate a pseudo-random identifier for a job. 
    """ 
    return str(uuid.uuid4()) 

def _generate_job_key(jid): 
    """ 
    Generate the redis key from the job id to be used when storing, retrieving or updating 
    a job in the database. 
    """ 
    return 'job.{}'.format(jid) 

def instantiate_job(jid, status, start, end): 
    """ 
    Create the job object description as a python dictionary. Requires the job id, status, 
    start and end parameters. 
    """ 
    if type(jid) == str: 
        return {'id': jid, 
        'status': status, 
        'start': start, 
        'end': end 
        } 
    return {'id': jid.decode('utf-8'), 
    'status': status.decode('utf-8'), 
    'start': start.decode('utf-8'), 
    'end': end.decode('utf-8') 
    } 

def get_job_by_id(jid):
    """
    Retrieve a job from the Redis database by its job id.
    Returns the job dictionary if found, otherwise None.
    """
    job_key = _generate_job_key(jid)
    # Retrieve all fields and values for the hash stored at job_key
    job_data = rd.hgetall(job_key)

    # hgetall returns an empty dictionary if the key does not exist
    if not job_data:
        return None

    decoded_job_data = {
        key.decode('utf-8'): value.decode('utf-8')
        for key, value in job_data.items()
    }

    if all(field in decoded_job_data for field in ['id', 'status', 'start', 'end']):
        return instantiate_job(
            decoded_job_data.get('id'),
            decoded_job_data.get('status'),
            decoded_job_data.get('start'),
            decoded_job_data.get('end')
        )
    else:
        # Handle case where the retrieved hash doesn't contain expected fields
        print(f"Warning: Job data for {jid} is incomplete.")
        return None

def _save_job(job_key, job_dict): 
    """Save a job object in the Redis database.""" 
    rd.hset(job_key, mapping=job_dict) 
 
def _queue_job(jid): 
    """Add a job to the redis queue.""" 
    q.put(jid)
 
def add_job(start, end, status="submitted"): 
    """Add a job to the redis queue.""" 
    jid = generate_jid() 
    job_dict = instantiate_job(jid, status, start, end) 
    _save_job(_generate_job_key(jid), job_dict) 
    _queue_job(jid) 
    return job_dict 
 
 
def update_job_status(jid, status): 
    """Update the status of job with job id `jid` to status `status`.""" 
    job = get_job_by_id(jid) 
    if job: 
        job['status'] = status 
        _save_job(_generate_job_key(jid), job) 
    else: 
        raise Exception()