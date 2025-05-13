import discord
import os
import random

TOKEN = ('aca esta va el tokenn')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necesario para enviar mensajes privados

client = discord.Client(intents=intents)

# Variables de juego
partida_en_curso = False
jugadores_esperados = 0
jugadores = []
canal_partida = None

@client.event
async def on_ready():
    print(f'✅ Bot conectado como {client.user}')

@client.event
async def on_message(message):
    global partida_en_curso, jugadores_esperados, jugadores, canal_partida

    if message.author == client.user:
        return

    contenido = message.content.lower()

    if contenido.startswith('!mafia crear'):
        if partida_en_curso:
            await message.channel.send("❗ Ya hay una partida en curso.")
            return

        partes = contenido.split()
        if len(partes) != 3 or not partes[2].isdigit():
            await message.channel.send("❌ Uso correcto: `!mafia crear <número de jugadores>`")
            return

        jugadores_esperados = int(partes[2])
        if jugadores_esperados < 4:
            await message.channel.send("⚠️ Se necesita al menos 4 jugadores.")
            return

        partida_en_curso = True
        jugadores = [message.author]
        canal_partida = message.channel

        await canal_partida.send(
            f"🎲 Se ha creado una partida para {jugadores_esperados} jugadores. "
            f"{message.author.display_name} se ha unido. Usa `!mafia unirme` para participar. "
            f"Jugadores actuales: 1/{jugadores_esperados}"
        )

    elif contenido == '!mafia unirme':
        if not partida_en_curso:
            await message.channel.send("❗ No hay ninguna partida activa.")
            return

        if message.author in jugadores:
            await message.channel.send("⚠️ Ya estás en la partida.")
            return

        jugadores.append(message.author)
        await canal_partida.send(
            f"✅ {message.author.display_name} se ha unido. Jugadores actuales: {len(jugadores)}/{jugadores_esperados}"
        )

        if len(jugadores) == jugadores_esperados:
            await canal_partida.send("🎉 Todos los jugadores se han unido. Asignando roles...")
            await asignar_roles()

async def asignar_roles():
    global partida_en_curso, jugadores

    num_jugadores = len(jugadores)
    roles = generar_roles(num_jugadores)
    random.shuffle(jugadores)
    random.shuffle(roles)

    for jugador, rol in zip(jugadores, roles):
        try:
            mensaje = f"📩 Tu rol es **{rol}**."
            if rol == "Mafioso":
                mensaje += "\nDurante la noche, usa `!matar <nombre>` para eliminar a alguien."
            elif rol == "Doctor":
                mensaje += "\nDurante la noche, usa `!curar <nombre>` para proteger a alguien."
            elif rol == "Detective":
                mensaje += "\nDurante la noche, usa `!investigar <nombre>` para conocer su rol."

            await jugador.send(mensaje)
        except:
            print(f"⚠️ No se pudo enviar mensaje privado a {jugador.name}.")

    await canal_partida.send("📬 Todos los roles fueron asignados por mensaje privado.")
    # Reset para nueva partida
    partida_en_curso = False
    jugadores.clear()

def generar_roles(num_jugadores):
    roles = ["Mafioso", "Doctor", "Detective"]
    restantes = num_jugadores - len(roles)
    roles += ["Ciudadano"] * restantes
    return roles

client.run(TOKEN)
