from django.db import models
from django.contrib.auth.models import User, UserManager


BOT_TYPES = (
#    (0, "Logbot"),
#    (1, "Pastebot"),
    (2, "Googlebot"),
)
STATUS_TYPES = (
    (0, "Offline"),
    (1, "Running"),
    (2, "Updating"),
    (3, "Error"),
)


class Customer(User):
    # Used for user creation
    objects = UserManager()


class Bot(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=36)
    nick = models.CharField(max_length=36)
    type = models.IntegerField(max_length=1, choices=BOT_TYPES)
    server = models.URLField(verify_exists=False)
    port = models.PositiveIntegerField(max_length=4)
    channels = models.CharField(max_length=2000)
    server_password = models.CharField(max_length=36)
    nickserv_password = models.CharField(max_length=36)
    status = models.IntegerField(max_length=1, choices=STATUS_TYPES)
    
    @models.permalink
    def get_absolute_url(self):
        return ('bothost.common.views.common_bot', [str(self.id)])
    
#class Update(models.Model):
#    bot = models.ForeignKey("Bot")
#    type = models.CharField(max_length=36, choices=UPDATE_TYPES)
#    arguments = models.CharField(max_length=2000)
    
#class BotData(models.Model):
#    bot = models.ForeignKey("Bot")
#    date = models.DateField(auto_now_add=True)
#    time = models.TimeField(auto_now_add=True)
#    content = models.CharField(max_length=2000)

