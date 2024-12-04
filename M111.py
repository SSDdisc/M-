import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = ''  
bot = telebot.TeleBot(TOKEN)

user_data = {}


questions = [
    {
        "question": "Где живет Дед Мороз?",
        "options": ["В Великом Устюге", "В Новосибирске", "В Иркутске"],
        "answer": "В Великом Устюге"
    },
    {
        "question": "Какой год считается годом основания Москвы?",
        "options": ["1147", "1212", "1492"],
        "answer": "1147"
    },
    {
        "question": "Какая планета известна как 'красная планета'?",
        "options": ["Земля", "Марс", "Венера"],
        "answer": "Марс"
    },
    {
        "question": "Какой писатель автор 'Войны и мира'?",
        "options": ["Федор Достоевский", "Лев Толстой", "Антон Чехов"],
        "answer": "Лев Толстой"
    },
    {
        "question": "Год Октяборьской революции?",
        "options": ["1916", "1827", "1917"],
        "answer": "1917"
    },
    {
        "question": "Какое наименьшее целое число?",
        "options": ["-1", "0", "1"],
        "answer": "0"
    },
    {
        "question": "Какой элемент является основным компонентом алмаза?",
        "options": ["Углерод", "Кремний", "Железо"],
        "answer": "Углерод"
    },
    {
        "question": "Какое животные изображены на гербе Новосибирска?",
        "options": ["Соболя", "Медведь", "Лев"],
        "answer": "Соболя"
    },
    {
        "question": "Какая из этих планет является самой большой в Солнечной системе?",
        "options": ["Земля", "Юпитер", "Сатурн"],
        "answer": "Юпитер"
    },
]

@bot.message_handler(commands=['start'])
def start_quiz(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'score': 0, 'current_question': 0}
    bot.send_message(chat_id, "Викторина началась! Вот первый вопрос:")
    ask_question(chat_id)

def ask_question(chat_id):
    question_index = user_data[chat_id]['current_question']
    
    if question_index < len(questions):
        question = questions[question_index]["question"]
        answers = questions[question_index]["options"]
        correct_answer = questions[question_index]["answer"]
        
        user_data[chat_id]['current_answer'] = correct_answer

        keyboard = InlineKeyboardMarkup()
        for answer in answers:
            keyboard.add(InlineKeyboardButton(text=answer, callback_data=answer))

        bot.send_message(chat_id, question, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, f"Тест завершен! Ваш итоговый счет: {user_data[chat_id]['score']}")
        del user_data[chat_id] 

@bot.callback_query_handler(func=lambda call: True)
def handle_answer(call):
    chat_id = call.message.chat.id
    if chat_id not in user_data:
        bot.send_message(chat_id, "Вы еще не начали викторину. Пожалуйста, начните с команды /start.")
        return

    correct_answer = user_data[chat_id]['current_answer']

    if call.data == correct_answer:
        user_data[chat_id]['score'] += 1
        response_message = f"Правильно! Ваши очки: {user_data[chat_id]['score']}"
    else:
        response_message = f"Неверно! Правильный ответ: {correct_answer}. Ваши очки: {user_data[chat_id]['score']}"

    bot.send_message(chat_id, response_message)
    
    user_data[chat_id]['current_question'] += 1
    ask_question(chat_id)

bot.polling()
