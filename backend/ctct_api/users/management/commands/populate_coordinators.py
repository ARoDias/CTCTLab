from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from users.models import Classroom, TeacherProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with specific CTCT teachers and associates them with classrooms'

    def add_teacher(self, first_name, last_name, email, department, phone, classrooms):
        # Use the email prefix as the username
        username = email.split('@')[0]
        # Check if a user exists with the given username
        user, created = User.objects.get_or_create(
            username=username, defaults={
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
            }
        )
        if created:
            # Set a memorable password
            default_password = "CTCT2024!"
            user.set_password(default_password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Teacher {first_name} {last_name} created with password {default_password}'))
        else:
            self.stdout.write(self.style.WARNING(f'Teacher {first_name} {last_name} already exists'))

        # Create or update the teacher profile with the given department and phone
        teacher_profile, profile_created = TeacherProfile.objects.update_or_create(
            user=user,
            defaults={
                'department': department,
                'phone': phone
            }
        )
        
        if profile_created:
            self.stdout.write(self.style.SUCCESS(f'TeacherProfile for {first_name} {last_name} created with department: {department} and phone: {phone}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'TeacherProfile for {first_name} {last_name} updated with department: {department} and phone: {phone}'))

        # Associate the teacher with the given classrooms
        for classroom_name in classrooms:
            classroom, _ = Classroom.objects.get_or_create(name=classroom_name)
            teacher_profile.classrooms.add(classroom)
            self.stdout.write(self.style.SUCCESS(f'Classroom {classroom_name} added to {first_name} {last_name}'))

        return teacher_profile
    def handle(self, *args, **options):
        teachers_data = [
            ('Fernando', 'Ferreira', 'flf@fct.unl.pt', 'DEEC', '969070002', ['TP4', 'TP8']),
            ('João Pedro', 'Veiga', 'jpv@fct.unl.pt', 'DCR', '919606940', ['TP1', 'TP5']),
            ('Ricardo', 'Franco', 'rft@fct.unl.pt', 'DQ', '916961952', ['TP3', 'TP7']),
            ('Rita', 'Branquinho', 'ritasba@fct.unl.pt', 'DCM', '926498900', ['TP2', 'TP6']),
            ('Nelson Chibeles', 'Martins', 'npm@fct.unl.pt', 'DM', '914437320', [])
    ]

        for first_name, last_name, email, department, phone, classrooms in teachers_data:
            self.add_teacher(first_name, last_name, email, department, phone, classrooms)

        for first_name, last_name, email, department, phone, classrooms in teachers_data:
            # Create or get the teacher profile
            teacher_profile = self.add_teacher(first_name, last_name, email, department, phone, classrooms)
            if not classrooms:  # Grant admin privileges if no classrooms are associated
                teacher_profile.user.is_staff = True
                teacher_profile.user.is_superuser = True
                teacher_profile.user.save()
                self.stdout.write(self.style.SUCCESS(f'Admin privileges granted to {first_name} {last_name}'))

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with specific teachers and associated them with classrooms'))
