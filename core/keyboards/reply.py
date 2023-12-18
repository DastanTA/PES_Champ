from aiogram.utils.keyboard import ReplyKeyboardBuilder


def first_reg_keyboard():
    keyboard_builder = ReplyKeyboardBuilder()

    keyboard_builder.button(text="Отправить свой контакт", request_contact=True)
    keyboard_builder.adjust(2)
    keyboard_builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False,
        selective=True,
        input_field_placeholder='Пусть каждый, кто будет участвовать в чемпионатах, '
                                'нажмет на кнопку "Отправить свой контакт". А тот кто запускал команду "/start", '
                                'должен будет нажать на кнопку "готово", когда все отправят свои контакты.'
    )
