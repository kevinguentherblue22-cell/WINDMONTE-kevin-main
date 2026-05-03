import os
import pickle
import tkinter as tk
from tkinter import filedialog

import matplotlib.pyplot as plt
import numpy as np

# Specify the pickle files to load here.
# Use absolute paths or paths relative to this script.
file_paths = [
     r"output_data_Design_A.pkl",
     r"output_data_Design_B.pkl",
     r"output_data_Design_C.pkl",
     r"output_data_Design_D.pkl"
]

# Optional legend labels for each file. If left empty, filenames will be used.
legend_labels = [
     "Design A",
     "Design B",
     "Design C",
     "Design D"
]


def load_pickle_run_data(file_path):
    """Load a pickle file and return the RunData object."""
    with open(file_path, 'rb') as f:
        loaded = pickle.load(f)

    if isinstance(loaded, (tuple, list)) and len(loaded) == 3:
        # Some pickle files are saved as [RunData, U_systematic, U_random].
        # The second and third entries are not list-like in that case.
        if not isinstance(loaded[1], (list, tuple, dict)) and not isinstance(loaded[2], (list, tuple, dict)):
            return loaded[0]
    return loaded


def extract_uncertainty_vs_x(run_data, xvar, yvar):
    """Extract x and uncertainty magnitude y values from RunData."""
    plotpoints = range(2, len(run_data) - 1)
    x = [run_data[i][xvar].nom for i in plotpoints]
    y = [run_data[i][yvar].U for i in plotpoints]
    return np.array(x), np.array(y)


def plot_overlay_uncertainties(file_paths, legend_labels=None, xvar='AOA', yvars=('CD', 'CL')):
    """Overlay uncertainty magnitudes for multiple RunData pickle files."""
    if len(file_paths) == 0:
        print('No files selected.')
        return

    if legend_labels is None or len(legend_labels) != len(file_paths):
        legend_labels = [os.path.basename(fp) for fp in file_paths]

    fig, axes = plt.subplots(1, len(yvars), figsize=(14, 5), squeeze=False)

    for file_path, label in zip(file_paths, legend_labels):
        try:
            run_data = load_pickle_run_data(file_path)
        except Exception as exc:
            print(f'Failed to load {file_path}: {exc}')
            continue

        for ax, yvar in zip(axes[0], yvars):
            try:
                x, y = extract_uncertainty_vs_x(run_data, xvar, yvar)
            except Exception as exc:
                print(f'Failed to extract {yvar} from {file_path}: {exc}')
                continue

            ax.plot(x, y, linewidth=2, label=label)
            ax.set_title(f'{yvar} uncertainty vs {xvar}')
            ax.set_xlabel(xvar)
            ax.set_ylabel('Uncertainty magnitude')
            ax.grid(True, linestyle=':', alpha=0.6)
            ax.legend(fontsize='small')

    fig.tight_layout()
    plt.show()


def select_files_and_plot():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(
        title='Select one or more pickle files',
        filetypes=[('Pickle files', '*.pkl'), ('All files', '*.*')]
    )
    if file_paths:
        plot_overlay_uncertainties(file_paths)
    else:
        print('No files selected.')


if __name__ == '__main__':
    if len(file_paths) > 0:
        plot_overlay_uncertainties(file_paths, legend_labels)
    else:
        select_files_and_plot()
