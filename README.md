# 🐾 PawMatch – AI-Powered Pet Adoption Platform

PawMatch is a web application that helps users find their perfect pet match using an **AI-powered recommendation system**.  
It combines a friendly **frontend**, a **Flask backend**, a **MongoDB database**, and a simple **AI model** (TF-IDF + similarity) to recommend pets based on user preferences.

---

## 🚀 Features

- 📋 Lifestyle questionnaire (home size, activity level, allergies, experience, kids).  
- 🤖 AI recommendation engine to suggest the best pet matches.  
- 🐶 View all available pets with filters (breed, type, size, age).  
- ℹ️ “Learn More” pop-ups with pet details.  
- 📩 Contact shelter form for adoption inquiries.  
- 🌙 Dark mode toggle for better UX.

---

## 🛠️ Technologies Used

**Frontend**  
- HTML5, CSS3, JavaScript (Vanilla JS)  

**Backend**  
- Flask (Python web framework)  
- Flask-CORS (to allow frontend ↔ backend communication)  

**Database**  
- MongoDB Atlas (cloud database for storing pet info)  
- PyMongo (Python driver to connect Flask with MongoDB)  

**AI & ML**  
- Scikit-learn:  
  - `TfidfVectorizer` → converts pet descriptions into vectors.  
  - `cosine_similarity` → measures similarity between user preferences and pet descriptions.  
- Custom attribute scoring system (size, allergies, activity, kids, experience).  

---

## ⚙️ Installation

### 1) Clone the repository
```bash
git clone https://github.com/your-username/pawmatch.git
cd pawmatch
2) Create virtual environment
bash
Copy code
python -m venv .venv
3) Activate virtual environment
Windows (PowerShell):

bash
Copy code
.\.venv\Scripts\Activate.ps1
Mac/Linux:

bash
Copy code
source .venv/bin/activate
4) Install dependencies
bash
Copy code
pip install -r requirements.txt
5) Set up MongoDB Atlas
Create a MongoDB Atlas cluster.

Get your connection string (example):

ruby
Copy code
mongodb+srv://username:password@cluster0.mongodb.net/?retryWrites=true&w=majority
Replace it in app.py:

python
Copy code
MONGODB_URI = "your_connection_string_here"
6) Seed the database with pets
Run the seed file to populate MongoDB:

bash
Copy code
python seed_data.py
7) Run the app
bash
Copy code
python app.py
Then open: http://127.0.0.1:5000

🧠 How the AI Works
User preferences → Collected from the questionnaire.
Example: home_size=medium, activity=high, allergies=none.

TF-IDF (Text Analysis) → Converts all pet descriptions into vectors, then compares them with the user’s preferences.

Cosine Similarity → Calculates how close the user’s “query” is to each pet’s description.

Attribute Scoring → Custom rules for size, allergies, activity, kids, and experience are added.

Final Score = 0.6 * attribute_score + 0.4 * similarity_score

Pets are sorted by score → Top 10 are shown as “Your Recommended Pets”.

📂 Project Structure
php
Copy code
pawmatch/
│── app.py              # Flask backend + AI routes
│── seed_data.py        # Script to populate database with pets
│── requirements.txt    # Python dependencies
│── static/
│   ├── index.html      # Frontend
│   ├── styles.css      # Styling
│   ├── app.js          # Frontend logic
│   └── images/         # Local pet images
