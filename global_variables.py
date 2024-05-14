from highrise import (BaseBot, Item, Position, SessionMetadata, User)
from highrise.models import *
from F_guard_carg import *

tipstate = False
tiptimerestaurar = 0
tiptime = 0
tipcantidad = 0

adminsList = ["XhernanX", "x"]
owner_id = ""
bot_id = ""
room_id = "65879452025531dd793da4b1"
carcelAuto = False
carcelList = ""
owner_name = "x"
carcelList = {}
GlobalAnuncio = {}
nombreParaSeguir = ""
dancing_users = {}
warpsLista = {}
vipList = {}

BotemoteTimerest = 0
Botemotetime = 0
BotDanceBaile = "random"

Game1Status = False

listemotebot = {
    'emote-gangnam': 7.5,
    'emote-trampoline': 5,
    'dance-handsup': 22.5,
    'dance-orangejustice': 6.5,
    'dance-floss': 21.5,
    'dance-touch': 12,
    'emote-frollicking': 4
}

#emote-shrink emote-trampoline
listReset = {
    'heartfingers': {
        'id': 'emote-heartfingers',
        'tiempo': 3.5
    },
    'love': {
        'id': 'emote-hearteyes',
        'tiempo': 4.5
    },
    'kiss': {
        'id': 'emote-kiss',
        'tiempo': 2.5
    },
    'shy': {
        'id': 'emote-shy',
        'tiempo': 4
    },
    'cutey': {
        'id': 'emote-cutey',
        'tiempo': 2.5
    },
    'pose5': {
        'id': 'emote-pose5',
        'tiempo': 4
    },
    'pose3': {
        'id': 'emote-pose3',
        'tiempo': 4.5
    },
    'pose1': {
        'id': 'emote-pose1',
        'tiempo': 2.5
    },
    'pose8': {
        'id': 'emote-pose8',
        'tiempo': 4
    },
    'pose7': {
        'id': 'emote-pose7',
        'tiempo': 4.5
    },
    'frog': {
        'id': 'emote-frog',
        'tiempo': 14
    },
    'confused': {
        'id': 'emote-confused',
        'tiempo': 8
    },
    'hot': {
        'id': 'emote-hot',
        'tiempo': 3.5
    },
    'curtsy': {
        'id': 'emote-curtsy',
        'tiempo': 2
    },
    'bow': {
        'id': 'emote-bow',
        'tiempo': 2.5
    },
    'celebrate': {
        'id': 'emoji-celebrate',
        'tiempo': 3
    },
    'gagg': {
        'id': 'emoji-gagging',
        'tiempo': 5
    },
    'flex': {
        'id': 'emoji-flex',
        'tiempo': 1.5
    },
    'greedy': {
        'id': 'emote-greedy',
        'tiempo': 4
    },
    'cursing': {
        'id': 'emoji-cursing',
        'tiempo': 2
    },
    'lust': {
        'id': 'emote-lust',
        'tiempo': 4
    },
    'thumb': {
        'id': 'emoji-thumbsup',
        'tiempo': 2
    },
    'angry': {
        'id': 'emoji-angry',
        'tiempo': 5
    },
    'tired': {
        'id': 'emote-tired',
        'tiempo': 4
    },
    'wave': {
        'id': 'emote-wave',
        'tiempo': 2
    },
    'sad': {
        'id': 'emote-sad',
        'tiempo': 5
    },
    'fashion': {
        'id': 'emote-fashionista',
        'tiempo': 5
    },
    'zombie': {
        'id': 'emote-zombierun',
        'tiempo': 9
    },
    'weird': {
        'id': 'dance-weird',
        'tiempo': 21
    },
    'superpose': {
        'id': 'emote-superpose',
        'tiempo': 4
    },
    'energy': {
        'id': 'emote-energyball',
        'tiempo': 7
    },
    'maniac': {
        'id': 'emote-maniac',
        'tiempo': 4
    },
    'sword': {
        'id': 'emote-swordfight',
        'tiempo': 5
    },
    'teleport': {
        'id': 'emote-teleporting',
        'tiempo': 11
    },
    'float': {
        'id': 'emote-float',
        'tiempo': 8
    },
    'teleki': {
        'id': 'idle-emote-telekinesis',
        'tiempo': 10
    },
    'enth': {
        'id': 'idle-enthusiastic',
        'tiempo': 15
    },
    'charging': {
        'id': 'emote-charging',
        'tiempo': 8
    },
    'angel': {
        'id': 'emote-snowangel',
        'tiempo': 5.5
    },
    'penny': {
        'id': 'dance-pennywise',
        'tiempo': 0.5
    },
    'model': {
        'id': 'emote-model',
        'tiempo': 6
    },
    'icecream': {
        'id': 'dance-icecream',
        'tiempo': 14
    },
    'wrong': {
        'id': 'dance-wrong',
        'tiempo': 12
    },
    'punk': {
        'id': 'emote-punkguitar',
        'tiempo': 8
    },
    'guitar': {
        'id': 'idle-guitar',
        'tiempo': 12
    },
    'sayso': {
        'id': 'idle-dance-tiktok4',
        'tiempo': 15
    },
    'casual': {
        'id': 'idle-dance-casual',
        'tiempo': 9
    },
    'tik10': {
        'id': 'dance-tiktok10',
        'tiempo': 8
    },
    'tik9': {
        'id': 'dance-tiktok9',
        'tiempo': 11
    },
    'sing': {
        'id': 'idle_singing',
        'tiempo': 10.5
    },
    'snake': {
        'id': 'emote-snake',
        'tiempo': 5
    },
    'shop': {
        'id': 'dance-shoppingcart',
        'tiempo': 4
    },
    'russian': {
        'id': 'dance-russian',
        'tiempo': 10
    },
    'tik2': {
        'id': 'dance-tiktok2',
        'tiempo': 10
    },
    'bp': {
        'id': 'dance-blackpink',
        'tiempo': 6
    },
    'stargazer': {
        'id': 'emote-stargazer',
        'tiempo': 6
    },
    'tik8': {
        'id': 'dance-tiktok8',
        'tiempo': 10
    },
    'pingui': {
        'id': 'dance-pinguin',
        'tiempo': 11
    },
    'timejump': {
        'id': 'emote-timejump',
        'tiempo': 4
    },
    'skating': {
        'id': 'emote-iceskating',
        'tiempo': 8
    },
    'anime': {
        'id': 'dance-anime',
        'tiempo': 8
    },
    'shy2': {
        'id': 'emote-shy2',
        'tiempo': 5
    },
    'gotta': {
        'id': 'idle-toilet',
        'tiempo': 20
    },
    'hyped': {
        'id': 'emote-hyped',
        'tiempo': 8
    },
    'sleigh': {
        'id': 'emote-sleigh',
        'tiempo': 13
    },
    'jingle': {
        'id': 'dance-jinglebell',
        'tiempo': 10
    },
    'creepycute': {
        'id': 'emote-creepycute',
        'tiempo': 7
    },
    'creepy': {
        'id': 'dance-creepypuppet',
        'tiempo': 7
    },
    'repose': {
        'id': 'sit-relaxed',
        'tiempo': 30
    },
    'boxer': {
        'id': 'emote-boxer',
        'tiempo': 5
    },
    'nervous': {
        'id': 'idle-nervous',
        'tiempo': 15
    },
    'astronaut': {
        'id': 'emote-astronaut',
        'tiempo': 14
    },
    'scritchy': {
        'id': 'idle-wild',
        'tiempo': 26
    },
    'kawai': {
        'id': 'dance-kawai',
        'tiempo': 10
    },
    'touch': {
        'id': 'dance-touch',
        'tiempo': 12
    },
    'kissing': {
        'id': 'emote-kissing-bound',
        'tiempo': 6.5
    },
    'foryou': {
        'id': 'emote-gift',
        'tiempo': 5
    },
    'cutesalute': {
        'id': 'emote-cutesalute',
        'tiempo': 3
    },
    'cute': {
        'id': 'emote-cute',
        'tiempo': 6
    },
    'tiktok': {
        'id': 'dance-tiktok11',
        'tiempo': 9
    },
    'minijump': {
        'id': 'emote-pose6',
        'tiempo': 6
    },
    'boom': {
        'id': 'emote-headblowup',
        'tiempo': 12
    },
    'arabesque': {
        'id': 'emote-pose10',
        'tiempo': 4
    },
    'jump': {
        'id': 'emote-celebrate',
        'tiempo': 4
    },
    'pushit': {
        'id': 'dance-employee',
        'tiempo': 6.5
    },
    'salute': {
        'id': 'emote-salute',
        'tiempo': 3
    },
    'launch': {
        'id': 'emote-launch',
        'tiempo': 8
    },
    'bigjump': {
        'id': 'emote-celebrationstep',
        'tiempo': 3
    }
}


