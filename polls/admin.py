
from django.contrib import admin
from django.forms import BaseInlineFormSet, forms

from .forms import VerifyTagAdmin
from .models import Choice, Question, Comment, Tag


class ChoiceFormSet(BaseInlineFormSet):
    def clean(self):
        super(ChoiceFormSet, self).clean()
        if any(self.errors):
            return
        choice_texts = []
        duplicates = False
        for form in self.forms:
            if form.cleaned_data:
                choice_text = form.cleaned_data['choice_text']
                if choice_text:
                    if choice_text in choice_texts:
                        duplicates = True
                    choice_texts.append(choice_text)
                if duplicates:
                    raise forms.ValidationError(
                        'Choice already exists.'
                    )


class ChoiceInline(admin.TabularInline):
    model = Choice
    formset = ChoiceFormSet
    min_num = 2


class TagInline(admin.TabularInline):
    model = Question.tags.through
    extra = 3


class TagAdmin(admin.ModelAdmin):
    form = VerifyTagAdmin
    exclude = ('question',)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldset = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields':['pub_date'], 'classes':['collapse']}),
        ('created by', {'fields': ['user']}),
        ('Expiry date', {'fields': ['expiry_date']}),
        ('Order no', {'fields': ['order_no']})

    ]
    inlines = [ChoiceInline, TagInline, CommentInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently',
                    'choices_count', 'user')
    list_filter = ['order_no']
    search_fields = ['question_text']

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        else:
            return False,


admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
admin.site.register(Tag, TagAdmin)

