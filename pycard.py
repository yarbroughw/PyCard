#!/usr/bin/python

import os.path as path, os
import argparse
import time
import plotdata

def _makeparser():
  parser = argparse.ArgumentParser()
  parser.add_argument("rootdir", help="specifies root directory for traversal")
  parser.add_argument("-m","--maxfiles", help="max number of files to traverse over",
                        type=int)
  return parser

class enterprise:
  """treks through the filesystem, collecting data!"""
  
  log = {}
  data = { 
            'totalnum':   0, 
            'totalsize':  0,
            'maxdepth':   0, 
            'average':    0,
            'maxsize':    0,
            'minsize':    0
            
         }

  def logfile(self,item):
    """logs files encountered during trek()"""
    self.data['totalnum'] += 1
    self.log[item] = os.stat(item)                    # create a log entry about "item"
    
  def analyze(self):
    """returns metadata taken from log"""
    totalsize = 0
    log = self.log
    data = self.data
    data['minsize'] = log[log.keys()[0]].st_size

    if not log:
      print "log is empty."
      return

    for item in log:
      currentsize = log[item].st_size
      data['totalsize'] += currentsize                # update total size count

      currentdepth = item.count(os.sep)               # count '/' chars in filepath to measure depth
      if currentdepth > data['maxdepth']: 
        data['maxdepth'] = currentdepth               # update max depth if biggest
      if currentsize > data['maxsize']: 
        data['maxsize'] = currentsize                 # update max depth if biggest
      if currentsize < data['minsize']: 
        data['minsize'] = currentsize                 # update max depth if biggest

    data['average'] = data['totalsize'] / data['totalnum']
    self.data = data
    return

  def printdata(self):
    """prints results of analyze()"""  
    print "   total file count \t=  {}".format(self.data['totalnum'])
    print "   total size \t\t=  {} bytes ({:.2f} MB)".format(self.data['totalsize'], 
                                                    self.data['totalsize']/float(1048576))
    print "   average size \t=  {} bytes ({:.2f} MB)".format(self.data['average'], 
                                                    self.data['average']/float(1048576))
    print "   max file size \t=  {} bytes ({:.2f} MB)".format(self.data['maxsize'], 
                                                    self.data['maxsize']/float(1048576))
    print "   min file size \t=  {} bytes ({:.2f} MB)".format(self.data['minsize'], 
                                                    self.data['minsize']/float(1048576))
    print "   max depth \t\t=  {} directories".format(self.data['maxdepth'])

  def trek(self, directory, maxfiles):
    """recursively traverses the file system, starting at 'directory'"""
    for item in os.listdir(directory):
      try:
        itempath = path.join(directory,item)
        if not path.islink(itempath):                                 # dont follow symlinks
          if path.isdir(itempath):                                    # follow directories
            self.trek(itempath,maxfiles)
          elif maxfiles == None or self.data['totalnum'] < maxfiles:  # dont exceed max (from args)
            self.logfile(itempath)
          else:                                                       # otherwise, return
            return
      except OSError:
        pass  # skip permissions errors

def main():
  parser = _makeparser()
  args = parser.parse_args()

  e = enterprise()

  root = path.abspath(args.rootdir)
  print 'traversing file system with {} as root...'.format(root)
  t1 = time.time()
  e.trek(root, args.maxfiles)
  t2 = time.time()
  print 'traversing the file system took %0.3f ms.' % ((t2-t1)*1000.0)

  print 'analyzing results...'
  e.analyze()
  print "traversal from {} shows:".format(root)
  e.printdata()

  print 'generating graph...'
  plotdata.plot_sizedistr(e.log, args.rootdir)

# standard python boilerplate
if __name__ == '__main__':
  main()
