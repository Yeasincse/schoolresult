from django.contrib import admin

from results.models import StudentInfo, StdSubject, Marks, Rank, SubjectTecher




class RankInstanceInline(admin.TabularInline):
    model=Rank
    fk_name='std'
    extra=0


STD_CLASS = (
    ('6', 'Six'),
    ('7', 'Seven'),
    ('8', 'Eight'),
    ('9', 'Nine'),
    ('10', 'Ten'),
)


class SubjectInstanceInline(admin.TabularInline):
    model = Marks
    fk_name = 'std_name'
    extra = 8

    exclude = ['subject_gradepoint', 'subject_gpa','subject_gpa_sub', 'subject_marks', 'subject_total_marks']

    #filter_horizontal = ('Six','Ten')

    #raw_id_fields = ("subject_name",)

    
class SubjectInstance(admin.StackedInline):
    model = StdSubject
    fk_name = 'teacher'
    extra = 8
    
    exclude = ['subject_form_searh_name',
               'subject_full_marks', 'subject_total_marks', 'first_second_full_marks']
    
    



@admin.register(StudentInfo)
class StudentAdmin(admin.ModelAdmin):
    list_filter = ('std_class', 'std_gender', 'std_group')
    list_display = ('std_name', 'std_class', 'std_group', 'std_gender', 'std_roll')
    inlines = [SubjectInstanceInline]

    
    search_fields = ('std_name','std_roll','std_group')

    
    exclude = ['std_total_marks', 'std_gpa','std_grade_point_total_sum','std_marks_with_fail_sub', 'std_grade_point_total_subject_avg', 'std_fail_subject','school_rank','class_rank']
    
    class Media:
        js = (
            '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
            'js/myscript.js',       # project static folder
            'app/js/myscript.js',   # app static folder
        )






@admin.register(StdSubject)
class SubjectModelAdmin(admin.ModelAdmin):
    list_filter = ('subjet_class', 'subject_type')
    list_display = ('subject_name', 'subjet_class',
                    'subject_type', 'subject_full_marks')

    search_fields = ('subject_name', 'subject_code')










@admin.register(SubjectTecher)
class SubjectTecherModel(admin.ModelAdmin):
    list_filter = ('teacher_name','teach_phone_number')
    search_fields = ('teacher_name', 'teach_phone_number')
    
    inlines = [SubjectInstance]

