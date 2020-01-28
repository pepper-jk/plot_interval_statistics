import matplotlib.pyplot as plt
import numpy as np

import development_matplotlib.paper_plots as pp

def savepdfviasvg(fig, name, **kwargs):
    import subprocess
    fig.savefig(name + ".svg", format="svg", **kwargs)
    incmd = ["inkscape", name + ".svg", "--export-pdf={}.pdf".format(name),
                "--export-pdf-version=1.5"]  # "--export-ignore-filters",
    subprocess.check_output(incmd)

def plot(data: list(dict({str: dict}))=None, plot_name: str="bar", ylabel: str=None, xlabel: str=None) -> bool:
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
    half = int(len(data)/2)
    add = -half
    bars = []
    for values in data.values():
        bars.append(ax.bar(ind+width*add, list(values.values()), width))
        add = add + 1

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
    ax.legend(bars, data.keys(), bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=4, mode="expand", borderaxespad=0.)

    # plot
    filename = plot_name.lower().replace(" ", "_")
    savepdfviasvg(fig, filename, dpi=300, bbox_inches='tight')
    #plt.savefig(filename, dpi=300, bbox_inches='tight', format='pdf')

    return True
