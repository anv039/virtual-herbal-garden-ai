# app.py (full, with Groq location recommendations)

import os
import json
import time
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from langchain_groq import ChatGroq  # Groq LLM client

# --- API keys / config ---
GROQ_API_KEY = "gsk_...."
PIXABAY_API_KEY = os.getenv("GROQ_API_KEY")
PIXABAY_API_URL = "....."
PLANT_DATA_FILE = "definitive_plant_dataset.json"
IMAGE_CACHE_FILE = "image_cache.json"

# --- Featured Plants List ---
FEATURED_PLANTS = [
    "Ashwagandha", "Ginseng", "Turmeric", "St. John's Wort", "Ginkgo", "Echinacea",
    "Ginger", "Garlic", "Holy Basil", "Neem", "Aloe Vera", "Gotu Kola"
]

app = Flask(__name__, static_folder="static")
CORS(app)

# --- Global data and cache ---
plant_data = []
image_cache = {}


def load_image_cache():
    global image_cache
    try:
        if os.path.exists(IMAGE_CACHE_FILE):
            with open(IMAGE_CACHE_FILE, "r", encoding="utf-8") as f:
                image_cache = json.load(f)
                print(f"Successfully loaded {len(image_cache)} items from image cache.")
    except (json.JSONDecodeError, IOError):
        image_cache = {}


def save_image_cache():
    try:
        with open(IMAGE_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(image_cache, f, indent=4)
    except IOError:
        pass


# --- Load plant dataset once ---
try:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    json_file_path = os.path.join(base_dir, PLANT_DATA_FILE)

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "plants" in data:
            plant_data = data["plants"]
            print(f"Successfully loaded {len(plant_data)} plants from {json_file_path}")
        else:
            print(f"Error: 'plants' key not found in {PLANT_DATA_FILE}")
except FileNotFoundError:
    print(f"CRITICAL ERROR: {PLANT_DATA_FILE} not found. Searched at: {json_file_path}")
except Exception as e:
    print(f"Error loading plant data: {e}")

load_image_cache()


# --- Helpers ---

def find_plant_in_local_json(search_term):
    if not plant_data:
        return None
    search_term_lower = search_term.lower()
    for plant in plant_data:
        if search_term_lower == plant.get("scientific_name", "").lower():
            return plant.copy()
        common_names = [name.lower() for name in plant.get("common_names", [])]
        if search_term_lower in common_names:
            return plant.copy()
    return None


def fetch_image_url_from_pixabay(common_name, scientific_name):
    cache_key = common_name or scientific_name
    if cache_key in image_cache:
        print(f"CACHE HIT for '{cache_key}'.")
        return image_cache[cache_key]

    print(f"CACHE MISS for '{cache_key}'. Calling API...")
    time.sleep(1)

    search_queries = [f"{common_name} herb", f"{common_name}", f"{scientific_name}"]
    search_queries = list(set(q for q in search_queries if q))

    image_url = None
    for query in search_queries:
        try:
            params = {
                "key": PIXABAY_API_KEY,
                "q": query,
                "image_type": "photo",
                "per_page": 3,
            }
            response = requests.get(PIXABAY_API_URL, params=params, timeout=8)
            response.raise_for_status()
            data = response.json()
            if data.get("hits"):
                image_url = data["hits"][0].get("webformatURL")
                if image_url:
                    break
        except requests.exceptions.RequestException:
            continue

    if not image_url and "image_url" in locals() and locals()["image_url"]:
        image_url = locals()["image_url"]

    image_cache[cache_key] = image_url
    save_image_cache()
    return image_url


def get_local_plant_names_groq(location):
    """Query Groq LLM to get local medicinal plant names"""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0,
        max_tokens=300,
    )
    prompt = (
        f"List medicinal plants commonly found in {location}, India. "
        f"Give common and scientific names in an array format like "
        f"[\"Common Name\", \"Scientific Name\"], one per line."
    )
    response = llm.invoke(prompt)
    return response


def get_location_recommendations_groq(location):
    """Ask Groq for extra recommendations for a location."""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        max_tokens=400,
    )
    prompt = (
        f"You are an agronomy and medicinal-plant expert.\n"
        f"For the location '{location}, India', give:\n"
        f"1. A short paragraph about climate and soil.\n"
        f"2. A bullet list of 5–10 medicinal plants that grow well there.\n"
        f"3. A bullet list of 5–10 food or cash crops that are suitable to grow "
        f"right now in the current season (assume typical weather).\n"
        f"Write in concise, user-friendly language."
    )
    response = llm.invoke(prompt)
    return response.content


def parse_groq_plant_list(llm_content):
    """Parse Groq LLM's output for plant name pairs"""
    pairs = re.findall(r'\["([^"]+)",\s*"([^"]+)"\]', llm_content)
    return pairs


