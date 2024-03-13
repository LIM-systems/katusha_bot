from asgiref.sync import sync_to_async
from shedule_app import models as mdl
from datetime import datetime, timedelta
from bot.config import DAYS
import logging

@sync_to_async()
def check_new_user(user_id):
    tg_id = mdl.User.objects.filter(telegram_id=user_id).first()
    return tg_id

@sync_to_async()
def get_users_ids():
    users = mdl.User.objects.filter(telegram_id__isnull=False).all()
    telegram_ids = [user.telegram_id for user in users]
    return telegram_ids

@sync_to_async()
def change_phone(user_id, phone):
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    user.tel_number = phone
    user.save()

@sync_to_async()
def change_birthday(user_id, birthday):
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    user.birthday = birthday
    user.save()

@sync_to_async()
def change_name(user_id, name):
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    user.name = name
    user.save()

@sync_to_async()
def identification_by_tel_number(user_id, tel_number):
    str_number = str(tel_number)
    formatted_number = '{}({})-{}-{}-{}'.format(str_number[0], 
            str_number[1:4], str_number[4:7], str_number[7:9], str_number[9:])
    user = mdl.User.objects.filter(tel_number=formatted_number).first()
    if not user:
        return None
    user.telegram_id = user_id
    user.save()
    return user.name

@sync_to_async()
def add_new_user(name, phone_number, birthday, source, user_id):
    new_user = mdl.User.objects.create(
            name=name, 
            tel_number=phone_number,
            birthday=birthday,
            telegram_id=user_id,
            source=source,
            newbie=True
        )
    new_user.save()

@sync_to_async()
def get_trainings(day):
    trainings = mdl.Training.objects.filter(was_end=False).all()
    if not trainings:
        return None
    todays = trainings.filter(day=day).all()
    today_trainings = []
    if todays:
        for today in todays:
            today_trainings.append({
                'place': today.place,
                'day': today.day,
                'time': today.time
            })
    return today_trainings

@sync_to_async()
def get_trainings_for_rate(today_day, yesterday_day):
    # # для тестов
    # test_date_time = "2023-11-20 00:00:00"
    # now = datetime.strptime(test_date_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    trainings_today = mdl.Training.objects.filter(day=today_day).all()
    trainings_yesterday = mdl.Training.objects.filter(day=yesterday_day).all()
    if not trainings_today and not trainings_yesterday: return None
    today = now 
    yesterday = now - timedelta(days=1)

    trainings_for_rate = []

    training_date = today.date()
    for training in trainings_today:
        training_time = training.time
        date_time = datetime.combine(training_date, training_time)
        entry = mdl.Journal.objects.filter(training=training, date_time=date_time).first()
        if not entry: continue
        time_difference_hours = (now - entry.date_time).total_seconds() // 3600
        if entry and 2 <= int(time_difference_hours) <= 4:
            trainings_for_rate.append({
                'date': training_date,
                'day': training.day,
                'time': training.time
            })

    training_date = yesterday.date()
    for training in trainings_yesterday:
        training_time = training.time
        date_time = datetime.combine(training_date, training_time)
        entry = mdl.Journal.objects.filter(training=training, date_time=date_time).first()
        if not entry: continue
        time_difference_hours = (now - entry.date_time).total_seconds() // 3600
        if entry and 2 <= int(time_difference_hours): # <= 4
            trainings_for_rate.append({
                'date': training_date,
                'day': training.day,
                'time': training.time,
                'place': training.place
            })
    
    if not trainings_for_rate: return None
    return trainings_for_rate


@sync_to_async()
def get_training_data_for_accept(date, training_id, user_id):
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    training = mdl.Training.objects.filter(id=training_id).first()
    training_time = training.time
    date_time = datetime.combine(date, training_time)
    journal_entry = mdl.Journal.objects.filter(training=training, user=user, date_time=date_time).first()
    
    return journal_entry.date_time


