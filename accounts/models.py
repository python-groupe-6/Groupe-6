from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, help_text="FontAwesome icon class")
    criteria = models.CharField(max_length=255, help_text="Internal code for unlocking logic")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='fr', choices=[('fr', 'Français'), ('en', 'English')])
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    # Gamification fields
    xp = models.IntegerField(default=0)
    streak = models.IntegerField(default=0)
    last_activity = models.DateField(null=True, blank=True)
    badges = models.ManyToManyField(Badge, blank=True)

    @property
    def level(self):
        # simple level logic: Level 1 = 0 XP, Level 2 = 500 XP, Level 3 = 1000 XP...
        return (self.xp // 500) + 1

    @property
    def xp_progress(self):
        # Progress within current level
        return (self.xp % 500) / 500 * 100

    def update_xp_and_streak(self, score, total_questions, difficulty_multiplier=1):
        from datetime import date, timedelta
        
        # 1. Update XP
        # Base XP: 10 points per correct answer * difficulty
        points_earned = (score * 10) * difficulty_multiplier
        # Bonus for perfect score
        if score == total_questions:
            points_earned += 50
        
        self.xp += points_earned

        # 2. Update Streak
        today = date.today()
        if self.last_activity == today:
            # Already active today, do nothing for streak
            pass
        elif self.last_activity == today - timedelta(days=1):
            # Active yesterday, increment streak
            self.streak += 1
        else:
            # Missed a day (or more), reset streak to 1
            self.streak = 1
        
        self.last_activity = today
        self.save()
        
        return points_earned


    def __str__(self):
        return f"Profil de {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
    instance.profile.save()
