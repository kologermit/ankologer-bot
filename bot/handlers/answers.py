class Answers:
    start = """{name}, Приветствую тебя! 👋
Меня зовут Кологерманская Анна Николаевна, я учитель информатики и профориентолог🖥 
Познакомимся ближе?🔍"""
    yes = "Да✅"
    no = "Нет❌"
    correct = "Верно✅"
    invalid = "Неверно❌"
    back = "Назад🔙"
    about_button = "Подробнее"

    class Menu:
        presentation = """<b>Кологерманская Анна Николаевна</b>, я учитель информатики и профориентолог🖥
<b>ИНН:</b> 183472740304
"""
        presentation_link = "https://docs.google.com/presentation/d/1Rc0HJfp0oorGC2UTfd1nGtwQmXPdcg03PTGB19u1Zys/edit#slide=id.g28103dc4af2_3_12"
        menu = "Я рада, что мы уже знакомы, тогда смотри, что у меня есть для тебя"
        registration_button = "Регистрация📋"
        me_button = "Информация обо мне📋"
        products_list_button = "Список курсов📋"
        products = "Вот мои товары:"

    class Registration:
        send_name = "Отправьте ваше <b>имя</b>"
        name = "Сохранено имя <b>{name}</b>\nТеперь введите почту"
        name_error = "Ошибка в имени❌"
        name_resend = "Отправьте исправленное имя"
        invalid_email = "Введена неправильная почта <b>{email}</b>❌"
        email = "Сохранена почта <b>{email}</b>\nТеперь отправьте номер телефона (+79999999999)"
        email_error = "Ошибка в почте❌"
        email_resend = "Отправьте исправленную почту"
        invalid_phone = "Введён неправильный номер телефона <b>{phone}</b>❌"
        phone = """Подтвердите введённые данные:
<b>Имя:</b> {name}
<b>Почта:</b> {email}
<b>Номер телефона:</b> {phone}"""
        phone_error = "Ошибка в номере телефона❌"
        phone_resend = "Отправьте исправленный номер телефона"
        correct = "Спасибо за регистрацию!✅"
        invalid = "Регистрация отменена!❌"

    class Products:
        product = "<b>Название:</b> {name}\n<b>Цена:</b> {price}р"
        no_verified = "Вы не зарегистрированы, поэтому не можете купить продукцию"
        menu = "Выберите товар из списка"
        full = "<b>Название:</b> {name}\n\n<b>Описание:</b> {description}\n\n<b>Цена</b> {price}"

    class Admin:
        menu = "Меню:"
        load_products = "Отправьте файл с расширением .xlsx"