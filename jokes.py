"""
50 bird jokes for 6-8 year olds, plus a deterministic "joke of the
day" picker - everyone sees the same joke on the same calendar day,
and it rotates through the full list before repeating.
"""
import datetime

JOKES = [
    "Why do hummingbirds hum? Because they don't know the words!",
    "What do you call a bird that's scared of everything? A chicken!",
    "Why do birds fly south for the winter? Because it's too far to walk!",
    "What did the owl say when he caught a mouse? \"Who's for dinner?\"",
    "Why did the bird go to the doctor? It had a fowl cough!",
    "What do you call a very rude bird? A mockingbird!",
    "Why don't seagulls fly over the bay? Then they'd be bagels!",
    "What's an owl's favourite subject at school? Owl-gebra!",
    "What do you call an owl who does magic tricks? Hoo-dini!",
    "Why do woodpeckers peck on wood? Because they can't peck on steel!",
    "What kind of bird can lift the heaviest things? A crane!",
    "Why did the turkey join the school band? It already had drumsticks!",
    "What do owls say when it's raining? \"It's owl-ways wet out here!\"",
    "Why did the chicken cross the playground? To get to the other slide!",
    "Why don't eagles like fast food? They can never catch it in time!",
    "What do you call a bird that's stuck in a doorway? A swallow who can't swallow!",
    "What's a duck's favourite snack? Anything with quackers!",
    "Why did the pelican get told off at the buffet? Because of his big bill!",
    "What do you call a bird who tells jokes? A comedi-hen!",
    "Why did the owl feel poorly? He had the tweets!",
    "What do you call a bird in the winter? Brrrr-d!",
    "What kind of bird works at a building site? A crane, obviously!",
    "Why do flamingos stand on one leg? Because if they lifted both, they'd fall over!",
    "What do you call a chicken who counts her eggs? A mathema-hen!",
    "Why did the little bird get an A on his test? Because he flew through it!",
    "What's a parrot's favourite game? Repeat after me!",
    "Why don't birds use mobile phones? Because they already have Twitter!",
    "What do you call an owl that's really good at maths? A wise owl, of course!",
    "Why did the duck cross the road? To prove he wasn't chicken!",
    "What's a bird's favourite type of story? A tall tail!",
    "Why did the robin sit on the TV? Because he wanted to watch the feather forecast!",
    "What do you call a duck that gets top marks in school? A wise quacker!",
    "Why do owls hoot? Because they'd look silly if they barked!",
    "What do you call two birds in love? Tweethearts!",
    "Why did the bird get told off in the library? Because it kept tweeting!",
    "What do you call a bird that's always cold? A brrrd of prey!",
    "Why don't owls ever get lost? Because they always know which way is which-way!",
    "What do you call a chicken that likes gardening? A hen with green fingers!",
    "Why did the sparrow apologise? Because he was tweeting sorry!",
    "What do you call a very clever bird? A wise owl!",
    "Why don't birds ever get speeding tickets? Because they always fly the speed limit!",
    "What's a bird's favourite kind of weather? Feather-friendly!",
    "What did the mother bird say to the naughty chick? \"Fly straight, young man!\"",
    "Why did the owl throw a party? Because he was having a hoo-ha!",
    "What's an owl's favourite kind of book? A whoo-dunnit!",
    "Why do robins have red chests? Because they're always blushing!",
    "What do you call a very fast bird? A swift, of course!",
    "What's a bird's favourite thing to eat for breakfast? Tweetos!",
    "Why did the little bird bring a ladder to school? Because he wanted to go to high school!",
    "What do you call a bird who's terrible at hide and seek? A cuckoo — it always gives itself away!",
]


def get_joke_of_the_day() -> str:
    """Same joke for everyone on a given calendar day, rotating through
    the whole list before repeating."""
    day_of_year = datetime.datetime.utcnow().date().timetuple().tm_yday
    index = day_of_year % len(JOKES)
    return JOKES[index]
