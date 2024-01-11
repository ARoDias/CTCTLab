from django.core.management.base import BaseCommand
from users.models import Classroom, ClassroomType

class Command(BaseCommand):
    help = 'Populates the database with classrooms'

    def handle(self, *args, **options):
        # Data for P classrooms with their capacities
        p_classrooms = [
            ('P1', 40), ('P2', 40), ('P3', 40), ('P4', 40),
            ('P5', 30), ('P6', 40), ('P7', 40), ('P8', 40),
            ('P9', 40), ('P10', 30), ('P11', 30), ('P12', 40),
            ('P13', 40), ('P14', 40), ('P15', 40), ('P16', 40),
            ('P17', 40), ('P18', 40), ('P19', 30), ('P20', 40),
            ('P21', 30), ('P22', 30), ('P23', 40), ('P24', 30),
            ('P25', 30), ('P26', 40), ('P27', 30), ('P28', 30),
            ('P29', 40), ('P30', 30), ('P31', 40), ('P32', 30),
        ]

        # Create P classrooms
        for name, capacity in p_classrooms:
            Classroom.objects.create(name=name, capacity=capacity, class_type=ClassroomType.P)

        # Data for TP classrooms with varying capacities
        tp_classrooms = {
            'TP1': 190, 'TP2': 190, 'TP3': 100, 'TP4': 100,
            'TP5': 190, 'TP6': 190, 'TP7': 190, 'TP8': 190,
        }

        # Create TP classrooms
        for name, capacity in tp_classrooms.items():
            Classroom.objects.create(name=name, capacity=capacity, class_type=ClassroomType.TP)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with classrooms'))
