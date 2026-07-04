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
        self.jobs = []
    
    
    
    def job_list(self):
        while True:
            add_new = input("Add another job? [y/n]").strip().lower()
            if add_new != 'y':
                break
            else: 
                self.jobs(self.terminal_job())
        
    
    def terminal_job():
            material = input("Material:").strip()
            directory = input("Main directory:").strip().expanduser()
            comment = input("Comment:")
            new_job = Job(material=material, directory=Path(directory), comment=comment)          
            return new_job
    
    
    