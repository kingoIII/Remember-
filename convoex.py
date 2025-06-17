
import json
import pandas as pd
import re
from collections import defaultdict

# Path to the conversation JSON file
CONVO_JSON_PATH = 'conversations.json'

# Step 1: Define category keywords (your list, unchanged)
categories = {
    "Biblia": [
        "dios", "jesús", "cristo", "espíritu santo", "biblia", "escrituras", "moisés", "israel",
        "juan bautista", "satanás", "ángel", "demonio", "cielo", "infierno", "salvación", "pecado",
        "oración", "fe", "milagro", "iglesia", "profeta", "apóstol", "mandamiento", "resurrección",
        "god", "jesus", "christ", "holy spirit", "bible", "scriptures", "moses", "israel",
        "john the baptist", "satan", "angel", "demon", "heaven", "hell", "salvation", "sin",
        "prayer", "faith", "miracle", "church", "prophet", "apostle", "commandment", "resurrection"
    ],
    "Música": [
        "música", "canción", "acorde", "nota", "ritmo", "tempo", "guitarra", "piano", "batería",
        "cantar", "banda", "concierto", "melodía", "armonía", "letra", "compositor", "sinfonía",
        "género", "reggaetón", "cumbia", "rock", "pop", "jazz", "salsa", "corrido", "mariachi",
        "music", "song", "chord", "note", "rhythm", "tempo", "guitar", "piano", "drums",
        "sing", "band", "concert", "melody", "harmony", "lyrics", "composer", "symphony",
        "genre", "reggaeton", "cumbia", "rock", "pop", "jazz", "salsa", "corrido", "mariachi"
    ],
    "Matemáticas": [
        "matemática", "suma", "resta", "multiplicación", "división", "álgebra", "cálculo",
        "ecuación", "número", "geometría", "ángulo", "fracción", "derivada", "integral",
        "probabilidad", "estadística", "matriz", "vector", "función", "teorema",
        "mathematics", "math", "addition", "subtraction", "multiplication", "division",
        "algebra", "calculus", "equation", "number", "geometry", "angle", "fraction",
        "derivative", "integral", "probability", "statistics", "matrix", "vector", "function",
        "theorem"
    ],
    "Filosofía": [
        "filosofía", "verdad", "existencia", "moral", "ética", "libertad", "conciencia", "ser",
        "alma", "razón", "destino", "justicia", "bien", "mal", "conocimiento", "realidad",
        "metafísica", "lógica", "pensamiento", "idealismo", "existencialismo",
        "philosophy", "truth", "existence", "morality", "ethics", "freedom", "consciousness",
        "being", "soul", "reason", "destiny", "justice", "good", "evil", "knowledge", "reality",
        "metaphysics", "logic", "thought", "idealism", "existentialism"
    ],
    "Ciencia": [
        "ciencia", "física", "química", "biología", "átomo", "molécula", "energía", "experimento",
        "teoría", "hipótesis", "gravedad", "evolución", "célula", "genética", "universo",
        "galaxia", "planeta", "tecnología", "investigación", "descubrimiento",
        "science", "physics", "chemistry", "biology", "atom", "molecule", "energy", "experiment",
        "theory", "hypothesis", "gravity", "evolution", "cell", "genetics", "universe",
        "galaxy", "planet", "technology", "research", "discovery"
    ],
    "Estupideces": [
        "estúpido", "pendejada", "broma", "chiste", "tontería", "meme", "ridículo", "absurdo",
        "gracioso", "payaso", "locura", "disparate", "mierda", "burla", "risas",
        "stupid", "bullshit", "joke", "prank", "nonsense", "meme", "ridiculous", "absurd",
        "funny", "clown", "crazy", "silliness", "crap", "mockery", "laughs"
    ]
}


# Step 2: Load JSON file (array of objects)
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            data = {}
    return data

# Step 3: Calculate category percentages
def extract_message_fields(message_id, message_obj):
    # Extract fields from nested message structure
    msg = message_obj.get('message', {})
    author = msg.get('author', {})
    content = msg.get('content', {})
    metadata = msg.get('metadata', {})
    return {
        'id': message_id,
        'author_role': author.get('role'),
        'author_name': author.get('name'),
        'create_time': msg.get('create_time'),
        'update_time': msg.get('update_time'),
        'text': (content.get('parts', [''])[0] if isinstance(content.get('parts'), list) and content.get('parts') else ''),
        'content_type': content.get('content_type'),
        'status': msg.get('status'),
        'end_turn': msg.get('end_turn'),
        'weight': msg.get('weight'),
        'recipient': msg.get('recipient'),
        'channel': msg.get('channel'),
        'parent': message_obj.get('parent'),
        'children': message_obj.get('children'),
        # Add more fields as needed from metadata or elsewhere
    }

def categorize_by_percentage(data, categories):
    categorized = []
    # If data is a dict (message_id: message_obj), iterate over items
    if isinstance(data, dict):
        entries = [extract_message_fields(mid, mobj) for mid, mobj in data.items()]
    else:
        entries = data
    for entry in entries:
        text = entry.get('text', '').lower()
        # Count keyword hits per category
        category_counts = defaultdict(int)
        total_hits = 0
        for cat_name, keywords in categories.items():
            for keyword in keywords:
                hits = len(re.findall(rf'\b{re.escape(keyword.lower())}\b', text))
                category_counts[cat_name] += hits
                total_hits += hits
        # Calculate percentages
        percentages = {}
        for cat_name in categories:
            if total_hits > 0:
                percentages[cat_name] = (category_counts[cat_name] / total_hits) * 100
            else:
                percentages[cat_name] = 0.0
        # Add all original fields plus percentages
        result = dict(entry)
        result.update(percentages)
        categorized.append(result)
    return categorized

# Step 4: Save to CSV
def save_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Fucking done, check out {output_file}, you badass.")

# Step 5: Main function

def process_json(input_file, output_file):
    data = load_json(input_file)
    categorized_data = categorize_by_percentage(data, categories)
    save_to_csv(categorized_data, output_file)

if __name__ == "__main__":
    input_file = CONVO_JSON_PATH  # Use the defined path variable
    output_file = 'conversation_percentages.csv'  # Output CSV
    process_json(input_file, output_file)
