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

def plot(data: list(dict({str: dict}))=None, plot_name: str="bar", ylabel: str=None, xlabel: str=None, annotate: bool=False, legend: bool=True) -> bool:
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
        width = width*2
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