@sync_to_async()
def accept_training(date, training_id, user_id):
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    training = mdl.Training.objects.filter(id=training_id).first()
    training_time = training.time
    date_time = datetime.combine(date, training_time)
    journal_entry = mdl.Journal.objects.filter(training=training, user=user, date_time=date_time).first()
    
    journal_entry.previuos_answer = journal_entry.accept
    journal_entry.accept = True
    journal_entry.second_not = True
    journal_entry.answer_time = datetime.now()
    journal_entry.save()

    date_time = date_time.strftime("%d.%m.%Y %H:%M")
    training_data = {
        'date_time': date_time,
        'place': journal_entry.training.place,
        'address': journal_entry.training.address,
        'route': journal_entry.training.route
    }
    return training_data

@sync_to_async()
def declain_training(date, training_id, user_id):
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    training = mdl.Training.objects.filter(id=training_id).first()
    training_time = training.time
    date_time = datetime.combine(date, training_time)
    journal_entry = mdl.Journal.objects.filter(training=training, user=user, date_time=date_time).first()
    journal_entry.previuos_answer = journal_entry.accept
    journal_entry.accept = False
    journal_entry.second_not = True
    journal_entry.answer_time = datetime.now()
    journal_entry.save()

@sync_to_async()
def get_users_for_first_not(training):
    now = datetime.now()
    current_time = datetime.strptime(now.strftime("%H:%M:%S"), '%H:%M:%S').time()
    day = training.get('day')
    training_time = training.get('time')
    place = training.get('place')
    training = mdl.Training.objects.filter(place=place, day=day, time=training_time, was_end=False).first()
    if current_time >= training.time:
        return None
    
    users = mdl.User.objects.filter(telegram_id__isnull=False).all()
    today = now.date()
    time = training.time
    date_time = datetime.combine(today, time)
    users_data = []
    for user in users:
        user_trainings = mdl.Journal.objects.filter(user=user).order_by('date_time').all()
        truant = False
        #если клиент первый раз воспользовался ботом, то у него него не будет записей тренировок
        #в журнале, поэтому проверяем. если тренировки есть
        if user_trainings:
            # смотрим сколько пропущенных подряд было до этого из последних 6ти
            user_trainings = user_trainings.exclude(date_time__date=today)
            last_trainings = len(user_trainings)-6
            if last_trainings >= 0:
                missed_trainings = user_trainings[last_trainings:]
                missed_trainings.reverse()
                missed_counter = 0
                for missed_training in missed_trainings:
                    if not missed_training.accept:
                        missed_counter += 1
                    else:
                        break
                if missed_counter == 6:
                    #если пропущенных 6 подряд, то объявлем клиента прогульщиком
                    truant = True
            #далее смотрим есть ли у него запись на сегодняшнюю тренировку
            #если он останавливал бота и снова его запустил, то записи может и не быть
            journal_entry = mdl.Journal.objects.filter(training=training, user=user, date_time=date_time).first()
            if not journal_entry:
                #и добавляем пользователя в список для оповещения
                users_data.append({
                    'id': user.telegram_id,
                    'name': user.name,
                    'truant': truant,
                    'first_not': True
                })
        else:
            #если пользователь ни разу не был на тренировках и сегодня
            #добавился в бота оповестить его
            users_data.append({
                'id': user.telegram_id,
                'name': user.name,
                'truant': truant,
                'first_not': True
            })
    #если оповещать некого
    if len(users_data) == 0:
        return None
    training_data = {
        'id': training.id,
        'day': day,
        'date': today,
        'time': training.time,
        'place': training.place,
        'address': training.address,
        'route': training.route,
        'comment_1': training.comment_1,
        'comment_2': training.comment_2,
    }
    return {
        'users_data': users_data,
        'training_data': training_data
    }

