import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = '7827909435:AAF9sHyBdgON8NOMH1gWCw8YjHnJyYxCBVI'
bot = telebot.TeleBot(TOKEN)

user_data = {}

questions = [
    {
        "question": "Какой праздник отмечается 1 января?",
        "options": ["Рождество", "День народного единства", "Новый Год"],
        "answer": "Новый Год"
    },
    {
        "question": "Какой символ 2024?",
        "options": ["Кот", "Змея", "Кролик"],
        "answer": "Змея"
    },
    {
        "question": "Какой цвет больше ассоциируется к Новому Году ?",
        "options": ["Синий", "Красный", "Зелёный"],
        "answer": "Красный"
    },
    {
        "question": "Какой фрукт больше ассоциируется к Новому Году ?",
        "options": ["Мандарин", "Яблоко", "Банан"],
        "answer": "Мандарин"
    },
    {
        "question": "Кто поздравляет всех граждан России с Новым Годом?",
        "options": ["Мэр", "Президент", "Депутат"],
        "answer": "Президент"
    },
    {
        "question": "Как называют снежного человека, которого лепят зимой?",
        "options": ["Снеговик", "Снегожук", "Снегокот"],
        "answer": "Снеговик"
    },
    {
        "question": "Что часто вешают на новогоднюю елку?",
        "options": ["Кастрюли", "Чашки", "Игрушки"],
        "answer": "Игрушки"
    },
    {
        "question": "Что традиционно ставят под ёлку?",
        "options": ["Сковородки", "Подарки", "Свечи"],
        "answer": "Подарки"
    },
    {
        "question": "Какой персонаж приносит подарки детям в России?",
        "options": ["Санта-Клаус", "Дед Мороз", "Эльфы"],
        "answer": "Дед Мороз"
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