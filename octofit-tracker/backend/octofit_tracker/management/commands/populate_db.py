from django.core.management.base import BaseCommand
from octofit_tracker.models import Team, User, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()
        Workout.objects.all().delete()

        # Create Teams
        marvel = Team.objects.create(name='Team Marvel', universe='Marvel')
        dc = Team.objects.create(name='Team DC', universe='DC')

        # Create Users (Superheroes)
        users = [
            User(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
            User(name='Iron Man', email='ironman@marvel.com', team=marvel),
            User(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
            User(name='Batman', email='batman@dc.com', team=dc),
        ]
        for user in users:
            user.save()

        # Create Workouts
        workouts = [
            Workout(name='Super Strength', description='Heavy lifting and strength training', difficulty='Hard'),
            Workout(name='Agility Training', description='Speed and agility drills', difficulty='Medium'),
        ]
        for workout in workouts:
            workout.save()

        # Create Activities
        Activity.objects.create(user=users[0], type='Web Swinging', duration=60, date=timezone.now())
        Activity.objects.create(user=users[1], type='Suit Training', duration=45, date=timezone.now())
        Activity.objects.create(user=users[2], type='Lasso Practice', duration=30, date=timezone.now())
        Activity.objects.create(user=users[3], type='Detective Work', duration=90, date=timezone.now())

        # Create Leaderboard
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data!'))
