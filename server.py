from flask import Flask, request, redirect
import json
import os

app = Flask(__name__, static_folder='.', template_folder='.')

DATA_FILE = 'data.json'

def load_accounts():
    if not os.path.exists(DATA_FILE):
        return {"users": [], "admins": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_accounts(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return redirect('/login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    accounts = load_accounts()

    # تحقق أولاً من حسابات الأدمن
    for admin in accounts.get('admins', []):
        if admin['email'] == email and admin['password'] == password:
            return "مرحباً ادمن، تم تسجيل الدخول بنجاح"  # يمكن تعديل هذا لإعادة التوجيه للوحة تحكم الأدمن

    # ثم تحقق من حسابات المستخدمين
    for user in accounts.get('users', []):
        if user['email'] == email and user['password'] == password:
            return "مرحباً مستخدم، تم تسجيل الدخول بنجاح"  # يمكن تعديل هذا لإعادة التوجيه للصفحة الرئيسية للمستخدم

    return "بيانات الاعتماد غير صحيحة", 401

@app.route('/signup', methods=['POST'])
def signup():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    confirmPassword = request.form.get('confirmPassword')

    if password != confirmPassword:
        return "كلمة المرور غير متطابقة", 400

    accounts = load_accounts()

    # التأكد من عدم تكرار الايميل في حسابات المستخدم أو الأدمن
    for user in accounts.get('users', []):
        if user['email'] == email:
            return "الايميل مستخدم بالفعل", 400
    for admin in accounts.get('admins', []):
        if admin['email'] == email:
            return "الايميل مستخدم بالفعل", 400

    new_user = {
        "firstName": firstName,
        "lastName": lastName,
        "phone": phone,
        "email": email,
        "password": password  # تأكيد: في الإنتاج يجب استخدام تشفير لكلمة المرور
    }
    accounts.setdefault('users', []).append(new_user)
    save_accounts(accounts)
    return "تم انشاء الحساب بنجاح", 200

if __name__ == '__main__':
    app.run(debug=True)