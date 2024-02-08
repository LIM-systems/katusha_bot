from django.db import models
from bot.config import DAYS

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50, verbose_name='ФИО')
    tel_number = models.CharField(max_length=16, verbose_name='Телефон', help_text='В формате: 8000000000')
    telegram_id = models.BigIntegerField(verbose_name='Телеграм ID', blank=True, null=True)
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    newbie = models.BooleanField(default=False, verbose_name='Новичок?')

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    def __str__(self):
        return self.name


class Training(models.Model):
    
    time = models.TimeField(verbose_name='Время тренировки')
    day = models.CharField(max_length=20,verbose_name='День тренировки', choices=DAYS)
    repeat = models.BooleanField(default=False, verbose_name='Повторять каждую неделю?')
    place = models.CharField(max_length=100,verbose_name='Место проведения')
    address = models.CharField(max_length=100, verbose_name='Адрес проведения')
    was_end = models.BooleanField(default=False, verbose_name='Завершена')
    route = models.URLField(verbose_name='Ссылка на маршрут')

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'

    def __str__(self):
        for day in DAYS:
            if self.day in day:
                week_day = day[1]
                break
        return f'{week_day} {self.place}'
    

class Journal(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, verbose_name='Тренировка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник')
    accept = models.BooleanField(verbose_name='Запись подтверждена', 
                                blank=True, null=True)
    answer_time = models.DateTimeField(verbose_name='Время ответа', blank=True, null=True)
    previuos_answer = models.BooleanField(blank=True, null=True)
    second_not = models.BooleanField(default=False)
    date_time = models.DateTimeField(verbose_name='Дата тренировки', blank=True, null=True)
    rate = models.IntegerField(blank=True, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Журнал тренировок'
        verbose_name_plural = 'Журнал тренировок'

    def __str__(self):
        return str(self.date_time)
    
class Rate(models.Model):
    date_time = models.DateTimeField(verbose_name='Дата и время', blank=True, null=True)
    place = models.CharField(max_length=100, verbose_name='Место')
    address = models.CharField(max_length=150, verbose_name='Адрес проведения')
    rate = models.FloatField(blank=True, null=True, verbose_name='Оценка')

    class Meta:
        verbose_name = 'Оценка Тренировки'
        verbose_name_plural = 'Оценки Тренировок'

    def __str__(self):
        return str(self.date_time)
    

class Message(models.Model):
    user_id = models.BigIntegerField()
    incoming_msg_id = models.BigIntegerField()
    outgoing_msg_id = models.BigIntegerField()

    def __str__(self):
        return str(self.user_id)
    
class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    users = models.ManyToManyField(User, verbose_name='Игроки')

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

    def __str__(self):
        return self.name
    

class Game(models.Model):
    place = models.CharField(max_length=50, verbose_name='Место')
    address = models.CharField(max_length=50, verbose_name='Адрес')
    route = models.URLField(verbose_name='Ссылка на маршрут')
    date_time = models.DateTimeField(verbose_name='Дата и время')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, verbose_name='Команда', null=True)

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'

    def __str__(self):
        return self.place
    

class GameJournal(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Игра')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Участник')
    date_time = models.DateTimeField(verbose_name='Дата игры', blank=True, null=True)
    accept = models.BooleanField(verbose_name='Запись подтверждена', 
                                blank=True, null=True)
    previuos_answer = models.BooleanField(blank=True, null=True)
    answer_time = models.DateTimeField(verbose_name='Время ответа', blank=True, null=True)

    class Meta:
        verbose_name = 'Журнал игр'
        verbose_name_plural = 'Журнал игр'

    def __str__(self):
        return str(self.game)

