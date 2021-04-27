from rest_framework import serializers
from polls.models import Question, Choice, Comment


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('choice_text', 'votes')


class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=False)
    pub_date = serializers.DateTimeField(format="%d-%b-%Y",
                                         input_formats=['%d-%b-%Y',
                                                        'iso-8601'])
    expiry_date = serializers.DateTimeField(format="%d-%b-%Y",
                                            input_formats=['%d-%b-%Y',
                                                           'iso-8601'])

    class Meta:
        model = Question
        fields = ('question_text', 'pub_date', 'user', 'expiry_date',
                  'choices')

    def create(self, validated_data):
        choices = validated_data.pop('choices')
        question = Question.objects.create(**validated_data)
        for choice in choices:
            Choice.objects.create(**choice, question=question)
        return question


class CommentSerializer(serializers.ModelSerializer):
    question_text = serializers.CharField(read_only=True,
                                          source='question.question_text')

    class Meta:
        model = Comment
        fields = ['question_text', 'question', 'email', 'content']
        extra_kwargs = {
            'question': {'write_only': True}
        }