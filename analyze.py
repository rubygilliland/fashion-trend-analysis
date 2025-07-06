import pandas as pd

# Load the data
df = pd.read_csv('data/spring_2026_shows.csv')

# Preview
# print(df.columns)
# df.head()

import re

def clean_text(text):
    text = str(text).lower()  # make lowercase
    text = re.sub(r'[^a-z\s]', '', text)  # remove punctuation and numbers
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

# View the top 30
print(word_freq.most_common(30))

from collections import defaultdict

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

# Print results
print("Category Frequency:")
for category, count in category_counts.items():
    print(f"{category}: {count}")

color_hits = [word for word in filtered_words if word in color_words]
fabric_hits = [word for word in filtered_words if word in fabric_words]
silhouette_hits = [word for word in filtered_words if word in silhouette_words]
piece_hits = [word for word in filtered_words if word in piece_words]

print("Top Colors:", Counter(color_hits).most_common(10))
print("Top Fabrics:", Counter(fabric_hits).most_common(10))
print("Top Silhouettes:", Counter(silhouette_hits).most_common(10))
print("Top Pieces: ", Counter(piece_hits).most_common(10))
