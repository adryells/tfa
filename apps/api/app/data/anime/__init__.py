from faker import Faker
from pydantic import BaseModel


class AnimeData(BaseModel):
    name: str
    synopsis: str
    num_episodes: int
    average_ep_duration: int


fake = Faker()


two_piece = AnimeData(
    name="Two Piece",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)

xaruto = AnimeData(
    name="Xaruto",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)

dragon_ballers = AnimeData(
    name="Dragon Ballers",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)


bleaching = AnimeData(
    name="Bleaching",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)

superdoze = AnimeData(
    name="Super Doze",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)

killua_stories = AnimeData(
    name="Killua Stories",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)

lifenote = AnimeData(
    name="Lifenote",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)

ten_laws = AnimeData(
    name="Ten laws",
    synopsis=fake.text(),
    num_episodes=fake.pyint(min_value=4, max_value=60),
    average_ep_duration=fake.pyint(min_value=300, max_value=2000)
)


animes = [
    two_piece,
    xaruto,
    dragon_ballers,
    killua_stories,
    bleaching,
    superdoze,
    lifenote,
    ten_laws
]
