import matplotlib.pyplot as plt
import seaborn as sns


def save_plot(fig, path):
    fig.savefig(path, bbox_inches='tight', dpi=150)
