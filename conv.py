import json
import pandas as pd
import re

# Define category keywords (expanded bilingual list)
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


# Path to the conversation JSON file
CONVO_JSON_PATH = 'conversations.json'

# Load JSON file (array of objects)
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error loading JSON: {e}")
            data = []
    return data


# Extract all fields from each entry and categorize
def categorize_conversations(data, categories):
    categorized = []
    for entry in data:
        text = entry.get('text', '').lower()
        # Find category
        category = "Sin categoría"
        for cat_name, keywords in categories.items():
            for keyword in keywords:
                if re.search(rf'\b{re.escape(keyword.lower())}\b', text):
                    category = cat_name
                    break
            if category != "Sin categoría":
                break
        # Copy all fields from entry, add category
        result = dict(entry)
        result['category'] = category
        categorized.append(result)
    return categorized

# Save to CSV
def save_to_csv(data, output_file):
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Saved to {output_file}")


# Extract message fields
def extract_message_fields(message_id, message_obj):
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
        # Add more fields as needed
    }


# Main function
def process_json(input_file, output_file):
    # Load data
    data = load_json(input_file)
    # If data is a dict (message_id: message_obj), convert to list of extracted fields
    if isinstance(data, dict):
        entries = [extract_message_fields(mid, mobj) for mid, mobj in data.items()]
    else:
        entries = data
    # Categorize
    categorized_data = categorize_conversations(entries, categories)
    # Save to CSV
    save_to_csv(categorized_data, output_file)

def main():
    with open(CONVO_JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Extract all messages
    rows = [extract_message_fields(mid, mobj) for mid, mobj in data.items()]
    # Save all messages to CSV
    df = pd.DataFrame(rows)
    df.to_csv('all_messages.csv', index=False, encoding='utf-8')
    # Save only the last message to a separate CSV (if needed)
    if rows:
        pd.DataFrame([rows[-1]]).to_csv('last_message.csv', index=False, encoding='utf-8')

if __name__ == "__main__":
    input_file = CONVO_JSON_PATH  # Use the defined path variable
    output_file = 'categorized_conversations.csv'  # Output CSV
    process_json(input_file, output_file)
    main()