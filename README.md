# Student Performance Prediction System – Django & Machine Learning

This is a full-stack web application built using Python **Django Framework**, **MySQL**, and a **Logistic Regression ML model** to predict whether a student will pass or fail based on their academic parameters such as attendance, assignment scores, and test scores.

---

## 🔍 Features

- Django-based web application with admin/teacher CRUD
- Student login & registration with PIN
- Machine Learning prediction of student performance
- Real-time **probability %** of Pass/Fail
- **Suggestion engine** for weak areas (attendance, assignment, test)
- Data visualization using Chart.js
- PDF and CSV export of student data
- Tailwind styled UI similar to a University ERP system
- Separate teacher/admin dashboard and student dashboard

---

## 🧠 Technologies Used

| Layer           | Technology                                           |
|-----------------|------------------------------------------------------|
| Backend         | Python, Django                                       |
| ML Algorithm    | Logistic Regression (scikit-learn)                   |
| Frontend        | HTML, Tailwind CSS, Chart.js                         |
| Database        | MySQL (also works with SQLite for testing)           |

---

## 🧾 Project Structure

```
student_performance_prediction/
├─ manage.py
├─ student_system/           
│   ├─ settings.py
│   └─ ...
├─ performance/             
│   ├─ models.py
│   ├─ views.py
│   ├─ urls.py
│   ├─ forms.py
│   ├─ management/commands/loaddummy.py
│   └─ templates/performance/
├─ requirements.txt
```

---

## ⚙️ How to Run Locally

1. Clone the repository  
2. Create a virtual environment  
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. (Optional) Load dummy data:
   ```bash
   python manage.py loaddummy
   ```

6. Run server:
   ```bash
   python manage.py runserver
   ```

---

## 🧠 Machine Learning Logic

```python
X_train = np.array([[90,85,80], [40,35,30], [60,50,55]])
y_train = np.array([1, 0, 1])
model = LogisticRegression()
model.fit(X_train, y_train)
```

Prediction probability is calculated and stored as `prediction_score` and student's result is set to **PASS** or **FAIL**.

---

## 🎓 Conclusion

This project showcases how machine learning can be integrated with full-stack web development to provide actionable insights to students and teachers. It can be further expanded with more sophisticated ML models and larger datasets.

---

## ⭐ Author

**Ali Faiz**
