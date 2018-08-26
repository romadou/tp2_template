import os
import signal
import subprocess


class Process(object):
    process = None

    """start_process: start process 
    if there isn't any other process started
    
    Returns:
        [int] -- Return the pid (process id) if the process start correctly / None if there is a process started before
    """

    def start_process(self):
        if self.process == None:
            cmd = "python process.py"
            self.process = subprocess.Popen(cmd.split(), preexec_fn=os.setsid)
            return self.process.pid
        return None
    
    """stop_process: kill the process if there is a process executed
    """

    def stop_process(self):
        if self.process != None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process = None

    """is_running: confirms if the process has already been started
    
    Returns:
        [boolean] -- Return true if the process was started / false if the process was not started before
    """
    def is_running(self):
        return self.process != None
