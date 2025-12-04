import textwrap

import httpx
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup
from pyromod.exceptions.listener_timeout import ListenerTimeout

from sabores_da_terra.settings import Settings

bot = Client("Sabores_da_terra_bot",
             Settings().TELEGRAM_API_ID,
             Settings().TELEGRAM_API_HASH,
             Settings().TELEGRAM_BOT_TOKEN
)


@bot.on_message(~filters.text & filters.private)
async def only_text(client, message):
    await message.reply('Sou um robô, mande apenas textos!')


@bot.on_message(filters.command('produtos'))
async def read_products(client, message):
    user_id = message.from_user.id

    while True:
        try:
            msg = '''
            Digite o nome do produto que deseja (ex: laranja)
            ou **sair** para finalizar:'''

            answer = await client.ask(
                user_id,
                textwrap.dedent(msg),
                filters=filters.text,
                timeout=30
            )

        except ListenerTimeout:
            await message.reply(
                "⏰ Tempo esgotado! Use /produtos novamente."
            )
            return

        product_name = answer.text.strip()

        if product_name.lower() == "sair":
            await message.reply(
                "Busca finalizada! Acesse (link) e faça sua compra.")
            return

        async with httpx.AsyncClient() as cl:
            response = await cl.get(
                'http://localhost:8000/api/products/filters',
                params={"name": product_name}
            )

            product = response.json()['products']

        if product:
            msg = f'''
            **{product[0]['name'].upper()}**\n
            Descrição: {product[0]['description']}
            Estoque: {product[0]['stock_quantity']}
            Preço: R$ {float(product[0]['price']):.2f}
            '''
            if product[0]['image']:

                await message.reply_photo(
                    photo=product[0]['image'],
                    caption=textwrap.dedent(msg).strip()
                )
            else:
                await message.reply(textwrap.dedent(msg))
        else:
            await message.reply("❌ Produto não encontrado.")


@bot.on_message(filters.command('site'))
async def web_site(client, message):
    await message.reply('Acesse (link) para comprar nossos produtos!')


@bot.on_message(filters.command('social'))
async def social_media(client, message):
    msg = 'WhatsApp: (99)99999-9999 \n Instagram: (link e @)'
    await message.reply(msg.strip())


@bot.on_message(filters.command('menu'))
async def menu(client, message):
    msg = '''
    Esse é o menu de navegação, digite ou aperte a opção desejada.
    Veja abaixo todos os recursos:\n
    **Produtos**
    /produtos - Para ver o **preço** e o **estoque** de um produto desejado.
    **Site**
    /site - Para ver e comprar nossos produtos.\n
    **Redes Sociais**
    /social - Para ter acesso as nossas **redes sociais** e ficar por dentro
    das novidades da nossa loja.\n
    Gostou dos nossos produtos? Acesse (link) e faça sua compra agora.
    '''

    await message.reply(
        textwrap.dedent(msg).strip(),
        reply_markup=ReplyKeyboardMarkup(
            [
                ['/produtos', '/site', '/social']
            ],
            resize_keyboard=True
        )
    )


@bot.on_message()
async def main(client, message):
    user = message.chat.username or 'Visitante'
    msg = f'''
        Bem vindo(a) {user} ao Sabores da Terra!
        Uma Loja online de produtos orgânicos produzidos na sua cidade.
        Digite /menu para navegar nas opções.'''

    await message.reply(textwrap.dedent(msg).strip())


bot.run()
