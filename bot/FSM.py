from aiogram.fsm.state import State, StatesGroup


class MessageStates(StatesGroup):
    main_menu = State()
    post_msgs = State()
