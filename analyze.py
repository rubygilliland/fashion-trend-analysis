import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib import rc
import re
from collections import Counter


# removes numbers and punctuation of words in "review" column of csv
def clean_text(text):

    # make lowercase
    text = str(text).lower()  

    # remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', '', text)  
    return text

# common color descriptors
color_words = {
    'white', 'black', 'red', 'pink', 'blue', 'green', 'beige', 'brown', 'yellow',
    'orange', 'grey', 'gray', 'purple', 'gold', 'silver', 'neon', 'ivory', 'nude',
    'metallic', 'cream', 'navy', 'khaki', 'pastel', 'pastels', 'blush', 'butteryellow',
    'mocha', 'rose', 'fuchsia', 'coral', 'peach', 'teracotta', 'maroon', 'burgundy',
    'lavender', 'lilac', 'periwinkle', 'mauve', 'maud', 'plum', 'teal', 'turquoise,'
    'aqua', 'mint', 'seafoam', 'olive', 'forestgreen', 'moss', 'sage', 'camel', 'rust',
    'ochre', 'mustard', 'sand', 'bronze', 'copper', 'charcoal', 'midnight', 'aubergine', 
    'ink', 'wine', 'cerulean', 'skyblue', 'dustyblue', 'babypink', 'babyblue', 
    'wispypink', 'dustypink', 'mintgreen', 'chocolatebrown'
}

# common fabric descriptors
fabric_words = {
    'cotton', 'linen', 'leather', 'denim', 'silk', 'satin', 'wool', 'lace',
    'tulle', 'knit', 'chiffon', 'sheer', 'mesh', 'velvet', 'organza', 'jersey',
    'tweed', 'fur', 'suede', 'nylon', 'cottons', 'transparent', 'wool', 'wools'
    'cashmere', 'shearling', 'organza', 'jacquard', 'brocade', 'crepe', 'corduroy',
    'canvas', 'netting', 'fleece', 'nylon', 'polyester', 'spandex', 'PVC', 'vinyl,'
    'lycra', 'neoprene', 'taffeta', 'terrycloth', 'modal'
}

# common silhouette descriptors
silhouette_words = {
    'fitted', 'oversized', 'voluminous', 'structured', 'flowy', 'cinched',
    'asymmetrical', 'draped', 'tailored', 'boxy', 'cropped', 'high waisted',
    'pleated', 'puff', 'flared', 'layered', 'shift', 'sheath', 'wrap', 'slip',
    'streamlined', 'relaxed', 'sculptural', 'ball gown', 'empire', 'mermaid',
    'column', 'trumpet', 'peplum', 'biascut', 'wideleg', 'bootcut', 'straightleg',
    'skinny', 'tapered', 'lowrise', 'baggy', 'caped', 'strapless', 'low-rise'
    'offtheshoulder', 'dolman', 'raglan', 'high-waisted', 'off-the-shoulder',
    'mini', 'maxi', 'midi', 'bodycon'
}

# common piece descriptors
piece_words = {
    'shorts', 'top', 'tops', 'jacket', 'jackets', 'jorts', 'dresses',
    'blouse', 'blouses', 'skirt', 'skirts', 'tank', 'tanks', 'boot', 'boots', 
    'hat', 'hats', 'heels', 'sneakers', 'trainers', 'glasses', 'sunglasses', 'scarf',
    'scarves', 'cargo', 'pants', 'jeans', 'blazer', 'blazers', 'tee', 'tees', 'sweater', 
    'sweaters', 't-shirt', 'vest', 'sweatshirt', 'sweatshirts', 'microshorts', 'micro-shorts'
    'coat', 'coats', 'trench', 'trenchcoat', 'overcoat', 'cardigan', 'cardigans',
    'bralette', 'bodysuit', 'gown', 'kimono', 'parka', 'pullover', 'romper', 'jumpsuit',
    'suit', 'suits', 'cape', 'cloak', 'glove', 'gloves', 'loafer', 'loafers', 'mule', 'mules',
    'sandals', 'slides', 'slippers', 'clogs', 'turtleneck', 'turtlenecks', 'legging', 'leggings',
    'miniskirt', 'mini-skirt', 'miniskirts', 'mini-skirts', 
}

# common details
details_words = {
    'buttons', 'zippers', 'snaps', 'ties', 'hookandeye', 'lacing', 'buckles', 'drawstrings',
    'pleats', 'darts', 'slits', 'cutouts', 'ruching', 'gathering', 'draping', 'boning',
    'vents', 'padding', 'seams', 'paneling', 'piping', 'tie-dye', 'ruched', 'graphics'
    'ruffles', 'frills', 'bows', 'feathers', 'sequins', 'beads', 'crystals', 'graphic',
    'embroidery', 'applique', 'fringe', 'studs', 'grommets', 'rosettes', 'quilting', 'smocking',
    'rawedges', 'distressing', 'metallicfinish', 'highshine', 'matte', 'gloss',
    'fading', 'tiedye', 'prints', 'patterns', 'patchwork', 'lasercut', 'flocking'
}

