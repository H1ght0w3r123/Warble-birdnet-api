"""
34 bird jokes for 6-8 year olds, plus a deterministic "joke of the
day" picker - everyone sees the same joke on the same calendar day,
rotating through the whole list before repeating.

Each joke is stored as a separate setup/punchline pair (not one
combined string) so the app can show the setup first and only reveal
the punchline once tapped.
"""
import datetime

JOKES = [
    {"setup": "Why do hummingbirds hum?", "punchline": "Because they don't know the words!"},
    {"setup": "What do you call a bird that's scared of everything?", "punchline": "A chicken!"},
    {"setup": "Why do birds fly south for the winter?", "punchline": "Because it's too far to walk!"},
    {"setup": "Why did the bird go to the doctor?", "punchline": "It had a fowl cough!"},
    {"setup": "What do you call a very rude bird?", "punchline": "A mockingbird!"},
    {"setup": "Why don't seagulls fly over the bay?", "punchline": "Then they'd be bagels!"},
    {"setup": "What's an owl's favourite subject at school?", "punchline": "Owl-gebra!"},
    {"setup": "What do you call an owl who does magic tricks?", "punchline": "Hoo-dini!"},
    {"setup": "Why did the chicken cross the playground?", "punchline": "To get to the other slide!"},
    {"setup": "Why don't eagles like fast food?", "punchline": "They can never catch it in time!"},
    {"setup": "What's a duck's favourite snack?", "punchline": "Anything with quackers!"},
    {"setup": "What do you call a bird who tells jokes?", "punchline": "A comedi-hen!"},
    {"setup": "What do you call a bird in the winter?", "punchline": "Brrrr-d!"},
    {"setup": "Why do flamingos stand on one leg?", "punchline": "Because if they lifted both, they'd fall over!"},
    {"setup": "What do you call a chicken who counts her eggs?", "punchline": "A mathema-hen!"},
    {"setup": "What's a parrot's favourite game?", "punchline": "Repeat after me!"},
    {"setup": "Why did the duck cross the road?", "punchline": "To prove he wasn't chicken!"},
    {"setup": "Why do owls hoot?", "punchline": "Because they'd look silly if they barked!"},
    {"setup": "What do you call two birds in love?", "punchline": "Tweethearts!"},
    {"setup": "What's an owl's favourite kind of book?", "punchline": "A whoo-dunnit!"},
    {"setup": "Why did the little bird bring a ladder to school?", "punchline": "Because he wanted to go to high school!"},
    {"setup": "What do you call a penguin in the desert?", "punchline": "Lost!"},
    {"setup": "What do you call a bird that's always exactly on time?", "punchline": "Punc-tu-owl!"},
    {"setup": "Why did the owl get invited to every party?", "punchline": "Because he was a real hoot!"},
    {"setup": "What do you call a duck that steals things?", "punchline": "A robber duck!"},
    {"setup": "What did the baby owl say to his mum when he got home?", "punchline": "\"Owl be back later!\""},
    {"setup": "Why did the woodpecker get a promotion?", "punchline": "Because he really knocked it out of the park!"},
    {"setup": "Why did the owl sit on the branch all night?", "punchline": "He was pulling an owl-nighter!"},
    {"setup": "Why did the penguin stand in the fridge?", "punchline": "Because he wanted to keep his cool!"},
    {"setup": "What did one owl say to the other on Valentine's Day?", "punchline": "\"Owl always love you!\""},
    {"setup": "What do you call a bird of prey who's scared of everything?", "punchline": "A chicken hawk!"},
    {"setup": "What kind of bird can carry the heaviest things?", "punchline": "A crane!"},
    {"setup": "Why did the little bird get sent to his room?", "punchline": "For using fowl language!"},
    {"setup": "What do you call a bird who's brilliant at basketball?", "punchline": "A slam-duck!"},
]


def get_joke_of_the_day() -> dict:
    """Same joke for everyone on a given calendar day, rotating through
    the whole list before repeating. Returns {"setup": ..., "punchline": ...}."""
    day_of_year = datetime.datetime.utcnow().date().timetuple().tm_yday
    index = day_of_year % len(JOKES)
    return JOKES[index]
