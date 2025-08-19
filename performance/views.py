from django.shortcuts import render, redirect, get_object_or_404
from .forms import StudentForm, StudentRegistrationForm
from .models import Student
from sklearn.linear_model import LogisticRegression
import numpy as np
from django.http import HttpResponse
import csv
from reportlab.pdfgen import canvas

# Teacher or Admin Dashboard
def home(request):
    total_students = Student.objects.count()
    pass_count = Student.objects.filter(result='PASS').count()
    fail_count = Student.objects.filter(result='FAIL').count()

    pass_percent = round(pass_count/total_students*100, 2) if total_students > 0 else 0
    fail_percent = round(fail_count/total_students*100, 2) if total_students > 0 else 0

    return render(request, 'performance/home.html', {
        'total_students': total_students,
        'pass_count': pass_count,
        'fail_count': fail_count,
        'pass_percent': pass_percent,
        'fail_percent': fail_percent
    })


# Student Registration Form
def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            # Set default scores because registration doesn't include them
            student.attendance = 0
            student.assignment_score = 0
            student.test_score = 0
            student.teacher_feedback = "Not yet evaluated"
            student.save()
            return redirect('student_login')
    else:
        form = StudentRegistrationForm()

    return render(request, 'performance/student_register.html', {'form': form})


# Student Login
def student_login(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        pin = request.POST.get('pin')
        try:
            student = Student.objects.get(name=name, pin=pin)
            # Store session
            request.session['student_id'] = student.id
            return redirect('student_detail', pk=student.id)
        except Student.DoesNotExist:
            return render(request, 'performance/student_login.html', {'error': 'Invalid credentials'})
    return render(request, 'performance/student_login.html')


# Student detailed analysis view
def student_detail(request, pk):
    # Redirect to login if not in session
    if not request.session.get('student_id'):
        return redirect('student_login')

    student = get_object_or_404(Student, pk=pk)

    labels = ['Attendance', 'Assignment', 'Test']
    scores = [student.attendance, student.assignment_score, student.test_score]

    # If prediction missing (0) then set results neutral
    pass_val = student.prediction_score or 0
    fail_val = 100 - pass_val

    # Suggestion logic
    suggestions = []
    if student.attendance < 60:
        suggestions.append("Improve Attendance")
    if student.assignment_score < 60:
        suggestions.append("Improve Assignment work")
    if student.test_score < 60:
        suggestions.append("Improve Test Preparation")
    if not suggestions:
        suggestions = ["Keep up the good work!"]

    return render(request, 'performance/student_detail.html', {
        'student': student,
        'labels': labels,
        'scores': scores,
        'pass_val': pass_val,
        'fail_val': fail_val,
        'suggestions': suggestions
    })


# Teacher CRUD & ML prediction
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            X_train = np.array([[90, 85, 80], [40, 35, 30], [60, 50, 55]])
            y_train = np.array([1, 0, 1])
            model = LogisticRegression()
            model.fit(X_train, y_train)
            prob = model.predict_proba([[student.attendance, student.assignment_score, student.test_score]])[0][1] * 100
            student.prediction_score = round(prob, 2)
            student.result = 'PASS' if prob >= 50 else 'FAIL'
            student.save()
            return redirect('student_list')
    else:
        form = StudentForm()

    return render(request, 'performance/add_student.html', {'form': form})


def student_list(request):
    students = Student.objects.all()
    filter_val = request.GET.get('filter')
    if filter_val:
        students = students.filter(result=filter_val)
    return render(request, 'performance/student_list.html', {'students': students})


def edit_student(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'performance/edit_student.html', {'form': form, 'student': student})


def delete_student(request, pk):
    student = Student.objects.get(pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'performance/delete.html', {'student': student})


# Export CSV
def export_csv(request):
    students = Student.objects.all()
    resp = HttpResponse(content_type='text/csv')
    resp['Content-Disposition'] = 'attachment; filename="students.csv"'
    writer = csv.writer(resp)
    writer.writerow(['Name', 'Email', 'Mobile', 'Attendance', 'Assignment', 'Test', 'Prediction', 'Result'])
    for s in students:
        writer.writerow([s.name, s.email, s.mobile, s.attendance, s.assignment_score, s.test_score, s.prediction_score, s.result])
    return resp


# Export PDF
def export_pdf(request):
    students = Student.objects.all()
    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = 'attachment; filename="students_report.pdf"'
    p = canvas.Canvas(resp)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Students Report")

    y = 760
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Name")
    p.drawString(200, y, "Email")
    p.drawString(350, y, "Result")

    p.setFont("Helvetica", 11)
    y -= 20
    for s in students:
        p.drawString(50, y, s.name)
        p.drawString(200, y, s.email or '')
        p.drawString(350, y, s.result or '')
        y -= 20
        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return resp
