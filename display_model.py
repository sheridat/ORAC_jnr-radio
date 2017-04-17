#!/usr/bin/env python
"""
$Id: display_model.py,v 1.9 2017/03/08 18:30:14 bob Exp $

Author: Chris Hager <chris@linuxuser.at>
License: MIT
URL: https://github.com/metachris/raspberrypi-utils

Modified by: Bob Rathbone  (bob@bobrathbone.com)
Site   : http://www.bobrathbone.com

License: GNU V3, See https://www.gnu.org/copyleft/gpl.html

Disclaimer: Software is provided as is and absolutly no warranties are implied or given.
            The authors shall not be liable for any loss or damage however caused.

This script detects a Raspberry Pi's model, manufacturer and mb ram, based
on the cpu revision number. Data source:
http://elinux.org/RPi_HardwareHistory

You can instantiate the ModelInfo class either with a parameter `rev_hex`
(eg. `m = ModelInfo("000f")`), or without a parameter
(eg. `m = ModelInfo()`) in which case it will try to detect it via
`/proc/cpuinfo`. Accessible attributes:


    class ModelInfo:
        model = ''     # 'A' or 'B'
        revision = ''  # '1.0' or '2.0'
        ram_mb = 0     # integer value representing ram in mb
        maker = ''     # manufacturer (eg. 'Qisda')
        info = ''      # additional info (eg. 'D14' removed)


"""
import re


# From http://elinux.org/RPi_HardwareHistory
model_data = {
    '2': ('B', '1.0', 256, 'Cambridge', ''),
    '3': ('B', '1.0', 256, 'Cambridge', 'Fuses mod and D14 removed'),
    '4': ('B', '2.0', 256, 'Sony', ''),
    '5': ('B', '2.0', 256, 'Qisda', ''),
    '6': ('B', '2.0', 256, 'Egoman', ''),
    '7': ('A', '2.0', 256, 'Egoman', ''),
    '8': ('A', '2.0', 256, 'Sony', ''),
    '9': ('A', '2.0', 256, 'Qisda', ''),
    'd': ('B', '2.0', 512, 'Egoman', ''),
    'e': ('B', '2.0', 512, 'Sony', ''),
    'f': ('B', '2.0', 512, 'Qisda', ''),
    '10': ('B+', '1.0', 512, 'Sony', ''),
    '11': ('Compute Module 1', '1.0', 512, 'Sony', ''),
    '12': ('A+', '1.1', 256, 'Sony', ''),
    '13': ('B+', '1.2', 512, 'Unknown', ''),
    '14': ('Compute Module 1', '1.0', 512, 'Embest', ''),
    '15': ('A+', '1.0', 512, 'Embest', '256MB or 512MB'),
    'a01040': ('2B', '1.0', 1024, 'Sony', ''),
    'a01041': ('2B', '1.1', 1024, 'Embest', ''),
    'a21041': ('2B', '1.1', 1024, 'Embest', ''),
    'a22042': ('2B', '1.2', 1024, 'Embest', 'with BCM2837'),
    'a02082': ('3B', '2.0', 1024, 'Sony', 'Quad Core 1.2MHz, Onboard WiFi and Bluetooth 4.1'),
    'a22082': ('3B', '2.0', 1024, 'Embest', 'Quad Core 1.2MHz, Onboard WiFi and Bluetooth 4.1'),
    'a02082': ('3B', '1.2', 1024, 'Sony', 'Quad Core 1.2MHz, Onboard WiFi and Bluetooth 4.1'),
    'a020a0': ('Compute Module 3', '1.0', 1024, 'Sony', 'and CM3 Lite'),
    'a22082': ('3B', '1.2', 1024, 'Embest', 'Quad Core 1.2MHz, Onboard WiFi and Bluetooth 4.1'),
    'a32082': ('3B', '1.2', 1024, 'Sony (Japan)', 'Quad Core 1.2MHz, Onboard WiFi and Bluetooth 4.1'),
    '900091': ('A+', '1.1', 512, 'Sony', ''),
    '900092': ('Pi Zero', '1.2', 512, 'Sony', ''),
    '900093': ('Pi Zero', '1.3', 512, 'Sony', ''),
    '920093': ('Pi Zero', '1.3', 512, 'Embest', ''),
    '9200c1': ('Pi Zero W', '1.1', 512, 'Sony', 'Onboard WiFi and Bluetooth 4.1'),
}


class ModelInfo(object):
    """
    You can instantiate ModelInfo either with a parameter `rev_hex`
    (eg. `m = ModelInfo("000f")`), or without a parameter
    (eg. `m = ModelInfo()`) in which case it will try to detect it via
    `/proc/cpuinfo`
    """
    model = ''
    revision = ''
    ram_mb = 0
    maker = ''
    info = ''

    def __init__(self, rev_hex=None):
        if not rev_hex:
            with open("/proc/cpuinfo") as f:
                cpuinfo = f.read()
            rev_hex = re.search(r"(?<=\nRevision)[ |:|\t]*(\w+)", cpuinfo) \
                    .group(1)

        self.revision_hex = rev_hex[-4:] if rev_hex[:4] == "1000" else rev_hex
        try:
                self.model, self.revision, self.ram_mb, self.maker, self.info = \
                        model_data[rev_hex.lstrip("0")]
        except:
                print "Unknown model", rev_hex.lstrip("0")

    def __repr__(self):
        s = "%s: Model %s, Revision %s, RAM: %s MB, Maker: %s%s" % ( \
                self.revision_hex, self.model, self.revision, self.ram_mb, \
                self.maker, ", %s" % self.info if self.info else "")
        return s




if __name__ == "__main__":
    m = ModelInfo()
    print(m)

