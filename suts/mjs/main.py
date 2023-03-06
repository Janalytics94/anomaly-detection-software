import sys
import random
import urllib.request

from lid_ds.core import Scenario
from lid_ds.core.collector.json_file_store import JSONFileStorage
from lid_ds.sim import gen_schedule_wait_times, Sampler
from lid_ds.core.image import StdinCommand, Image, ExecCommand
from lid_ds.utils.docker_utils import get_ip_address


class MJS(Scenario):
    victim_ip = ""

    def init_victim(self, container, logger):
        pass

    def wait_for_availability(self, container):
        global victim_ip
        victim_ip = get_ip_address(container)
        print(f"Expect victim to be ready @ {victim_ip}")
        return True

if __name__ == '__main__':
    recording_time = int(sys.argv[1])
    exploit_time = 0
    wait_times={}

    storage_services = [JSONFileStorage()]
    victim = Image('victim_mjs')
    exploit = Image("exploit_mjs",
                    command=ExecCommand(
                        ""),
                    init_args="")
    normal = Image("normal_mjs",
                   command=StdinCommand(""),
                   init_args="")

    mjs_scenario = MJS(
        victim=victim,
        normal=normal,
        exploit=exploit,
        wait_times=wait_times,
        warmup_time=3,
        recording_time=recording_time,
        storage_services=storage_services,
        exploit_start_time=exploit_time
    )

    mjs_scenario()