def enter_user_list(user_id, user_emote, emote_tiempo):
  dancing_users[user_id] = {
      "emote": user_emote,
      "status": True,
      "tiempo": emote_tiempo
  }


def enter_user_carcel(user_id, tiempo_var, userName):
  global carcelList
  carcelList[user_id] = {"tiempo": tiempo_var, "nombre": userName}


class Emote:
  name: str
  id: str
  duration: float
  is_free: bool

  def __init__(self, name: str, id: str, duration: float, is_free: bool):
    self.name = name
    self.id = id
    self.duration = duration
    self.is_free = is_free


def emoteObtener(nombre: str):
  for emote in emotes:
    if emote.name.lower() == nombre:
      return emote.id, emote.duration
  return None, None


emotes: list[Emote] = [
    Emote(name="Rest", id="sit-idle-cute", duration=17.062613, is_free=False),
    Emote(name="Zombie", id="idle_zombie", duration=28.754937, is_free=False),
    Emote(name="Relaxed",
          id="idle_layingdown2",
          duration=21.546653,
          is_free=False),
    Emote(name="Attentive",
          id="idle_layingdown",
          duration=24.585168,
          is_free=False),
    Emote(name="Sleepy", id="idle-sleep", duration=22.620446, is_free=False),
    Emote(name="Pouty Face", id="idle-sad", duration=24.377214, is_free=False),
    Emote(name="Posh", id="idle-posh", duration=21.851256, is_free=False),
    Emote(name="Sleepy",
          id="idle-loop-tired",
          duration=21.959007,
          is_free=False),
    Emote(name="Tap Loop",
          id="idle-loop-tapdance",
          duration=6.261593,
          is_free=False),
    Emote(name="Sit",
          id="idle-loop-sitfloor",
          duration=22.321055,
          is_free=True),
    Emote(name="Shy", id="idle-loop-shy", duration=16.47449, is_free=False),
    Emote(name="Bummed", id="idle-loop-sad", duration=6.052999, is_free=False),
    Emote(name="Chillin",
          id="idle-loop-happy",
          duration=18.798322,
          is_free=False),
    Emote(name="Annoyed",
          id="idle-loop-annoyed",
          duration=17.058522,
          is_free=False),
    Emote(name="Aerobics",
          id="idle-loop-aerobics",
          duration=8.507535,
          is_free=False),
    Emote(name="Ponder", id="idle-lookup", duration=22.339865, is_free=False),
    Emote(name="Hero Pose", id="idle-hero", duration=21.877099, is_free=False),
    Emote(name="Relaxing",
          id="idle-floorsleeping2",
          duration=17.253372,
          is_free=False),
    Emote(name="Cozy Nap",
          id="idle-floorsleeping",
          duration=13.935264,
          is_free=False),
    Emote(name="Enthused",
          id="idle-enthusiastic",
          duration=15.941537,
          is_free=True),
    Emote(name="Boogie Swing",
          id="idle-dance-swinging",
          duration=13.198551,
          is_free=False),
    Emote(name="Feel The Beat",
          id="idle-dance-headbobbing",
          duration=25.367458,
          is_free=False),
    Emote(name="Irritated", id="idle-angry", duration=25.427848,
          is_free=False),
    Emote(name="Yes", id="emote-yes", duration=2.565001, is_free=True),
    Emote(name="I Believe I Can Fly",
          id="emote-wings",
          duration=13.134487,
          is_free=False),
    Emote(name="The Wave", id="emote-wave", duration=2.690873, is_free=True),
    Emote(name="Tired", id="emote-tired", duration=4.61063, is_free=True),
    Emote(name="Think", id="emote-think", duration=3.691104, is_free=False),
    Emote(name="Theatrical",
          id="emote-theatrical",
          duration=8.591869,
          is_free=False),
    Emote(name="Tap Dance",
          id="emote-tapdance",
          duration=11.057294,
          is_free=False),
    Emote(name="Super Run",
          id="emote-superrun",
          duration=6.273226,
          is_free=False),
    Emote(name="Super Punch",
          id="emote-superpunch",
          duration=3.751054,
          is_free=False),
    Emote(name="Sumo Fight",
          id="emote-sumo",
          duration=10.868834,
          is_free=False),
    Emote(name="Thumb Suck",
          id="emote-suckthumb",
          duration=4.185944,
          is_free=False),
    Emote(name="Splits Drop",
          id="emote-splitsdrop",
          duration=4.46931,
          is_free=False),
    Emote(name="Snowball Fight!",
          id="emote-snowball",
          duration=5.230467,
          is_free=True),
    Emote(name="Snow Angel",
          id="emote-snowangel",
          duration=6.218627,
          is_free=True),
    Emote(name="Shy", id="emote-shy", duration=4.477567, is_free=True),
    Emote(name="Secret Handshake",
          id="emote-secrethandshake",
          duration=3.879024,
          is_free=False),
    Emote(name="Sad", id="emote-sad", duration=5.411073, is_free=True),
    Emote(name="Rope Pull",
          id="emote-ropepull",
          duration=8.769656,
          is_free=False),
    Emote(name="Roll", id="emote-roll", duration=3.560517, is_free=False),
    Emote(name="ROFL!", id="emote-rofl", duration=6.314731, is_free=False),
    Emote(name="Robot", id="emote-robot", duration=7.607362, is_free=False),
    Emote(name="Rainbow", id="emote-rainbow", duration=2.813373,
          is_free=False),
    Emote(name="Proposing",
          id="emote-proposing",
          duration=4.27888,
          is_free=False),
    Emote(name="Peekaboo!",
          id="emote-peekaboo",
          duration=3.629867,
          is_free=False),
    Emote(name="Peace", id="emote-peace", duration=5.755004, is_free=False),
    Emote(name="Panic", id="emote-panic", duration=2.850966, is_free=False),
    Emote(name="No", id="emote-no", duration=2.703034, is_free=True),
    Emote(name="Ninja Run",
          id="emote-ninjarun",
          duration=4.754721,
          is_free=False),
    Emote(name="Night Fever",
          id="emote-nightfever",
          duration=5.488424,
          is_free=False),
    Emote(name="Monster Fail",
          id="emote-monster_fail",
          duration=4.632708,
          is_free=False),
    Emote(name="Model", id="emote-model", duration=6.490173, is_free=True),
    Emote(name="Flirty Wave", id="emote-lust", duration=4.655965,
          is_free=True),
    Emote(name="Level Up!", id="emote-levelup", duration=6.0545,
          is_free=False),
    Emote(name="Amused",
          id="emote-laughing2",
          duration=5.056641,
          is_free=False),
    Emote(name="Laugh", id="emote-laughing", duration=2.69161, is_free=True),
    Emote(name="Kiss", id="emote-kiss", duration=2.387175, is_free=True),
    Emote(name="Super Kick",
          id="emote-kicking",
          duration=4.867992,
          is_free=False),
    Emote(name="Jump", id="emote-jumpb", duration=3.584234, is_free=False),
    Emote(name="Judo Chop",
          id="emote-judochop",
          duration=2.427442,
          is_free=False),
    Emote(name="Imaginary Jetpack",
          id="emote-jetpack",
          duration=16.759457,
          is_free=False),
    Emote(name="Hug Yourself",
          id="emote-hugyourself",
          duration=4.992751,
          is_free=False),
    Emote(name="Sweating", id="emote-hot", duration=4.353037, is_free=True),
    Emote(name="Hero Entrance",
          id="emote-hero",
          duration=4.996096,
          is_free=False),
    Emote(name="Hello", id="emote-hello", duration=2.734844, is_free=True),
    Emote(name="Headball",
          id="emote-headball",
          duration=10.073119,
          is_free=False),
    Emote(name="Harlem Shake",
          id="emote-harlemshake",
          duration=13.558597,
          is_free=False),
    Emote(name="Happy", id="emote-happy", duration=3.483462, is_free=False),
    Emote(name="Handstand",
          id="emote-handstand",
          duration=4.015678,
          is_free=False),
    Emote(name="Greedy Emote",
          id="emote-greedy",
          duration=4.639828,
          is_free=True),
    Emote(name="Graceful", id="emote-graceful", duration=3.7498,
          is_free=False),
    Emote(name="Moonwalk",
          id="emote-gordonshuffle",
          duration=8.052307,
          is_free=False),
    Emote(name="Ghost Float",
          id="emote-ghost-idle",
          duration=19.570492,
          is_free=False),
    Emote(name="Gangnam Style",
          id="emote-gangnam",
          duration=7.275486,
          is_free=False),
    Emote(name="Frolic ",
          id="emote-frollicking",
          duration=3.700665,
          is_free=False),
    Emote(name="Faint", id="emote-fainting", duration=18.423499,
          is_free=False),
    Emote(name="Clumsy", id="emote-fail2", duration=6.475972, is_free=False),
    Emote(name="Fall", id="emote-fail1", duration=5.617942, is_free=False),
    Emote(name="Face Palm",
          id="emote-exasperatedb",
          duration=2.722748,
          is_free=True),
    Emote(name="Exasperated",
          id="emote-exasperated",
          duration=2.367483,
          is_free=False),
    Emote(name="Elbow Bump",
          id="emote-elbowbump",
          duration=3.799768,
          is_free=False),
    Emote(name="Disco", id="emote-disco", duration=5.366973, is_free=False),
    Emote(name="Blast Off",
          id="emote-disappear",
          duration=6.195985,
          is_free=False),
    Emote(name="Faint Drop",
          id="emote-deathdrop",
          duration=3.762728,
          is_free=False),
    Emote(name="Collapse", id="emote-death2", duration=4.855549,
          is_free=False),
    Emote(name="Revival", id="emote-death", duration=6.615967, is_free=False),
    Emote(name="Dab", id="emote-dab", duration=2.717871, is_free=False),
    Emote(name="Curtsy", id="emote-curtsy", duration=2.425714, is_free=True),
    Emote(name="Confusion",
          id="emote-confused",
          duration=8.578827,
          is_free=True),
    Emote(name="Cold", id="emote-cold", duration=3.664348, is_free=False),
    Emote(name="Charging",
          id="emote-charging",
          duration=8.025079,
          is_free=True),
    Emote(name="Bunny Hop",
          id="emote-bunnyhop",
          duration=12.380685,
          is_free=False),
    Emote(name="Bow", id="emote-bow", duration=3.344036, is_free=True),
    Emote(name="Boo", id="emote-boo", duration=4.501502, is_free=False),
    Emote(name="Home Run!",
          id="emote-baseball",
          duration=7.254841,
          is_free=False),
    Emote(name="Falling Apart",
          id="emote-apart",
          duration=4.809542,
          is_free=False),
    Emote(name="Thumbs Up",
          id="emoji-thumbsup",
          duration=2.702369,
          is_free=True),
    Emote(name="Point", id="emoji-there", duration=2.059095, is_free=False),
    Emote(name="Sneeze", id="emoji-sneeze", duration=2.996694, is_free=False),
    Emote(name="Smirk", id="emoji-smirking", duration=4.823158, is_free=False),
    Emote(name="Sick", id="emoji-sick", duration=5.070367, is_free=False),
    Emote(name="Gasp", id="emoji-scared", duration=3.008487, is_free=False),
    Emote(name="Punch", id="emoji-punch", duration=1.755783, is_free=False),
    Emote(name="Pray", id="emoji-pray", duration=4.503179, is_free=False),
    Emote(name="Stinky", id="emoji-poop", duration=4.795735, is_free=False),
    Emote(name="Naughty", id="emoji-naughty", duration=4.277602,
          is_free=False),
    Emote(name="Mind Blown",
          id="emoji-mind-blown",
          duration=2.397167,
          is_free=False),
    Emote(name="Lying", id="emoji-lying", duration=6.313748, is_free=False),
    Emote(name="Levitate", id="emoji-halo", duration=5.837754, is_free=False),
    Emote(name="Fireball Lunge",
          id="emoji-hadoken",
          duration=2.723709,
          is_free=False),
    Emote(name="Give Up", id="emoji-give-up", duration=5.407888,
          is_free=False),
    Emote(name="Tummy Ache",
          id="emoji-gagging",
          duration=5.500202,
          is_free=True),
    Emote(name="Flex", id="emoji-flex", duration=2.099351, is_free=True),
    Emote(name="Stunned", id="emoji-dizzy", duration=4.053049, is_free=False),
    Emote(name="Cursing Emote",
          id="emoji-cursing",
          duration=2.382069,
          is_free=True),
    Emote(name="Sob", id="emoji-crying", duration=3.696499, is_free=False),
    Emote(name="Clap", id="emoji-clapping", duration=2.161757, is_free=False),
    Emote(name="Raise The Roof",
          id="emoji-celebrate",
          duration=3.412258,
          is_free=True),
    Emote(name="Arrogance",
          id="emoji-arrogance",
          duration=6.869441,
          is_free=False),
    Emote(name="Angry", id="emoji-angry", duration=5.760023, is_free=True),
    Emote(name="Vogue Hands",
          id="dance-voguehands",
          duration=9.150634,
          is_free=False),
    Emote(name="Savage Dance",
          id="dance-tiktok8",
          duration=10.938702,
          is_free=True),
    Emote(name="Don't Start Now",
          id="dance-tiktok2",
          duration=10.392353,
          is_free=True),
    Emote(name="Yoga Flow",
          id="dance-spiritual",
          duration=15.795092,
          is_free=False),
    Emote(name="Smoothwalk",
          id="dance-smoothwalk",
          duration=6.690023,
          is_free=False),
    Emote(name="Ring on It",
          id="dance-singleladies",
          duration=21.191372,
          is_free=False),
    Emote(name="Let's Go Shopping",
          id="dance-shoppingcart",
          duration=4.316035,
          is_free=True),
    Emote(name="Russian Dance",
          id="dance-russian",
          duration=10.252905,
          is_free=True),
    Emote(name="Robotic",
          id="dance-robotic",
          duration=17.814959,
          is_free=False),
    Emote(name="Penny's Dance",
          id="dance-pennywise",
          duration=1.214349,
          is_free=True),
    Emote(name="Orange Juice Dance",
          id="dance-orangejustice",
          duration=6.475263,
          is_free=False),
    Emote(name="Rock Out", id="dance-metal", duration=15.076377,
          is_free=False),
    Emote(name="Karate",
          id="dance-martial-artist",
          duration=13.284405,
          is_free=False),
    Emote(name="Macarena",
          id="dance-macarena",
          duration=12.214141,
          is_free=True),
    Emote(name="Hands in the Air",
          id="dance-handsup",
          duration=22.283413,
          is_free=False),
    Emote(name="Floss", id="dance-floss", duration=21.329661, is_free=False),
    Emote(name="Duck Walk",
          id="dance-duckwalk",
          duration=11.748784,
          is_free=False),
    Emote(name="Breakdance",
          id="dance-breakdance",
          duration=17.623849,
          is_free=False),
    Emote(name="K-Pop Dance",
          id="dance-blackpink",
          duration=7.150958,
          is_free=True),
    Emote(name="Push Ups",
          id="dance-aerobics",
          duration=8.796402,
          is_free=False),
    Emote(name="Hyped", id="emote-hyped", duration=7.492423, is_free=True),
    Emote(name="Jinglebell", id="dance-jinglebell", duration=11, is_free=True),
    Emote(name="Nervous", id="idle-nervous", duration=21.714221, is_free=True),
    Emote(name="Toilet", id="idle-toilet", duration=32.174447, is_free=True),
    Emote(name="Attention",
          id="emote-attention",
          duration=4.401206,
          is_free=False),
    Emote(name="Astronaut",
          id="emote-astronaut",
          duration=13.791175,
          is_free=True),
    Emote(name="Dance Zombie",
          id="dance-zombie",
          duration=12.922772,
          is_free=True),
    Emote(name="Ghost", id="emoji-ghost", duration=3.472759, is_free=False),
    Emote(name="Heart Eyes",
          id="emote-hearteyes",
          duration=4.034386,
          is_free=True),
    Emote(name="Swordfight",
          id="emote-swordfight",
          duration=5.914365,
          is_free=True),
    Emote(name="TimeJump",
          id="emote-timejump",
          duration=4.007305,
          is_free=True),
    Emote(name="Snake", id="emote-snake", duration=5.262578, is_free=True),
    Emote(name="Heart Fingers",
          id="emote-heartfingers",
          duration=4.001974,
          is_free=True),
    Emote(name="Heart Shape",
          id="emote-heartshape",
          duration=6.232394,
          is_free=False),
    Emote(name="Hug", id="emote-hug", duration=3.503262, is_free=False),
    Emote(name="Laugh", id="emote-lagughing", duration=1.125537,
          is_free=False),
    Emote(name="Eyeroll", id="emoji-eyeroll", duration=3.020264,
          is_free=False),
    Emote(name="Embarrassed",
          id="emote-embarrassed",
          duration=7.414283,
          is_free=False),
    Emote(name="Float", id="emote-float", duration=8.995302, is_free=True),
    Emote(name="Telekinesis",
          id="emote-telekinesis",
          duration=10.492032,
          is_free=True),
    Emote(name="Sexy dance", id="dance-sexy", duration=12.30883,
          is_free=False),
    Emote(name="Puppet", id="emote-puppet", duration=16.325823, is_free=False),
    Emote(name="Fighter idle",
          id="idle-fighter",
          duration=17.19123,
          is_free=False),
    Emote(name="Penguin dance",
          id="dance-pinguin",
          duration=11.58291,
          is_free=True),
    Emote(name="Creepy puppet",
          id="dance-creepypuppet",
          duration=6.416121,
          is_free=True),
    Emote(name="Sleigh", id="emote-sleigh", duration=11.333165, is_free=True),
    Emote(name="Maniac", id="emote-maniac", duration=4.906886, is_free=True),
    Emote(name="Energy Ball",
          id="emote-energyball",
          duration=7.575354,
          is_free=True),
    Emote(name="Singing", id="idle_singing", duration=10.260182, is_free=True),
    Emote(name="Frog", id="emote-frog", duration=14.55257, is_free=True),
    Emote(name="Superpose",
          id="emote-superpose",
          duration=4.530791,
          is_free=True),
    Emote(name="Cute", id="emote-cute", duration=6.170464, is_free=True),
    Emote(name="TikTok Dance 9",
          id="dance-tiktok9",
          duration=11.892918,
          is_free=True),
    Emote(name="Weird Dance",
          id="dance-weird",
          duration=21.556237,
          is_free=True),
    Emote(name="TikTok Dance 10",
          id="dance-tiktok10",
          duration=8.225648,
          is_free=True),
    Emote(name="Pose 7", id="emote-pose7", duration=4.655283, is_free=True),
    Emote(name="Pose 8", id="emote-pose8", duration=4.808806, is_free=True),
    Emote(name="Casual Dance",
          id="idle-dance-casual",
          duration=9.079756,
          is_free=True),
    Emote(name="Pose 1", id="emote-pose1", duration=2.825795, is_free=True),
    Emote(name="Pose 3", id="emote-pose3", duration=5.10562, is_free=True),
    Emote(name="Pose 5", id="emote-pose5", duration=4.621532, is_free=True),
    Emote(name="Cutey", id="emote-cutey", duration=3.26032, is_free=True),
    Emote(name="Punk Guitar",
          id="emote-punkguitar",
          duration=9.365807,
          is_free=True),
    Emote(name="Zombie Run",
          id="emote-zombierun",
          duration=9.182984,
          is_free=False),
    Emote(name="Fashionista",
          id="emote-fashionista",
          duration=5.606485,
          is_free=True),
    Emote(name="Gravity", id="emote-gravity", duration=8.955966, is_free=True),
    Emote(name="Ice Cream Dance",
          id="dance-icecream",
          duration=14.769573,
          is_free=True),
    Emote(name="Wrong Dance",
          id="dance-wrong",
          duration=12.422389,
          is_free=True),
    Emote(name="UwU", id="idle-uwu", duration=24.761968, is_free=True),
    Emote(name="TikTok Dance 4",
          id="idle-dance-tiktok4",
          duration=15.500708,
          is_free=True),
    Emote(name="Advanced Shy",
          id="emote-shy2",
          duration=4.989278,
          is_free=True),
    Emote(name="Anime Dance", id="dance-anime", duration=8.46671,
          is_free=True),
    Emote(name="Kawaii", id="dance-kawai", duration=10.290789, is_free=True),
    Emote(name="Scritchy", id="idle-wild", duration=26.422824, is_free=True),
    Emote(name="Ice Skating",
          id="emote-iceskating",
          duration=7.299156,
          is_free=True),
    Emote(name="SurpriseBig",
          id="emote-pose6",
          duration=5.375124,
          is_free=True),
    Emote(name="Celebration Step",
          id="emote-celebrationstep",
          duration=3.353703,
          is_free=True),
    Emote(name="Creepycute",
          id="emote-creepycute",
          duration=7.902453,
          is_free=True),
    Emote(name="Frustrated",
          id="emote-frustrated",
          duration=5.584622,
          is_free=False),
    Emote(name="Pose 10", id="emote-pose10", duration=3.989871, is_free=True),
    Emote(name="Relaxed", id="sit-relaxed", duration=29.889858, is_free=False),
    Emote(name="Laid Back", id="sit-open", duration=26.025963, is_free=False),
    Emote(name="Star gazing",
          id="emote-stargaze",
          duration=1.127464,
          is_free=False),
    Emote(name="Slap", id="emote-slap", duration=2.724945, is_free=False),
    Emote(name="Boxer", id="emote-boxer", duration=5.555702, is_free=True),
    Emote(name="Head Blowup",
          id="emote-headblowup",
          duration=11.667537,
          is_free=True),
    Emote(name="KawaiiGoGo", id="emote-kawaiigogo", duration=10,
          is_free=False),
    Emote(name="Repose", id="emote-repose", duration=1.118455, is_free=False),
    Emote(name="Tiktok7",
          id="idle-dance-tiktok7",
          duration=12.956484,
          is_free=False),
    Emote(name="Shrink", id="emote-shrink", duration=8.738784, is_free=False),
    Emote(name="Ditzy Pose", id="emote-pose9", duration=4.583117,
          is_free=True),
    Emote(name="Teleporting",
          id="emote-teleporting",
          duration=11.7676,
          is_free=True),
    Emote(name="Touch", id="dance-touch", duration=11.7, is_free=True),
    Emote(name="Air Guitar",
          id="idle-guitar",
          duration=13.229398,
          is_free=True),
    Emote(name="This Is For You", id="emote-gift", duration=5.8, is_free=True),
    Emote(name="Push it", id="dance-employee", duration=8, is_free=True),
    Emote(name="Sweet Smooch", id="emote-kissing", duration=5, is_free=False),
    Emote(name="Wop Dance", id="dance-tiktok11", duration=11, is_free=True),
    Emote(name="Cute Salute", id="emote-cutesalute", duration=3, is_free=True),
    Emote(name="At Attention", id="emote-salute", duration=3, is_free=True),
]
