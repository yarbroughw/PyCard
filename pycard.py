#!/usr/bin/python

from os import listdir, stat
import os.path as path
import argparse

def _makeparser():
  parser = argparse.ArgumentParser()
  parser.add_argument("rootdir", help="specify root directory for traversal")
  return parser

class enterprise:
  """treks through the filesystem, collecting data!"""
  
  avgsize, maxsize, minsize, total = 0,0,0,0
  log = {}

  def logfile(self,item):
    self.log[item] = stat(item)  # create a log entry about "item"
    self.total = len(self.log)
    
  def analyze(self):
    totalsize = 0
    log = self.log
    if not log:
      print "log is empty."
      return False
    for item in log:
      totalsize += log[item].st_size
    return totalsize

  def trek(self,directory):
    for item in listdir(directory):
      try:
        itempath = path.join(directory,item)
        if path.isdir(itempath) and not path.islink(itempath): # dont follow symlinks
          self.trek(itempath)
        else:
          self.logfile(itempath)
      except OSError:
        pass  # skip permissions errors

def main():
  parser = _makeparser()
  args = parser.parse_args()
  root = path.abspath(args.rootdir)
  e = enterprise()
  print 'traversing file system with {} as root...'.format(root)
  e.trek(root)
  print 'analyzing results...'
  totalsize = e.analyze()
  print '{} files, total.'.format(e.total)
  print 'total size = {} bytes.'.format(totalsize) 

# standard python boilerplate
if __name__ == '__main__':
  main()
