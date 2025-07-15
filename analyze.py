import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import re
from collections import defaultdict
from collections import Counter

# Load the data
df = pd.read_csv('data/spring_2026_shows.csv')

# removes numbers and punctuation of words in "review" column of csv
def clean_text(text):

    # make lowercase
    text = str(text).lower()  

    # remove punctuation and numbers
    text = re.sub(r'[^a-z\s]', '', text)  
    return text

df['cleaned_review'] = df['Review'].apply(clean_text)

# stop words to exlcude from review analysis
stop_words = set([
    'the', 'and', 'of', 'in', 'to', 'a', 'with', 'on', 'at', 'for', 'from',
    'that', 'this', 'it', 'by', 'as', 'was', 'an', 'its', 'is', 'he', 'she',
    'they', 'we', 'are', 'his', 'her', 'or', 'but', 'be', 'not', 'have', 'has',
    'had', 'which', 'you', 'their', 'who', 'i', 'all', 'will', 'more', 'one', 
    'my', 'me', 'look', 'there', 'were', 'end', 'said', 'where', 'into', 'open', 
    'when', 'wanted', 'go', 'going', 'back', 'also', 'only', 'most', 'like', 'them'
    , 'off', 'went', 'over', 'about', 'what', 'so', 'made', 'much', 'time', 'up', 
    'really', 'just', 'out', 'no', 'new', 'now', 'how', 'such', 'even', 'ever'
])

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
    'sweaters', 't-shirt', 'vest'
}

# filters "review" text by removing common filler words
def filter_words():

    # Combine all words
    all_words = ' '.join(df['cleaned_review']).split()

    # Filter out stop words
    filtered_words = [word for word in all_words if word not in stop_words]
    return filtered_words

# gets counts for all words in a category (color, fabric, etc.)
def get_counts(filtered_words, category):
    return Counter([word for word in filtered_words if word in category])


# creates bar chart for looks per designer
def looks_per_designer():

    # Sort by number of looks
    df_sorted = df.sort_values(by='Num Looks', ascending=False)

    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted['Designer'], df_sorted['Num Looks'])

    plt.title('Number of Looks per Designer – Spring 2026')
    plt.xlabel('Designer')
    plt.ylabel('Number of Looks')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_on_ax(ax, counts, title, color):
    items = dict(counts.most_common(10))
    ax.bar(items.keys(), items.values(), color=color)
    ax.set_title(title, fontsize=14)
    ax.set_xticks(range(len(items)))
    ax.set_xticklabels(items.keys(), rotation=45, ha='right')
    ax.set_ylabel('Mentions')
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))


def main():
    filtered_words = filter_words()
    looks_per_designer()

    color_counts = get_counts(filtered_words, color_words)
    fabric_counts = get_counts(filtered_words, fabric_words)
    silhouette_counts = get_counts(filtered_words, silhouette_words)
    piece_counts = get_counts(filtered_words, piece_words)
    
    # keyword bar charts
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    plot_on_ax(axes[0, 0], color_counts, 'Color Mentions', 'salmon')
    plot_on_ax(axes[0, 1], fabric_counts, 'Fabric Mentions', 'lightblue')
    plot_on_ax(axes[1, 0], silhouette_counts, 'Silhouette Mentions', 'pink')
    plot_on_ax(axes[1, 1], piece_counts, 'Clothing Item Mentions', 'lightgreen')

    fig.suptitle('Top Fashion Keywords in Spring 2026 Runway Reviews', fontsize=16, y=1.03)
    plt.tight_layout()
    plt.show()

main()