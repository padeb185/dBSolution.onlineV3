from django.contrib import admin

from .models import Notification, ParametresNotifications, PreferenceNotification, RegleNotification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("titre", "type", "destinataire", "emetteur", "lue", "email_envoye", "created_at")
    list_filter = ("type", "lue")
    search_fields = ("titre", "message")


@admin.register(RegleNotification)
class RegleNotificationAdmin(admin.ModelAdmin):
    list_display = ("type", "actif", "roles", "canal_app", "canal_email")


@admin.register(PreferenceNotification)
class PreferenceNotificationAdmin(admin.ModelAdmin):
    list_display = ("utilisateur", "type", "recevoir_app", "recevoir_email")
    list_filter = ("type",)


admin.site.register(ParametresNotifications)
