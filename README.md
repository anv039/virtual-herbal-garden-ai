# 🌿 Virtual Herbal Garden – AI Powered Medicinal Plant Discovery Platform

Virtual Herbal Garden is a full-stack educational web application that helps users explore medicinal plants and their scientific properties.
The platform integrates curated plant data, AI-based recommendations, and 3D biomolecular visualization to create an interactive learning experience for students and researchers.

---

# 🚀 Features

### 🔎 Plant Search & Exploration

Users can search for medicinal plants and view detailed information including:

* Scientific name
* Medicinal uses
* Phytochemistry
* Cultivation conditions
* Habitat
* Reference sources (Wikipedia / scientific sources)

---

### 🌎 Location-Aware Plant Recommendations

The application uses **Groq LLM (LLaMA-3)** to recommend medicinal plants commonly found in the user’s region.

Workflow:

1. User grants location permission
2. Backend queries Groq API
3. AI generates medicinal plants relevant to that region
4. Users can explore full details of those plants

---

### 🧬 Scientific Dataset

A curated dataset of **185+ medicinal plants** was created by aggregating data from scientific sources such as:

* Wikipedia
* NCBI
* PubMed

The dataset contains:

* Phytochemical information
* Genetic sequence data
* Medicinal properties
* Plant taxonomy

---

### 🖼 Dynamic Image Retrieval

Plant images are dynamically fetched using the **Pixabay API**, with local caching implemented to reduce redundant API calls and improve performance.

---

### 🧪 3D Biomolecular Visualization

The platform integrates a **3D viewer (Mol*)** allowing biomedical students to visualize protein structures related to plant compounds directly in the browser.

---

# 🏗 System Architecture

Frontend
HTML • CSS • JavaScript

Backend
Python • Flask

AI Integration
Groq LLM (LLaMA-3 via LangChain)

External APIs
Pixabay API

Data Storage
JSON Dataset (~185 Plants)

Visualization
Mol* 3D Molecular Viewer

---

# 📂 Project Structure

```
virtual-herbal-garden-ai
│
├── app.py
├── database_setup.py
├── add_plants.py
├── definitive_plant_dataset.json
├── plant.json
│
├── static
│   └── index.html
│
├── images
│   └── plant images
│
├── models
│   └── 3D plant models (.glb)
│
├── styles.css
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

Clone the repository:

```
git clone https://github.com/anv039/virtual-herbal-garden-ai.git
cd virtual-herbal-garden-ai
```

Create a virtual environment:

```
python -m venv .venv
```

Activate environment:

Windows

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
PIXABAY_API_KEY=your_pixabay_api_key
```

---

# ▶️ Running the Application

Start the backend server:

```
python app.py
```

Then open:

```
static/index.html
```

---

# 🎯 Future Improvements

* Deploy the application online
* Replace JSON dataset with PostgreSQL for scalability
* Add user accounts and bookmarking
* Expand dataset to 1000+ medicinal plants
* Add ML-based plant classification

---

# 👨‍💻 Author

**Anant Kumar Verma**

Computer Science Engineering
Manipal University Jaipur

---

# ⭐ If you like this project

Give the repository a star ⭐
