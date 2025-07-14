import pandas as pd
import matplotlib.pyplot as plt
import re
from collections import defaultdict

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

# Preview cleaned text
df[['Designer', 'cleaned_review']].head()

from collections import Counter

# Basic list of English stop words
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

# Combine all words
all_words = ' '.join(df['cleaned_review']).split()

# Filter out stop words
filtered_words = [word for word in all_words if word not in stop_words]

# Count the most common remaining words
word_freq = Counter(filtered_words)

# Initialize counts
category_counts = defaultdict(int)

color_words = {
    'white', 'black', 'red', 'pink', 'blue', 'green', 'beige', 'brown', 'yellow',
    'orange', 'grey', 'gray', 'purple', 'gold', 'silver', 'neon', 'ivory', 'nude',
    'metallic', 'cream', 'navy', 'khaki', 'pastel', 'pastels'
}

fabric_words = {
    'cotton', 'linen', 'leather', 'denim', 'silk', 'satin', 'wool', 'lace',
    'tulle', 'knit', 'chiffon', 'sheer', 'mesh', 'velvet', 'organza', 'jersey',
    'tweed', 'fur', 'suede', 'nylon', 'cottons', 'transparent', 'wool', 'wools'
}

silhouette_words = {
    'fitted', 'oversized', 'voluminous', 'structured', 'flowy', 'cinched',
    'asymmetrical', 'draped', 'tailored', 'boxy', 'cropped', 'highwaisted',
    'pleated', 'puff', 'flared', 'layered', 'shift', 'sheath', 'wrap', 'slip'
}

piece_words = {
    'shorts', 'top', 'tops', 'jacket', 'jackets', 'jorts', 'dresses',
    'blouse', 'blouses', 'skirt', 'skirts', 'tank', 'tanks', 'boot', 'boots', 
    'hat', 'hats', 'heels', 'sneakers', 'trainers', 'glasses', 'sunglasses', 'scarf',
    'scarves', 'cargo', 'pants', 'jeans', 'blazer', 'blazers', 'tee', 'tees', 'sweater', 
    'sweaters', 't-shirt'
}

# Go through each word
for word in filtered_words:
    if word in color_words:
        category_counts['Color'] += 1
    elif word in fabric_words:
        category_counts['Fabric'] += 1
    elif word in silhouette_words:
        category_counts['Silhouette'] += 1
    elif word in piece_words:
        category_counts["Pieces"] += 1


color_counts = Counter([word for word in filtered_words if word in color_words])
fabric_counts = Counter([word for word in filtered_words if word in fabric_words])
silhouette_counts = Counter([word for word in filtered_words if word in silhouette_words])
piece_counts = Counter([word for word in filtered_words if word in piece_words])

# Sort by number of looks
df_sorted = df.sort_values(by='Num Looks', ascending=False)

# Create bar chart
def looks_per_designer():
    plt.figure(figsize=(12, 6))
    plt.bar(df_sorted['Designer'], df_sorted['Num Looks'])

    plt.title('Number of Looks per Designer – Spring 2026')
    plt.xlabel('Designer')
    plt.ylabel('Number of Looks')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def plot_bar(counts, title, color=None):
    items = dict(counts.most_common(10))
    plt.figure(figsize=(10, 5))
    plt.bar(items.keys(), items.values(), color=color)
    plt.title(title)
    plt.xlabel('Keyword')
    plt.ylabel('Mentions')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    looks_per_designer()

    # keyword bar charts
    plot_bar(color_counts, 'Top Color Mentions', color='salmon')
    plot_bar(fabric_counts, 'Top Fabric Mentions', color='lightblue')
    plot_bar(silhouette_counts, 'Top Silhouette Mentions', color='plum')
    plot_bar(piece_counts, 'Top Clothing Item Mentions', color='lightgreen')

main()