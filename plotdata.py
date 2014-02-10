'''
    plotdata.py
    plotting function, to be called by pycard.py
'''
import matplotlib.pyplot as plt
import numpy as np

def plot_sizedistr(data, root):
    sizes = []
    for item in data:
        if data[item].st_size > 0:
            sizes.append(np.log(data[item].st_size))
        else:
            sizes.append(0)
    bins = range(3,22)

    plt.xticks(bins, ["$2^{%s}$" % i for i in bins])
    plt.hist(sizes, bins, normed=True, log=True);

    ax = plt.axes() 
    ax.yaxis.grid() #horizontal lines
    plt.xlabel('File Size in Bytes')
    plt.ylabel('Frequency (log)')
    title = 'File Size Frequency in {}'.format(root)
    plt.title(title)
    plt.show()
