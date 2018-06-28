from django.db import models
from django.contrib.auth.models import AbstractUser
from .grade_sheet import SubjectGrade, SubjectGradePoint

class CustomUser(AbstractUser):
    name=models.CharField('Full Name',max_length=100)



class StdCommon(models.Model):
    pub_date=models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now_add=True)


class StdSubject(StdCommon):
    REGULAR='R'
    OPTIONAL='O'

    SUBJECT_TYPE_CHOICE=(
        (REGULAR, 'REGULAR'),
        (OPTIONAL, 'OPTIONAL')
    )


    subject_name = models.CharField('Subject Name', max_length=100)
    subject_type = models.CharField(
        'Subject Type', max_length=1, default=REGULAR, choices=SUBJECT_TYPE_CHOICE)
    subject_full_marks = models.DecimalField(
        'Full Marks', max_digits=5, decimal_places=2, default=100)
    subject_pass_marks = models.DecimalField(
        'Pass Marks', max_digits=5, decimal_places=2)
    

    def __str__(self):
        return self.subject_name


class StudentInfo(StdCommon):
    STD_CLASS=(
        ('6','SIX'),
        ('7','SEVEN'),
    )
    std_name = models.CharField('Student Name',max_length=100, help_text='Mr Monir')
    std_class = models.CharField('Student Class',max_length=2, choices=STD_CLASS, default=6, help_text='Select a class')
    std_roll = models.IntegerField('Roll Number',help_text='Only Number')

    std_subjects = models.ManyToManyField(StdSubject)

    def __str__(self):
        return self.std_name





class Marks(StdCommon):
    std_name=models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    subject_name = models.ForeignKey(StdSubject, on_delete=models.CASCADE)
    subject_marks=models.DecimalField(max_digits=5, decimal_places=2)

    subject_gradepoint=models.DecimalField('Grade Point', max_digits=3, decimal_places=1, blank=True, null=True, help_text="Please keep blank")
    subject_gpa = models.CharField('Subject GPA', max_length=5, blank=True, null=True, help_text="Please keep blank")
    std_result=models.FloatField(blank=True, null=True)
   


    def __str__(self):
        return self.std_name.std_name+' Class: '+str(self.std_name.std_class)+' Roll: '+str(self.std_name.std_roll) +' ' + self.subject_name.subject_name +' '+str(self.subject_marks)



    def subject_grade(self):
        grade = SubjectGrade(self.subject_marks,self.subject_name.subject_full_marks).subgrade()
        return grade

    def subject_grade_point(self):
        grade = SubjectGradePoint( self.subject_marks, self.subject_name.subject_full_marks).subgrade()
        return grade


    def save(self, *args, **kwargs):
        grade_point = SubjectGradePoint(self.subject_marks, self.subject_name.subject_full_marks).subgrade()
        gpa = SubjectGrade(self.subject_marks,self.subject_name.subject_full_marks).subgrade()

        if self.subject_name.subject_type=='O':
            if self.subject_marks >= ((self.subject_name.subject_full_marks/100)*50) and self.subject_marks <= self.subject_name.subject_full_marks:
                subject_opt_grade_point = grade_point-2

                self.subject_gradepoint = subject_opt_grade_point
                self.subject_gpa = gpa
            elif self.subject_marks >= ((self.subject_name.subject_full_marks/100)*33) and self.subject_marks < ((self.subject_name.subject_full_marks/100)*50):
                self.subject_gradepoint = 0
                self.subject_gpa=gpa

            elif self.subject_marks < ((self.subject_name.subject_full_marks/100)*33):
                self.subject_gradepoint = 0
                self.subject_gpa = gpa

                
        elif self.subject_name.subject_type=='R':
            self.subject_gradepoint = grade_point
            self.subject_gpa = gpa

        

        

        super().save(*args, **kwargs)


    






class Person(models.Model):
    name=models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Group(models.Model):
    name=models.CharField(max_length=120)
    members=models.ManyToManyField(Person, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    person=models.ForeignKey(Person, on_delete=models.CASCADE)
    group=models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined=models.DateField()
    invite_reason=models.CharField(max_length=64)