@sync_to_async()
def get_users_for_second_not(day, place, time):
    now = datetime.now()
    today = now.date()
    training = mdl.Training.objects.filter(day=day, time=time, place=place, was_end=False).first()
    time = training.time
    date_time = datetime.combine(today, time)
    entries = mdl.Journal.objects.filter(training=training, date_time=date_time, accept=None, second_not=False).all()
    
    users_data = []
    users = mdl.User.objects.filter(telegram_id__isnull=False).all()
    for user in users:
        entry = mdl.Journal.objects.filter(training=training, date_time=date_time, user=user).first()
        if not entry:
            users_data.append({
                'id': user.telegram_id,
                'name': user.name,
                'first_not': True,
                'newbie': True
            })
    if not entries and not users_data:
        return None
    for entry in entries:
        users_data.append({
                'id': entry.user.telegram_id,
                'name': entry.user.name,
                'first_not': False
            })
    training_data = {
        'id': training.id,
        'day': day,
        'date': today,
        'time': training.time,
        'place': training.place,
        'address': training.address,
        'route': training.route,
    }
    return {
        'users_data': users_data,
        'training_data': training_data
    }

@sync_to_async()
def get_training_info(id=None):
    # # для тестов
    # test_date_time = "2023-11-17 08:00:00"
    # now = datetime.strptime(test_date_time, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    today = now.date()
    week_day = now.strftime("%A").lower()
    if id:
        trainings = mdl.Training.objects.filter(id=id).all()
    else:
        trainings = mdl.Training.objects.filter(day=week_day, was_end=False).all()
    if not trainings:
        return 'not today'
    current_time = datetime.strptime(now.strftime("%H:%M:%S"), '%H:%M:%S').time()
    current_hours = int(current_time.hour)
    trainings_data = []
    for training in trainings:
        training_time = training.time
        training_hours = int(training_time.hour)
        if training_hours <= current_hours:
            return None
        trainings_data.append({
            'id': training.id,
            'date': today,
            'day': training.day,
            'time': training.time,
            'place': training.place,
            'address': training.address,
            'comment_1': training.comment_1,
            'comment_2': training.comment_2,
        })
    return trainings_data


@sync_to_async()
def make_entry(user_telegram_id, training_data, newbie=False):
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    training_day = training_data.get('day')
    training_date = training_data.get('date')
    training_time = training_data.get('time')
    training_place = training_data.get('place')
    training = mdl.Training.objects.filter(place=training_place, day=training_day, time=training_time).first()
    date_time = datetime.combine(training_date, training_time)
    entry = mdl.Journal.objects.filter(training=training, user=user, date_time=date_time).first()
    if not entry:
        if newbie:
            second_not = True
        else:
            second_not = False
        new_entry = mdl.Journal.objects.create(
            training=training,
            user=user,
            date_time = date_time,
            second_not=second_not
        )
        new_entry.save()
    else:
        entry.second_not = True
        entry.save()

@sync_to_async()
def get_users_for_not_rate(training):
    day = training.get('day')
    time = training.get('time')
    date = training.get('date')
    place = training.get('place')
    #по дню определяем тренировку
    training = mdl.Training.objects.filter(place=place, day=day, time=time, was_end=False).first()
    date_time = datetime.combine(date, time)
    #ищем эту тренировку среди всех записей в журнале
    journal_entries = mdl.Journal.objects.filter(training=training, date_time=date_time).all()
    if not journal_entries: return None
    #берём последнюю запись с этой тренировкой
    last_journal_entry = journal_entries[len(journal_entries) - 1]
    #находим все записи с такой же датой и этой же тренировкой
    journal_entries = journal_entries.filter(date_time=last_journal_entry.date_time).all()
    users_data = []
    journal_entries_ids = []
    if journal_entries:
        for journal_entry in journal_entries:
            if journal_entry.rate is None and journal_entry.accept:
                users_data.append({
                    'id': journal_entry.user.telegram_id,
                    'name': journal_entry.user.name,
                    'training_time': journal_entry.training.time,
                    'training_place': journal_entry.training.place,
                    'training_address': journal_entry.training.address,
                })
                journal_entry.user.newbie = False
                journal_entry.user.save()
                journal_entry.save()
                journal_entries_ids.append(journal_entry.id)
        rate_entry = mdl.Rate.objects.filter(place=place, address=training.address,
                                            date_time=journal_entries[0].date_time).first()
        if not rate_entry:
            new_rate = mdl.Rate.objects.create(
                date_time = journal_entries[0].date_time,
                place = training.place,
                address = training.address,
            )
            new_rate.save()
        if not training.repeat:
            training.was_end = True
            training.save()
        if len(users_data) == 0:
            return None
        return {
            'training_ids': journal_entries_ids,
            'users_data': users_data
        }
    return None

