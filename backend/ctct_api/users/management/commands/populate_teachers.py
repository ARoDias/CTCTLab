from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Classroom, TeacherProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with teachers and associates them with classrooms'

    def create_teacher(self, full_name):
        first_name, last_name = full_name.split(maxsplit=1)
        username = first_name.lower() + '.' + last_name.lower()
        user, created = User.objects.get_or_create(username=username, defaults={
            'first_name': first_name,
            'last_name': last_name,
            'is_teacher': True
        })
        teacher_profile, _ = TeacherProfile.objects.get_or_create(user=user)
        return teacher_profile

    def handle(self, *args, **options):
        # Map of practical class teachers
        p_teachers = {
            'P1': 'Lígia Castro', 'P2': 'Adriane Michels Brito', 
            'P3': 'João Feio Almeida', 'P4': 'Florbela Pereira', 
            'P5': 'Inês Coutinho', 'P6': 'Nuno Miguel Marques', 
            'P7': 'Alexandra Maria Ramos Tenera', 'P8': 'Pedro Lamas', 
            'P9': 'Madalena Dionisio', 'P10': 'Catarina Oliveira dos Santos', 
            'P11': 'João Diogo', 'P12': 'Teresa Santos Silva', 
            'P13': 'Joaquim Simão', 'P14': 'Paulo Doutor', 
            'P15': 'Mauro Guerra', 'P16': 'Paulo Legoinha', 
            'P17': 'Luísa Ferreira Lopes', 'P18': 'Margarida Rolim', 
            'P19': 'Alexandre Costa', 'P20': 'Mário Ramos', 
            'P21': 'Gonçalo Carrera', 'P22': 'Cláudia Campos Pessoa', 
            'P23': 'Isabel Nobre', 'P24': 'Diogo Sousa', 
            'P25': 'Krasimira Petrova', 'P26': 'Ana Margarida Marques', 
            'P27': 'Naiara Machado Casagrande', 'P28': 'Diana Freire Daccak', 
            'P29': 'Fernando Cruz', 'P30': 'Sara Sobral Babo', 
            'P31': 'Rui Marreiros', 'P32': 'Ana Rita Coelho'
        }
    
        # Map of theoretical-practical class teachers
        tp_teachers = {
            'TP1': 'Ricardo Franco', 'TP2': 'Rita Branquinho', 
            'TP3': 'João Pedro Veiga', 'TP4': 'Fernando Ferreira',
            'TP5': 'Ricardo Franco', 'TP6': 'Rita Branquinho', 
            'TP7': 'João Pedro Veiga', 'TP8': 'Fernando Ferreira'
        }

        # Create and associate teachers for P classrooms
        for classroom_name, teacher_name in p_teachers.items():
            classroom = Classroom.objects.get(name=classroom_name)
            teacher_profile = self.create_teacher(teacher_name)
            teacher_profile.classrooms.add(classroom)

        # Create and associate teachers for TP classrooms
        for classroom_name, teacher_name in tp_teachers.items():
            classroom = Classroom.objects.get(name=classroom_name)
            teacher_profile = self.create_teacher(teacher_name)
            teacher_profile.classrooms.add(classroom)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with teachers and associated them with classrooms'))
