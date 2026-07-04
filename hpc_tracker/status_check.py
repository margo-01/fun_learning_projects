import warnings
from file_read_backwards import FileReadBackwards


def check_CASTEP_output(job):
    run = None
    finished = None
    converged = None
    
    file = list(job.directory.glob("*.castep"))
    if not file: 
        warnings.warn(f"Job in directory: {job.directory} not executed ")
        run = False
    else:
        run = True
        with FileReadBackwards(file, encoding="utf-8") as frb:
            for l in frb:
                if "Peak Memory Use" not in l : 
                    finished = False
                    warnings.warn(f"Job in directory: {job.directory} called but not finished ")

                else:
                    finished = True
                    #convergence keywords for GO and SP
                
    
    return run, finished, converged 



def check_ProjP_output():
    pass

def check_TS_output():
    pass