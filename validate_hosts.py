#!/usr/bin/env python3

import curses
import dns.resolver
import itertools
import pathlib
import socket
import sys


#### Global Variables
file_pattern = 'list.*'
stdscr = curses.initscr()

def cast_curses():
  #### curses intiator(s)
  # TODO: Actually make use of curses  
  curses.noecho()
  curses.cbreak()
  stdscr.keypad(True)


def lift_curses():
  curses.echo()
  curses.nocbreak()
  stdscr.keypad(False)

#### the "I'm still doing stuff" thingy
spinner = itertools.cycle(['|','/','-','\\'])


#### Functions
def dns_query(hostname):
  resolver = dns.resolver.Resolver(configure=False)
  resolver.nameservers = ['1.1.1.1']
  try:
    dns_data =  resolver.resolve(hostname)
    return True
  except:
    return False


#### MAIN
hosts_path = pathlib.Path('/etc/pihole/')
hosts_files = tuple(hosts_path.glob(file_pattern))
cast_curses()
try:
  for file_path in hosts_files:
    with file_path.open() as fi:
      host_lines = [line.rstrip('\n') for line in fi]
      for line in host_lines:
        out_str = str(next(spinner)) + " " + str(line) + "\r"
        out_len = len(out_str)
        sys.stdout.write(out_str)
        sys.stdout.flush()
        if dns_query(line) == False:
          write_data = "sed /" + str(line) + "/d " + str(file_path) + "\n"
          with open("results.txt", "a") as fo:
            fo.write(write_data)
        blank = str(" " * out_len) + "\r"
        sys.stdout.write(blank)
        sys.stdout.flush()
except:
  lift_curses()
  sys.exit()
finally:
  lift_curses()