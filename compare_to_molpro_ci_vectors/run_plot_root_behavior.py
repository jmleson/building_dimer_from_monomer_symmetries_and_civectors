import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from compare_to_molpro_ci_vectors.help_functions.parse_output_file_for_state_dependent_ci_vectors import \
    parse_output_file_for_state_dependent_ci_vectors
from compare_to_molpro_ci_vectors.help_functions.format_plot import format_plot, save_my_figures
from compare_to_molpro_ci_vectors.help_functions.transform_molpro_order_into_own_ordering import \
    transform_molpro_order_into_own_ordering_D2h
from src.latex.format_irred_representations import format_irred_representations


def plot_root_behavior(molecule:str, state:str="4.1", total_fig=None, total_ax=None, color_handles=[], marker_handles=[]):#
    path = f"compare_to_molpro_ci_vectors/data_storage/"

    data = []
    list_of_z_files = list(range(100, 705, 5)) #+ [2000]
    for z in list_of_z_files:
        file = f"{molecule}-x2-CASCI-FICNEVPT2-mult5-ccpVTZ-abstandZ{z}-Plots.out"
        info = parse_output_file_for_state_dependent_ci_vectors(path + file)

        info[state]["Z"] = z
        data.append(info[state])

    df = pd.DataFrame(data)
    df.to_csv(f"compare_to_molpro_ci_vectors/outputs/{molecule}_state{state.replace('.','_')}_behavior.csv", sep=";", index=False)

    if total_fig is None or total_ax is None:
        total_fig, total_ax = plt.subplots()

    single_fig, single_ax = plt.subplots()
    df["Z"] = df["Z"].apply(lambda x: float(x) / 10)
    df.columns = df.columns.str.replace(" ", "", regex=False)
    for col in df.columns:
        if col == "Z":
            continue
        df[col] = df[col].astype(float)

        sorted_occ = transform_molpro_order_into_own_ordering_D2h(col)[0]

        label = ''.join([f"({format_irred_representations(irred)})^{o.replace('a','1')}" for irred, o in sorted_occ.items()])

        if state == "4.1":
            total_ax.plot(df["Z"], df[col],"|", color=get_color(col), markeredgewidth=2)
            marker_handles.append({"style": "|", "label": f"state {state}"})
        elif state == "5.1":
            total_ax.plot(df["Z"], df[col], "-", label="$"+label+"$", color=get_color(col))
            color_handles.append({"style": get_color(col), "label": r"$\mathbf{"+label+"}$"})
            marker_handles.append({"style": "-", "label": f"state {state}"})
        else:
            label = "other states than 4.1 or 5.1"
            handles, labels = total_ax.get_legend_handles_labels()
            mask = abs(df[col]) > 1e-5
            if label not in labels:
                total_ax.plot(df["Z"][mask], df[col][mask], ".", label=label, color="#cccccc", ms=5)
                color_handles.append({"style": "#cccccc", "label": label})
            else:
                total_ax.plot(df["Z"][mask], df[col][mask], ".", label=None, color="#cccccc", ms=5)
                color_handles.append({"style": "#cccccc", "label": label})
            marker_handles.append({"style": ".", "label": "other states"})

        single_ax.plot(df["Z"], df[col], label=r"$\mathbf{" + label + r"}$", color=get_color(col))

    single_ax.set_xlabel(r"Dimer Distance along Z [Å]")
    total_ax.set_xlabel(r"Dimer Distance along Z [Å]")
    single_ax.set_ylabel("Prefactor of CI Vector Component [a.u.]")
    total_ax.set_ylabel("Prefactor of CI Vector Component [a.u.]")
    legend = single_ax.legend(
        title="CI Vector Components",
        loc="center left", bbox_to_anchor=(1.02, 0.5)
    )
    plt.ylim(-0.75,0.75)
    single_ax.set_title(f"state {state}")
    format_plot(fig=single_fig, ax=single_ax)
    save_my_figures(f"compare_to_molpro_ci_vectors/outputs/{molecule}-plot_root{state.replace('.','_')}_behavior",
                    fig=single_fig, bbox_extra_artists=[legend])
    plt.close(single_fig)
    return total_fig , total_ax, color_handles, marker_handles



def get_color(ci_part:str):
    # in molpro order
    if ci_part in ["a22a0aa0", "0aa0a22a"]:
        return "darkgreen"
    if ci_part in ["aaaa0220", "0220aaaa"]:
        return "limegreen"
    if ci_part in ["a2a0a2a0", "0a2a0a2a"]:
        return "pink"
    if ci_part in ["02aa02aa", "aa20aa20"]:
        return "orange"
    if ci_part in ["a2a00a2a", "aa2002aa", "02aaaa20", "0a2aa2a0"]:
        return "blue"




def total_plot_of_root_behaviors(molecule:str, states:list[str]):

    fig, ax = None, None
    color_handles, marker_handles = [], []
    for state in states:
        fig, ax, color_handles, marker_handles = plot_root_behavior(molecule=molecule, state=state,
                                                                    total_fig=fig, total_ax=ax,
                                                                    color_handles=color_handles,
                                                                    marker_handles=marker_handles)

    # remove duplicates of legend entries and sort them:
    color_handles = list({c["label"]: c for c in color_handles}.values())
    color_handles = sorted(
        color_handles,
        key=lambda c: (c["label"].startswith("other"), c["style"])
    )

    marker_handles = list({c["label"]: c for c in marker_handles}.values())
    marker_handles = sorted(
        marker_handles,
        key=lambda c: (c["label"].startswith("other"), c["label"])
    )

    # format legend entries:
    marker_handles = [
        Line2D(
            [0], [0],
            marker=(m["style"] if m["style"] != "-" else None),
            color="black",
            linestyle=("None" if m["style"] != "-" else "-"),
            label=m["label"],
            markeredgewidth=2
        )
        for m in marker_handles
    ]
    color_handles = [
        Patch(color=c["style"], label=c["label"])
        for c in color_handles
    ]

    legend_color = ax.legend(
        handles=color_handles,
        title="CI Vector Components",
        loc="upper center",
        bbox_to_anchor=(0.325, 2.0),
        ncol=1, frameon=True,
        handlelength=1,
        handleheight=1
    )
    ax.add_artist(legend_color)

    legend_marker = ax.legend(
        handles=marker_handles,
        title="States",
        loc="upper center",
        bbox_to_anchor=(0.86, 1.256),
        ncol=1, frameon=True,
        handlelength=1,
        handleheight=1
    )

    # format and save plot:
    format_plot(fig=fig, ax=ax)
    save_my_figures(f"compare_to_molpro_ci_vectors/outputs/{molecule}-TOTALplot_root_behavior",
                    fig=fig, bbox_extra_artists=[legend_color, legend_marker])
    plt.close()
    return


if __name__ == "__main__":
    for molecule in ["C6H6", "C6Cl6", "C6F6"]:

        states = [
            "1.1", "2.1", "3.1", "6.1", "7.1",
                  "1.4", "2.4", "3.4", "4.4", "1.5", "2.5", "3.5",
                  "1.8", "2.8", "3.8", "4.8",
                  "4.1", "5.1"]

        total_plot_of_root_behaviors(molecule=molecule, states=states)