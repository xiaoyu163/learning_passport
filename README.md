## Installation

Follow these steps to set up the Learning Passport System on your local machine:

1. **Clone the repository:**
 
    https://github.com/xiaoyu163/learning_passport.git
    cd learning-passport
  
2. **Create a virtual environment:**
    python -m venv env


3. **Activate the virtual environment:**

   .\env\Scripts\activate

4. **Install the required packages:**

    pip install -r requirements.txt

5. **Apply database migrations:**

    python manage.py migrate

6. **Create a superuser (for accessing the Django admin panel):**
    python manage.py createsuperuser


7. **Run the development server:**
    python manage.py runserver
   
