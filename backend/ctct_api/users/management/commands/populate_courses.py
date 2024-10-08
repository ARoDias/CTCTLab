# ctct_api/management/commands/populate_courses.py
from django.core.management.base import BaseCommand
from users.models import Course

class Command(BaseCommand):
    help = 'Populates the database with courses'

    def handle(self, *args, **options):
        course_names = [
            'Química Aplicada',
            'Tecnologia Agro-Industrial',
            'Matemática Aplicada à Gestão do Risco',
            'Matemática',
            'Engenharia Química e Biológica',
            'Engenharia de Micro e Nanotecnologias',
            'Engenharia Mecânica',
            'Engenharia de Materiais',
            'Engenharia Informática',
            'Engenharia e Gestão Industrial',
            'Engenharia Geológica',
            'Engenharia Física',
            'Engenharia Eletrotécnica e de Computadores',
            'Engenharia Civil',
            'Engenharia Biomédica',
            'Engenharia do Ambiente',
            'Bioquímica',
            'Biologia Celular e Molecular',
            'Outro',
        ]

        for course_name in course_names:
            course, created = Course.objects.get_or_create(name=course_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Course {course.name} created'))
            else:
                self.stdout.write(self.style.WARNING(f'Course {course.name} already exists'))


