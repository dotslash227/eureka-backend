from django.contrib import admin
from .models import Quiz, Question, Option

class OptionInline(admin.StackedInline):    
    model = Option
    extra = 1    

class QuestionInline(admin.StackedInline):    
    inlines = [OptionInline]    
    model = Question
    extra = 4

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Option)