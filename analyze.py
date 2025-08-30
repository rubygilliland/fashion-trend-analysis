import pandas as pd
import re
from collections import Counter


# removes numbers and punctuation of words in "review" column of csv
def clean_text(text):
    text = str(text).lower()  
    
    # keep letters, spaces, and hyphens (remove numbers & punctuation only)
    text = re.sub(r'[^a-z\s-]', '', text)  
    
    # normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# common color descriptors
color_words = {
    # basics
    'white', 'black', 'red', 'pink', 'blue', 'green', 'beige', 'brown', 'yellow',
    'orange', 'grey', 'gray', 'purple', 'gold', 'silver', 'ivory', 'nude', 'cream',
    'navy', 'khaki', 'neon', 'pastel', 'pastels',

    # warm & soft tones
    'blush', 'butteryellow', 'butter-yellow', 'butter yellow''mocha', 'rose', 'fuchsia', 
    'coral', 'peach', 'terracotta', 'apricot', 'melon', 'cantaloupe', 'strawberry', 
    'raspberry', 'cherry', 'cranberry',

    # dark & rich tones
    'maroon', 'burgundy', 'wine', 'oxblood', 'aubergine', 'plum', 'mahogany', 'brick',
    'rust', 'cinnamon', 'chocolate', 'coffee', 'espresso',
    'chocolatebrown', 'chocolate brown', 'chocolate-brown',

    # light & pastel tones
    'lavender', 'lilac', 'periwinkle', 'mauve',
    'dustypink', 'dusty pink', 'dusty-pink',
    'babypink', 'baby pink', 'baby-pink',
    'babyblue', 'baby blue', 'baby-blue',
    'skyblue', 'sky blue', 'sky-blue',
    'dustyblue', 'dusty blue', 'dusty-blue',
    'wispypink', 'wispy pink', 'wispy-pink',
    'mintgreen', 'mint green', 'mint-green',
    'seafoam', 'buttermint', 'celadon', 'pistachio',

    # jewel tones
    'emerald', 'jade', 'malachite', 'teal', 'turquoise', 'aqua', 'topaz', 'amber',
    'amethyst', 'sapphire', 'ruby', 'garnet', 'opal', 'onyx', 'cobalt', 'ultramarine',

    # earthy & natural
    'olive',
    'forestgreen', 'forest green', 'forest-green',
    'moss', 'hunter', 'fern', 'spruce', 'pine',
    'camel', 'sand', 'taupe', 'stone', 'slate', 'earthy', 'ochre', 'mustard',

    # metals & shine
    'bronze', 'copper', 'charcoal', 'graphite', 'metallic',
    'rosegold', 'rose gold', 'rose-gold',
    'gunmetal', 'pewter', 'platinum', 'chrome', 'brass',

    # dark/neutral spectrum
    'ink', 'midnight', 'obsidian', 'ash', 'smoke', 'storm',
    'pearl', 'eggshell', 'bone', 'antiquewhite', 'antique white', 'antique-white',
    'vintagewhite', 'vintage white', 'vintage-white',

    # trend/fashion shades
    'caramel', 'tangerine', 'saffron', 'chartreuse', 'lime', 'citron', 'neon', 'neons',
    'hotpink', 'hot pink', 'electric blue', 'electricblue', 'azure', 'buttercream', ''
    'dustyrose', 'dusty rose', 'dusty rose'

    # style descriptors
    'muted', 'tonal', 'neutral', 'jeweltone', 'jeweltones', 'jewel-tone', 'jewel tone'
}  