@sync_to_async()
def add_0_to_entry(training_id):
    journal_entry = mdl.Journal.objects.filter(id=training_id).first()
    journal_entry.rate = 0
    journal_entry.save()

@sync_to_async()
def set_rate(rate, training_id):
    journal_entry = mdl.Journal.objects.filter(id=training_id).first()
    journal_entry.rate = rate
    journal_entry.save()
    date_time = journal_entry.date_time
    place = journal_entry.training.place
    address = journal_entry.training.address
    rate_entry = mdl.Rate.objects.filter(place=place, address=address, date_time=date_time).first()
    journal_entries_yesterday = mdl.Journal.objects.filter(training=journal_entry.training, 
                                                        date_time=date_time).all()
    rates = []
    for entry in journal_entries_yesterday:
        if entry.rate != 0 and entry.rate != None:
            rates.append(entry.rate)
    average_score = round(sum(rates) / float(len(rates)), 1)
    rate_entry.rate = average_score
    rate_entry.save()


@sync_to_async()
def get_accept_users(training_id):
    now = datetime.now().date()
    then = now + timedelta(days = 1)
    today = now.strftime("%Y-%m-%d")
    training = mdl.Training.objects.filter(id=training_id).first()
    time = training.time
    date_time = datetime.combine(now, time)
    journal_entries = mdl.Journal.objects.filter(training=training, date_time=date_time).order_by('answer_time').all()
    if not journal_entries:
        return None
    
    users_data = []
    for journal_entry in journal_entries:
        if journal_entry.accept or (journal_entry.accept == False and journal_entry.previuos_answer):
            birthday = ''
            if journal_entry.user.birthday.strftime("%d.%m") == now.strftime("%d.%m"):
                birthday = '(Сегодня день рождения🥳)'
            if journal_entry.user.birthday.strftime("%d.%m") == then.strftime("%d.%m"):
                birthday = '(Завтра день рождения🥳)'
            newbie = ''
            if journal_entry.user.newbie:
                newbie = '(Новичок)'
            changed = False
            if journal_entry.accept == False and journal_entry.previuos_answer:
                changed = True
            users_data.append({
                'name': journal_entry.user.name,
                'birthday': birthday,
                'newbie': newbie,
                'changed': changed
            })
            training_data = {
                'place': training.place,
                'address': training.address,
                'time': training.time,
            }
    if not users_data or not training_data:
        return None
    return {'users_data':users_data, 'training_data':training_data}

@sync_to_async()
def get_rated_trainings(training_date=None):
    if not training_date:
        now = datetime.now().date()
        training_date = now - timedelta(days = 1)
    journal_entries = mdl.Journal.objects.filter(date_time__date=training_date).exclude(rate=None).exclude(rate=0).all()
    if not journal_entries:
        return None
    trainings_ids = []
    trainings_data = []
    for entry in journal_entries:
        if entry.training.id not in trainings_ids:
            trainings_ids.append(entry.training.id)
            trainings_data.append({
                'id': entry.training.id,
                'time': entry.training.time,
                'place': entry.training.place,
                'address': entry.training.address,
                'date': training_date
            })

    return trainings_data

@sync_to_async()
def get_training_rates(training_data):
    training_date = training_data.get('date')
    training_time = training_data.get('time')
    date_time = datetime.combine(training_date, training_time)
    training = mdl.Training.objects.filter(id=training_data.get('id')).first()
    journal_entries = mdl.Journal.objects.filter(training=training, date_time=date_time).exclude(rate=None).exclude(rate=0).all()
    if not journal_entries:
        return None
    rate = mdl.Rate.objects.filter(place=training.place, address=training.address,  
                                date_time=date_time).first()
    users = []
    for entry in journal_entries:
        users.append({
            'name': entry.user.name,
            'rate': entry.rate,
        })
    return {
        'users': users,
        'average_score': rate.rate
    }


