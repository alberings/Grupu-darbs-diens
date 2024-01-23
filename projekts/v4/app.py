
from flask import Flask, flash, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask_admin import Admin


app = Flask(__name__)
app.secret_key = 'your_secret_key' 
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def home():
    
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/nutreins')
def nutreins():
    return render_template('nutreins.html')



@app.route('/get-menu-plan', methods=['GET', 'POST'])
def get_menu_plan():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        
        caloric_needs_input = request.form.get('caloric_needs', '0') 
        try:
           
            caloric_needs = int(caloric_needs_input)
        except ValueError:
         
            caloric_needs = 0  

       
        dietary_restrictions = request.form.get('dietaryRestrictions', '').split(',')

       
        user_details = session['user']

        
        menu_plan = generate_menu_plan(caloric_needs, dietary_restrictions)


         
        user = User.query.get(session['user']['id'])
        user.menu_plan = json.dumps(menu_plan)
        db.session.commit()
       
        return render_template('display_menu.html', menu_plan=menu_plan)

    return render_template('get_menu_plan.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle form submission here (e.g., send an email)
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('contact'))

    return render_template('contact.html')


from random import choice
import requests


BREAKFAST_FOODS = ['cereal', 'oatmeal', 'yogurt', 'pancakes', 'scrambled eggs', 'smoothie', 'muffins', 'granola', 'fruit salad', 'waffles', 'bagel', 'omelette', 'french toast', 'bacon', 'sausage', 'croissant', 'hash browns', 'cottage cheese', 'frittata', 'porridge']
LUNCH_FOODS = ['sandwich', 'salad', 'soup', 'wraps', 'pizza', 'quiche', 'pasta salad', 'sushi', 'bowl', 'bento box', 'taco', 'burrito', 'samosa', 'pita bread', 'noodle soup', 'chicken tenders', 'hot dog', 'gyro', 'spring roll', 'club sandwich']
DINNER_FOODS = ['pasta', 'vegetables', 'rice', 'meat', 'fish', 'stir-fry', 'curry', 'lasagna', 'grilled chicken', 'steak', 'shrimp scampi', 'sushi roll', 'baked potato', 'spaghetti', 'lobster tail', 'chow mein', 'pork chops', 'beef stew', 'vegetable stir-fry', 'salmon']



def fetch_foods_for_restriction(restriction, api_key, meal_type):
    
    meal_type_filter = {
        'Breakfast': BREAKFAST_FOODS,
        'Lunch': LUNCH_FOODS,
        'Dinner': DINNER_FOODS
    }
    
    search_query = f"{restriction} {' OR '.join(meal_type_filter[meal_type])}"
    
   
    response = requests.get(
        'https://api.nal.usda.gov/fdc/v1/foods/search',
        params={
            'api_key': api_key,
            'query': search_query,
            'pageSize': 100
        }
    )
    if response.status_code == 200:
        raw_foods = response.json().get('foods', [])
        
        simplified_foods = []
        for food in raw_foods:
           
            calories = next((nutrient['value'] for nutrient in food.get('foodNutrients', [])
                             if nutrient['nutrientName'] == 'Energy' and nutrient['unitName'] == 'KCAL'), None)
            if calories:  
                food_data = {
                    'fdcId': food.get('fdcId'),
                    'description': food.get('description'),
                    'calories': calories
                }
                simplified_foods.append(food_data)
        return simplified_foods
    return []

def get_meal_options(foods, calories_per_meal, used_foods):
    
    suitable_foods = [food for food in foods if food['calories'] <= calories_per_meal and food['fdcId'] not in used_foods]
    return suitable_foods

def select_food_for_meal(meal_options, used_foods):
    for food in meal_options:
        food_id = food['fdcId']
        if food_id not in used_foods:
            used_foods.add(food_id)
            return food
    return None

def generate_daily_menu(calories_per_meal, dietary_restrictions, api_key, used_foods, meal_type):
   
    meal_specific_foods = []
    for restriction in dietary_restrictions:
        foods = fetch_foods_for_restriction(restriction, api_key, meal_type)
        meal_specific_foods.extend(foods)
    
    
    meal_options = get_meal_options(meal_specific_foods, calories_per_meal, used_foods)
    selected_food = select_food_for_meal(meal_options, used_foods)
    
    return selected_food or 'Placeholder food item'

