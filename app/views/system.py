# -*- coding: utf-8 -*-
import json
import os
import subprocess
import psutil
from datetime import datetime
from flask import Blueprint, jsonify

mod = Blueprint('system', __name__)


@mod.route('/info')
def get_system_info():
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    temp = os.popen('vcgencmd measure_temp').readline().replace("temp=", "").replace('\'C\n', '')
    mem = psutil.virtual_memory()
    net = psutil.net_io_counters()
    swap = psutil.swap_memory()
    disk = psutil.disk_partitions()

    info = {'uptime': str(uptime).split('.')[0],
            'load': os.getloadavg(),
            'temp': temp,
            'net': {'recv': net.bytes_recv,
                    'sent': net.bytes_sent},
            'memory': {'used': mem.total - mem.available,
                       'total': mem.total},
            'swap': {'used': swap.used,
                     'total': swap.total}
            }
    if len(disk) > 2:
        part = disk[2]
        disk_usg = psutil.disk_usage(part.mountpoint)
        info['disk'] = {'device': part.device,
                        'mount': part.mountpoint,
                        'total': disk_usg.total,
                        'used': disk_usg.used
                        }

    return json.dumps(info)


@mod.route('/shutdown')
def shutdown():
    subprocess.call(["sudo", "halt"])
    return jsonify({'status': 0})


@mod.route('/reboot')
def reboot():
    subprocess.call(["sudo", "reboot"])
    return jsonify({'status': 0})
