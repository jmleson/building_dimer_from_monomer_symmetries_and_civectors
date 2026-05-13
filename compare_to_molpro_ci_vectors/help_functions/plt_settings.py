import matplotlib.pyplot as my_plt
import matplotlib.font_manager as fm


font_path = '/usr/share/fonts/truetype/ancient-scripts/Symbola_hint.ttf'  # Beispiel: '/usr/share/fonts/truetype/Symbola.ttf'
prop = fm.FontProperties(fname=font_path)
fm.fontManager.addfont(font_path)


main_text_size = 11.6# herausgefunden per textblock / overlay of figure and text in latex
minor_text_size = main_text_size - 2
footnote_text_size = 11
my_plt.rcParams.update({
    'font.family': ['DejaVu Sans', 'Noto Sans Symbols'],
    'font.size': main_text_size,          # Grund-Schriftgröße (alle Texte)
    'text.usetex': True,
    'text.latex.preamble' : r'''
        \usepackage{graphicx}
        \usepackage{mathtools}
    ''',
})
my_plt.xticks(rotation=45)


legend_kwargs = dict(
    labelspacing=0.25,
    handlelength=1.2,
    handletextpad=0.4,
    columnspacing=0.9,
    borderpad=0.3,
    markerscale=0.85,
)
# -> use per:   legend = ax.legend(**legend_kwargs)

default_figure_height = 4.8
default_figure_width = 6.4



def blend_colors(c1, c2, alpha=0.5):
    if alpha > 0.5:
        raise Exception('alpha > 0.5')
    r = alpha * c1[0] + alpha * c2[0]
    g = alpha * c1[1] + alpha * c2[1]
    b = alpha * c1[2] + alpha * c2[2]
    return (r, g, b)
