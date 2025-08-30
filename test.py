from analyze import analyze_single_season, compare_seasons
from plot import plot_single_season, plot_compared_seasons

def main():
    counts1 = analyze_single_season("data/spring_2025_ready_to_wear_shows.csv")
    plot_single_season(counts1, "Spring 2025 Ready to Wear")

    #counts1, counts2 = compare_seasons("data/spring_2025_ready_to_wear_shows.csv", "data/spring_2024_ready_to_wear_shows.csv")
    #plot_compared_seasons(counts1, "Spring 2025 RTW", counts2, "Spring 2024 RTW")

main()