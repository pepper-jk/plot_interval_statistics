import matplotlib.pyplot as plt
import numpy as np

import development_matplotlib.paper_plots as pp

def savepdfviasvg(fig, name, **kwargs):
    import subprocess
    fig.savefig(name + ".svg", format="svg", **kwargs)
    incmd = ["inkscape", name + ".svg", "--export-pdf={}.pdf".format(name),
                "--export-pdf-version=1.5"]  # "--export-ignore-filters",
    subprocess.check_output(incmd)

def autolabel(ax, rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 0.985*height,
                '{}'.format(height), ha=ha[xpos], va='bottom')

def plot_bars(data: list(dict({str: dict}))=None, plot_name: str="bar", ylabel: str=None, xlabel: str=None, annotate: bool=False, legend: bool=True) -> bool:
    """
    Plot dataset entropies.

    :param data: a list of dictionaries containing entropies from multiple entropies
    :param plot_name: name of the output file
    :return: True on success and False on failure
    """

    # default data for testing
    if data is None:
        print("Error: no data")
        return False

    types = []
    # FIXME: workaround, since data[0].keys() does not work
    for key in data.keys():
        types += list(data[key].keys())
        break

    # use the Garcia preset
    pp.pre_paper_plot(True)

    fig, ax = plt.subplots()

    ind = np.arange(start=0, stop=2*(len(types)), step=2)
    plt.xticks(ind)
    width = 0.24
    if annotate:
        width = width*3.5
    half = int(len(data)/2)
    add = -half
    bars = []
    for values in data.values():
        bars.append(ax.bar(ind+width*add, list(values.values()), width))
        add = add + 1

    # label bars
    if annotate:
        for rects in bars:
            autolabel(ax, rects)

    # label
    if plot_name.lower().find("entropy") != -1:
        ylabel = "Entropy"
        if plot_name.lower().find("normalized") != -1:
            ylabel = "Normalized Entropy"
    if ylabel != None:
        ax.set_ylabel(ylabel)
    if xlabel != None:
        ax.set_xlabel(xlabel)
    #ax.set_title(plot_name)
    ax.set_xticklabels(types)

    # use the Garcia preset
    pp.post_paper_plot(change=True, bw_friendly=True, adjust_spines=False, sci_y=False)

    # legend
    if legend:
        ax.legend(bars, data.keys(), bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)

    # plot
    filename = plot_name.lower().replace(" ", "_")
    savepdfviasvg(fig, filename, dpi=300, bbox_inches='tight')
    #plt.savefig(filename, dpi=300, bbox_inches='tight', format='pdf')

    return True

def plot_lines(data: dict(dict({str: list}))=None, plot_name: str="line", limiter=[0,-1], ylabel: str=None, xlabel: str=None, annotate: bool=False, legend: bool=True) -> bool:


    # default data for testing
    if data is None:
        print("Error: no data")
        return False

    # use the Garcia preset
    pp.pre_paper_plot(True)

    fig, ax = plt.subplots()

    for key, values in data.items():
        if limiter != [0,-1]:
            xvalues = range(limiter[0]+1,limiter[-1]+1)
        else:
            xvalues = range(1,len(list(values)))
        ax.plot(xvalues,values[limiter[0]:limiter[-1]], label=key.replace("_", " "))

    #ls = np.linspace(float(min(values[:100])),float(max(values[:100])),num=6)
    #print(ls)

    #plt.ylim(0.0,1)

    xlabel = 'Time Windows'
    if limiter != [0,-1]:
        xlabel += ' (limited)'
    ax.set_xlabel(xlabel)
    ax.set_ylabel(plot_name.replace("_", " "))
    if ylabel != None:
        ax.set_ylabel(ylabel)

    # use the Garcia preset
    pp.post_paper_plot(change=True, bw_friendly=True, adjust_spines=False, sci_y=False)

    # legend
    if legend:
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)

    # plot
    filename = plot_name.lower().replace(" ", "_")
    if limiter != [0,-1]:
        filename += '_limited'
    savepdfviasvg(fig, filename, dpi=600, bbox_inches='tight')

    return True

def plot_multi_lines(data: dict(dict({str: list}))=None, attributes: dict()=None, plot_name: str="line", limiter: list=[0,-1], vline: list=[], ylabel: str=None, xlabel: str=None, annotate: bool=False, legend: bool=True) -> bool:

    # default data for testing
    if data is None:
        print("Error: no data")
        return False

    # use the Garcia preset
    pp.pre_paper_plot(True)

    plt.rcParams['figure.figsize'] = (8, 4)

    i = 1
    for attr, name in attributes.items():
        ax = plt.subplot(len(attributes.items()), 1, i)
        for key, values in data[attr].items():
            if limiter != [0,-1]:
                xvalues = range(limiter[0]+1,limiter[-1]+1)
            else:
                xvalues = range(1,len(list(values)))
            plt.xlim(xvalues[0],xvalues[-1])
            plt.plot(xvalues,values[limiter[0]:limiter[-1]], label=key.replace("_", " "))
        for x in vline:
            plt.axvline(x, color='tab:gray', alpha=.75)

        title = name.replace("_", " ")
        if ylabel != None:
            title = ylabel
        plt.text(0.01, 0.5, title,
                 horizontalalignment='left',
                 verticalalignment='center',
                 transform = ax.transAxes)

        # legend
        if i == 1 and legend:
            plt.legend(bbox_to_anchor=(0., 1.2, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)

        if i != len(attributes.items()):
            plt.tick_params(
                axis='x',          # changes apply to the x-axis
                which='both',      # both major and minor ticks are affected
                bottom=False,      # ticks along the bottom edge are off
                top=False,         # ticks along the top edge are off
                labelbottom=False) # labels along the bottom edge are off

        i += 1

    xlabel = 'Time Windows'
    if limiter != [0,-1]:
        xlabel += ' (limited)'
    plt.xlabel(xlabel)

    # use the Garcia preset
    pp.post_paper_plot(change=True, bw_friendly=True, adjust_spines=False, sci_y=False)

    # plot
    filename = plot_name.lower().replace(" ", "_")
    if limiter != [0,-1]:
        filename += '_limited'

    import subprocess
    plt.savefig(filename + ".svg", format="svg")
    incmd = ["inkscape", filename + ".svg", "--export-pdf={}.pdf".format(filename),
                "--export-pdf-version=1.5"]  # "--export-ignore-filters",
    subprocess.check_output(incmd)

    return True
