from flask import Flask, render_template, url_for, request, jsonify, session
import json
import os
import calculations
from livereload import Server
from calculations.calculations import CALC_REGISTRY
from dotenv import load_dotenv
import requests
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth


cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)


app = Flask(__name__) 

app.config['TEMPLATES_AUTO_RELOAD'] = True

load_dotenv()

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev-secret")


json_path = os.path.join(app.root_path, 'data', 'calculations.json')
with open(json_path, encoding='utf-8') as f:
    data = json.load(f)
cards = []
for category in data['categories']:
    for card in category.get('calculations', []):
        card['category'] = category.get('name', '')
        cards.append(card)
def execute_function(function_name, parameters):
    try:
        
        function = getattr(calculations, function_name)

        param_dict = {param: float(request.form[param]) for param in parameters}
        
        result = function(**param_dict)
        return result
    except Exception as e:
        return str(e)

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_message = request.json.get('message')
        # Here you would process the message and generate a response
        response = f"You said: {user_message}"
        return jsonify({'response': response})
    return render_template('chat.html')


@app.route('/login', methods=['POST'])
def login():
    auth_header = request.headers.get("Authorization", "")
    print("[Login] Received header:", auth_header)

    if not auth_header.startswith("Bearer "):
        print("Missing or invalid Authorization header")
        return "Unauthorized", 401

    id_token = auth_header.split(" ")[1]
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        uid = decoded['uid']
        session.permanent = True  # Optional
        session['user'] = uid
        print("[Login] Session set for UID:", uid)
        return '', 200
    except Exception as e:
        print("[Login] Token verification failed:", e)
        return "Unauthorized", 401



@app.route('/explain', methods=['POST'])
def explain():
    req_data = request.get_json()
    calc_name = req_data.get('calc_name')
    result = req_data.get('result')
    parameters = req_data.get('parameters', {})
    additional_context = req_data.get('additional_context', '')

  
    def extract_param(keys):
        for key in keys:
            for param_key in parameters:
                if param_key.lower() == key:
                    return parameters[param_key]
        return ''

    age = extract_param(['age'])
    sex = extract_param(['sex'])
    race = extract_param(['race'])

   
    for key in list(parameters.keys()):
        if key.lower() in ['age', 'sex', 'race']:
            parameters.pop(key)

    age_str = f"\nPatient Age: {age}" if age else ""
    sex_str = f"\nPatient Sex: {sex}" if sex else ""
    race_str = f"\nPatient Race: {race}" if race else ""
    context_str = f"\nAdditional Context: {additional_context}" if additional_context else ""

    unit = ""
    for category in data['categories']:
        for calc in category.get('calculations', []):
            if calc['name'] == calc_name:
                unit = calc.get('result_unit', '') or ''
                break
    
    param_str = ""
    if parameters:
        param_str = "\nCalculation Parameters:\n" + "\n".join(
            f"- {k}: {v}" for k, v in parameters.items()
        )
        
    

    prompt = f"""You are a senior clinical nursing assistant AI. When I provide you a lab value or a medical calculation result, you will:
  1) State whether the result is within the normal reference range (or above/below),
  2) Explain what an abnormal value could imply about the patient’s condition,
  3) List any potential nursing concerns or next steps.
  4) Use plain language—suitable for a registered nurse (RN),
  5) Keep your answer to 3–5 bullet points.

Calculation Name: {calc_name}
Result Value: {result} {unit}
Unit: {unit}
{age_str}{sex_str}{race_str}{context_str}
{param_str}

Please provide your explanation now:"""
    

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    try:
        response = requests.post(url, json=payload)
        print("Gemini response:", response.status_code, response.text)
        explanation = "Sorry, could not get explanation."
        if response.ok:
            explanation = response.json()['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"explanation": explanation})
    except Exception as e:
        print("Gemini error:", e)
        return jsonify({"explanation": "Sorry, could not get explanation."})


@app.route('/')
def index():
     cards = data['categories']
     user = session.get('user', None)
     return render_template(
        'index.html',
        cards=cards,
        user=user
    )


   
@app.route('/card/<slug>', methods=['GET', 'POST'])
def card_detail(slug):
    for category in data['categories']:
        if category.get('slug', '') == slug:
      
            if request.method == 'POST':
                calculation_name = request.form['calculation_name']
                calculation = next((calc for calc in category.get('calculations', []) if calc['name'] == calculation_name), None)
                if calculation:
                    func = CALC_REGISTRY.get(calculation_name)
                    if not func:
                        return jsonify(result=None, error="Calculation not implemented.")
                    kwargs = {}
                    for param in calculation['parameters']:
                        param_name = param['name']
                        value = request.form.get(param_name)
                        if value is None or value == '':
                            return jsonify(result=None, error=f"Missing value for {param_name}")
                        if param.get('type') == 'float':
                            try:
                                value = float(value)
                            except Exception:
                                return jsonify(result=None, error=f"Invalid float for {param_name}")
                        elif param.get('type') == 'integer':
                            try:
                                value = int(value)
                            except Exception:
                                return jsonify(result=None, error=f"Invalid integer for {param_name}")
                        elif param.get('type') == 'boolean':
                            value = value.lower() in ['true', '1', 'yes', 'on']
                        kwargs[param_name] = value
                    try:
                        print("Calling:", func, "with", kwargs)
                        result = func(**kwargs)
                        return jsonify(result=result, unit=calculation.get('result_unit', ''))
                    except Exception as e:
                        return jsonify(result=None, error=str(e))
                return jsonify(result=None, error="Calculation not found.")
           
            return render_template('card_detail.html', category=category)
    return "Category not found", 404


@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    results = []
    for category in data['categories']:
        for calc in category.get('calculations', []):
            if query in calc['name'].lower() or query in calc.get('description', '').lower():
                # Add category slug for linking
                calc_copy = calc.copy()
                calc_copy['category_slug'] = category.get('slug', '')
                results.append(calc_copy)
    return render_template('search_results.html', query=query, results=results)

@app.route('/search_api')
def search_api():
    query = request.args.get('query', '').lower()
    results = []
    for category in data['categories']:
        category_slug = category.get('slug', '')
        for calc in category.get('calculations', []):
            if query in calc['name'].lower() or query in calc.get('description', '').lower():
                results.append({
                    'name': calc['name'],
                    'description': calc.get('description', ''),
                    'category_slug': category_slug
                })
    return jsonify(results)


@app.route('/dashboard')
def dashboard():
    print("🔍 Session contents:", dict(session))
    uid = session.get('user')
    if not uid:
        print("No user in session")
        return "Unauthorized", 401
    print("Dashboard access for:", uid)
    return render_template("dashboard.html", user=uid)


@app.route('/policyai')
def policyai():
    uid = session.get('user')
    if not uid:
        return "Unauthorized", 401
    return render_template("chat.html", user=uid)


if __name__ == '__main__':
    server = Server(app.wsgi_app)
    server.serve()
