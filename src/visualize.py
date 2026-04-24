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

    bars = ax.barh(df["player_name"], df["performance_score"], color="#1a73e8", edgecolor="none")

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


def plot_xg_vs_goals(player_stats_df, min_shots=3, save=True):
    """
    Scatter plt - xG per 90 vs goals per 90.
    Size = total shots. Highlights undervalued players.
    """
    df = player_stats_df[player_stats_df["total_shots"] >= min_shots].copy()

    fig, ax = plt.subplots(figsize=(10, 7))

    scatter = ax.scatter(
        df["xg_p90"],
        df["goals_p90"],
        s = df["total_shots"] * 8,
        aplha = 0.6,
        color = "#1a73e8",
        edgecolors = "white",
        linewidths = 0.5
    )

    #Reference line - goals = xG (perfect conversion)
    max_val = max(df["xg_p90"].max(), df["goals_p90"].max()) + 0.01
    ax.plot([0, max_val], [0, max_val], color="gray", linestyle="--", linewidth=1, labels="Goals = xG (average conversion)")

    #Label top players by performance score
    top = df.nlargest(5, "performance_score")
    for _, row in top.iterrows():
        ax.annotate(    
            row["player_name"].split()[0],      #first name only to avoid clutter
            (row["xg_p90"], row["goals_p90"]),
            textcoords = "offset points",
            xytext = (6, 4),
            fontsize = 8,
            color = "333333"
        )
    
    ax.set_xlabel("xG per 90 min", fontsize = 11)
    ax.set_ylabel("Goals per 90 min", fontsize = 11)
    ax.set_title("xG per 90 vs Goals per 90\n(bubble size = total shots)", fontsize = 13, fontweight = "bold")
    ax.legend(fontsize = 9)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        path = os.path.join(VISUALS_PATH, "xg_vs_goals.png")
        plt.savefig(path, dpi = 150, bbox_inches = "tight")
        print(f"Chart saved: {path}")
    
    plt.show()


def plt_undervalued_players(undervalued_df, save=True):
    """
    Bar chart - undervalued players ranked by xG per 90.
    Shows xG vs actual goals side by side.
    """
    df = undervalued_df.sort_values("xg_p90", ascending = True).copy()

    fig, ax = plt.subplots(figsize = (10, 5))

    y = range(len(df))
    bar_height = 0.35

    ax.barh([i + bar_height / 2 for i in y], df["xg_p90"], height = bar_height, label = "xG per 90", color = "#1a73e8", edgecolor = "none")
    ax.barh([i - bar_height / 2 for i in y], df["goals_p90"], height = bar_height, label = "Goals per 90", color = "#34a853", edgecolor = "none")

    ax.set_yticks(list(y))
    ax.set_ytickslabels(df["player_name"], fontsize = 9)
    ax.set_xlabel("Per 90 minutes", fontsize = 11)
    ax.set_title("Undervalued Players - xG vs Goals per 90", fontsize = 13, fontweight = "bold")
    ax.legend(fontsize = 9)
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()

    if save:
        path = os.path.join(VISUALS_PATH, "undervalued_players.png")
        plt.savefig(path, dpi = 150, bbox_inches = "tight")
        print(f"Chart saved: {path}")

    plt.show()