def generate_menu_plan(caloric_needs, dietary_restrictions):
    api_key = '6Le1CjOVZ7KRDINkGiVeIrfRQAKneVwWFDQTiEmk'
    meals_per_day = 3
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    menu_plan = {}
    used_foods = set()

    calories_per_meal = int(caloric_needs) // (meals_per_day * len(days))
    
    print(f"Total calories needed: {caloric_needs}")
    print(f"Calories per meal: {calories_per_meal}")

    for day in days:
        menu_plan[day] = {
            'Breakfast': generate_daily_menu(calories_per_meal, dietary_restrictions, api_key, used_foods, 'Breakfast'),
            'Lunch': generate_daily_menu(calories_per_meal, dietary_restrictions, api_key, used_foods, 'Lunch'),
            'Dinner': generate_daily_menu(calories_per_meal, dietary_restrictions, api_key, used_foods, 'Dinner')
        }
        
        # Print the calories for each meal
        print(f"{day} - Breakfast Calories: {menu_plan[day]['Breakfast']['calories']}")
        print(f"{day} - Lunch Calories: {menu_plan[day]['Lunch']['calories']}")
        print(f"{day} - Dinner Calories: {menu_plan[day]['Dinner']['calories']}")

    return menu_plan





@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
       
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        height = request.form.get('height')
        weight = request.form.get('weight')
        age = request.form.get('age')
        gender = request.form.get('gender')
        activity_level = request.form.get('activity_level')
        dietary_restrictions = request.form.get('dietary_restrictions')
        allergies = request.form.get('allergies')

       
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return 'User already exists'

        hashed_password = generate_password_hash(password)

        new_user = User(email=email, password=hashed_password, name=name, 
                        height=height, weight=weight, age=age, gender=gender,
                        activity_level=activity_level, dietary_restrictions=dietary_restrictions,
                        allergies=allergies)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        
        user = User.query.filter_by(email=email).first()

        
        if user and check_password_hash(user.password, password):
           
            session['user'] = {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'height': user.height,
                'weight': user.weight,
                'age': user.age,
                'gender': user.gender,
                'activity_level': user.activity_level,
                'dietary_restrictions': user.dietary_restrictions,
                'allergies': user.allergies
            }
            
           
            if user.is_admin:
                session['logged_in'] = True
                return redirect('/admin')

            return redirect(url_for('profile'))

        return "Invalid credentials"  

    return render_template('login.html')


@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = User.query.get(session['user']['id'])
   
    if user.menu_plan:
        menu_plan = json.loads(user.menu_plan)  
    else:
        menu_plan = None  

    return render_template('profile.html', user=session['user'], menu_plan=menu_plan)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']
    user = User.query.get(user_id)

    if request.method == 'POST':
      
        user.name = request.form['name']
        user.height = float(request.form['height']) if request.form['height'] else None
        user.weight = float(request.form['weight']) if request.form['weight'] else None
        user.age = int(request.form['age']) if request.form['age'] else None
        user.gender = request.form['gender']
        user.activity_level = request.form['activity_level']
        user.dietary_restrictions = request.form['dietary_restrictions']
        user.allergies = request.form['allergies']

        db.session.commit()

       
        session['user'] = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'height': user.height,
            'weight': user.weight,
            'age': user.age,
            'gender': user.gender,
            'activity_level': user.activity_level,
            'dietary_restrictions': user.dietary_restrictions,
            'allergies': user.allergies
        }

        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)



from flask_admin.contrib.sqla import ModelView

class UserModelView(ModelView):
    column_exclude_list = ['password']  

class MyModelView(ModelView):
    def is_accessible(self):
        return session.get('logged_in', False) and session.get('user', {}).get('is_admin', False)

class MealModelView(ModelView):
    
    pass
class FoodItemModelView(ModelView):
    pass  

class NutritionProfileModelView(ModelView):
    pass  


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)
admin = Admin(app, name='Admin Interface', template_mode='bootstrap3')
migrate = Migrate(app, db)

app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(100))

   
    height = db.Column(db.Float)  
    weight = db.Column(db.Float)  
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    activity_level = db.Column(db.String(50))  
    dietary_restrictions = db.Column(db.String(200))  
    allergies = db.Column(db.String(200))  
    menu_plan = db.Column(db.Text, default='{}')
    is_admin = db.Column(db.Boolean, default=False)


class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.Text)
    nutritional_values = db.Column(db.Text)  

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer)
    macronutrients = db.Column(db.String(200))  

class NutritionProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    caloric_intake = db.Column(db.Integer) 
    macronutrient_ratio = db.Column(db.String(100))  

    user = db.relationship('User', backref=db.backref('nutrition_profile', lazy=True))


admin.add_view(UserModelView(User, db.session))
admin.add_view(MealModelView(Meal, db.session))
admin.add_view(FoodItemModelView(FoodItem, db.session))
admin.add_view(NutritionProfileModelView(NutritionProfile, db.session))

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)