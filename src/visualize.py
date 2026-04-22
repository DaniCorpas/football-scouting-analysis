import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import os

#Output folder for saved charts
VISUALS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "visuals"
)
os.makedirs(VISUALS_PATH, exist_ok=True)

def plot_top_players(player_stats_df, top_n=10, save=True):
    """
    Bar chart - top N players by performance score
    """
    df = player_stats_df.head(top_n).copy()
    df = df.sort_values("performance_score", ascending=True)  # Sort for better visualization

    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(df["player_name"], df["performance_score"], color="#166ad8", edgecolor="none")

    #Add value labels inside bars
    for bar in bars:
        width = bar.get_width()
        ax.text(width - 0.01, bar.get_y() + bar.get_height() / 2,
                f"{width:.3f}", va="center", ha="right", color="white", fontsize=9)
        
    ax.set_xlabel("Performance Score", fontsize=11)
    ax.set_title(f"Top {top_n} Players by Performance Score", fontsize=13, fontweight="bold")
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        path = os.path.join(VISUALS_PATH, "top_players.png")
        plt.savefig(path, dpi=150, bbox_inches="tight")
        print(f"Chart saved: {path}")

    plt.show()

    