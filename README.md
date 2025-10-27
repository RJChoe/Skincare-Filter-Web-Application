# Skincare Allergy Filter

## Project Overview
The **Skincare Allergy Filter** is a web application that helps users determine if skincare products are safe based on their personal allergies. Users can enter their allergies along with a product's ingredient list, and the app will check for potential allergens and return a safety recommendation.

---

## Features
- **Personal Allergy Input:** Users can list their known allergens.
- **Ingredient Check:** Users can input a skincare product’s ingredient list.
- **Safety Alert:** The app notifies whether the product is safe or contains allergens.

---

## How It Works
1. Users enter their personal allergies (e.g., nuts, parabens, fragrance).  
2. Users input the skincare product's ingredient list.  
3. The application compares the ingredient list against the user's allergies.  
4. The app returns a result:
   - **Safe:** No allergens detected.
   - **Unsafe:** Product contains one or more allergens.

---

## Tech Stack
- **Framework:** Python Django (handles both frontend and backend)  
- **Database:** SQLite (default) or any Django-supported database  

---

## Installation
How to install and set up your project:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/skincare-allergy-filter.git
   ```

2. Navigate to the project folder:
```bash
cd skincare-allergy-filter
```

3. Create a virtual environment:
```bash
python -m venv .venv
```

4. Activate the virtual environment:

    - **Windows:**
```bash
.venv\Scripts\activate
```

    - **macOS/Linux:**
```bash
source .venv/bin/activate
```

5. Install dependencies:
```bash
pip install -r requirements.txt
```

6. Apply migrations:
```bash
pip install -r requirements.txt
```

7. Run the development server:
```bash
python manage.py runserver
```

8. Open your browser and visit http://localhost:8000

---

##Usage
1. Enter your personal allergies.
2. Input the ingredients of a skincare product.
3. Click "Check Safety".
4. View the results indicating whether the product is safe.

---

## Screenshots/Demo
Here’s an example of how the app looks:
Allergy Input Page
![Website requesting User's Allergy Input](link to image)

Ingredients Input Page
![Website requesting input of skincare product's ingredients](link to image)

Result Page
![Website with the Result Page. Green background for "SAFE" & Red background for "UNSAFE".](link to image)

((Replace the above images with actual screenshots from your project in a screenshots/ folder.))