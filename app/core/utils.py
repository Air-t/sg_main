from datetime import datetime, timedelta

from core.models import CloseChoice, UserExam


def now_plus_15_min():
    """Return actual datetime plus 15min ahead"""
    return datetime.now() + timedelta(minutes=15)


def evaluate_exam(exam, user):
    print(user)
    print(type(user))
    user_score = 0
    pass_score = exam.pass_percentage
    print(pass_score)
    questions = exam.closequestion_set.all().select_related()
    user_choices = CloseChoice.objects.all().filter(close_question__exam=exam).filter(closeanswer__user=user)
    for question in questions:
        question_points = question.max_points
        user_answers = user_choices.filter(close_question=question)
        valid_choices = question.closechoice_set.all().filter(is_true=True)
        print(user_answers)
        print(valid_choices)
        if set(user_answers) == set(valid_choices):
            user_score += question_points
        print(user_score)
    user_exam = UserExam.objects.create(student=user, exam=exam, score=user_score, is_passed=True)
    try:
        user_exam.save()
    except Exception as e:
        print('Error saving UserExam')

    print(user_score)
    return user_exam