@sync_to_async()
def get_shedule():
    trainings = mdl.Training.objects.filter(was_end=False).all()
    trainings_data = []
    for training in trainings:
        for day in DAYS:
            if training.day == day[0]:
                week_day = day[1]
        trainings_data.append({
            'day': week_day,
            'time': training.time.strftime("%H:%M"),
            'place': training.place,
            'address': training.address
        })
    return trainings_data

@sync_to_async()
def save_new_messages(user_id, outgoing, incoming):
    user = mdl.Message.objects.create(
        user_id=user_id,
        outgoing_msg_id=outgoing,
        incoming_msg_id=incoming
    )
    user.save()


@sync_to_async()
def get_msg_id_for_reply(reply_msg_id):
    msg = mdl.Message.objects.filter(incoming_msg_id=reply_msg_id).first()
    if msg:
        return {
            'msg_id': msg.outgoing_msg_id,
            'user_id': msg.user_id
        }
    msg = mdl.Message.objects.filter(outgoing_msg_id=reply_msg_id).first()
    if msg:
        return {
            'msg_id': msg.incoming_msg_id,
            'user_id': msg.user_id
        }
        
    return None

@sync_to_async()
def get_games():
    now = datetime.now()
    dif = timedelta(seconds=24 * 60 * 60)
    games = mdl.Game.objects.all()
    if not games:
        return None
    games_data = []
    for game in games:
        if game.date_time - now <= dif and game.date_time > now:
            games_data.append(game)
    if len(games_data) == 0:
        return None
    return games_data

@sync_to_async()
def get_users_game_notfn(date_time):
    game = mdl.Game.objects.filter(date_time=date_time).first()
    users_data = []
    for user in game.team.users.all():
        journal_entry = mdl.GameJournal.objects.filter(date_time=date_time, user=user).first()
        if not journal_entry:
            telegram_id = user.telegram_id
            name = user.name
            users_data.append({
                'id': telegram_id,
                'name': name
            })
    if len(users_data) == 0:
        return None
    return users_data

@sync_to_async()
def make_game_entry(date_time, user_id):
    game = mdl.Game.objects.filter(date_time=date_time).first()
    user = mdl.User.objects.filter(telegram_id=user_id).first()
    journal_entry = mdl.GameJournal.objects.filter(date_time=date_time, user=user).first()
    if not journal_entry:
        new_entry = mdl.GameJournal.objects.create(
                game = game,
                user = user,
                date_time = date_time
            )
        new_entry.save()


@sync_to_async()
def get_game_data_for_accept(game_id, user_telegram_id):
    game = mdl.Game.objects.filter(id=game_id).first()
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    journal_entry = mdl.GameJournal.objects.filter(game=game, user=user, date_time=game.date_time).first()
    return {
        'datetime': journal_entry.date_time,
        'place': game.place,
        'address': game.address,
        'route': game.route,
    }

@sync_to_async()
def accept_game(game_id, user_telegram_id):
    game = mdl.Game.objects.filter(id=game_id).first()
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    journal_entry = mdl.GameJournal.objects.filter(game=game, user=user, date_time=game.date_time).first()
    if not journal_entry:
        return None
    journal_entry.answer_time = datetime.now()
    journal_entry.previuos_answer = journal_entry.accept
    journal_entry.accept = True
    journal_entry.save()
    return True

@sync_to_async()
def declain_game(game_id, user_telegram_id):
    game = mdl.Game.objects.filter(id=game_id).first()
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    journal_entry = mdl.GameJournal.objects.filter(game=game, user=user, date_time=game.date_time).first()
    if not journal_entry:
        return None
    journal_entry.answer_time = datetime.now()
    journal_entry.previuos_answer = journal_entry.accept
    journal_entry.accept = False
    journal_entry.save()
    return True


