from django.contrib import admin
from shedule_app import models as md
from shedule_app.forms import UserAdminForm
from django.db.models import QuerySet
from datetime import datetime

# Register your models here.


@admin.register(md.User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('name', 'tel_number', 'birthday', 'newbie')
    list_filter = ('name', 'tel_number', 'birthday', 'newbie')
    exclude = ('telegram_id',)

    def save_model(self, request, obj, form, change):
        str_number = str(obj.tel_number)
        formatted_number = '{}({})-{}-{}-{}'.format(str_number[0], 
            str_number[1:4], str_number[4:7], str_number[7:9], str_number[9:])
        obj.tel_number = formatted_number
        super().save_model(request, obj, form, change)


@admin.register(md.Training)
class TrainingAdmin(admin.ModelAdmin):
    exclude = ('was_end',)
    list_display = ('place', 'address', 'time', 'day', 'repeat',)
    list_filter = ('place', 'address', 'time', 'day', 'repeat',)


@admin.register(md.Journal)
class JournalAdmin(admin.ModelAdmin):
    exclude = ('second_not', 'previuos_answer')
    list_display = ('training', 'user', 'accept', 'answer_time', 'rate', 'date_time')
    list_filter = ('training', 'user', 'accept', 'answer_time', 'rate', 'date_time')


@admin.register(md.Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'place', 'address', 'rate',)
    list_filter = ('date_time', 'place', 'address', 'rate',)
    readonly_fields = ('date_time', 'place', 'address', 'rate',)

@admin.register(md.Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)

@admin.register(md.Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('place', 'address', 'team', 'date_time')
    list_filter = ('place', 'address', 'team', 'date_time')
    actions = ['copy_game']

    @admin.action(description='Сделать копию игры')
    def copy_game(self, request, queryset: QuerySet):
        game = queryset.first()
        new_game = md.Game.objects.create(
                place=game.place,
                address=game.address,
                team=game.team,
                route=game.route,
                date_time=datetime.strptime('1970-01-01 00:00:00', '%Y-%m-%d %H:%M:%S')
            )
        new_game.save()



@admin.register(md.GameJournal)
class GameJournalAdmin(admin.ModelAdmin):
    list_display = ('game', 'user', 'accept', 'answer_time', 'date_time')
    list_filter = ('game', 'user', 'accept', 'answer_time', 'date_time')