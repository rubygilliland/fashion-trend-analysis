import pandas as pd
import glob, os
import matplotlib.pyplot as plt
from analyze import get_counts
from collections import Counter
import numpy as np

def classify_trend(values):
    values = [int(v) for v in values]
    if len(values) < 2:
        return "Steady"
    slope = np.polyfit(range(len(values)), values, 1)[0]
    if slope > 0.1:
        return "Rising"
    elif slope < -0.1:
        return "Declining"
    else:
        return "Steady"

def get_clean_rev(csv_path):
    """
    Reads the Cleaned Review column from a CSV and returns as a single string.
    """
    df = pd.read_csv(csv_path)
    clean_review = ' '.join([str(r) for r in df['Cleaned Review'].dropna()])
    return clean_review

def analyze_trends(file_pattern_or_list, category):
    # Determine input type
    if isinstance(file_pattern_or_list, list):
        files = file_pattern_or_list
    else:
        files = glob.glob(file_pattern_or_list)
        if os.path.isdir(file_pattern_or_list):
            files = glob.glob(os.path.join(file_pattern_or_list, "*.csv"))

    files.sort()
    season_order = []
    all_items = set()

    for f in files:
        review = get_clean_rev(f)
        counts = get_counts(review)
        season_order.append(counts)
        cat_counts = counts.get(category, Counter())
        all_items.update(cat_counts.keys())

    trends = {}
    for item in all_items:
        values = [sum(cat_counts.get(item, 0) for cat_counts in counts.values())
                  for counts in season_order]
        trends[item] = classify_trend(values)

    return trends, season_order

def plot_trends(trends, season_order, category):
    categories = ['Rising', 'Steady', 'Declining']
    colors = {'Rising': 'green', 'Steady': 'gray', 'Declining': 'red'}
    n_seasons = len(season_order)

    fig, axes = plt.subplots(1, 3, figsize=(20, 6), sharex=False)

    for ax, cat in zip(axes, categories):
        items = [item for item, trend_type in trends.items() if trend_type == cat]

        if not items:
            ax.set_title(f"{cat} Trends (none)")
            ax.axis("off")
            continue

        # compute total mentions for each item to select top 5
        total_mentions = {}
        for item in items:
            total_mentions[item] = sum(sum(cat_counts.get(item, 0) for cat_counts in counts.values())
                                       for counts in season_order)

        top_items = sorted(total_mentions.items(), key=lambda x: x[1], reverse=True)[:5]

        # sort last points to prevent overlapping labels
        last_points = []
        for item, _ in top_items:
            y = [sum(cat_counts.get(item, 0) for cat_counts in counts.values())
                 for counts in season_order]
            last_points.append((item, y[-1]))
        last_points.sort(key=lambda x: x[1])
        offset_step = max(1, max([lp[1] for lp in last_points]) * 0.02)

        max_count = 0
        for i, (item, last_y) in enumerate(last_points):
            y = [sum(cat_counts.get(item, 0) for cat_counts in counts.values())
                 for counts in season_order]
            x = np.arange(1, n_seasons+1)
            max_count = max(max_count, max(y, default=0))

            ax.plot(x, y, marker='o', color=colors[cat], alpha=0.7)

            offset = i * offset_step
            ax.text(
                x[-1]+0.1, y[-1]+offset,
                item,
                fontsize=8, color=colors[cat],
                verticalalignment='bottom'
            )

        ax.set_title(f"{cat} Trends (Top 5)")
        ax.set_ylabel("Mentions")
        ax.set_ylim(0, max_count + 1)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_xticks(np.arange(1, n_seasons+1))
        ax.set_xticklabels([str(i) for i in range(1, n_seasons+1)])
        ax.set_xlabel("Seasons Index")
        fig.suptitle(category.capitalize() + ' Trends Across ' + str(n_seasons) + ' Seasons', 
                   fontsize = 14, y = 0.99)

    plt.tight_layout()
    plt.show()


def run_fashion_trend_analysis(file_pattern_or_list, category):
    """
    Wrapper function: analyze trends for a specific category and plot results.
    Parameters:
        file_pattern_or_list: list of CSV paths or a glob pattern like 'data/*.csv'
        category: string, e.g. 'colors', 'patterns', 'fabrics', etc.
    Returns:
        trends: dict mapping item -> trend type
        season_order: list of counts per season
    """
    trends, season_order = analyze_trends(file_pattern_or_list, category)
    plot_trends(trends, season_order, category)
    return trends, season_order

run_fashion_trend_analysis("data/*.csv", "colors")
