import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rc

# organizes and plots category data for single given dataset/season
def plot_single_season(counts, season):

    # re-formats season string
    title_season = season.replace('-', ' ').title()

    # sets font for display
    rc('font', **{'family': "Times New Roman"}) 

    # configures display grid for multiple data plots
    fig, axes = plt.subplots(nrows = 2, ncols = 3, figsize = (12, 8))

    # adds a title to the grid
    fig.suptitle('Top Fashion Keywords in ' + title_season + ' Runway Reviews', fontsize=16, y=0.99)

    # plots data on grid for all categories
    plot_data(axes[0, 0], counts.get('colors'), 'Color Mentions', '#FFEDF1', False)
    plot_data(axes[0, 1], counts.get('fabrics'), 'Fabric Mentions', '#EBCFCC', False)
    plot_data(axes[0, 2], counts.get('details'), 'Detail Mentions', '#EADCDC', False)
    plot_data(axes[1, 0], counts.get('silhouettes'), 'Silhouette Mentions', '#E8D6D4', False)
    plot_data(axes[1, 1], counts.get('pieces'), 'Clothing Item Mentions', '#F4EBE9', False)
    plot_data(axes[1, 2], counts.get('patterns'), 'Pattern Mentions', '#FFEDED', False)

    plt.tight_layout()
    #plt.show()
    return fig

# organizes, plots, and compares top data from two datasets/seasons
def plot_compared_seasons(counts_1, season_1, counts_2, season_2):

    # reformats seasons strings
    title_season_1 = season_1.replace('-', ' ').title()
    title_season_2 = season_2.replace('-', ' ').title()

    # sets font for display
    rc('font', **{'family': "Times New Roman"}) 

    # configures display grid for multiple data plots
    fig, axes = plt.subplots(nrows = 2, ncols = 3, figsize = (12, 8))

    # adds title to grid
    fig.suptitle('Comparison of Top Keywords in ' + title_season_1 + ' vs ' + title_season_2 + ' Runway Reviews', 
                   fontsize = 14, y = 0.99)
    
    # plots data for each keyword category for both reviews
    plot_data(axes[0, 0], counts_1.get('colors'), 'Top Colors', '#FFEDF1', True, counts_2.get('colors'))
    plot_data(axes[0, 1], counts_1.get('fabrics'), 'Top Fabrics', '#FFEDF1', True, counts_2.get('fabrics'))
    plot_data(axes[0, 2], counts_1.get('details'), 'Top Details', '#FFEDF1', True, counts_2.get('details'))
    plot_data(axes[1, 0], counts_1.get('silhouettes'), 'Top Silhouettes', '#FFEDF1', True, counts_2.get('silhouettes'))
    plot_data(axes[1, 1], counts_1.get('pieces'), 'Top Pieces', '#FFEDF1', True, counts_2.get('pieces'))
    plot_data(axes[1, 2], counts_1.get('patterns'), 'Top Patterns', '#FFEDF1', True, counts_2.get('patterns'))

    plt.tight_layout()
    #plt.show()
    return fig
    
    
# plots given data on grid
# counts_2 is optional as is only used when comparing two data sets
def plot_data(ax, counts_1, title, color, compare, counts_2 = {}):

    # for comparing two data sets
    if compare:

        # gets top keywords for current category of each season
        common_1 = counts_1.most_common(1)
        common_2 = counts_2.most_common(1)

        # uses two distinct colors for each season
        colors = [color, '#EBCFCC']

        # plots the bars for each season
        ax.bar(['S1', 'S2'],  [common_1[0][1], common_2[0][1]],  color = colors)

        # adds labels and tickers
        ax.set_xticks(range(2))
        ax.set_xticklabels([common_1[0][0], common_2[0][0]], rotation=45, ha='right')
       
    # for analyzing a single season
    else:

        # gets top 10 words for each keyword category
        items = dict(counts_1.most_common(10))

        # creates bar for each word
        ax.bar(items.keys(), items.values(), color=color)

        # adds labels and tickers
        ax.set_xticks(range(len(items)))
        ax.set_xticklabels(items.keys(), rotation=45, ha='right')

    # adds titles
    ax.set_title(title, fontsize=14)
    ax.set_ylabel('Mentions')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))