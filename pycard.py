#!/usr/bin/python

import .path as path, os
import argparse

def _makeparser():
  parser = argparse.ArgumentParser()
  parser.add_argument("rootdir", help="specifies root directory for traversal")
  parser.add_argument("-m","--maxfiles", help="max number of files to traverse over",
      type=int)
  return parser

class enterprise:
  """treks through the filesystem, collecting data!"""
  
  # avgsize, maxsize, minsize, total = 0,0,0,0
  log = {}
  data = { 
            'totalnum':   0, 
            'totalsize':  0,
            'maxbreadth': 0, 
            'maxdepth':   0, 
            'average':    0
         }

  def logfile(self,item):
    """logs files encountered during trek()"""
    self.data['totalnum'] += 1
    self.log[item] = os.stat(item)  # create a log entry about "item"
    
  def analyze(self):
    """analyzes file data in log"""
    totalsize = 0
    log = self.log
    data = self.data

    if not log:
      print "log is empty."
      return

    for item in log:
      data['totalsize'] += log[item].st_size

      currentdepth = item.count(os.sep)               # count '/' chars in filepath
      if currentdepth > data['maxdepth']: 
        data['maxdepth'] = currentdepth

    data['average'] = data['totalsize'] / data['totalnum']
    self.data = data
    return

  def trek(self, directory, maxfiles):
    """recursively traverses the file system, starting at 'directory'"""
    for item in os.listdir(directory):
      try:
        itempath = path.join(directory,item)
        if not path.islink(itempath):                                 # dont follow symlinks
          if path.isdir(itempath):                                    # follow directories
            self.trek(itempath,maxfiles)
          elif maxfiles == None or self.data['total'] < maxfiles:     # dont exceed max
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
  e.trek(root, args.maxfiles)

  print 'analyzing results...'
  e.analyze()

  print 'traversal from {} shows:'.format(root)
  print "   total file count \t=  {}".format(e.data['totalnum'])
  print "   total size \t\t=  {} bytes".format(e.data['totalsize'])
  print "   average size \t=  {} bytes".format(e.data['average'])
  print "   max breadth \t\t=  {}".format(e.data['maxbreadth'])
  print "   max depth \t\t=  {} directories".format(e.data['maxdepth'])

# standard python boilerplate
if __name__ == '__main__':
  main()