@sync_to_async()
def check_games(user_telegram_id):
    now = datetime.now()
    dif = timedelta(seconds=24 * 60 * 60)
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    teams = mdl.Team.objects.filter(users=user).all()
    games = mdl.Game.objects.filter(team__in=teams).all()
    if not games:
        return None
    games_data = []
    for game in games:
        if game.date_time - now <= dif and game.date_time > now:
            journal_entry = mdl.GameJournal.objects.filter(user=user,date_time=game.date_time).first()
            if journal_entry:
                games_data.append(game)
    if len(games_data) == 0:
        return None
    return games_data

@sync_to_async()
def get_game_data(game_id, user_telegram_id):
    now = datetime.now()
    dif = timedelta(seconds=24 * 60 * 60)
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    game = mdl.Game.objects.filter(id=game_id).first()
    if game.date_time - now <= dif and game.date_time > now:
        user = {
            'id': user.telegram_id,
            'name': user.name
        }
        return {
            'game': game,
            'user': user
        }


@sync_to_async()
def check_games_admin():
    now = datetime.now()
    dif = timedelta(seconds=24 * 60 * 60)
    dif2 = timedelta(seconds=2 * 60 * 60)
    games = mdl.Game.objects.all()
    if not games:
        return None
    games_data = []
    for game in games:
        game_date = game.date_time.date()
        current_date = now.date()
        time_difference = game.date_time - now
        if (time_difference <= dif and time_difference.total_seconds() >= 0) or game_date == current_date:
            games_data.append({
                'id': game.id,
                'place': game.place,
                'team': game.team.name,
                'date_time': game.date_time
            })
    if len(games_data) == 0:
        return None
    
    return games_data

@sync_to_async()
def get_game_users_admin(game_id, date_time):
    game = mdl.Game.objects.filter(id=game_id).first()
    journal_entries = mdl.GameJournal.objects.filter(game=game, date_time=date_time).all()
    users_data = []
    for entry in journal_entries:
        if not entry.accept and entry.previuos_answer:
            changed = True
        else:
            changed = False
        if entry.accept or (not entry.accept and entry.previuos_answer):
            users_data.append({
                'id': entry.user.telegram_id,
                'name': entry.user.name,
                'newbie': entry.user.newbie,
                'birthday': entry.user.birthday,
                'changed': changed,
                'team': game.team.name,
                'game': game,
                'answer_time': entry.answer_time
            })
    if len(users_data) == 0:
        return None
    sorted_users_data = sorted(users_data, key=lambda x: x['answer_time'])
    return sorted_users_data


#получение абонементов
@sync_to_async()
def get_abonements():
    abonements = mdl.Abonements.objects.all()
    return [abonement for abonement in abonements]


@sync_to_async()
def get_abonement(id):
    abonement = mdl.Abonements.objects.filter(id=id).first()
    return abonement


@sync_to_async()
def set_abonement_entry(user_telegram_id, abonement_id):
    user = mdl.User.objects.filter(telegram_id=user_telegram_id).first()
    abonement = mdl.Abonements.objects.filter(id=abonement_id).first()
    mdl.AbonementJournal.objects.create(user=user, abonement=abonement)


@sync_to_async()
def get_subscriptions():
    subscriptions = mdl.AbonementJournal.objects.filter(abonement__is_subscribe=True, end=False).all()
    now = datetime.now()
    # fake_now = datetime(2024, 5, 23)
    ntf_users = []
    for subscription in subscriptions:
        abonement_time = subscription.abonement.time
        was_buy_time = subscription.date_time.month
        if abonement_time is not None:
            months_difference = now.month - abonement_time
            if months_difference == was_buy_time:
                ntf_users.append({
                    'tg_id': subscription.user.telegram_id,
                    'abonement': subscription.abonement.name
                })
                subscription.end = True
                subscription.save()
    return ntf_users
