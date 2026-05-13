from help_functions.format_axis_broken_x import format_axis_broken_x
from help_functions.plt_settings import minor_text_size, my_plt, main_text_size
import re


def latex_bold(s:str):
    if not isinstance(s, str):
        raise Exception("string to format is not str!")
    if "\n" in s:
        parts = s.split("\n")
        return "\n".join([latex_bold(s) for s in parts])
    if "$" in s and not "mathbf" in s:
        s = bold_math(s)
    return r'\textbf{' + str(s)+ r'}'



def bold_math(s: str) -> str:
    if "$" not in s or "mathbf" in s:
        return s
    pattern = re.compile(r'(\$)(.+?)(\$)')
    def repl(match: re.Match) -> str:
        inner = match.group(2)
        if r'\mathbf' in inner:
            return match.group(0)
        return f"${{\\mathbf{{{inner}}}}}$"
    return pattern.sub(repl, s, count=1)


def apply_fonts_ax(fig, ax):
    # x_label_pos = ax.xaxis.label.get_position()

    size_main = main_text_size
    size_ticks = minor_text_size

    # Titel und Achsenlabels
    if ax.title:
        ax.title.set_fontsize(size_main)
        ax.title.set_weight('bold')
    ax.title.set_text(latex_bold(ax.title.get_text()))

    for label, set_label in [(ax.xaxis.label, ax.set_xlabel),
                             (ax.yaxis.label, ax.set_ylabel)]:
        label.set_fontsize(size_main)
        set_label(latex_bold(label.get_text()))
        label.set_weight('bold')

    # Tick-Labels
    for tick in ax.xaxis.get_ticklabels():
        tick.set_fontsize(size_ticks)
        tick.set_weight('bold')
        tick.set_text(latex_bold(tick.get_text()))# does not seem to have much effect
    xticks = ax.get_xticks()
    ax.xaxis.set_major_locator(my_plt.FixedLocator(xticks))
    if len(ax.xaxis.get_ticklabels()) > 0:
        ax.set_xticklabels([latex_bold(t.get_text()) for t in ax.xaxis.get_ticklabels()])
    for tick in ax.yaxis.get_ticklabels():
        tick.set_fontsize(size_ticks)
        tick.set_weight('bold')
        tick.set_text(latex_bold(tick.get_text()))# does not seem to have much effect
    yticks = ax.get_yticks()
    ax.yaxis.set_major_locator(my_plt.FixedLocator(yticks))
    if len(ax.yaxis.get_ticklabels()) > 0:
        ax.set_yticklabels([latex_bold(t.get_text()) for t in ax.yaxis.get_ticklabels()])

    # Legende(n):
    for legend in ax.artists + [ax.get_legend()] + fig.artists:
        if legend:
            # title not bold
            for text in legend.get_texts():
                text.set_fontsize(size_ticks)
                text.set_weight('bold')
                text.set_text(latex_bold(text.get_text()))

    for leg in fig.legends:
        for text in leg.get_texts():
            text.set_fontsize(size_ticks)
            text.set_weight('bold')
            text.set_text(latex_bold(text.get_text()))
    for text_obj in fig.texts:
        text_obj.set_fontsize(size_main)
        text_obj.set_fontweight('bold')
        text_obj.set_text(latex_bold(text_obj.get_text()))

    # ax.xaxis.label.set_position(x_label_pos)


def save_my_figures(name:str, fig=None, bbox_extra_artists:list=[]):
    if "pdf" in name or "png" in name:
        raise Exception("PDF not supposed to be in name, is added automatically")
    if fig is None:
        fig = my_plt.gcf()
    # fig.tight_layout()
    bbox_extra_artists = [b for b in bbox_extra_artists if b is not None]
    fig.savefig(f"{name}.pdf",
                bbox_inches='tight',#<- Plot will occupy maximum of available space
                transparent=True,
                dpi=300, pad_inches=0,
                bbox_extra_artists=bbox_extra_artists#Extra-Elemente berücksichten, wie z.B. Legende
                )
    fig.savefig(f"{name}.png",
                bbox_inches='tight',#<- Plot will occupy maximum of available space
                transparent=True,
                dpi=300, pad_inches=0,
                bbox_extra_artists=bbox_extra_artists#Extra-Elemente berücksichten, wie z.B. Legende
                )




def format_plot(fig, ax, grid_limit=["y", "x"], y_axis=["left"], x_axis=["bottom"]):
    if "bottom" in x_axis:
        format_axis_broken_x(ax)
    if "top" in x_axis:
        format_axis_broken_x(ax)

    for axis in grid_limit:
        ax.grid(True, axis=axis, linestyle=":", alpha=0.4)

    apply_fonts_ax(fig, ax)