# common fabric descriptors
fabric_words = {
    # natural fibers
    'cotton', 'cottons', 'linen', 'linens', 'silk', 'silks', 'wool', 'wools', 'cashmere',
    'alpaca', 'angora', 'mohair', 'hemp', 'jute', 'ramie',

    # leather & skins
    'leather', 'suede', 'patent', 'alligator', 'crocodile', 'python', 
    'snakeskin', 'shearling', 'sheepskin',

    # denim & casual
    'denim', 'denims', 'chambray', 'canvas', 'corduroy', 'twill',

    # luxe & delicate
    'velvet', 'velvets', 'velour', 'satin', 'satins', 'silk satin', 'silk-satin', 'silksatin',
    'chiffon', 'organza', 'jacquard', 'brocade', 'crepe', 'taffeta', 'georgette',

    # knits & stretch
    'knit', 'knits', 'jersey', 'ribbed', 'spandex', 'lycra', 'modal', 'tencel', 'rayon',
    'viscose', 'bamboo', 'interlock',

    # performance / technical
    'nylon', 'polyester', 'acrylic', 'neoprene', 'elastane', 'microfiber',

    # casual / comfy
    'fleece', 'flannel', 'terrycloth', 'terry', 'sweatshirt', 'sweater',

    # sheer / light
    'lace', 'tulle', 'mesh', 'netting', 'sheer', 'transparent', 'semi-sheer',

    # embellishment / surface
    'sequin', 'sequins', 'beaded', 'embroidered', 'embroidery', 'appliqué', 
    'metallic-thread', 'lamé', 'glitter',

    # faux & imitations
    'fauxfur', 'faux fur', 'faux-fur',
    'pleather', 'veganleather', 'vegan leather', 'vegan-leather',
    'pvc', 'vinyl',

    # others
    'tweed', 'crochet', 'macrame'
}


# common silhouette descriptors
silhouette_words = {
    # fitted vs loose
    'fitted', 'oversized', 'voluminous', 'structured', 'flowy', 'cinched',
    'relaxed', 'boxy', 'baggy', 'streamlined', 'sculptural',

    # cut & drape
    'asymmetrical', 'draped', 'tailored', 'wrap', 'biascut', 'bias-cut',
    'peplum', 'layered', 'pleated', 'puff', 'flared', 'cape', 'caped', 'draping'

    # waist and rise
    'high waisted', 'high-waisted', 'lowrise', 'low-rise', 'mid-rise', 'midrise',

    # leg cuts
    'wideleg', 'wide-leg', 'straightleg', 'straight-leg', 'bootcut', 'skinny', 'tapered',

    # sleeve & shoulder
    'strapless', 'offtheshoulder', 'off-the-shoulder', 'dolman', 'raglan', 'balloon-sleeve',
    'bishop-sleeve', 'puffed-sleeve',

    # dresses & skirts
    'mini', 'midi', 'maxi', 'shift', 'sheath', 'ball gown', 'empire', 'mermaid',
    'column', 'trumpet', 'a-line', 'fit-and-flare', 'peplum-skirt', 'tiered', 'wrap-dress',

    # bodycon & figure-hugging
    'bodycon', 'body-con', 'body conscious', 'slim-fit', 'slim fit',

    # layering & texture silhouettes
    'layered', 'tiered', 'ruffled', 'asymmetric-hem', 'high-low', 'high low',

    # other fashion descriptors
    'bell-sleeve', 'capelet', 'kimono', 'poncho', 'trench', 'shirt-dress', 'shirt dress'
}


