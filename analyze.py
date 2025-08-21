import pandas as pd
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
def analyze_single_season(csv_path):
    clean_review= get_clean_rev(csv_path)
    keyword_counts = get_counts(clean_review)
    return keyword_counts

# used to analyze and compare two seasons
def compare_seasons(csv_path_1, csv_path_2):
    clean_review_1 = get_clean_rev(csv_path_1)
    keyword_counts_1 = get_counts(clean_review_1)

    clean_review_2 = get_clean_rev(csv_path_2)
    keyword_counts_2 = get_counts(clean_review_2)

    return keyword_counts_1, keyword_counts_2

