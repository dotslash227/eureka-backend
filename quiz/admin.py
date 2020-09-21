from django.contrib import admin
from .models import Quiz, Question, Option, Results

class OptionInline(admin.StackedInline):
    model = Option
    extra = 1    

class QuestionInline(admin.StackedInline):    
    inlines = [OptionInline]    
    model = Question
    extra = 4

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

class OptionAdmin(admin.ModelAdmin):
    list_display = ["option", "question", "id"]
    list_filter = ["correct"]

admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question)
admin.site.register(Option, OptionAdmin)
admin.site.register(Results)