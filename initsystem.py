"""
Manage services.
Supports SystemV init or systemd.
Example:

```
>>> from initsystem import Service
>>> couchdb = Service('couchdb')
>>> couchdb.is_running()
False
>>> couchdb.start()
>>> couchdb.is_running()
True
>>> couchdb.stop()
>>> couchdb.is_running()
False
```
"""
from typing import *
import subprocess

def determine_initsystem() -> Optional[str]:
    """
    Gets the init system in use by getting the PID 1 process' name
    """
    p1 = subprocess.run(['ps', '-p1'], capture_output=True).stdout.decode()
    if 'systemd' in p1:
        return 'systemd'
    elif 'init' in p1:
        return 'systemv'

class Service:
    def __init__(self, name: str) -> None:
        self.name = name
        self.init_system = determine_initsystem()
        if self.init_system is None:
            raise NotImplementedError(f'Current init system is not supported. Please use systemd or systemv init')
    
    def start(self) -> bool:
        """
        Starts the service
        """
        subprocess.run(self._get_command('start')).check_returncode()
    
    def stop(self) -> bool:
        """
        Stops the service
        """
        subprocess.run(self._get_command('stop')).check_returncode()
    
    def is_running(self) -> bool:
        """
        Check if the service is running.
        """
        if self.init_system == 'systemd':
            # Need to search in stdout for systemd
            stdout = subprocess.run(self._get_command('status'), capture_output=True).stdout.decode()
            return 'Active: active' in stdout
        elif self.init_system == 'systemv':
            # SystemV init just returns wheether the service is 
            # running or not in the return code
            return subprocess.run(self._get_command('status')).returncode == 0
        else:
            raise NotImplementedError(f'Current init system is not supported. Please use systemd or systemv init')

    def _get_command(self, action: str) -> List[str]:
        """
        Constructs a list of commands to give to subprocess.run
        """
        if self.init_system == 'systemd':
            return ['sudo', 'systemctl', action, self.name]
        elif self.init_system == 'systemv':
            return ['sudo', 'service', self.name, action]