# common piece descriptors
piece_words = {
    # tops
    'top', 'tops', 'tee', 'tees', 't-shirt', 'tshirts', 'tank', 'tanks',
    'blouse', 'blouses', 'shirt', 'shirts', 'cropped top', 'cropped-top', 'croppedtop',
    'turtleneck', 'turtlenecks', 'pullover', 'hoodie', 'hoodies', 'sweater', 'sweaters',
    'sweatshirt', 'sweatshirts', 'vest', 'bralette', 'bodysuit', 'cardigan', 'cardigans',

    # bottoms
    'shorts', 'microshorts', 'micro-shorts', 'micro shorts', 'jorts', 'jeans', 'pants', 
    'trousers', 'legging', 'leggings', 'skirt', 'skirts', 'miniskirt', 'mini-skirt',
    'miniskirts', 'mini-skirts', 'cargo pants', 'cargo-pants', 'cargo', 'wide-leg pants',
    'wideleg pants', 'wideleg-pants', 'straight-leg pants', 'straightleg pants',

    # dresses & jumpsuits
    'dress', 'dresses', 'gown', 'maxi dress', 'maxi-dress', 'midi dress', 'midi-dress',
    'wrap dress', 'wrap-dress', 'sheath dress', 'sheath-dress', 'romper', 'jumpsuit', 'suit', 'suits',
    'mini dress', 'minidress', 'mini-dress', 'slip', 'slips'

    # outerwear
    'jacket', 'jackets', 'coat', 'coats', 'trench', 'trench coat', 'trenchcoat', 'overcoat', 
    'parka', 'cape', 'cloak', 'blazer', 'blazers', 'poncho', 'kimono', 'duster',

    # footwear
    'boot', 'boots', 'heel', 'heels', 'sneaker', 'sneakers', 'trainer', 'trainers', 
    'loafer', 'loafers', 'mule', 'mules', 'sandals', 'slides', 'slippers', 'clogs', 'espadrilles',

    # accessories
    'hat', 'hats', 'scarf', 'scarves', 'glove', 'gloves', 'belt', 'belts', 
    'sunglasses', 'glasses', 'headband', 'headbands', 'beanie', 'beanies', 'visor',

    # novelty / trendy
    'micro skirt', 'micro-skirt', 'microskirt', 'crop top', 'crop-top', 'croptop', 
    'bodycon dress', 'bodycon-dress', 'bodycondress', 'cardigan', 'cardigans', 'hooded coat', 
    'hooded-coat', 'mini skirt', 'mini-skirt', 'miniskirt'
}


# common details
details_words = {
    # closures & ties
    'buttons', 'button', 'zippers', 'zipper', 'snaps', 'snap', 'ties', 'tie', 
    'hookandeye', 'hook-and-eye', 'hook and eye', 'lacing', 'lace-up', 'lace up',
    'buckles', 'drawstrings', 'draw-string', 'draw string',

    # shaping & structure
    'pleats', 'pleating', 'darts', 'slits', 'cutouts', 'cut-outs', 'ruched', 'ruching', 
    'gathering', 'gathered', 'boning', 'vents', 'padding', 'seams', 
    'paneling', 'piping', 'rawedges', 'raw edges', 'distressing', 'highshine', 'high shine', 
    'matte', 'gloss', 'fading', 'quilting', 
    'quilted', 'smocking', 'smocked', 'lasercut', 'laser-cut', 'laser cut', 'flocking',

    # embellishments
    'ruffles', 'ruffled', 'frills', 'bows', 'feathers', 'sequins', 'beads', 'beaded', 
    'crystals', 'graphic', 'graphics', 'embroidery', 'embroidered', 'applique', 'appliqué', 
    'fringe', 'fringing', 'studs', 'grommets', 'rosettes', 'patchwork', 'high-shine',
    'logo', 'monogram', 'text', 'artprint', 'art print',
}

# common patterns
pattern_words = {
    'floral', 'florals', 'paisley', 'plaid', 'tartan', 'houndstooth', 'check', 'checks', 
    'gingham', 'stripe', 'stripes', 'pinstripe', 'pin-stripe', 'polkadot', 'polka-dot', 
    'dot', 'animalprint', 'animal print', 'animal-print', 'leopard', 'zebra', 'snake', 
    'camouflage', 'camo', 'geometric', 'abstract', 'tie-dye', 'tie dye', 'tiedye', 'ombre', 
    'colorblock', 'color-block', 'brocade', 'ikat', 'chevron', 'print mixing'
    'marble', 'swirl', 'wave', 'mesh', 'net', 'grid', 'argyle', 'jacquard', 'printmixing', 
    'animal print', 'animal-print', 'floral print', 'floral-print', 'geometric print', 
    'geometric-print', 'tie-dye print', 'tie-dye-print', 'plain', 'print-mixing'
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

    # saves updated dataframe with cleaned reviews back to same csv
    df.to_csv(csv_path, index=False)

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

