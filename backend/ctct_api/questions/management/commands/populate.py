# ainda nao esta a ser utilizado porque os modelos estao diferentes, preencher no fim se necessario
from django.core.management.base import BaseCommand
from users.models import User, Course, StudentProfile, TeacherProfile, Classroom
from questions.models import Question, Questionnaire

from random import randint

class Command(BaseCommand):
    help = 'Populates the database'
 # Cria perguntas de vários tipos e adiciona ao banco de dados
    mc_question = Question.objects.create(
        question_text='Qual é a sua opinião sobre o programa Erasmus?',
        question_type='MC',
        options='Excelente,Bom,Neutro,Mau,Terrível'
    )

    tf_question = Question.objects.create(
        question_text='Acha que a experiência Erasmus é benéfica para o currículo?',
        question_type='TF',
        options='Verdadeiro,Falso'
    )

    ls_question = Question.objects.create(
        question_text='Como classificaria a sua experiência Erasmus numa escala de 1 a 5?',
        question_type='LS',
        scale_range=5
    )

    dm_question = Question.objects.create(
        question_text='Qual é a sua idade?',
        question_type='DM',
        demographic_type='age'
    )

    oe_question = Question.objects.create(
        question_text='Que conselho daria a um estudante que está a considerar o programa Erasmus?',
        question_type='OE',
    )

    # Cria um questionário e adiciona as perguntas
    questionnaire = Questionnaire.objects.create(
        title='Questionário Erasmus',
        description='Um questionário para recolher opiniões sobre o programa Erasmus.'
    )
    questionnaire.questions.add(mc_question, tf_question, ls_question, dm_question, oe_question)

    questionnaire.save()
    def create_users(self):
        for i in range(1, 21):  # Create 20 users, 10 students and 10 teachers
            if i <= 10:
                User.objects.create(username=f'student{i}', password='123', is_student=True)
            else:
                User.objects.create(username=f'teacher{i}', password='123', is_teacher=True)

    def create_classrooms(self):
        for i in range(1, 11):  # Create 10 classrooms
            Classroom.objects.create(class_id=f'Classroom{i}')

    def create_student_profiles(self):
        users = User.objects.filter(is_student=True)
        courses = Course.objects.all()
        classrooms = Classroom.objects.all()
        for user in users:
            StudentProfile.objects.create(user=user, classroom=classrooms[randint(0,9)], student_number=randint(1,100), course=courses[randint(0,9)], age=randint(18,30), gender='M', data_consent=True)

    def create_teacher_profiles(self):
        users = User.objects.filter(is_teacher=True)
        classrooms = Classroom.objects.all()
        for user in users:
            TeacherProfile.objects.create(user=user, classroom=classrooms[randint(0,9)])

    def handle(self, *args, **options):
        self.create_users()
        self.create_classrooms()
        self.create_student_profiles()
        self.create_teacher_profiles()
        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))

