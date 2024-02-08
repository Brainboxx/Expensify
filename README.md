# Expensify
An Expense Tracker api using Python, Django and Django Rest Framework
# Features
- JWT-authentication: Users can obtain a JWT token by sending a POST request to /api/token/ with their
username and password. 
- Expenses: Authenticated users View, create, update, and delete expenses. 
- Budgets: Authenticated users can view, create, update and delete thier budgets
- Analytics: Detailed analytics such as total expenses in a given time period, category-wise expenses, and remaining budget for each category.

# Installation
1. Clone this repository to your local machine.
   ```
   git clone https://github.com/Brainboxx/Expensify.git
   ```
2. Navigate to the project directory.
   ```
   cd Expensify
   ```
3. Create a virtual environment (recommended).
   ```
   python -m venv venv
   ```
4. Activate the virtual environment
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On Mac:
     ```
     source venv/bin/activate
     ```  
5. Navigate to django project root
   ```
   cd expensify
   ```
6. Install the required dependencies.
   ```
   pip install -r requirements.txt
   ```  
7. Set up the database.
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```
8. Create a superuser account to access the admin panel.
   ```
   python manage.py createsuperuser
   ```   
9. Start the development server.
   ```
   python manage.py runserver
   ```
# Endpoints & Usage

- Explore and interact with the API endpoints for authentication, expenses, budgets via the docs at http://localhost:8000/api/schema/docs/.
- NOTE: The 'http://localhost:8000/analytics/' endpoint takes a start_date and end_date parameter when sending a GET request.
