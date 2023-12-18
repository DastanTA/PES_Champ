from aiogram.utils.keyboard import ReplyKeyboardBuilder


def first_reg_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="I'm in!")
    keyboard_builder.button(text="Done")
    keyboard_builder.adjust(2)
    return keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Push button!'
    )

#Пусть каждый, кто будет участвовать в чемпионатах, нажмет на кнопку "Отправить свой контакт".
# А тот кто запускал команду "/start", должен будет нажать на кнопку "Готово", когда все отправят свои контакты.
