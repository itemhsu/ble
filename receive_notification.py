#!/usr/bin/python -u
# -*- mode: python; coding: utf-8 -*-

# Copyright (C) 2014, Oscar Acena <oscaracena@gmail.com>
# This software is under the terms of Apache License v2 or later.

from __future__ import print_function

import sys
from threading import Event
from gattlib import GATTRequester


class Requester(GATTRequester):
    def __init__(self, wakeup, *args):
        GATTRequester.__init__(self, *args)
        self.wakeup = wakeup

    def on_notification(self, handle, data):
        print("- notification on handle: {}\n".format(handle))
        print(data)
        #self.wakeup.set()


class ReceiveNotification(object):
    def __init__(self, address):
        self.received = Event()
        self.requester = Requester(self.received, address, False)

        self.connect()
        self.wait_notification()

    def connect(self):
        print("Connecting...", end=' ')
        sys.stdout.flush()

        #self.requester.connect(True)
        #self.requester.connect(wait=True, channel_type='random')
        self.requester.connect(wait=True)
        print("OK!")

    def wait_notification(self):
        print("\nThis is a bit tricky. You need to make your device to send\n"
              "some notification. I'll wait...")
        self.received.wait()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: {} <addr>".format(sys.argv[0]))
        sys.exit(1)

    ReceiveNotification(sys.argv[1])
    print("Done.")
