import telebot
from database.dbapi import DatabaseConnector
API_TOKEN = '5113081373:AAEexaQG5Dk9bJn_STzqym9gbdE5qtQ8Fk0'

bot = telebot.TeleBot(API_TOKEN, parse_mode=None)
db = DatabaseConnector(username='rhaenysg', database='rhaenysg') # blairlyt




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.send_message(message.chat.id,'''Привет я бот - библиотекарь. Я обладаю следующим функционалом:\n 
	Добавление книги в общую библиотеку /add\n
	Взятие книги из библиотеки для чтения /borrow\n 
	Возвращение книги в библиотеку после чтения /retrieve\n  
	Удаление книги из библиотеки /delete\n  
	Вывод списка книг /list \n  
	Поиск книги в библиотеке /find\n  
	Формирование файла со статистикой использования книги и отправление ссылки на скачивание этого файла /stats ''')




@bot.message_handler(commands=['add'])
def add(message):
	bot.send_message(message.chat.id,'Введите название книги')
	bot.register_next_step_handler(message, add__get_name)


def add__get_name(message):
	global bookName
	bookName = message.text
	bot.send_message(message.chat.id,'Введите автора книги')
	bot.register_next_step_handler(message, add__get_author)


def add__get_author(message):
	global authorName
	authorName = message.text
	bot.send_message(message.chat.id,'Введите год издания')
	bot.register_next_step_handler(message, add__year_check)


def add__year_check(message):
	global presYear
	presYear = message.text
	try:
		__bookId = db.add(str(bookName), str(authorName), str(presYear))
		bot.send_message(message.chat.id, f'Книга добавлена id: {__bookId}')
	except Exception as e:
		bot.send_message(message.chat.id, f'Ошибка при добавлении книги')
		print(str(e))




@bot.message_handler(commands=['delete'])
def delete(message):
	bot.send_message(message.chat.id,'Введите название книги')
	bot.register_next_step_handler(message, delete__get_name)


def delete__get_name(message):
	global bookName
	bookName = message.text
	bot.send_message(message.chat.id,'Введите автора книги')
	bot.register_next_step_handler(message, delete__get_author)


def delete__get_author(message):
	global authorName
	authorName = message.text
	bot.send_message(message.chat.id,'Введите год издания')
	bot.register_next_step_handler(message, delete__year_check)


def delete__year_check(message):
	global presYear
	presYear = message.text
	__book = db.delete(str(bookName), str(authorName), str(presYear))
	if __book:
		bot.send_message(message.chat.id, f'Книга удалена')
	else:
		bot.send_message(message.chat.id, f'Невозможно удалить книгу')




@bot.message_handler(commands=['list'])
def list_books(message):
	__list = db.list_books()
	__str = ''
	for el in __list:
		__str += el[0] + ', ' + el[1] + ', ' + el[2] + '\n'
	bot.send_message(message.chat.id, __str)




@bot.message_handler(commands=['find'])
def find(message):
	bot.send_message(message.chat.id, 'Введите название книги')
	bot.register_next_step_handler(message, find__get_name)


def find__get_name(message):
	global bookName
	bookName = message.text
	bot.send_message(message.chat.id, 'Введите автора книги')
	bot.register_next_step_handler(message, find__get_author)


def find__get_author(message):
	global authorName
	authorName = message.text
	bot.send_message(message.chat.id, 'Введите год издания')
	bot.register_next_step_handler(message, find__year_check)


def find__year_check(message):
	global presYear
	presYear = message.text
	__book = db.get_book(str(bookName), str(authorName), str(presYear))
	if __book:
		bot.send_message(message.chat.id, f'Найдена книга: {__book.author}, {__book.title}, {__book.published}.')
	else:
		bot.send_message(message.chat.id, f'Такой книги у нас нет')




@bot.message_handler(commands=['borrow'])
def borrow(message):
	if db.get_borrow(message.from_user.id) != None:
		bot.send_message(message.chat.id, 'Книгу сейчас невозможно взять')
	else:
		bot.send_message(message.chat.id, 'Введите название книги')
		bot.register_next_step_handler(message, borrow__get_name)


def borrow__get_name(message):
	global bookName
	bookName = message.text
	bot.send_message(message.chat.id, 'Введите автора книги')
	bot.register_next_step_handler(message, borrow__get_author)


def borrow__get_author(message):
	global authorName
	authorName = message.text
	bot.send_message(message.chat.id, 'Введите год издания')
	bot.register_next_step_handler(message, borrow__year_check)


def borrow__year_check(message):
	global presYear
	global book_to_borrow_id # глобально отдельный Id держать или целый бук?
	presYear = message.text

	book = db.get_book(str(bookName), str(authorName), str(presYear))
	print(book)
	if book:
		bot.send_message(message.chat.id, f'Найдена книга: {book.author}, {book.title}, {book.published}. Берём?')
		book_to_borrow_id = book.book_id
		bot.register_next_step_handler(message, borrow__agreement)
	else:
		bot.send_message(message.chat.id, f'Такой книги у нас нет')


def borrow__agreement(message):
	if message.text == 'Да':
		db.borrow(book_to_borrow_id, message.from_user.id)
		bot.send_message(message.chat.id, 'Вы взяли книгу')
	else:
		bot.send_message(message.chat.id, f'Книгу сейчас невозможно взять')




@bot.message_handler(commands=['retrieve'])
def retrieve_borrowed_book(message):
	borrowId = db.get_borrow(message.from_user.id)
	if (borrowId):
		retr = db.retrieve(borrowId)
		bot.send_message(message.chat.id, f'Вы вернули книгу {retr.title}, {retr.author}, {retr.published}')
	else:
		bot.send_message(message.chat.id, f'Возвращать нечего')




@bot.message_handler(commands=['stats'])
def stats(message):
	bot.send_message(message.chat.id, 'Введите название книги')
	bot.register_next_step_handler(message, stats__get_name)


def stats__get_name(message):
	global bookName
	bookName = message.text
	bot.send_message(message.chat.id,'Введите автора книги')
	bot.register_next_step_handler(message, stats__get_author)


def stats__get_author(message):
	global authorName
	authorName = message.text
	bot.send_message(message.chat.id,'Введите год издания')
	bot.register_next_step_handler(message, stats__year_check)


def stats__year_check(message):
	global presYear
	presYear = message.text

	gottenbook = db.get_book(str(bookName), str(authorName), str(presYear))

	if gottenbook != None:
		STATISTICS_URL = f'https://localhost/download/{gottenbook.book_id}'
		bot.send_message(message.chat.id, f'Статистика доступна по адресу {STATISTICS_URL}')
	else:
		bot.send_message(message.chat.id, f'Нет такой книги')




@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.send_message(message.chat.id, message.text)




bot.polling(none_stop=True, interval=0)