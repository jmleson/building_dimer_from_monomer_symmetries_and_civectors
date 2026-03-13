import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FixedLocator, FixedFormatter


def format_axis_broken_x(ax):
    """
    Doppelstriche im 45° Winkel zur x-Achse mit optionalem horizontalen Offset.

    Parameter:
    - offset: Verschiebung der Doppelstriche entlang der x-Achse (Axes-Koordinaten)
    """
    line_length = 0.04
    line_width = 1.5
    gap = 0.0173
    offset = 0.01

    data_min, data_max = ax.dataLim.xmin, ax.dataLim.xmax
    if data_min < 0 < data_max:
        return  # gemischte Daten: keine Unterbrechung

    xmin, xmax = ax.get_xlim()
    if xmin <= 0 <= xmax:
        return
    gap_fraction = 0.04
    x_gap = (xmax - xmin) * gap_fraction

    kwargs = dict(transform=ax.transAxes, color='k', lw=line_width, clip_on=False)

    # 45° Linie: dx = dy
    dx = dy = line_length / np.sqrt(2)

    if data_min >= 0:
        # Positiv: Doppelstrich links
        new_left = xmin - x_gap
        ax.set_xlim(new_left, xmax)
        base = 0.02 + offset  # Abstand von Achse + Offset

        # erster Strich
        x0, x1 = base - dx/2, base + dx/2
        y0, y1 = -dy/2, dy/2
        ax.plot((x0, x1), (y0, y1), **kwargs)

        # zweiter Strich, nur horizontal verschoben
        x0_gap = x0 + gap
        x1_gap = x1 + gap
        ax.plot((x0_gap, x1_gap), (y0, y1), **kwargs)

        # x-Ticks
        xticks = ax.get_xticks()
        tick_positions = [new_left] + [t for t in xticks if t >= xmin]
        tick_labels = ['0'] + [f'{t:g}' for t in xticks if t >= xmin]

    elif data_max <= 0:
        # Negativ: Doppelstrich rechts
        new_right = xmax + x_gap
        ax.set_xlim(xmin, new_right)
        base = 1 - 0.02 - offset  # Abstand von Achsenende - Offset

        # erster Strich
        x0, x1 = base - dx/2, base + dx/2
        y0, y1 = -dy/2, dy/2
        ax.plot((x0, x1), (y0, y1), **kwargs)

        # zweiter Strich, nur horizontal verschoben
        x0_gap = x0 - gap
        x1_gap = x1 - gap
        ax.plot((x0_gap, x1_gap), (y0, y1), **kwargs)

        # x-Ticks
        xticks = ax.get_xticks()
        tick_positions = [t for t in xticks if t <= xmax] + [new_right]
        tick_labels = [f'{t:g}' for t in xticks if t <= xmax] + ['0']

    ax.xaxis.set_major_locator(FixedLocator(tick_positions))
    ax.xaxis.set_major_formatter(FixedFormatter(tick_labels))



if __name__ == "__main__":
    # INFO     TEST CASES
    y = np.arange(5)

    # --- Negativ ---
    x_neg = np.array([-70, -65, -60, -55, -50])
    fig, ax = plt.subplots()
    ax.plot(x_neg, y, marker='o')
    format_axis_broken_x(ax)
    plt.title("Negativ, Doppelstrich rechts")
    plt.show()

    # --- Gemischt ---
    x_mix = np.array([-20, -10, 0, 10, 20])
    fig, ax = plt.subplots()
    ax.plot(x_mix, y, marker='o')
    format_axis_broken_x(ax)
    plt.title("Gemischt, keine Unterbrechung")
    plt.show()
