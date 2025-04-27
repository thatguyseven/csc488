from jobs import q, update_job_status
import time

@q.worker # fill in 
def execute_job(jid): 
    """ 
    Retrieve a job id from the task queue and execute the job. 
    Monitors the job to completion and updates the database accordingly. 
    """ 
    # fill in ... 
    # the basic steps are: 
    # 1) get job id from message and update job status to indicate that the job has started 
    update_job_status(jid, "in progress")
    # 2) start the analysis job and monitor it to completion. 
    time.sleep(15)
    # 3) update the job status to indicate that the job has finished. 
    update_job_status(jid, "complete")