# --- Routes ---

@app.route("/get-featured-plants", methods=["GET"])
def get_featured_plants():
    featured_plants_data = []
    for plant_name in FEATURED_PLANTS:
        plant_info = find_plant_in_local_json(plant_name)
        if plant_info:
            common_name = plant_info.get("common_names", [None])[0]
            scientific_name = plant_info.get("scientific_name")
            image_url = plant_info.get("image_url") or fetch_image_url_from_pixabay(
                common_name, scientific_name
            )
            plant_info["image"] = image_url or "/static/placeholder.png"
            featured_plants_data.append(plant_info)
    return jsonify(featured_plants_data)


@app.route("/search-plant", methods=["GET"])
def search_plant():
    plant_name_query = request.args.get("name")
    if not plant_name_query:
        return jsonify({"error": "No plant name provided"}), 400

    found_plant_local = find_plant_in_local_json(plant_name_query)

    if found_plant_local:
        common_name = found_plant_local.get("common_names", [None])[0]
        scientific_name = found_plant_local.get("scientific_name")
        image_url = found_plant_local.get("image_url") or fetch_image_url_from_pixabay(
            common_name, scientific_name
        )
        found_plant_local["image"] = image_url or "/static/placeholder.png"
        return jsonify(found_plant_local), 200
    else:
        return jsonify({"error": f"No plant found matching '{plant_name_query}'."}), 404


@app.route("/get-pdb-data/<pdb_id>")
def get_pdb_data(pdb_id):
    """Proxy to fetch 3D model data from RCSB PDB."""
    pdb_id = pdb_id.upper()
    if not re.match(r"^[a-zA-Z0-9]{4}$", pdb_id):
        return jsonify({"error": "Invalid PDB ID format"}), 400

    url = f"https://files.rcsb.org/download/{pdb_id}.cif"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        print(f"Successfully fetched PDB data for {pdb_id}")
        return response.text, 200, {"Content-Type": "text/plain"}
    except requests.exceptions.RequestException as e:
        print(f"Failed to proxy PDB data for {pdb_id}: {e}")
        return jsonify({"error": "Could not retrieve 3D model data from RCSB PDB."}), 502


@app.route("/search-by-location", methods=["POST"])
def search_by_location():
    """Search for medicinal plants by location using Groq LLM"""
    location = request.form.get("location", "").strip()
    if not location:
        return jsonify({"error": "No location provided", "plants": [], "recommendations": ""}), 400

    try:
        print(f"\n=== Searching plants for location: {location} ===")
        # Main plant list from Groq
        response = get_local_plant_names_groq(location)
        print(f"Groq API Response (first 400 chars):\n{response.content[:400]}...\n")

        pairs = parse_groq_plant_list(response.content)
        print(f"Parsed plant pairs: {pairs}\n")

        found = []
        not_found = []

        for common, sci in pairs:
            common_lower = common.lower()
            sci_lower = sci.lower()
            matched = False

            for plant in plant_data:
                plant_common_names = [name.lower() for name in plant.get("common_names", [])]
                plant_sci_name = plant.get("scientific_name", "").lower()

                if (
                    any(common_lower in pcn or pcn in common_lower for pcn in plant_common_names)
                    or sci_lower in plant_sci_name
                    or plant_sci_name in sci_lower
                ):
                    if plant not in found:
                        plant_copy = plant.copy()
                        image_url = plant_copy.get("image_url") or fetch_image_url_from_pixabay(
                            plant_copy.get("common_names", [None])[0],
                            plant_copy.get("scientific_name"),
                        )
                        plant_copy["image"] = image_url or "/static/placeholder.png"
                        found.append(plant_copy)
                        print(f"✓ MATCHED: {common} ({sci}) -> {plant.get('common_names', [None])[0]}")
                    matched = True
                    break

            if not matched:
                not_found.append(f"{common} ({sci})")

        print(f"\n✓ Found {len(found)} plants in database")
        if not_found:
            print(f"✗ Not found in database: {', '.join(not_found)}")

        # Extra Groq recommendations text
        extra_text = get_location_recommendations_groq(location)
        print(f"\nExtra recommendations text (first 200 chars):\n{extra_text[:200]}...\n")

        return jsonify({"plants": found, "recommendations": extra_text}), 200

    except Exception as e:
        import traceback

        print(f"Groq LLM Error: {e}")
        traceback.print_exc()
        return jsonify(
            {"error": "AI search failed. Please try again.", "plants": [], "recommendations": ""}
        ), 500


@app.route("/")
def index():
    """Serves the main index.html file."""
    return app.send_static_file("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
