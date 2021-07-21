import sys
from pathlib import Path
path = str(Path(__file__).parent.resolve())
if path not in sys.path: sys.path.append(path)

from target_attacker import TargetAttacker
from secu_attacker import SecuAttacker
from defender import Defender
from scanner import Scanner

class ProcessorFactory(object):
    @classmethod
    def init(cls, cmd):
        cmd_type = cmd["type"]
        if cmd_type == "defense":
            return Defender(cmd)
        elif cmd_type == "scan":
            return Scanner(cmd)
        elif cmd_type == "attack_target":
            return TargetAttacker(cmd)
        elif cmd_type == 'attack_secu':
            return SecuAttacker(cmd)
        else:
            print("Not implemented")
            exit(1)