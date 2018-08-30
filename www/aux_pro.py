import os
import signal
import subprocess


class Process(object):
    process = None

    """start_process: comienza el proceso si no estaba iniciado
    
    Returns:
        [int] -- Devuelve el pid (id de proceso) del proceso iniciado/existente
    """
    def start_process(self):
        if self.process == None:
            cmd = "python process.py"
            self.process = subprocess.Popen(cmd.split(), preexec_fn=os.setsid)
        return self.process.pid
    
    """stop_process: finaliza el proceso si estaba iniciado
    """

    def stop_process(self):
        if self.process != None:
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process = None

    """is_running: verifica si el proceso estaba iniciado
    
    Returns:
        [boolean] -- True si el proceso esta corriendo / False si no
    """
    def is_running(self):
        return self.process != None
