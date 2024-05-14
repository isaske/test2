#🤍♥️
#from highrise import BaseBot, Position
import asyncio
import random
import time
#from asyncio import run as arun
from asyncio import run

#from highrise.models import SessionMetadata, User
from highrise import (
    BaseBot,
    Item,
    Position,
    SessionMetadata,
    User,
    __main__,
)
from highrise.models import *
from global_variables import *
from F_guard_carg import *


class BotDefinition:

  def __init__(self, bot, room_id, api_token):
    self.bot = bot
    self.room_id = room_id
    self.api_token = api_token


async def teleporter(self: BaseBot, user, message: str) -> None:
  global warpsLista, room_id
  if any(message.lower().startswith(prefix)
         for prefix in ["/tele list", "!tele list", "/tp list", "!tp list"]):
    return
  try:
    command, soloParteDos = message.split(" ", 1)
  except Exception:
    await self.highrise.chat(
        "usa /tp <@username o coordenadas, ejemplos: 5 0 5")
    return
  UnParametro = False
  try:
    MensajePart_1, coordinate = soloParteDos.split(" ", 1)
    UnParametro = True
    try:

      #print("-el primer msj es un numero")
      #print(f"soloParteDos {soloParteDos}")
      #print(f"MensajePart_1 {MensajePart_1}")
      #print(f"coordinate {coordinate}")
      float(MensajePart_1)
      UnParametro = False
    except Exception:
      print("-el primer msj no es un numero")
      return

  except Exception:
    pass

  #lo solicito antes para no hacerlo mas veces
  room_users = (await self.highrise.get_room_users()).content
  print(UnParametro)
  if not UnParametro:  #solo hay 1 parametro
    #MOVER HACIA UN USUARIO
    partes = soloParteDos.split()
    if '@' in soloParteDos:

      soloParteDos = soloParteDos.replace("@", "")
      detector = False
      for usr, pos in room_users:
        if usr.username == soloParteDos:
          detector = True
          await self.highrise.teleport(user.id, pos)
          return
      if not detector:
        await self.highrise.chat("ERROR: No se encontro el usuario")
        return

    elif len(partes) == 1:
      #MOVER HACIA UN TELEPORT
        if room_id in warpsLista:
          teleport_list = warpsLista[room_id]
          for teleport in teleport_list:
            if teleport['name'] == soloParteDos:
              pos = teleport['pos']
              rol = teleport['rol']
              x, y, z = map(float, pos)
              await self.highrise.teleport(user.id,
                                           dest=Position(float(x), float(y),
                                                         float(z)))
            break
        else:
          await self.highrise.send_whisper(
              user.id, f"teleport '{soloParteDos}' no existe")
      

    else:
      try:
        #MOVER HACIA UNA COORDENADA
        x, y, z = soloParteDos.split(" ")
        await self.highrise.teleport(user.id,
                                     dest=Position(float(x), float(y),
                                                   float(z)))
      except ValueError:
        await self.highrise.chat("formato de coordenada incorrecto, usa x y z")
        return
  else:
    await self.highrise.chat("2 parametros")

async def enter_warp(self, room_id, warpname, pos, user_id):
  global warpsLista
  # Si la sala_id ya existe en warpsLista, actualiza o agrega el warpname
  if room_id in warpsLista:
    warps = warpsLista[room_id]

    # Busca si ya existe un warp con el mismo nombre
    warp_exists = False
    for warp in warps:
      if warp['name'] == warpname:
        # Si ya existe un warp con el mismo nombre, actualiza su posición
        warp['pos'] = pos
        warp_exists = True
        guardar = {'teleportsSalas': warpsLista}
        guardar_variables(guardar)
        await self.highrise.send_whisper(
            user_id,
            f"se ha actualizado el teleport {warpname} en tu ubicación")

        break
    if not warp_exists:
      # Si no existe un warp con el mismo nombre, agrega uno nuevo
      warps.append({'name': warpname, 'rol': "user", 'pos': pos})
      guardar = {'teleportsSalas': warpsLista}
      guardar_variables(guardar)
      await self.highrise.send_whisper(
          user_id, f"se ha creado el teleport '{warpname}' en tu ubicación")

  else:
    # Si la sala_id no existe en warpsLista, crea una nueva entrada
    warpsLista[room_id] = [{'name': warpname, 'rol': "user", 'pos': pos}]
    guardar = {'teleportsSalas': warpsLista}
    guardar_variables(guardar)
    await self.highrise.send_whisper(
        user_id, f"se ha creado el teleport '{warpname}' en tu ubicación")


