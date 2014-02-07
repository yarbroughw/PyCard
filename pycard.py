#!/usr/bin/python

from os import listdir, chdir
import sys, os.path

class enterprise:
  """treks through the filesystem, collecting data!"""
  
  avgsize, maxsize, minsize, total = 0,0,0,0

  def __init__(self):
    return

  def logfile(self,item):
    # update avg size
    # check if max?
    # check if min?
    self.total += 1
    print item
    # check depth? 

  def trek(self,directory):
    for item in listdir(directory):
      try:
        itempath = os.path.join(directory,item)
        if os.path.isdir(itempath) and not os.path.islink(itempath):
          self.trek(itempath)
        else:
          self.logfile(itempath)
      except OSError:
        print "OSError"
        pass

def main():
  root = '~'
  root = os.path.expanduser(root)
  e = enterprise()
  e.trek(root)
  print '{} files, total.'.format(e.total)

# standard python boilerplate
if __name__ == '__main__':
  main()