# common patterns
pattern_words = {
    'floral', 'paisley', 'plaid', 'tartan', 'houndstooth', 'check', 'gingham',
    'stripe', 'pinstripe', 'polkadot', 'dot', 'animalprint', 'leopard', 'zebra', 'snake',
    'camouflage', 'camo', 'geometric', 'abstract', 'tie-dye', 'ombre',
    'graphic', 'logo', 'monogram', 'text', 'artprint', 'patchwork', 'colorblock',
    'laceprint', 'brocade', 'ikat', 'chevron', 'marble', 'swirl', 'wave',
    'mesh', 'net', 'grid', 'argyle', 'jacquard', 'printmixing'
}

# gets counts for all words in a category (color, fabric, etc.)
def get_counts(review):
    review_lst = review.split()

    # creates keywords dictionary for easy looping
    keywords = {'colors': color_words, 'fabrics': fabric_words, 'silhouettes': silhouette_words, 
                'pieces': piece_words, 'patterns': pattern_words, 'details': details_words}
    
    counts = {}

    # iterates over every keywords collection
    for name, category in keywords.items():

        # counts num of words mentioned in each keyword group
        num = Counter([word for word in review_lst if word in category])

        # adds to counts dictionary for each word
        counts[name] = num

    return counts

# organizes and plots category data for single given dataset/season
def top_category_mentions(review, season):

    # sets font for display
    rc('font', **{'family': "Times New Roman"}) 

    # configures display grid for multiple data plots
    fig, axes = plt.subplots(nrows = 2, ncols = 3, figsize = (12, 8))

    # adds a title to the grid
    fig.suptitle('Top Fashion Keywords in ' + season + ' Runway Reviews', fontsize=16, y=0.99)

    # plots data on grid for all categories
    counts = get_counts(review)
    plot_data(axes[0, 0], counts.get('colors'), 'Color Mentions', '#FFEDF1', False)
    plot_data(axes[0, 1], counts.get('fabrics'), 'Fabric Mentions', '#EBCFCC', False)
    plot_data(axes[0, 2], counts.get('details'), 'Detail Mentions', '#EADCDC', False)
    plot_data(axes[1, 0], counts.get('silhouettes'), 'Silhouette Mentions', '#E8D6D4', False)
    plot_data(axes[1, 1], counts.get('pieces'), 'Clothing Item Mentions', '#F4EBE9', False)
    plot_data(axes[1, 2], counts.get('patterns'), 'Pattern Mentions', '#FFEDED', False)

    plt.tight_layout()
    plt.show()

# organizes, plots, and compares top data from two datasets/seasons
def compare_mentions(review_1, season_1, review_2, season_2):

    # sets font for display
    rc('font', **{'family': "Times New Roman"}) 

    # configures display grid for multiple data plots
    fig, axes = plt.subplots(nrows = 2, ncols = 3, figsize = (12, 8))

    # adds title to grid
    fig.suptitle('Comparison of Top Fashion Keywords in ' + season_1 + ' and ' + season_2 + ' Runway Reviews', 
                   fontsize = 16, y = 0.99)
    
    # gets counters for each review
    counts_1 = get_counts(review_1)
    counts_2 = get_counts(review_2)

    # plots data for each keyword category for both reviews
    plot_data(axes[0, 0], counts_1.get('colors'), 'Top Colors', '#FFEDF1', True, counts_2.get('colors'))
    plot_data(axes[0, 1], counts_1.get('fabrics'), 'Top Fabrics', '#FFEDF1', True, counts_2.get('fabrics'))
    plot_data(axes[0, 2], counts_1.get('details'), 'Top Details', '#FFEDF1', True, counts_2.get('details'))
    plot_data(axes[1, 0], counts_1.get('silhouettes'), 'Top Silhouettes', '#FFEDF1', True, counts_2.get('silhouettes'))
    plot_data(axes[1, 1], counts_1.get('pieces'), 'Top Pieces', '#FFEDF1', True, counts_2.get('pieces'))
    plot_data(axes[1, 2], counts_1.get('patterns'), 'Top Patterns', '#FFEDF1', True, counts_2.get('patterns'))

    plt.tight_layout()
    plt.show()
    
    
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

# cleans up review text
def get_clean_rev(csv_path):

    # reads in review from csv
    df = pd.read_csv(csv_path)

    # changes review to cleaned review using clean_text function
    df['Cleaned Review'] = df['Review'].apply(clean_text)

    # creates text of clean review
    clean_review = ' '.join([str(r) for r in df['Cleaned Review'].dropna()])
    return clean_review

# used to analyze a single season
def analyze_season(csv_path, season):
    clean_review = get_clean_rev(csv_path)
    top_category_mentions(clean_review, season)

# used to compare two seasons
def compare_seasons(csv_path_1, season_1, csv_path_2, season_2):
    clean_review_1 = get_clean_rev(csv_path_1)
    clean_review_2 = get_clean_rev(csv_path_2)
    compare_mentions(clean_review_1, season_1, clean_review_2, season_2)


def main():
    # Load the data

    #analyze_season('data/spring_2025_shows.csv', 'Spring 2025')
    #analyze_season('data/spring_2024_ready_to_wear_shows.csv', 'Spring 2024')

    compare_seasons('data/spring_2024_ready_to_wear_shows.csv', 'Spring 2024', 'data/spring_2025_shows.csv', 'Spring 2025')

main()
