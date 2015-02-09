"""
Bar chart demo with pairs of bars grouped for easy comparison.
"""
import numpy as np
import matplotlib.pyplot as plt

class Plot:
  def plotBar(self, x, y1, y2, y3, title):

    n_groups = len(x) 

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = plt.bar(index, y1, bar_width,
                     alpha=opacity,
                     color='b',
                     #yerr=std_men,
                     error_kw=error_config,
                     label='Total')

    rects2 = plt.bar(index + bar_width, y2, bar_width,
                     alpha=opacity,
                     color='r',
                     #yerr=std_women,
                     error_kw=error_config,
                     label='Chinese as first author')

    rects2 = plt.bar(index + bar_width, y3, bar_width,
                     alpha=opacity,
                     color='g',
                     #yerr=std_women,
                     error_kw=error_config,
                     label='Chinese as coauthor')

    plt.xlabel('year')
    plt.ylabel('number')
    plt.title(title)

    plt.xticks(index + bar_width, x)
    plt.legend(loc='upper left')

    plt.tight_layout()
    plt.show()

def main():
  plot = Plot()
  xlist  = [2001, 2002, 2003]
  y1list = [100, 200, 300]
  y2list = [10, 30, 70]
  plot.plotBar(xlist, y1list, y2list, "test")

if __name__ == '__main__':
  main()
