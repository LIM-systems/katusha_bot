from bot.loader import bot
from aiogram import types
from bot import django_crud as dj
from bot.config import ADM_ID, DEV_ID



async def sendMsg(type):
    if type == 'text':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_message(chat_id=id, text=msg.text)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_message(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                text=msg.text)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not msgs_id:
                bot_msg = await bot.send_message(chat_id=ADM_ID, text=msg.text)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_message(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                text=msg.text)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'voice':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_voice(chat_id=id, voice=msg.voice.file_id)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_voice(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                voice=msg.voice.file_id)
            elif not msgs_id:
                bot_msg = await bot.send_voice(chat_id=ADM_ID, voice=msg.voice.file_id)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_voice(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                voice=msg.voice.file_id)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'contact':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_contact(chat_id=id, first_name=msg.contact.first_name,
                                                phone_number=msg.contact.phone_number)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_contact(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                first_name=msg.contact.first_name,
                                                phone_number=msg.contact.phone_number)
            elif not msgs_id:
                bot_msg = await bot.send_contact(chat_id=ADM_ID, first_name=msg.contact.first_name,
                                                phone_number=msg.contact.phone_number)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_contact(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                first_name=msg.contact.first_name,
                                            phone_number=msg.contact.phone_number)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'location':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_location(chat_id=id, latitude=msg.location.latitude,
                                                longitude=msg.location.longitude)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_location(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                latitude=msg.location.latitude,
                                                longitude=msg.location.longitude)
            elif not msgs_id:
                bot_msg = await bot.send_location(chat_id=ADM_ID, latitude=msg.location.latitude,
                                                longitude=msg.location.longitude)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_location(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                latitude=msg.location.latitude,
                                                longitude=msg.location.longitude)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'sticker':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_sticker(chat_id=id, sticker=msg.sticker.file_id)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_sticker(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                sticker=msg.sticker.file_id)
            elif not msgs_id:
                bot_msg = await bot.send_sticker(chat_id=ADM_ID, sticker=msg.sticker.file_id)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_sticker(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                sticker=msg.sticker.file_id)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'photo':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_photo(chat_id=id, photo=msg.photo[-1].file_id, caption=msg.caption)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_photo(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                photo=msg.photo[-1].file_id, caption=msg.caption)
            elif not msgs_id:
                bot_msg = await bot.send_photo(chat_id=ADM_ID, photo=msg.photo[-1].file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_photo(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                photo=msg.photo[-1].file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'video':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_video(chat_id=id, video=msg.video.file_id, caption=msg.caption)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_video(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                video=msg.video.file_id, caption=msg.caption)
            elif not msgs_id:
                bot_msg = await bot.send_video(chat_id=ADM_ID, video=msg.video.file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_video(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                video=msg.video.file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'audio':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_audio(chat_id=id, audio=msg.audio.file_id, caption=msg.caption)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_audio(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                audio=msg.audio.file_id, caption=msg.caption)
            elif not msgs_id:
                bot_msg = await bot.send_audio(chat_id=ADM_ID, audio=msg.audio.file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_audio(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                audio=msg.audio.file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
    elif type == 'document':
        async def msg_type(msg, msgs_id=None, ADM_ID=None, id=None):
            user = await dj.check_new_user(msg.from_user.id)
            if user:
                name = user.name
            else:
                if not msg.from_user.first_name:
                    name = msg.from_user.last_name
                elif not msg.from_user.last_name:
                    name = msg.from_user.first_name
                else:
                    name = msg.from_user.first_name + " " + msg.from_user.last_name
            message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
            if not user:
                message += '\nПользователь не зарегистрирован\n'
            if id:
                bot_msg = await bot.send_document(chat_id=id, document=msg.document.file_id, caption=msg.caption)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            elif not ADM_ID:
                bot_msg = await bot.send_document(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                document=msg.document.file_id, caption=msg.caption)
            elif not msgs_id:
                bot_msg = await bot.send_document(chat_id=ADM_ID, document=msg.document.file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
            else:
                bot_msg = await bot.send_document(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                document=msg.document.file_id, caption=msg.caption)
                await bot.send_message(chat_id=ADM_ID, text=message)
                await dj.save_new_messages(msg.from_user.id, outgoing=msg.message_id, incoming=bot_msg.message_id)
                
    return msg_type
    

async def send_dialogue_message(msg):
    content_type = msg.content_type
    msg_type = await sendMsg(content_type)

    
    if msg.reply_to_message:
        reply_msg_id = msg.reply_to_message.message_id
        msgs_id = await dj.get_msg_id_for_reply(reply_msg_id)
        if not msgs_id and msg.from_user.id == ADM_ID:
            if 'Сообщение от🗣:' in msg.reply_to_message.text:
                id = msg.reply_to_message.text.split('\n')[2].split(' ')[1]
                await msg_type(msg, id=int(id))
            else:
                await msg.answer('''Сообщение на которое Вы отвечаете отсутствует у собеседника.''')
                return
        elif not msgs_id:
            await msg.answer('''Сообщение на которое Вы отвечаете отсутствует у собеседника.''')
            return
        elif msgs_id['user_id'] == ADM_ID and msgs_id['user_id'] == msg.from_user.id:
            await msg.answer('''Вы отвечаете сами себе?''')
            return
        elif msgs_id['user_id'] == msg.from_user.id:
            await msg_type(msg, msgs_id, ADM_ID)
        else:
            if msg.from_user.id == ADM_ID:
                await msg_type(msg,msgs_id)
            else:
                await msg_type(msg, msgs_id, ADM_ID)
    else:
        if msg.from_user.id == ADM_ID:
            await msg.answer("Пожалуйста, выберите сообщение, на которое хотите ответить.")
            return
        else:
            await msg_type(msg, ADM_ID=ADM_ID)
                
                

async def send_dialogue_message_with_media(msg, album):
    content_type = msg.content_type
    media_group = types.MediaGroup()
    messages_ids = []
    
    if not msg.from_user.first_name:
        name = msg.from_user.last_name
    elif not msg.from_user.last_name:
        name = msg.from_user.first_name
    else:
        name = msg.from_user.first_name + " " + msg.from_user.last_name
    message = f'👆 <b>Сообщение от🗣:</b>\n{name}\nid {msg.from_user.id}'
    
    if content_type == 'photo' or content_type == 'video':
        for key in album:
            if key.photo:
                if key.caption:
                    media_group.attach({"media": key.photo[-1].file_id, "type": 'photo', "caption" : key.caption})
                else:
                    media_group.attach({"media": key.photo[-1].file_id, "type": 'photo'})
            if key.video:
                if key.caption:
                    media_group.attach({"media": key.video.file_id, "type": 'video', "caption" : key.caption})
                else:
                    media_group.attach({"media": key.video.file_id, "type": 'video'})
            messages_ids.append(key.message_id)
        if msg.reply_to_message:
            reply_msg_id = msg.reply_to_message.message_id
            msgs_id = await dj.get_msg_id_for_reply(reply_msg_id)
            if not msgs_id and msg.from_user.id == ADM_ID:
                if 'Сообщение от🗣:' in msg.reply_to_message.text:
                    id = msg.reply_to_message.text.split('\n')[2].split(' ')[1]
                    bot_msg = await bot.send_media_group(chat_id=id, reply_to_message_id=msgs_id,
                                                media=media_group)
                    for i, key in enumerate(messages_ids):
                        await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
                        
                else:
                    await msg.answer('''Сообщение на которое Вы отвечаете отсутствует у собеседника.''')
                    return
            elif not msgs_id:
                await msg.answer('''Сообщение на которое Вы отвечаете отсутствует у собеседника.''')
                return
            elif msgs_id['user_id'] == ADM_ID and msgs_id['user_id'] == msg.from_user.id:
                await msg.answer('''Вы отвечаете сами себе?''')
                return
            elif msgs_id['user_id'] == msg.from_user.id:
                bot_msg = await bot.send_media_group(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                media=media_group)
                await bot.send_message(chat_id=ADM_ID, text=message)
                for i, key in enumerate(messages_ids):
                    await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
            else:
                if msg.from_user.id == ADM_ID:
                    bot_msg = await bot.send_media_group(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                media=media_group)
                    for i, key in enumerate(messages_ids):
                        await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
                else:
                    bot_msg = await bot.send_media_group(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                media=media_group)
                    await bot.send_message(chat_id=ADM_ID, text=message)
                    for i, key in enumerate(messages_ids):
                        await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
        else:
            if msg.from_user.id == ADM_ID:
                await msg.answer("Пожалуйста, выберите сообщение, на которое хотите ответить.")
                return
            else:
                bot_msg = await bot.send_media_group(chat_id=ADM_ID, media=media_group)
                await bot.send_message(chat_id=ADM_ID, text=message)
                for i, key in enumerate(messages_ids):
                    await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
    else:
        for key in album:
            media_group.attach({"media": key[content_type].file_id, "type": content_type})
            messages_ids.append(key.message_id)
        if msg.reply_to_message:
            reply_msg_id = msg.reply_to_message.message_id
            msgs_id = await dj.get_msg_id_for_reply(reply_msg_id)
            if not msgs_id and msg.from_user.id == ADM_ID:
                if 'Сообщение от🗣:' in msg.reply_to_message.text:
                    id = msg.reply_to_message.text.split('\n')[2].split(' ')[1]
                    bot_msg = await bot.send_media_group(chat_id=id, reply_to_message_id=msgs_id,
                                                media=media_group)
                    for i, key in enumerate(messages_ids):
                        await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
                        
                else:
                    await msg.answer('''Сообщение на которое Вы отвечаете отсутствует у собеседника.''')
                    return
            elif not msgs_id:
                await msg.answer('''Сообщение на которое Вы отвечаете отсутствует у собеседника.''')
                return
            elif msgs_id['user_id'] == ADM_ID and msgs_id['user_id'] == msg.from_user.id:
                await msg.answer('''Вы отвечаете сами себе?''')
                return
            elif msgs_id['user_id'] == msg.from_user.id:
                bot_msg = await bot.send_media_group(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                media=media_group)
                await bot.send_message(chat_id=ADM_ID, text=message)
                for i, key in enumerate(messages_ids):
                    await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
            else:
                if msg.from_user.id == ADM_ID:
                    bot_msg = await bot.send_media_group(chat_id=msgs_id['user_id'], reply_to_message_id=msgs_id['msg_id'],
                                                media=media_group)
                    for i, key in enumerate(messages_ids):
                        await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
                else:
                    bot_msg = await bot.send_media_group(chat_id=ADM_ID, reply_to_message_id=msgs_id['msg_id'],
                                                media=media_group)
                    await bot.send_message(chat_id=ADM_ID, text=message)
                    for i, key in enumerate(messages_ids):
                        await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)
        else:
            if msg.from_user.id == ADM_ID:
                await msg.answer("Пожалуйста, выберите сообщение, на которое хотите ответить.")
                return
            else:
                bot_msg = await bot.send_media_group(chat_id=ADM_ID, media=media_group)
                await bot.send_message(chat_id=ADM_ID, text=message)
                for i, key in enumerate(messages_ids):
                    await dj.save_new_messages(msg.from_user.id, outgoing=key, incoming=bot_msg[i].message_id)