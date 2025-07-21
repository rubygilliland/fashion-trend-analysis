import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
from collections import defaultdict
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
    'metallic', 'cream', 'navy', 'khaki', 'pastel', 'pastels'
}

# common fabric descriptors
fabric_words = {
    'cotton', 'linen', 'leather', 'denim', 'silk', 'satin', 'wool', 'lace',
    'tulle', 'knit', 'chiffon', 'sheer', 'mesh', 'velvet', 'organza', 'jersey',
    'tweed', 'fur', 'suede', 'nylon', 'cottons', 'transparent', 'wool', 'wools'
}

# common silhouette descriptors
silhouette_words = {
    'fitted', 'oversized', 'voluminous', 'structured', 'flowy', 'cinched',
    'asymmetrical', 'draped', 'tailored', 'boxy', 'cropped', 'highwaisted',
    'pleated', 'puff', 'flared', 'layered', 'shift', 'sheath', 'wrap', 'slip'
}

# common piece descriptors
piece_words = {
    'shorts', 'top', 'tops', 'jacket', 'jackets', 'jorts', 'dresses',
    'blouse', 'blouses', 'skirt', 'skirts', 'tank', 'tanks', 'boot', 'boots', 
    'hat', 'hats', 'heels', 'sneakers', 'trainers', 'glasses', 'sunglasses', 'scarf',
    'scarves', 'cargo', 'pants', 'jeans', 'blazer', 'blazers', 'tee', 'tees', 'sweater', 
    'sweaters', 't-shirt', 'vest', 'sweatshirt', 'sweatshirts'
}

# gets counts for all words in a category (color, fabric, etc.)
def get_counts(review, category):
    return Counter([word for word in review.split() if word in category])

# gathers and plots category data for given dataset/season
def top_category_mentions(review, season):
    color_counts = get_counts(review, color_words)
    fabric_counts = get_counts(review, fabric_words)
    silhouette_counts = get_counts(review, silhouette_words)
    piece_counts = get_counts(review, piece_words)

    # configures display grid for multiple data plots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # adds a title to the grid
    fig.suptitle('Top Fashion Keywords in ' + season + ' Runway Reviews', fontsize=16, y=0.95)

    # plots data on grid for all categories
    plot_data(axes[0, 0], color_counts, 'Color Mentions', 'salmon')
    plot_data(axes[0, 1], fabric_counts, 'Fabric Mentions', 'lightblue')
    plot_data(axes[1, 0], silhouette_counts, 'Silhouette Mentions', 'pink')
    plot_data(axes[1, 1], piece_counts, 'Clothing Item Mentions', 'lightgreen')

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

# plots given data on grid
def plot_data(ax, counts, title, color):
    items = dict(counts.most_common(10))

    ax.bar(items.keys(), items.values(), color=color)

    ax.set_title(title, fontsize=14)
    
    ax.set_xticks(range(len(items)))
    ax.set_xticklabels(items.keys(), rotation=45, ha='right')
    ax.set_ylabel('Mentions')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))


def main():
    # Load the data
    spring_25 = pd.read_csv('data/spring_2025_shows.csv')
    spring_26 = pd.read_csv('data/spring_2026_shows.csv')

    # add 'Season' column
    spring_25['Season'] = 'Spring 2025'
    spring_26['Season'] = 'Spring 2026'

    # combine data
    combined = pd.concat([spring_25, spring_26], ignore_index=True)
    combined.to_csv('data/all_spring_shows.csv', index=False)

    # clean reviews from each file
    spring_25['Cleaned Review'] = spring_25['Review'].apply(clean_text)
    spring_26['Cleaned Review'] = spring_26['Review'].apply(clean_text)
    combined['Cleaned Review'] = combined['Review'].apply(clean_text)
 
    all_sp25_reviews = ' '.join(spring_25["Cleaned Review"])
    top_category_mentions(all_sp25_reviews, "Spring 2025")

    all_sp26_reviews = ' '.join(spring_26['Cleaned Review'])
    top_category_mentions(all_sp26_reviews, "Spring 2026")

main()