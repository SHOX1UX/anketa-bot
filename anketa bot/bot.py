import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher,types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart,Command
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext #new
from states import Form #new
import re



TOKEN = "7101313879:AAHILgTj6_YwBrJSkrcZdZe_ItiLdEr-E0s" #Token kiriting
ADMIN =6450477410
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext):
    
    await state.set_state(Form.first_name)
    await message.answer(text="Assalomu alaykum, Ro'yhatdan o'tish uchun ismingizni kiriting")

@dp.message(F.text,Form.first_name)
async def first_name_register(message:Message,state:FSMContext):
    ism = message.text
    await state.update_data(first_name=ism)
    await state.set_state(Form.last_name)

    await message.answer(text="Familyangizni kiriting")

@dp.message(F.text,Form.last_name)
async def last_name_register(message:Message,state:FSMContext):
    familya = message.text
    await state.update_data(last_name = familya)
    await state.set_state(Form.phone_number)

    await message.answer(text="Tel nomeringizni kiriting")

@dp.message(F.text,Form.phone_number)
async def phone_number_register(message:Message,state:FSMContext):
    tel = message.text
    pattern = re.compile("^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$")
    if pattern.match(tel):
        await state.update_data(phone_number = tel)
        await state.set_state(Form.address)
        await message.answer(text="Manzilingizni kiriting")
    else:
        await message.answer(text="tel raqamni noto'g'ri kiritdingiz qayta qkiriting")
    
         



@dp.message(F.text,Form.address)
async def address_register(message:Message,state:FSMContext):
    manzil = message.text
    await state.update_data(address = manzil)
    await state.set_state(Form.t_yil)

    await message.answer(text="yilingizni kiriting")

@dp.message(F.text,Form.t_yil)
async def t_yil_register(message:Message,state:FSMContext):
    yil = message.text
    await state.update_data(t_yil = yil)
    await state.set_state(Form.father)

    await message.answer(text="Otangizni ismini kiriting")

@dp.message(F.text,Form.father)
async def father_register(message:Message,state:FSMContext):
    fat = message.text
    await state.update_data(father = fat)
    await state.set_state(Form.mother)

    await message.answer(text="onanggizni ismini kriting")

@dp.message(F.text,Form.mother)
async def mother_register(message:Message,state:FSMContext):
    mot = message.text
    await state.update_data(phone_number = mot)
    await state.set_state(Form.mfy)

    await message.answer(text="Mahallangizni kiriting")

@dp.message(F.text,Form.mfy)
async def mfy_register(message:Message,state:FSMContext):
    mf = message.text
    await state.update_data(phone_number = mf)
    data = await state.get_data()
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    phone_number = data.get("phone_number")
    address = data.get("address")
    t_yil = data.get("t_yil")
    father = data.get("father")
    mother = data.get("mother")

    await state.clear()

    text = f"Yangi foydalanuvchi ro'yhatdan o'tdi\n\nIsmi:{first_name}\nFamilyasi:{last_name}\nTel:{phone_number}\nManzil:{address}\nTug'ulgan yili:{t_yil}\nOtasini ismi:{father}\nOnasini ismi:{mother}"

    await message.answer(text="Siz muvafaqiyatli ro'yhatdan o'tdingiz")
    await bot.send_message(chat_id=ADMIN,text=text)




    await message.answer(text="Manzilingizni kiriting")




async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())