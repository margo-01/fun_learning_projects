import numpy as np
from pathlib import Path

from dataclasses import dataclass, field


@dataclass
class Job:
    material: str 
    directory: str
    comment: str

class JobTracker: 
    def __init__(self):
        pass
    
    
    
    
    def add_job():
        jobs = []
        while True:
            material = input("Material:")
            directory = input("Main directory:")
            comment = input("Comment:")
            new_job = Job(material=material, directory=Path(directory), comment=comment)
            jobs.append(new_job)
            next_job = input("Add another job?  [y/n]")
            start_over = input("Start over? [y/n]")
            if start_over.lower() == "y":
                continue
            if next_job.lower() == "n":
                break
            
        return jobs
    
    
    