from django.core.management.base import BaseCommand
from performance.models import Student
import random
import numpy as np
from sklearn.linear_model import LogisticRegression

class Command(BaseCommand):
    help = 'Load 100 dummy students with email, mobile, pin=1234'

    def handle(self, *args, **kwargs):
        X_train = np.array([[90,85,80],[40,35,30],[60,50,55]])
        y_train = np.array([1,0,1])
        model = LogisticRegression()
        model.fit(X_train, y_train)

        Student.objects.all().delete()

        for i in range(1,101):
            name = f'Student{i}'
            email = f'student{i}@example.com'
            mobile = f'9{random.randint(100000000, 999999999)}'
            att = random.randint(40,99)
            ass = random.randint(40,100)
            test = random.randint(35,100)
            pin = '1234'
            feedback = "Good Performance" if att>=60 else "Needs Improvement"

            prob = model.predict_proba([[att,ass,test]])[0][1]*100
            result = 'PASS' if prob >= 50 else 'FAIL'

            Student.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                attendance=att,
                assignment_score=ass,
                test_score=test,
                teacher_feedback=feedback,
                prediction_score=round(prob,2),
                result=result,
                pin=pin
            )

        self.stdout.write(self.style.SUCCESS('Created 100 students with pin=1234'))