class Bot(BaseBot):

  async def on_start(self, session_metadata: SessionMetadata) -> None:
    global owner_id, bot_id, bot_name, puerta_pos, carcelPos, owner_name, bot_Spawn, caraAngulo, warpsLista, vipList, adminsList
    print("-Bot iniciado-")
    bot_id = session_metadata.user_id
    owner_id = session_metadata.room_info.owner_id
    response = await self.webapi.get_user(owner_id)
    owner_name = response.user.username
    room_users = await self.highrise.get_room_users()
    for room_user, position in room_users.content:
      if room_user.id == bot_id:
        bot_name = room_user.username
        puerta_pos = position
        carcelPos = puerta_pos
        break

    variables = cargar_variables()
    carcelPos = (variables['carcelPosSave'])
    variables = cargar_variables()
    bot_Spawn = (variables['botspawnPosSave'])
    partesA = bot_Spawn.replace('[', '').replace(']', '')
    variables = cargar_variables()
    warpsLista = (variables['teleportsSalas'])
    variables = cargar_variables()
    vipList = (variables['vipListSave'])
    variables = cargar_variables()
    adminsList = (variables['adminsListSave'])

    try:
      warpsLista = eval(warpsLista)
    except Exception:
      pass
    try:
      vipList = eval(vipList)
    except Exception:
      pass
    try:
      adminsList = eval(adminsList)
    except Exception:
      pass

    partes = partesA.split(',')
    x = float(partes[0].strip())
    y = float(partes[1].strip())
    z = float(partes[2].strip())
    caraAngulo = str(partes[3].strip())
    caraAngulo = caraAngulo.replace("'", "")

    async def danceBotBucle():
      global Botemotetime
      while True:
        if Botemotetime <= 0:
          if BotDanceBaile == "random":
            Botemote = random.choice(list(listemotebot.keys()))
            time = listemotebot[Botemote]
            Botemotetime = time
            await self.highrise.send_emote(Botemote)
          else:
            await self.highrise.send_emote(BotDanceBaile)
            Botemotetime = BotemoteTimerest
        else:
          Botemotetime -= 0.5
        await asyncio.sleep(0.5)

    async def avisobot():
      while True:
        await asyncio.sleep(90)
        if GlobalAnuncio != "stop":
          await self.highrise.chat(GlobalAnuncio)

    async def start_dance_casual():
      global dancing_users
      while True:
        segureList = dict(dancing_users)
        for user_id, user_data in segureList.items():
          try:
            emote = user_data["emote"]
            status = user_data["status"]
            tiempo = user_data["tiempo"]

            if status:
              if tiempo <= 0:
                await self.highrise.send_emote(emote, user_id)
                tiempoReset = 0
                id_buscar = emote
                for emote, info in listReset.items():
                  if info['id'] == id_buscar:
                    tiempoReset = info['tiempo']

                dancing_users[user_id]["tiempo"] = tiempoReset
              else:
                tiempo -= 0.5  # Restar 0.5 al tiempo si no es menor o igual a cero
                dancing_users[user_id][
                    "tiempo"] = tiempo  # Actualizar el tiempo en el diccionario
                #print(dancing_users)
            # Si status es False, el código no envía el emote y continúa con el siguiente usuario.

          except:
            if user_id in dancing_users:
              del dancing_users[user_id]
            pass  # Manejar las excepciones según sea necesario

        await asyncio.sleep(0.5)

    async def carcelLoop():
      global carcelList
      while True:

        segureList = dict(carcelList)
        for user_id, user_data in segureList.items():
          try:
            tiempovar = user_data["tiempo"]
            username = user_data["nombre"]

            if tiempovar <= 0:
              if user_id in carcelList:
                await self.highrise.teleport(user_id, puerta_pos)
                del carcelList[user_id]
                await self.highrise.chat(
                    f"Ya eres libre @{username}! portate bien! 👮")
                await self.highrise.react("thumbs", user_id)
              pass

            else:
              tiempovar -= 1
              carcelList[user_id]["tiempo"] = tiempovar

          except:
            if user_id in carcelList:
              del carcelList[user_id]
            pass

        await asyncio.sleep(1)

    async def vipLoop():
      global vipList
      segundos = 0
      while True:
        segureList = dict(vipList)
        for user_name, user_time in segureList.items():
          try:
            tiempo = user_time
            nombre = user_name

            if tiempo == 1:
              if nombre in vipList:
                del vipList[nombre]
              pass

            elif tiempo >= 2:
              tiempo -= 1
              vipList[nombre] = tiempo

          except Exception:
            pass

        segundos += 1
        if segundos == 10:
          segundos = 0
          guardar = {'vipListSave': vipList}
          guardar_variables(guardar)

        await asyncio.sleep(1)

    # Función

    async def tiptimebucle():
      global tiptime
      while True:
        await asyncio.sleep(60)
        if tipstate:
          tiptime = int(tiptime)
          tiptime -= 1
          if tiptime <= 0:
            tiptime = tiptimerestaurar
            wallet = (await self.highrise.get_wallet()).content
            oroDisponible = wallet[0].amount
            room_users_response = await self.highrise.get_room_users()
            room_users = room_users_response.content
            num_users = len(room_users)
            if num_users <= 2:
              await self.highrise.chat("aún no hay 40 usuarios para dar tips")
            else:
              NumUserTip = num_users - 2
              oroSolicitado = NumUserTip * int(tipcantidad)

              if int(tipcantidad) in [1, 5, 10]:
                oroSolicitado += NumUserTip
              elif int(tipcantidad) == 50:
                oroSolicitado += 5 * NumUserTip
              else:
                oroSolicitado += 10 * NumUserTip

              if oroDisponible >= oroSolicitado:
                for user, _ in room_users:
                  user_name = user.username
                  if user.id not in [
                      owner_id,
                      bot_id,
                      "xxxx"  #agregar mas gente
                  ]:
                    await self.highrise.tip_user(user.id,
                                                 f"gold_bar_{tipcantidad}")
                    await self.highrise.chat(
                        f"{tipcantidad}g enviado a {user_name}")
                    await asyncio.sleep(1)
              else:
                await self.highrise.chat("sin fondos para tips automaticos")

    asyncio.create_task(avisobot())
    asyncio.create_task(start_dance_casual())
    asyncio.create_task(tiptimebucle())
    asyncio.create_task(carcelLoop())
    #asyncio.create_task(vipLoop())
    # Iniciar el bucle de baile automáticamente al inicio del programa

    await self.highrise.set_outfit(outfit=[
        Item(type='clothing',
             amount=1,
             id='body-flesh',
             account_bound=False,
             active_palette=0),
        Item(type='clothing',
             amount=1,
             id='eye-n_basic2018malesquaresleepy',
             account_bound=False,
             active_palette=7),
        Item(type='clothing',
             amount=1,
             id='eyebrow-n_basic2018newbrows07',
             account_bound=False,
             active_palette=0),
        Item(type='clothing',
             amount=1,
             id='nose-n_basic2018newnose05',
             account_bound=False,
             active_palette=0),
        Item(type='clothing',
             amount=1,
             id='mouth-basic2018chippermouth',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='glasses-n_starteritems201roundframesbrown',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='bag-n_room32019sweaterwrapblack',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='shirt-n_starteritems2019tankwhite',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='shorts-f_pantyhoseshortsnavy',
             account_bound=False,
             active_palette=-1),
        Item(type='clothing',
             amount=1,
             id='shoes-n_whitedans',
             account_bound=False,
             active_palette=-1),
    ])
    await self.highrise.teleport(bot_id, Position(x, y, z, facing=caraAngulo))
    await self.highrise.chat("Hola a todos!")
    await asyncio.sleep(0.5)
    await self.highrise.walk_to(Position(x, y, z, facing=caraAngulo))

    if tipstate:
      await self.highrise.chat(
          f"Los tips automaticos estan activados, se enviará {tipcantidad}g cada {tiptimerestaurar} minutos cuando hayan 40 o mas en la sala.\n\nPara desactivar escribe: /autotip stop"
      )
    await asyncio.sleep(0.5)
    asyncio.create_task(danceBotBucle())

  async def on_emote(self, user: User, emote_id: str,
                     receiver: User | None) -> None:
    """On a received emote."""
    #print(emote_id, user.username)

  async def on_tip(self, sender: User, receiver: User,
                   tip: CurrencyItem | Item) -> None:
    if receiver.username == bot_name:
      mensaje = ""
      corazones = 0
      if tip.amount == 1:
        mensaje = "tacañ@ 😒"
        corazones = 1
      elif tip.amount == 5:
        mensaje = "te quiero 💖"
        corazones = 3
      elif tip.amount == 10:
        mensaje = "nada mal 😉"
        corazones = 5
      elif tip.amount == 50:
        mensaje = "se ve que me quieres 🥺"
        corazones = 10
      elif tip.amount == 100:
        mensaje = "me amas admitelo 😏"
        corazones = 20
      elif tip.amount == 500:
        mensaje = "me enamore 😍"
        corazones = 30
      elif tip.amount == 1000:
        mensaje = "hazme un hijo 😳"
        corazones = 50
      elif tip.amount == 5000:
        mensaje = "😨 cuando nos casamos 😍"
        corazones = 70
      else:
        mensaje = "no me lo creo 😱"
      await self.highrise.chat(
          f"{sender.username} gracias por tu donacion de {tip.amount}g! {mensaje}"
      )
      for i in range(corazones):
        await self.highrise.react("heart", sender.id)
        await asyncio.sleep(0.1)

  async def on_user_join(self, user: User,
                         position: Position | AnchorPosition) -> None:
    global carcelAuto

    await self.highrise.react("wave", user.id)
    await self.highrise.send_whisper(user.id,
                                     f"Hola, {user.username} bienvenid@!")

    myid = user.id
    myname = user.username
    segureList = dict(carcelList)
    for user_id, user_data in segureList.items():
      try:
        if myid == user_id:
          vartiempo = user_data["tiempo"]
          name = user_data["nombre"]
          partesA = str(carcelPos).replace('[', '').replace(']', '')
          partes = partesA.split(',')
          x = float(partes[0].strip())
          y = float(partes[1].strip())
          z = float(partes[2].strip())
          horas = vartiempo // 3600
          minutos = (vartiempo % 3600) // 60
          segundos = vartiempo % 60
          if vartiempo >= 3600:
            await self.highrise.chat(
                f"@{name.upper()} aun te quedan {horas}h {minutos}m {segundos}s en la cárcel bandid@! 👮"
            )

          elif vartiempo >= 60:
            await self.highrise.chat(
                f"@{name.upper()} aun te quedan {minutos}m {segundos}s en la cárcel bandid@! 👮"
            )

          else:
            await self.highrise.chat(
                f"@{name.upper()} aun te quedan {segundos}s en la cárcel bandid@! 👮"
            )
          await self.highrise.teleport(myid,
                                       Position(x, y, z, facing='FrontLeft'))
          return
      except:
        pass
    if carcelAuto:
      if not myid == owner_id:
        enter_user_carcel(myid, 30 * 60, myname)

        partesA = str(carcelPos).replace('[', '').replace(']', '')
        partes = partesA.split(',')
        x = float(partes[0].strip())
        y = float(partes[1].strip())
        z = float(partes[2].strip())

        await self.highrise.chat(
            f"@{myname.upper()} estarás encerrad@ por 30 min 👮")
        await self.highrise.teleport(myid, Position(x,
                                                    y,
                                                    z,
                                                    facing='FrontLeft'))

  #CONFESIONES
  async def on_whisper(self, user: User, message: str) -> None:
    await self.highrise.chat(message)
    print(f"[WHISPER] {user.username} {message}")

  async def on_chat(self, user: User, message: str) -> None:
    global tiptimerestaurar, tiptime, tipstate, tipcantidad, GlobalAnuncio, \
     nombreParaSeguir, dancing_users, owner_name, carcelList, carcelPos, \
     bot_name, carcelAuto, adminsList, caraAngulo, BotDanceBaile, \
     Botemotetime, BotemoteTimerest, Game1num, Game1Status, listemotebot, \
     vipList, warpsLista
    """En un chat recibido en toda la sala."""

    if message.lower().startswith("/anuncio"):
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()

        if len(partes) == 1:
          await self.highrise.chat(
              "\nactualiza tu anuncio usando\n/anuncio [mensaje]")
        if len(partes) >= 2:
          partes = message.split(" ")
          anuncio = ' '.join(partes[1:])
          if anuncio == "stop":
            await self.highrise.chat("se han detenido los anuncios automaticos"
                                     )
          guardar = {'anuncioAuto': anuncio}
          guardar_variables(guardar)
          GlobalAnuncio = (guardar['anuncioAuto'])
          if GlobalAnuncio != "stop":
            await self.highrise.chat(
                f"Anuncio automatico Actualizado.\n\n{GlobalAnuncio}")

    #Revisar dinero
    if message.startswith("/billetera"):
      if user.username == owner_name or user.username in adminsList:
        wallet = (await self.highrise.get_wallet()).content
        await self.highrise.chat(
            f"La billetera del bot contiene {wallet[0].amount}g")

    if message.startswith("/tip"):
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()
        if len(partes) >= 2:

          numeros_validos = {1, 5, 10, 50, 100}
          partes = message.split(" ")
          parteCantidad = partes[1].strip()

          if not parteCantidad.isdigit():
            parteCantidad = 0

          if int(parteCantidad) not in numeros_validos:

            await self.highrise.chat(
                "ERROR: utiliza numeros entre 1,5,10,50,100")

          else:

            wallet = (await self.highrise.get_wallet()).content
            oroDisponible = wallet[0].amount
            room_users_response = await self.highrise.get_room_users()
            room_users = room_users_response.content
            num_users = len(room_users)
            if num_users == 2:
              await self.highrise.chat(
                  "ERROR: No hay suficientes usuarios para dar tips")
            else:
              NumUserTip = num_users - 2
              oroSolicitado = NumUserTip * int(parteCantidad)

              if int(parteCantidad) in [1, 5, 10]:
                oroSolicitado += NumUserTip
              elif int(parteCantidad) == 50:
                oroSolicitado += 5 * NumUserTip
              else:
                oroSolicitado += 10 * NumUserTip

              if oroDisponible >= oroSolicitado:
                for user, _ in room_users:
                  user_id = user.id
                  user_name = user.username
                  if user_id not in [
                      owner_id,
                      bot_id,
                      "xxxx"  #agregar mas gente
                  ]:
                    await self.highrise.tip_user(user_id,
                                                 f"gold_bar_{parteCantidad}")
                    await self.highrise.chat(
                        f"{parteCantidad}g enviado a {user_name}")
                    await asyncio.sleep(1)
              else:
                await self.highrise.chat("ERRROR: Bot sin fondos")
                await self.highrise.send_whisper(
                    user.id,
                    f"ERROR: no es posible repartir a todos, tienes {oroDisponible}g y necesitas {oroSolicitado}g"
                )

        else:
          # Manejar el caso en que no haya suficientes elementos en partes
          await self.highrise.chat(
              "ERROR: No se proporcionó la cantidad. ej: /tip 1")

    if message.lower().startswith("/autotip"):
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()

        if len(partes) == 2:
          partes = message.split(" ")
          parteComando = partes[1].strip()
          if parteComando == "stop":
            tipstate = False
            guardar = {'autoTipSave': ""}
            guardar_variables(guardar)
            await self.highrise.chat(
                "Tips automaticos desactivados correctamente.\nPara volver a activar usa\n/autotip [cantidad] [minutos]"
            )
            return

        if len(partes) <= 2:
          await self.highrise.chat(
              "Utiliza\n/autotip [cantidad] [minutos]\npara repartir tips automaticamente cuando hayan 40 o mas en la sala.\n\n/autotip stop, para detenerlo"
          )
          return

        if len(partes) >= 3:

          numeros_validos = {1, 5, 10, 50, 100}
          partes = message.split(" ")
          parteCantidad = partes[1].strip()
          parteTiempo = partes[2].strip()
          ComandoAprobado = True

          if not parteCantidad.isdigit() or int(
              parteCantidad) not in numeros_validos:
            ComandoAprobado = False
            await self.highrise.chat(
                "Error Cantidad: utiliza números entre 1, 5, 10, 50, 100 de oro a enviar"
            )

          if not (parteTiempo.isdigit() and 1 <= int(parteTiempo) <= 60):
            ComandoAprobado = False
            await self.highrise.chat(
                "Error Tiempo: debe ser un numero entre 1 y 60 (minutos)")

          if ComandoAprobado:

            tiptimerestaurar = int(parteTiempo)
            tiptime = parteTiempo
            tipcantidad = parteCantidad
            tipstate = True

            guardar = {'autoTipSave': "True"}
            guardar_variables(guardar)
            guardar = {'cantidadTipSave': tipcantidad}
            guardar_variables(guardar)
            guardar = {'tiempoTipSave': tiptime}
            guardar_variables(guardar)

            wallet = (await self.highrise.get_wallet()).content
            await self.highrise.chat(
                f"\noro disponible: {wallet[0].amount}g\nse enviaran {tipcantidad}g cada {tiptime} minutos cuando hayan 40 o mas en la sala.\n\nusa /autotip stop, para detenertlo"
            )
          else:
            await self.highrise.chat(
                "Utiliza\n/autotip [cantidad] [minutos]\npara repartir tips automaticamente cuando hayan 40 o mas en la sala.\n\n/autotip stop, para detenerlo"
            )
          return

    if message.lower().startswith("/id"):
      room_users = (await self.highrise.get_room_users()).content
      users_info = "\n".join(
          [f"{user.username} {user.id}" for user, _ in room_users])
      print(users_info)

    #futuro
    if message.startswith("/futuro"):
      pregunta = message[8:]
      FraseFinal = random.choice(
          ["Obviamente si 😎", " si 😎", "nel 🙄", "no, pero tu mamá si 😎"])
      await self.highrise.chat(
          f"{user.username} pregunta: {pregunta} Respuesta: {FraseFinal}")

    if message.startswith("/bot emote"):
      global BotDanceBaile, Botemotetime
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()
        if len(partes) >= 3:
          emote_name = ' '.join(partes[2:]).strip().lower()

          idEmote, timeEmote = emoteObtener(emote_name)

          if idEmote is not None:
            BotemoteTimerest = timeEmote
            BotDanceBaile = idEmote
            Botemotetime = 0

          else:
            await self.highrise.chat(f" Emote '{emote_name}' no encontrado")

    #emote all
    if message.startswith("/emote all"):
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()
        if len(partes) == 3:
          emote_name = partes[2].strip().lower()

          room_users = (await self.highrise.get_room_users()).content
          for user_info in room_users:
            user_id = user_info[0].id
            if user_id in dancing_users:
              dancing_users[user_id]["status"] = False

          tiempoReset = 0
          emote_id = ""
          detector = False
          if emote_name in listReset:
            detector = True
            emote_id = listReset[emote_name]['id']
            tiempoReset = listReset[emote_name]['tiempo']
          if not detector:
            await self.highrise.chat("Emote no existe")
            return
          for user_info in room_users:
            user = user_info[0]
            try:
              await self.highrise.send_emote(emote_id, user.id)
            except:
              pass

          await asyncio.sleep(tiempoReset)

          for user_info in room_users:
            user_id = user_info[0].id

            if user_id in dancing_users:
              dancing_users[user_id]["status"] = True
              dancing_users[user_id]["tiempo"] = 0

    #aa
    if message.startswith("usuarios"):
      room_users = (await self.highrise.get_room_users()).content
      user_names = [user.username for user, _ in room_users]
      for name in user_names:
        print(name)

  #match
    if message.lower().startswith("/match"):
      partes = message.split("@")
      if message.lower().startswith("/match @isaak55 @xxxx") or message.lower(
      ).startswith("/match @xxxx @isaak55"):

        await self.highrise.chat("Que le importa metiche 😒")

      elif len(partes) == 3:
        nombre_usuario1 = partes[1].strip()
        nombre_usuario2 = partes[2].strip()
        hash_usuario1 = hash(nombre_usuario1) + 4
        hash_usuario2 = hash(nombre_usuario2) + 2
        compatibilidad = abs(hash_usuario1 + hash_usuario2) % 101
        mensajeFinal = ""
        if compatibilidad >= 100:
          mensajeFinal = "¿esto es perfección o algo del diablo? 😱 no importa ya casense! 😍"
        elif compatibilidad >= 99:
          mensajeFinal = "no sé si estar feliz por tanta compatibilidad ❤️" "o triste porque solo faltaba 1% para la perfección 😳"
        elif compatibilidad >= 80:
          mensajeFinal = "los numeros hablan por si solos, ahora todo queda en sus manos, viviran entre las llamas de del amor o dejaran que la llama se extinga"
        elif compatibilidad >= 51:
          mensajeFinal = "Tienen una conexión más fuerte que mi internet! ¡eso es bastante! 😎"
        elif compatibilidad >= 50:
          mensajeFinal = "ni frío ni caliente, ¿quizás amigos con beneficios? 😏"
        elif compatibilidad >= 40:
          mensajeFinal = "bueno podría funcionar si evitan discusiones sobre la pizza con piña 🙄 "
        elif compatibilidad >= 20:
          mensajeFinal = "el amor es complicado, pero ¿porque no hacerlo más interesante? 😈"
        elif compatibilidad >= 2:
          mensajeFinal = "¿compañeros de vida o compañeros de celda? He ahí el dilema 🙃"
        elif compatibilidad >= 1:
          mensajeFinal = "increible mas de 0! hagan el intento! yo les pago la terapia 😎"
        elif compatibilidad >= 0:
          mensajeFinal = "¿Quién los emparejó? ¿Un experto en comedia romántica? 🤡"
        await self.highrise.chat(
            f"La compatibilidad de {nombre_usuario1} y {nombre_usuario2} es {compatibilidad}% {mensajeFinal}"
        )
      else:
        await self.highrise.chat(
            "Para /match se necesita 2 usuarios@\nintenta /match @nombre1 @nombre2 (no olvides el simbolo @)"
        )
        return None, None

    #BATTLE
    if message.lower().startswith("/pelea"):
      partes = message.split("@")
      if len(partes) == 2:
        nombre_usuario1 = user.username
        id_usuario1 = user.id
        nombre_usuario2 = partes[1].strip()

        if user.id in dancing_users:
          dancing_users[user.id]["status"] = False

        room_users = (await self.highrise.get_room_users()).content
        user_info = [(user.username, user.id) for user, _ in room_users]

        user_names = [info[0] for info in user_info]

        if nombre_usuario2 in user_names:
          user2_id = user_info[user_names.index(nombre_usuario2)][1]
          try:
            if user.id in dancing_users:
              dancing_users[user2_id]["status"] = False
          except:
            pass

          await self.highrise.chat(
              f"@{nombre_usuario1.upper()} a retado a una pelea epica a @{nombre_usuario2.upper()}! ¿quien ganará?"
          )
          emote_id = "emote-swordfight"
          await self.highrise.send_emote(emote_id, user2_id)
          await self.highrise.send_emote(emote_id, id_usuario1)
          time.sleep(5)
          winner_name = random.choice([nombre_usuario1, nombre_usuario2])
          loser_name = ""
          if winner_name.lower() == nombre_usuario1.lower():
            winner_name = winner_name.upper()
            loser_name = nombre_usuario2.upper()
            emote_id = "emoji-celebrate"
            await self.highrise.send_emote(emote_id, id_usuario1)
            emote_id = "emote-sad"
            await self.highrise.send_emote(emote_id, user2_id)

          else:
            winner_name = winner_name.upper()
            loser_name = nombre_usuario1.upper()
            emote_id = "emote-sad"
            await self.highrise.send_emote(emote_id, id_usuario1)
            emote_id = "emoji-celebrate"
            await self.highrise.send_emote(emote_id, user2_id)

          fraseFinal = random.choice([
              f"@{winner_name} emerge montando un unicornio invisible 🦄 que lanza rayos invisibles ⚡ @{loser_name} quedó impactado y rendido 😲",
              f"En medio de la pelea, @{winner_name} sacó un pinguino disfrazado de monja 🐧 @{loser_name} estuvo tan ocupado riéndose que no pudo contraatacar 😂",
              f"@{winner_name} invocó un tornado de algodón de azúcar que envolvió a @{loser_name} en dulzura, dejándolo con diabetes e incapaz de luchar 😞",
              f"La pelea se desvió hacia una competición de chistes malos, @{winner_name} hizo un chiste tan malo que @{loser_name} se desmayó de lo malo que era 🤡",
              f"En un giro inesperado, @{winner_name} desafió a @{loser_name} a un concurso de carreras de caracoles ciegos 🐌. Sorprendentemente ganó por un centímetro!😱",
              f"La pelea se convirtió en una competencia de baile de pollos hipnotizados🐥. La mirada hipnótica de @{winner_name} 👁️👄👁️ hizo que su pollo hiciera unos pasos increíbles!"
          ])
          await self.highrise.chat(
              f"{fraseFinal}. El ganador es @{winner_name}! ")
          await asyncio.sleep(3)
          if user.id in dancing_users:
            try:
              dancing_users[user.id]["status"] = True
              dancing_users[user.id]["tiempo"] = 0
            except:
              pass
            try:
              dancing_users[user2_id]["status"] = True
              dancing_users[user2_id.id]["tiempo"] = 0
            except:
              pass

        else:
          await self.highrise.chat(
              f"@{user.username} El usuario que mencionas no esta dentro de la sala"
          )
      else:
        await self.highrise.chat(
            f"@{user.username} utiliza /pelea @nombre (no olvides el simblo@")

    #BROMA
    if message.lower().startswith("/broma"):
      partes = message.split("@")
      if len(partes) == 2:
        nombre_usuario1 = user.username
        id_usuario1 = user.id
        nombre_usuario2 = partes[1].strip()

        room_users = (await self.highrise.get_room_users()).content
        user_info = [(user.username, user.id) for user, _ in room_users]

        user_names = [info[0] for info in user_info]

        if nombre_usuario2 in user_names:
          user2_id = user_info[user_names.index(nombre_usuario2)][1]
          try:
            if user.id in dancing_users:
              dancing_users[user2_id]["status"] = False
          except:
            pass

          await self.highrise.chat(
              f"@{nombre_usuario1.upper()} esta molestando a {nombre_usuario2.upper()}!"
          )
          emote_id = "emote-gravity"
          await self.highrise.send_emote(emote_id, user2_id)

        else:
          await self.highrise.chat(
              f"{user.username} El usuario que mencionas no esta dentro de la sala"
          )
      else:
        await self.highrise.chat(
            f"{user.username} utiliza /broma @nombre (no olvides el simblo@")

    #EMOTES INDIVIDUALES
    if "/poses" in message.lower():
      await self.highrise.send_whisper(
          user.id,
          "kiss sad wave tired angry thumb lust cursing greedy flex gagg celebrate bow curtsy hot confused super cute pose7 pose8 pose1 pose3 pose5 cute"
      )

    # Para ingresar al usuario a la lista

    #dance-orangejustice
    #emote-exasperatedb
    #dance-smoothwalk
    #dance-breakdance
    #dance-floss
    #emote-ghost-idle
    #emote-gordonshuffle
    #idle-dance-headbobbing

    #enviar emotes
    if message in listReset:
      launch_info = listReset[message]
      emote_id = launch_info['id'].lower()
      enter_user_list(user.id, emote_id, 0)

    # Comando para detener el baile casual para el usuario actual
    if "stop" in message.lower():
      if user.id in dancing_users and dancing_users[user.id]:
        del dancing_users[user.id]
        await self.highrise.send_emote("emote-hot", user.id)
    #-------
    if "besote" in message.lower() or "beso" in message.lower(
    ) or "besito" in message.lower() or "muak" in message.lower():

      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-kiss"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/no" in message.lower() or "no quiero" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-no"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "tristesa" in message.lower() or "estoy triste" in message.lower(
    ) or "toy triste" in message.lower() or "estoy sad" in message.lower(
    ) or "toy sad" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-sad"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "yes" in message.lower() or "si te creo" in message.lower(
    ) or "sisi" in message.lower() or "sii" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-yes"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/laughing" in message.lower() or "jaja" in message.lower(
    ) or "jask" in message.lower() or "jkj" in message.lower(
    ) or "ajaj" in message.lower() or "jsjs" in message.lower(
    ) or "jsk" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-laughing"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if (message.lower().startswith("/hello") or
        message.lower().startswith("hola") or message.lower().startswith("ola")
        or message.lower().startswith("o  li")) and not (
            "ola guap" in message.lower() or "oli guap" in message.lower()):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-hello"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0

    #-------
    if "que verguenza" in message.lower() or "soy timido" in message.lower(
    ) or "soy timida" in message.lower() or "me da pena" in message.lower(
    ) or "me da penita" in message.lower() or "soy tímido" in message.lower(
    ) or "soy tímida" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-shy"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass

      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "que flojera" in message.lower() or "tengo sueño" in message.lower(
    ) or "tengo pereza" in message.lower() or "tengo flojera" in message.lower(
    ):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-tired"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "malote" in message.lower() or "muy mal" in message.lower(
    ) or "que malo" in message.lower() or "que mala" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-angry"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/sit" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "idle-loop-sitfloor"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "vale" in message.lower() or message.lower().startswith("ok"):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-thumbsup"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "ola hermoz" in message.lower() or "hola guap" in message.lower(
    ) or "ola guap" in message.lower() or "hola lind" in message.lower(
    ) or "ola lind" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-lust"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "ptm" in message.lower() or "rayos" in message.lower(
    ) or "mrd" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-cursing"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "que raro" in message.lower() or "sospechoso" in message.lower(
    ) or "que extraño" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-greedy"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "asi es" in message.lower() or "así es" in message.lower(
    ) or "lo lograr" in message.lower() or "tu puedes" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-flex"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(1)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "wakala" in message.lower() or "asco" in message.lower(
    ) or "asquero" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-gagging"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "celebra" in message.lower() or "yupi" in message.lower(
    ) or "yey" in message.lower() or "estoy feliz" in message.lower(
    ) or "wujuu" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emoji-celebrate"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/model" in message.lower() or "soy guapo" in message.lower(
    ) or "soy guapa" in message.lower() or "que bello soy" in message.lower(
    ) or "que bella soy" in message.lower(
    ) or "que guapo soy" in message.lower(
    ) or "que guapa soy" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-model"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(6)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/penny" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "dance-pennywise"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(1)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "de nada" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-bow"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "el placer es" in message.lower() or "un placer" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-curtsy"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
        #-------
    if "/snowball" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-snowball"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "cansad" in message.lower() or "que calor" in message.lower(
    ) or "hace calor" in message.lower() or "tengo calor" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-hot"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/angel" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-snowangel"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "confundid" in message.lower() or "nose" in message.lower(
    ) or "nidea" in message.lower() or "que se yo" in message.lower(
    ) or "no lo se" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-confused"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(8)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/enth" in message.lower() or "encerio" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "idle-enthusiastic"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(9)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/teleport" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-teleporting"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(11)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/maniac" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-maniac"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if ("que lind" in message.lower() and "que hermo" not in message.lower()):
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-cute"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(6)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "entendido" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-pose1"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(2)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/pose3" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-pose3"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/pose5" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-pose5"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(4)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/cutey" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-cutey"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(3)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/zombie" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-zombierun"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(9)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/fashion" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-fashionista"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(5)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/gravity" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "emote-gravity"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(7)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0
    #-------
    if "/uwu" in message.lower():
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = False
      try:
        emote_id = "idle-uwu"
        await self.highrise.send_emote(emote_id, user.id)
      except:
        pass
      await asyncio.sleep(15)
      if user.id in dancing_users:
        dancing_users[user.id]["status"] = True
        dancing_users[user.id]["tiempo"] = 0

  #baile bot

    if "/bot bailame" in message.lower() or "bot bailame" in message.lower(
    ) or "bailame bot" in message.lower() or "bot baila" in message.lower(
    ) or "baila bot" in message.lower() or "báilame bot" in message.lower(
    ) or "bot báilame" in message.lower():
      emote_id = random.choice([
          "dance-macarena", "dance-tiktok8", "dance-blackpink",
          "dance-tiktok2", "dance-russian", "dance-shoppingcart",
          "emote-snake", "idle_singing", "dance-tiktok9", "dance-tiktok10",
          "idle-dance-casual", "idle-dance-tiktok4"
      ])
      await self.highrise.send_emote("dance-smoothwalk")

    #FRASES RAPIDAS

    #insulto al bot
    if "bot feo" in message.lower():
      response = random.choice([
          f"tu cola {user.username} 😠",
          f"que dices {user.username} yo soy hermoso 😌",
          f"fe@ tu {user.username} 😠"
      ])
      await self.highrise.chat(response)

    if "bot lindo" in message.lower() or "bot guapo" in message.lower():
      response = random.choice([
          f"me sonrojas {user.username} 🥰",
          f"tu tambien lo eres {user.username} ❤️",
          f"gracias {user.username} lo se 🤗"
      ])
      await self.highrise.chat(response)

    if "bot gay" in message.lower() or "bot tonto" in message.lower(
    ) or "bot weon" in message.lower() or "pinche bot" in message.lower(
    ) or "bot pendejo" in message.lower() or "bot mamahuevo" in message.lower(
    ):
      response = random.choice([
          f"tu mismo {user.username} 😠", f"tu mama será {user.username}",
          f"no me cuentes tus verdades {user.username} "
      ])
      await self.highrise.chat(response)

  #insulto al bot 2
    if "te odio bot" in message.lower() or "bot te odio" in message.lower():
      response = random.choice([
          f"Yo te quiero mucho {user.username}",
          f"Yo tambien te odio {user.username}",
          f"Por que tanto odio {user.username}?"
      ])
      await self.highrise.chat(response)

      #te amo bot
    if "te amo bot" in message.lower() or "bot te amo" in message.lower(
    ) or "bot te quiero" in message.lower(
    ) or "te quiero bot" in message.lower():
      if user.username == "xMissJeanx":
        await self.highrise.chat(
            f"Yo tambien te amo {user.username} mi unica bebe ♥️")
      else:
        await self.highrise.chat(f"Yo tambien te amo {user.username} ♥️")

  #CUANDO MORIRE
    if "/muerte" in message.lower():
      usuario = user.id
      hash_usuario = hash(str(usuario))
      compatibilidad = abs(hash_usuario) % 61
      if compatibilidad >= 60:
        mensajeFinal = "Morirás por aguantar un estornudo durante una reunión importante 🤧"
      elif compatibilidad >= 50:
        mensajeFinal = "Te reirás tanto que literalmente te partirás de risa 😂 y morirás 💀"
      elif compatibilidad >= 40:
        mensajeFinal = "Morirás por ser lanzado por un cañón en un circo después de confundirte con un payaso 🤡"
      elif compatibilidad >= 30:
        mensajeFinal = "Serás abducid@ por un grupo de vacas 🐄 alienígenas 👽 que querían aprender a bailar la macarena 💃"
      elif compatibilidad >= 20:
        mensajeFinal = "Morirás por intentar surfear una ola 🌊 en una tabla de planchar 💀"
      elif compatibilidad >= 10:
        mensajeFinal = "Morirás al ser tragado por un agujero de gusano 🐛🌌 en tu jardín mientras cavabas un hoyo 🕳️"
      elif compatibilidad >= 1:
        mensajeFinal = "Mueres de exceso de salud por comer una ensalada y atragantarte con una lechuga 🥬"
      elif compatibilidad >= 0:
        mensajeFinal = "Morirás pronto por jugar demaciado Highrise 👾💀"
      await self.highrise.chat(
          f"{user.username} Te quedan {compatibilidad} años de vida, {mensajeFinal}"
      )
  #CUANDO AMOR
    if "cuanto amor" in message:
      love_percentage = random.randint(1, 100)
      await self.highrise.chat(f"tu porcentaje de amor es: {love_percentage}%")

    if any(message.lower().startswith(prefix)
           for prefix in ["/tele", "!tele", "/tp", "!tp"]):

      parts = message.split()
      if any(message.lower().startswith(prefix) for prefix in [
          "/tele delete", "!tele delete", "/tp delete", "!tp delete",
          "/tele remove", "!tele remove", "/tp remove", "!tp remove"
      ]):
        if len(parts) >= 3:
          tercer_texto = parts[2]
          print(tercer_texto)
          if room_id in warpsLista:
            teleport_list = warpsLista[room_id]
            for teleport in teleport_list:
              if teleport['name'] == tercer_texto:
                teleport_list.remove(teleport)
                guardar = {'teleportsSalas': warpsLista}
                guardar_variables(guardar)
                await self.highrise.send_whisper(
                    user.id, f"teleport '{tercer_texto}' eliminado")
                break
            else:
              await self.highrise.send_whisper(
                  user.id, f"teleport '{tercer_texto}' no existe")
          else:
            await self.highrise.send_whisper(
                user.id, f"teleport '{tercer_texto}' no existe")
        else:
          await self.highrise.send_whisper(user.id, "/tele delete [teleport]")
      else:

        await teleporter(self, user, message)

    if message.startswith("/carcel"):
      if user.username == owner_name or user.username in adminsList:
        if message == "/carcel auto":
          if carcelAuto == False:
            carcelAuto = True
            await self.highrise.chat("Cárcel automática activada")
            return
          else:
            carcelAuto = False
            await self.highrise.chat("Cárcel automática desactivada")
          return

        if message == "/carcel liberar":
          room_users = (await self.highrise.get_room_users()).content
          user_ids_in_room = {user_info[0].id for user_info in room_users}
          carcelList_keys = list(carcelList.keys())
          detectar = any(user_id in user_ids_in_room
                         for user_id in carcelList_keys)

          if detectar:
            await self.highrise.chat("¡Todos libres! 👮👍")
          else:
            await self.highrise.chat("No hay nadie en la cárcel para liberar 👮"
                                     )
            return

          for user_id in carcelList_keys:
            name = carcelList[user_id]["nombre"]
            del carcelList[user_id]
            if user_id in user_ids_in_room:
              try:
                await self.highrise.teleport(user_id, puerta_pos)
              except:
                pass
          return
        if message == "/carcel todos":
          room_users = (await self.highrise.get_room_users()).content
          user_ids_in_room = {(user_info[0].id, user_info[0].username)
                              for user_info in room_users}
          carcelList_keys = list(carcelList.keys())
          comprobar = False
          # Verificar si hay al menos dos usuarios en la habitación
          for user_id, name in user_ids_in_room:
            if user_id not in carcelList_keys:
              if user_id not in [owner_id, bot_id]:
                comprobar = True

          if comprobar:
            await self.highrise.chat("Todos encarcelados por 30min! 👮👍")
            partesA = str(carcelPos).replace('[', '').replace(']', '')
            partes = partesA.split(',')
            x = float(partes[0].strip())
            y = float(partes[1].strip())
            z = float(partes[2].strip())
            for user_id, name in user_ids_in_room:
              if user_id not in carcelList_keys:
                if user_id not in [owner_id, bot_id]:
                  enter_user_carcel(user_id, 30 * 60, name)
                  await self.highrise.teleport(
                      user_id, Position(x, y, z, facing='FrontLeft'))
            return
          else:
            await self.highrise.chat("No hay nadie libre para encarcelar 👮")
            return
        if message == "/carcel limpiar":
          room_users = (await self.highrise.get_room_users()).content
          user_ids_in_room = {user_info[0].id for user_info in room_users}
          carcelList_keys = list(carcelList.keys())
          detectar = False
          for user_id in carcelList_keys:
            if user_id not in user_ids_in_room:
              detectar = True
              name = carcelList[user_id]["nombre"]
              del carcelList[user_id]
          if detectar:
            await self.highrise.chat(
                "lista cárcel actualizada con los presentes👮")
          else:
            await self.highrise.chat(
                "Lista limpia, todos los encarcelados están presente 👮")
          return

        if message == "/carcel lista":
          segureList = dict(carcelList)
          detector = False
          mensajes = []  # Lista para almacenar los mensajes
          usuarios_enviados = set(
          )  # Conjunto para mantener un registro de los usuarios a los que se les ha enviado mensaje
          for user_id, user_data in segureList.items():
            try:
              if user_id in carcelList:
                detector = True
                vartiempo = user_data["tiempo"]
                name = user_data["nombre"]
                horas = vartiempo // 3600
                minutos = (vartiempo % 3600) // 60
                segundos = vartiempo % 60
                mensaje = ""
                if vartiempo >= 3600:
                  mensaje += f"\n{name} le quedan {horas}h {minutos}m {segundos}s"
                elif vartiempo >= 60:
                  mensaje += f"\n{name} le quedan {minutos}m {segundos}s"
                else:
                  mensaje += f"\n{name} le quedan {segundos}s"
                # Verificar si el usuario ya ha sido enviado
                if user_id not in usuarios_enviados:
                  mensajes.append(mensaje)  # Agregar mensaje a la lista
                  usuarios_enviados.add(
                      user_id
                  )  # Registrar que se envió un mensaje a este usuario
            except Exception as e:
              pass

          # Enviar mensajes en grupos de 5 cada 0.5 segundos
          for i in range(0, len(mensajes), 5):
            await asyncio.sleep(0.5)  # Esperar 0.5 segundos
            await self.highrise.chat(''.join(mensajes[i:i + 5])
                                     )  # Enviar mensajes del grupo

          if detector == False:
            await self.highrise.chat("no hay nadie en la carcel")
          return
        partesEspacios = message.split()
        if len(partesEspacios) >= 3:
          partes = message.split("@")
          if len(partes) == 2:
            nombre_usuario2 = partes[1].strip().split()[0]
            numCarcel = partes[0].strip().split()[0]
            if nombre_usuario2 == bot_name:
              await self.highrise.chat("yo no hice nada! 😠")
              return
            vartiempo = partesEspacios[2].strip()
            mensaje_restante = ""
            if len(partesEspacios) >= 4:
              # Obtener el texto siguiente al tercer espacio
              texto_siguiente = ' '.join(partesEspacios[3:])
              # Tomar los primeros 40 caracteres del texto siguiente
              mensaje_restante = texto_siguiente[:1000]

            if vartiempo.isdigit():
              vartiempo = int(vartiempo)
              room_users = (await self.highrise.get_room_users()).content
              user_info = [(usr.username, usr.id) for usr, _ in room_users]
              user_names = [info[0] for info in user_info]
              if nombre_usuario2 in user_names:
                id_usuario2 = user_info[user_names.index(nombre_usuario2)][1]
                if vartiempo == 0:
                  segureList = dict(carcelList)
                  enLaLista = False
                  for user_id, user_data in segureList.items():
                    try:
                      if user_id in carcelList:
                        await self.highrise.teleport(id_usuario2, puerta_pos)
                        del carcelList[id_usuario2]
                        enLaLista = True
                        await self.highrise.chat(
                            f"Ya eres libre @{nombre_usuario2.upper()}! portate bien! 👮"
                        )
                        await self.highrise.react("thumbs", id_usuario2)

                        return
                    except:
                      pass
                  if not enLaLista:
                    await self.highrise.chat(
                        f"@{nombre_usuario2.upper()} no está en la cárcel 👮")
                  return
                if vartiempo >= 1440:
                  vartiempo = 1440

                enter_user_carcel(id_usuario2, vartiempo * 60, nombre_usuario2)

                partesA = str(carcelPos).replace('[', '').replace(']', '')
                partes = partesA.split(',')
                x = float(partes[0].strip())
                y = float(partes[1].strip())
                z = float(partes[2].strip())

                if vartiempo >= 60:
                  horas = vartiempo // 60  #
                  minutos_restantes = vartiempo % 60
                  vartiempo = str(horas) + "h y " + str(minutos_restantes)

                await self.highrise.chat(
                    f"{nombre_usuario2} estarás encerrad@ por {vartiempo}min {mensaje_restante} 👮"
                )
                await self.highrise.teleport(
                    id_usuario2, Position(x, y, z, facing='FrontLeft'))
              else:
                await self.highrise.chat(
                    "ERROR:usuario no existe\nUsa: /carcel @nombre [minutos] (motivo opcional)n/carcel @nombre 0 para liberar"
                )
            else:
              await self.highrise.chat(
                  "ERROR: minutos\n Usa: /carcel @nombre [minutos] (motivo opcional)n/carcel @nombre 0 para liberar"
              )
          else:
            await self.highrise.chat(
                "ERROR: falta @\nUsa: /carcel @nombre [minutos] (motivo opcional)n/carcel @nombre 0 para liberar"
            )
        else:
          partes = message.split("@")
          if len(partes) == 2:
            nombre_usuario2 = partes[1].strip().split()[0]
            if nombre_usuario2 == bot_name:
              await self.highrise.chat("yo no hice nada! 😠")
              return
            room_users = (await self.highrise.get_room_users()).content
            user_info = [(usr.username, usr.id) for usr, _ in room_users]
            user_names = [info[0] for info in user_info]
            if nombre_usuario2 in user_names:
              id_usuario2 = user_info[user_names.index(nombre_usuario2)][1]
              enter_user_carcel(id_usuario2, 30 * 60, nombre_usuario2)

              partesA = str(carcelPos).replace('[', '').replace(']', '')
              partes = partesA.split(',')
              x = float(partes[0].strip())
              y = float(partes[1].strip())
              z = float(partes[2].strip())

              await self.highrise.chat(
                  f"@{nombre_usuario2.upper()} estarás encerrad@ por 30 min 👮")
              await self.highrise.teleport(
                  id_usuario2, Position(x, y, z, facing='FrontLeft'))
            else:
              await self.highrise.chat(
                  "ERROR: usuario no esta en la sala.\n/carcel @nombre [minutos] (motivo opcional)\n/carcel @nombre 0 para liberar"
              )
          else:
            await self.highrise.chat(
                "\n/carcel @nombre [minutos] (motivo opcional)\n/carcel @nombre 0 para liberar\n/carcel liberar, para liberar a todos\n/carcel todos, para encarcelar a todos\n/carcel lista para ver la lista y tiempo restante"
            )
            await self.highrise.chat(
                "\n/carcel auto, activar o desactivar que entren automaticamente a la cárcel\n/setcarcel para establecer la posicion de la carcel"
            )

    if message.startswith("/setcarcel"):
      if user.username == owner_name or user.username in adminsList:
        room_users = (await self.highrise.get_room_users()).content
        user_id = user.id
        for usr, pos in room_users:  # Cambiado user a usr para evitar sobrescribir la variable user
          if usr.id == user_id:
            carcelPos = [pos.x, pos.y, pos.z]
            guardar = {'carcelPosSave': carcelPos}
            guardar_variables(guardar)
            await self.highrise.chat("Posicion de la cárcel actualizada. 👮")

    if "/bot sigueme" in message.lower():
      if user.username == owner_name or user.username in adminsList:
        nombreParaSeguir = user.username
        room_users = (await self.highrise.get_room_users()).content
        user_id = user.id
        for room_user, pos in room_users:  # Cambio de user a room_user
          if room_user.id == user_id:  # Acceder al ID de room_user en lugar de user
            if isinstance(pos,
                          Position):  # Verificar si pos es de tipo Position
              await self.highrise.walk_to(
                  Position(pos.x - 1, pos.y, pos.z - 1, pos.facing))
              return

    if "/bot stop" in message.lower():
      if user.username == owner_name or user.username in adminsList:
        nombreParaSeguir = ""

    if "/game" in message.lower():
      if not Game1Status:
        await self.highrise.chat("intenta adivinar el numero del 1 al 100!")
        Game1num = random.randint(1, 100)
        Game1Status = True
      else:
        await self.highrise.chat("Ya hay un juego en curso")

    if Game1Status == True and message.isdigit():

      respnump = int(message)
      cercania = abs(Game1num - respnump)
      if cercania <= 10:
        emoji = "🔥"
      else:
        emoji = "❄️"
      if Game1num == respnump:
        await self.highrise.chat(
            f"correcto @{user.username} el numero era {respnump} ✅")
        for i in range(3):
          await self.highrise.react("thumbs", user.id)
          await asyncio.sleep(0.4)

        Game1Status = False
      elif Game1num < respnump:
        await self.highrise.send_whisper(user.id, f"{respnump} 👇{emoji}")
      else:
        await self.highrise.send_whisper(user.id, f"{respnump} 👆{emoji}")

    if "/bot spawn" in message.lower():
      if user.username == owner_name or user.username in adminsList:
        room_users = (await self.highrise.get_room_users()).content
        user_id = user.id

        for room_user, pos in room_users:  # Cambio de user a room_user
          if room_user.id == user_id:  # Acceder al ID de room_user en lugar de user
            if isinstance(pos, Position):
              spawnPos = [pos.x, pos.y, pos.z, pos.facing]
              guardar = {'botspawnPosSave': spawnPos}
              caraAngulo = pos.facing
              guardar_variables(guardar)
              await self.highrise.teleport(
                  bot_id, Position(pos.x, pos.y, pos.z, pos.facing))
              await asyncio.sleep(0.5)
              await self.highrise.walk_to(
                  Position(pos.x, pos.y, pos.z, pos.facing))
              await self.highrise.chat("punto de spawn actualizado")
              return

    if any(message.lower().startswith(prefix)
           for prefix in ["/create tele", "!create tele"]):
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()
        if len(partes) >= 3:
          warp = partes[2].strip().lower()
          user_id = user.id
          room_users = (await self.highrise.get_room_users()).content
          for room_user, pos in room_users:
            if room_user.id == user_id:
              if isinstance(pos, Position):
                mipos = [pos.x, pos.y, pos.z]
                await enter_warp(self, room_id, warp, mipos, user_id)

              else:
                await self.highrise.send_whisper(
                    user_id, "no puedes crear un teleport sentado")
        else:
          await self.highrise.send_whisper(
              user.id,
              "usa /create tele [nombre] para crear un nuevo teleport")

    if any(message.lower().startswith(prefix)
           for prefix in ["/tele list", "!tele list"]):

      if room_id in warpsLista:
        name_list = [
            f"{entry['name']} [{entry['rol']}]"
            if entry['rol'] != 'user' else entry['name']
            for entry in warpsLista[room_id]
        ]
        name_str = "\n-".join(name_list)
        await self.highrise.send_whisper(user.id,
                                         f"lista teleports:\n-{name_str}")
      else:
        await self.highrise.send_whisper(
            user.id,
            f"Error: no hay teleports en esta sala\nusa /create tele [nombre] para crear un nuevo teleport"
        )

    if any(message.lower().startswith(prefix)
           for prefix in ["/vip list", "!vip list"]):
      if user.username == owner_name or user.username in adminsList:
        # Función para convertir segundos a días, horas, minutos y segundos
        if not vipList:
          await self.highrise.send_whisper(user.id, "no hay vips")
          return

        def convertir_tiempo(segundos):
          dias, segundos = divmod(segundos, 86400)
          horas, segundos = divmod(segundos, 3600)
          minutos, segundos = divmod(segundos, 60)
          return dias, horas, minutos, segundos
      # Dividir la lista de VIPs en bloques de 5 usuarios

        users_chunks = [
            list(vipList.items())[i:i + 5] for i in range(0, len(vipList), 5)
        ]
        # Enviar los mensajes de forma asincrónica
        for chunk in users_chunks:
          # Construir el mensaje para el grupo de usuarios
          messages = []
          for username, time_left in chunk:
            dias, horas, minutos, segundos = convertir_tiempo(time_left)
            message = f"{username} {dias}d {horas}h {minutos}m de vip"
            messages.append(message)
          # Unir todos los mensajes en un solo mensaje para enviar
          message = "\n".join(messages)
          # Enviar el mensaje al usuario actual
          await self.highrise.send_whisper(user.id, message)
          await asyncio.sleep(1)

    if any(message.lower().startswith(prefix)
           for prefix in ["/admin list", "!admin list"]):
      if user.username == owner_name or user.username in adminsList:
        # Verificar si hay administradores en la lista
        if not adminsList:
          await self.highrise.send_whisper(
              user.id, "No hay administradores en este momento.")
          return
        # Dividir la lista de administradores en bloques de 5 usuarios
        users_chunks = [
            adminsList[i:i + 5] for i in range(0, len(adminsList), 5)
        ]
        # Enviar los mensajes de forma asincrónica
        for chunk in users_chunks:
          # Construir el mensaje para el grupo de usuarios
          messages = [f"{username} es admin" for username in chunk]
          # Unir todos los mensajes en un solo mensaje para enviar
          message = "\n".join(messages)
          # Enviar el mensaje al usuario actual
          await self.highrise.send_whisper(user.id, message)
          await asyncio.sleep(1)

    if any(message.lower().startswith(prefix)
           for prefix in ["/role", "!role"]):
      if user.username == owner_name or user.username in adminsList:
        partes = message.split()
        user_id = user.id
        if len(partes) == 1:
          await self.highrise.send_whisper(
              user.id, "puedes dar rol a un usuario o a un teleport")
          await self.highrise.send_whisper(
              user.id,
              "usa:\n/role @usuario admin, para dar admin\n\n/role [nombre] vip [horas] usa 0 para dar vip permantente\n\n/role delete @usuario, para quitar rol"
          )
          await self.highrise.send_whisper(
              user.id,
              "usa:\n/role [teleport] [rol] para dar rol a un teleport\n\n/role delete [teleport] para quitar rol"
          )
          return
        if any(message.lower().startswith(prefix)
               for prefix in ["/role delete", "!role delete"]):
          if len(partes) <= 2:
            await self.highrise.send_whisper(
                user_id,
                "usa:\n/role delete [@usuario o teleport] quitar rol a un usuario o teleport"
            )
            return
          if len(partes) >= 3:
            name_warp = partes[2].strip()
            verificar = False
            print(name_warp)
            if "@" in name_warp:
              name_warp = name_warp.split("@")[1]
              print(name_warp)
              if name_warp in vipList:
                del vipList[name_warp]
                guardar = {'vipListSave': vipList}
                guardar_variables(guardar)
                await self.highrise.send_whisper(
                    user.id, f"@{name_warp} ya no es 'vip'")
                verificar = True
              if name_warp in adminsList:
                adminsList.remove(name_warp)
                guardar = {'adminsListSave': adminsList}
                guardar_variables(guardar)
                await self.highrise.send_whisper(
                    user.id, f"@{name_warp} ya no es 'admin'")
                verificar = True
              if not verificar:
                await self.highrise.send_whisper(
                    user.id, f"@{name_warp} no tiene ningun rol")
                verificar = True
            return
        parteUser = message.split("@")

        if len(parteUser) >= 2:
          if parteUser[1].strip():
            nombreUsuario = parteUser[1].strip().split()[0]
            if len(partes) >= 3:
              role = partes[2].strip()
              room_users = (await self.highrise.get_room_users()).content
              user_info = [(usr.username, usr.id) for usr, _ in room_users]
              user_names = [info[0] for info in user_info]
              if nombreUsuario in user_names:
                if owner_name != nombreUsuario:
                  if role.lower() in ["vip", "admin"]:
                    if role == "vip":
                      if len(partes) == 4:
                        tiempo = partes[3].strip().split()[0]
                        try:
                          tiempo = int(tiempo)
                          if tiempo >= 25:
                            tiempo = 24
                          segundos = tiempo * 3600
                          vipList[nombreUsuario] = segundos
                          guardar = {'vipListSave': vipList}
                          guardar_variables(guardar)
                          if tiempo == 0:
                            await self.highrise.send_whisper(
                                user_id,
                                f"'{nombreUsuario}' fue asignado al rol '{role}' permanentemente"
                            )
                          else:
                            await self.highrise.send_whisper(
                                user_id,
                                f"'{nombreUsuario}' fue asignado al rol '{role}' por {tiempo} horas"
                            )

                        except Exception:
                          await self.highrise.send_whisper(
                              user_id,
                              f"Error: no es un numero, ingresa el tiempo de vip en horas\n/role [nombre] vip [tiempo] usa 0 para dar vip permantente"
                          )

                      else:
                        await self.highrise.send_whisper(
                            user_id,
                            f"Error: ingresa el tiempo de vip en horas\n/role [nombre] vip [tiempo] usa 0 para dar vip permantente"
                        )
                    if role == "admin":
                      adminsList.append(nombreUsuario)
                      guardar = {'adminsListSave': adminsList}
                      guardar_variables(guardar)
                      await self.highrise.send_whisper(
                          user_id, f"@{nombreUsuario} ahora es admin")
                  else:
                    await self.highrise.send_whisper(
                        user_id,
                        f"Error: Rol '{role}' no válido. Use 'vip', 'admin'")
                else:
                  await self.highrise.send_whisper(
                      user_id,
                      f"Error: no puedes cambiar de rol al dueño de la sala")
              else:
                await self.highrise.send_whisper(
                    user.id,
                    f"Error: Usuario '{nombreUsuario}' no está en la sala")
            else:
              await self.highrise.send_whisper(
                  user.id, f"Error: falta rol\n/role @usuario [rol]")
          else:
            await self.highrise.send_whisper(
                user.id,
                "/role [nombre] [rol] (vip - admin) para dar un rol a un usuario"
            )
        else:
          if len(partes) >= 3:
            nombreWarp = partes[1].strip()

            if room_id in warpsLista:
              role = partes[2].strip()
              if any(
                  entry.get('name') == nombreWarp
                  for entry in warpsLista[room_id]):
                for warp in warpsLista[room_id]:
                  if warp['name'] == nombreWarp:
                    if role in ["vip", "admin", "user"]:
                      warp['rol'] = role  # Actualizar el rol del warp
                      guardar = {'teleportsSalas': warpsLista}
                      guardar_variables(guardar)
                      await self.highrise.send_whisper(
                          user_id,
                          f"Teleport '{nombreWarp}' asignado al rol '{role}'")

                    else:
                      await self.highrise.send_whisper(
                          user_id,
                          f"Error: Rol '{role}' no válido. Use 'vip', 'admin' o 'user'."
                      )
                    break

              else:
                await self.highrise.send_whisper(
                    user_id, f"Error: teleport '{nombreWarp}' no existe")
            else:
              await self.highrise.send_whisper(
                  user_id, f"Error: teleport '{nombreWarp}' no existe")
          else:
            await self.highrise.send_whisper(
                user_id, f"Error: falta rol\n/role [teleport] [rol]")
      else:
        await self.highrise.send_whisper(
            user.id, "/role [nombre] [rol] para dar un rol a un usuario")
        """"
        warp = partes[1].strip().lower()
        
        user_id = user.id
        room_users = (await self.highrise.get_room_users()).content
        for room_user, pos in room_users:
          if room_user.id == user_id:
            if isinstance(pos, Position):
              mipos = [pos.x, pos.y, pos.z]
              await enter_warp(self, room_id, warp, mipos, user_id)

          else:
            await self.highrise.send_whisper(
                user_id, "no puedes crear un teleport sentado")
  else:
    await self.highrise.send_whisper(
        user.id, "usa /settele [nombre] para crear un nuevo teleport") """

  #CHISTES

    if "bot cuentame un chiste" in message.lower(
    ) or "bot dime un chiste" in message.lower(
    ) or "bot cuéntame un chiste" in message.lower(
    ) or "/chiste" in message.lower() or "bot hazme reir" in message.lower():
      response = random.choice([
          "- Mamá, mamá, los spaghetti se están pegando. 😳 - Déjalos que se maten 😈",
          "Un pez le pregunta a otro pez: ¿qué hace tu mamá? 😳 Este le contesta: Nada 😐 ¿y la tuya qué hace? Nada también.😂",
          "Si se muere una pulga, ¿a dónde va? 😳 Al pulgatorio.😂",
          "A Juanito le dice la maestra: Juanito, ¿qué harías si te estuvieses ahogando en la piscina? 😳 Juanito le responde: Llorar para desahogarme profe 😎",
          "Hijo, me veo gorda, fea y vieja. ¿qué tengo? 😔 Mamá, tienes toda la razón 😂",
          "Camarero, ese filete tiene muchos nervios 🤨 -Pues normal, es la primera vez que se lo comen 😂",
          "Mi humor es tan negro que le disparaba la policia 😳",
          "Un marido le dice a su mujer: Apuesto a que no puedes decirme algo que me haga feliz y triste al mismo tiempo 😌 -Claro que si! tu pilin es más grande que la de tus hermanos 😎",
          "¿Qué hay que hacer para ampliar la libertad de una mujer? 🤔 ampliar la cocina! 😂 ok no me funen 😔",
          "Doctor, ¿qué me dijo antes? 🥺 ¿Géminis, Libra? 🤔 -Cáncer Andy cancer",
          "Mamá, mamá, el gato está malo 😔 -bueno lo apartas y te comes las patatas 🤗",
          "Papá, papá, en el colegio me pegan 😭 -Lo sé hijo, ya me enviaron el video de youtube 😂",
          "Una mujer se arrodilla a Orar: -Señor, si no puedo adelgazar, bendice a mis amigas con mucha comida y haz que engorden. Amén 😇",
          "Me acaba de picar una serpiente! 😫 - ¿Cobra? - No, gratis 😅",
          "Hola, ¿tienen libros para el cansancio? 🥺 - Sí, pero están agotados 😔",
          "– Doctor, me dan mucho miedo las multiplicaciones.\n- ¿Por?\n– Ayyyy!! 😱😖😖",
          "– Lo sentimos, pero está usted despedido.😤\n-Pero, ¿por qué?😭\n-Porque tarda mucho en entender las cosas.😠\n-Vale. ¿Pero puedo seguir viniendo a trabajar? 🥺",
          "– Vengo a presentar mi tesis. Se titula “Apatía, desgana y pereza en el marco de la sociedad actual 😊”.\nMuy bien. Adelante. Puede comenzar.🙂\nNo me apetece.😔\nBrillante.😲🤯",
          "Que ironía fue aquella vez que me golpearon con una enciclopedia y perdí el conocimiento.😔",
          "– ¿Señor por qué no se detuvo al escuchar las sirenas?🤨\n- Porque su canto conduce a los hombres a la muerte.🥺🥺\n- Sople aquí, por favor.🤦‍♂️",
          "– ¿Y tú qué haces?\nSoy deportista de alto rendimiento.😎\n¿En serio?😲\nSí, me rindo fácilmente 😌",
          "– ¿Cuál es su destino?🙂\nMi destino no está escrito aún.. Mi destino es un lienzo en blanco que estoy pintando con cada elección y acción que tomo a lo largo de mi vida..😌\nSeñor ¿quiere un boleto de tren o no?😡"
      ])

      await self.highrise.chat(response)

  async def on_channel(self, sender_id: str, message: str,
                       tags: set[str]) -> None:
    await self.highrise.chat(message)
    """En un mensaje de canal oculto."""

  #USUARIO SE MUEVE A UNA POSICION
  async def on_user_move(self, user: User,
                         pos: Position | AnchorPosition) -> None:
    """Cuando un usuario se mueve en la habitación."""
    if user.username == nombreParaSeguir:
      if isinstance(pos, Position):  # Verificar si pos es de tipo Position

        await self.highrise.walk_to(
            Position(pos.x - 1, pos.y, pos.z - 1, pos.facing))

  async def run(self, room_id, token):
    definitions = [BotDefinition(self, room_id, token)]
    await __main__.main(definitions)


if __name__ == "__main__":
  token = "2fd15dd284ce5693b5820e6321efa7f877a04e19548712a584069eab9027a83f"
  run(Bot().run(room_id, token))

#65b33f88449aa3006dcd6ac2 YOSK 17, 0, 6
#64b8b8b8687948e776bf90dc lola 7, 0, 11
#64b997ef387197bbedca3986   casa
#6477963ef8787721cd711bcd   casino
#64b9cbc2a20c4d5c6ee252d0   baño
#6529a9fc95b6e0782557a416 BAÑO cata
#64ad72cb1cd195ff48d8a58a eurus dragon
#6570b63088f31769aa73efbd casa hernan
#65879452025531dd793da4b1 casa hernan 2
#65de1ff75bd46d66746719a0
