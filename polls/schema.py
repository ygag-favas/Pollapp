import graphene
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from .models import Question, Choice

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('email',)


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ('choice_text', 'votes')


class QuestionType(DjangoObjectType):
    choices = graphene.List(ChoiceType)
    pub_date = graphene.String()
    expiry_date = graphene.String()

    def resolve_pub_date(question, info):
        return question.pub_date.strftime('%Y-%b-%d')

    def resolve_expiry_date(question, info):
        return question.pub_date.strftime('%Y-%b-%d')

    class Meta:
        model = Question
        fields = (
            'question_text', 'pub_date', 'user', 'expiry_date')

    def resolve_choices(question, info):
        return question.choice_set.all()


class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)

    def resolve_all_questions(root, info):
        return Question.objects.all()


schema = graphene.Schema(query=Query)
