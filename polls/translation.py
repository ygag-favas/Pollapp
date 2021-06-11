from modeltranslation.translator import TranslationOptions, translator
from polls.models import Question, Choice


class QuestionTranslationOptions(TranslationOptions):
    fields = ('question_text',)


class ChoiceTranslationOptions(TranslationOptions):
    fields = ('choice_text',)


translator.register(Choice, ChoiceTranslationOptions)
translator.register(Question, QuestionTranslationOptions)
