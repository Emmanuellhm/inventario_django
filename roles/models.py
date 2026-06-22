from django.db import models
from django.conf import settings

class Role(models.Model):
    """Role model to group permissions per user.
    Each role can be assigned to multiple users and a user can have multiple roles.
    """
    name = models.CharField(max_length=30, unique=True, help_text="Nombre del rol (p. ej. admin, manager, sales)")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='roles', blank=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.name
