from aiogram import types
from aiogram.enums.content_type import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from handlers.buttons import ReplyKeyboard as keyboard
from loader import dp
from service.amplitude import send_event
from service.assistant.assistant import Assistant
from service.chat.factory import ChatFactory
from service.fsm import TypeChatAnswersState, ChatState
from service.vision import Vision


async def get_or_create_thread_from_state(state: FSMContext):
    state_data = await state.get_data()
    if 'thread_id' not in state_data:
        thread = await Assistant().create_thread()
        thread_id = thread.id
        await state.update_data({'thread_id': f'{thread_id}'})
    else:
        thread_id = (await state.get_data()).get('thread_id')
    return thread_id


@dp.message(CommandStart())
async def choosing_type_answers_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TypeChatAnswersState.choosing_chat_type_answers)

    information = (f"hello {message.from_user.username}.\n"
                   f"Please select a method to receive your message.")

    await message.answer(information, reply_markup=keyboard.text_or_voice_answer)
    send_event('bot_started', message.from_user)


@dp.message(TypeChatAnswersState.choosing_chat_type_answers)
async def choosing_type_answer_handler(message: Message, state: FSMContext) -> None:
    if message.text in ["💬🤖🎙️ Voice answers", "💬🤖💬 Text answers"]:
        await state.set_state(TypeChatAnswersState.selected_type_chat_answers)

        if message.text == "💬🤖🎙️ Voice answers":
            await state.update_data({'type_answer': 'voice'})

        elif message.text == "💬🤖💬 Text answers":
            await state.update_data({'type_answer': 'text'})

        await message.answer("Please select chat.", reply_markup=keyboard.choosing_chat)
    else:
        await message.answer("Sorry, I can't understand your request.")


@dp.message(TypeChatAnswersState.selected_type_chat_answers)
async def choosing_chat_handler(message: Message, state: FSMContext) -> None:
    if message.text == '😟 chat about anxiety 🤖':
        await state.set_state(ChatState.chat_anxiety)
        await message.answer("I will help you chat about anxiety, send me a message please", reply_markup=keyboard.back)

    elif message.text == '📷 chat to determine mood from photo 🤖':
        await state.set_state(ChatState.chat_photo)
        await message.answer("Now I can determine mood from photo, send me photo please", reply_markup=keyboard.back)

    elif message.text == 'Back':
        await state.set_state(TypeChatAnswersState.choosing_chat_type_answers)
        await message.answer("Please select a method to receive your message.",
                             reply_markup=keyboard.text_or_voice_answer)
    else:
        await message.answer("Sorry, I can't understand your request.")


@dp.message(ChatState.chat_anxiety)
async def chat_anxiety_handler(message: Message, state: FSMContext) -> None:
    if message.text == 'Back':
        await state.set_state(TypeChatAnswersState.selected_type_chat_answers)
        await message.answer("Please select chat.", reply_markup=keyboard.choosing_chat)
        return

    if message.content_type in (ContentType.TEXT, ContentType.VOICE):
        thread_id = await get_or_create_thread_from_state(state)
        type_answer = (await state.get_data()).get('type_answer')
        chat = ChatFactory.create_chat(type_answer, thread_id)
        await chat.send_message(message=message)
        answer = await chat.get_answer()

        if type_answer == 'text':
            await message.reply(answer, reply_markup=keyboard.back)
            send_event('text_message_processed', message.from_user)

        elif type_answer == 'voice':
            await message.reply_voice(answer, reply_markup=keyboard.back)
            send_event('voice_message_processed', message.from_user)
    else:
        await message.answer("Sorry, here I can process only text and voice messages.")


@dp.message(ChatState.chat_photo)
async def analise_mood_on_photo_handler(message: types.Message, state: FSMContext) -> None:
    if message.text == "Back":
        await state.set_state(TypeChatAnswersState.selected_type_chat_answers)
        await message.answer("Please select chat.", reply_markup=keyboard.choosing_chat)
        return

    if message.content_type == ContentType.PHOTO:
        await message.answer('Please wait, your message is being processed...')

        vision = Vision(message.photo)
        answer = await vision.analise_emotions()
        type_answer = (await state.get_data()).get('type_answer')

        if type_answer == 'text':
            await message.reply(answer, reply_markup=keyboard.back)

        elif type_answer == 'voice':
            voice_answer = await vision.get_voice_answer()
            await message.reply_voice(voice_answer, reply_markup=keyboard.back)
        send_event('photo_analyzed', message.from_user)
    else:
        await message.answer("Sorry, here I can process only photo messages.")


@dp.message()
async def other_message_handler(message: types.Message, state: FSMContext) -> None:
    await state.set_state(TypeChatAnswersState.choosing_chat_type_answers)
    await message.answer("Unknown message", reply_markup=keyboard.text_or_voice_answer)
    send_event('unsupported_message_received', message.from_user)
