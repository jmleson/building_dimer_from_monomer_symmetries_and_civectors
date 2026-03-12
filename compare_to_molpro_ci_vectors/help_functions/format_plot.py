
import matplotlib.pyplot as my_plt



def apply_fonts_ax(fig, ax):
    size_main = 12
    size_ticks = 10
    # Titel und Achsenlabels
    if ax.title:
        ax.title.set_fontsize(size_main)
        ax.title.set_weight('bold')
    ax.xaxis.label.set_fontsize(size_main)
    ax.xaxis.label.set_weight('bold')
    ax.yaxis.label.set_fontsize(size_main)
    ax.yaxis.label.set_weight('bold')

    # Tick-Labels
    for tick in ax.xaxis.get_ticklabels():
        tick.set_fontsize(size_ticks)
        tick.set_weight('bold')
    for tick in ax.yaxis.get_ticklabels():
        tick.set_fontsize(size_ticks)
        tick.set_weight('bold')

    # Legende
    leg = ax.get_legend()
    if leg:
        for text in leg.get_texts():
            text.set_fontsize(size_ticks)
            text.set_weight('bold')

    for text_obj in fig.texts:
        text_obj.set_fontsize(size_main)
        text_obj.set_fontweight('bold')


def save_my_figures(name:str, fig=None, bbox_extra_artists:list=[]):
    if "pdf" in name:
        raise Exception("PDF not supposed to be in name, is added automatically")
    if fig is None:
        fig = my_plt.gcf()
    # fig.tight_layout()
    fig.savefig(f"{name}.pdf",
                bbox_inches='tight',#<- Plot will occupy maximum of available space
                transparent=True,
                dpi=300, pad_inches=0,
                bbox_extra_artists=bbox_extra_artists#Extra-Elemente berücksichten, wie z.B. Legende
                )


def format_plot(fig, ax):
    ax.grid(True, linestyle=":", alpha=0.4)
    apply_fonts_ax(fig, ax)