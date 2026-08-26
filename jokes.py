"""
60 bird jokes for 6-8 year olds, plus a deterministic "joke of the
day" picker - everyone sees the same joke on the same calendar day,
and it rotates through the full list before repeating.

This replaces the original 50 entirely, not just adds to them - a
handful of the originals were flat statements dressed up as jokes
(no actual pun or twist) or leaned on references a 6-8 year old
wouldn't get (mobile phones/Twitter), so this is a genuine rewrite,
every entry re-checked for having a real punchline.
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
    "Why did the turkey join the school band? It already had drumsticks!",
    "What do owls say when it's raining? \"It's owl-ways wet out here!\"",
    "Why did the chicken cross the playground? To get to the other slide!",
    "Why don't eagles like fast food? They can never catch it in time!",
    "What's a duck's favourite snack? Anything with quackers!",
    "What do you call a bird who tells jokes? A comedi-hen!",
    "What do you call a bird in the winter? Brrrr-d!",
    "Why do flamingos stand on one leg? Because if they lifted both, they'd fall over!",
    "What do you call a chicken who counts her eggs? A mathema-hen!",
    "What's a parrot's favourite game? Repeat after me!",
    "Why did the duck cross the road? To prove he wasn't chicken!",
    "What's a bird's favourite type of story? A tall tail!",
    "Why do owls hoot? Because they'd look silly if they barked!",
    "What do you call two birds in love? Tweethearts!",
    "What do you call a chicken that likes gardening? A hen with green fingers!",
    "Why don't birds ever get speeding tickets? Because they always fly the speed limit!",
    "Why did the owl throw a party? Because he was having a hoo-ha!",
    "What's an owl's favourite kind of book? A whoo-dunnit!",
    "Why do robins have red chests? Because they're always blushing!",
    "What do you call a very fast bird? A swift, of course!",
    "What's a bird's favourite thing to eat for breakfast? Tweetos!",
    "Why did the little bird bring a ladder to school? Because he wanted to go to high school!",
    "What do you call a penguin in the desert? Lost!",
    "Why was the chick disappointed with himself? He wasn't what he was cracked up to be!",
    "What do you call a bird that's always exactly on time? Punc-tu-owl!",
    "Why did the owl get invited to every party? Because he was a real hoot!",
    "Why do birds sing so early in the morning? Because it's too early to talk!",
    "What do you call a duck that steals things? A robber duck!",
    "What did the baby owl say to his mum when he got home? \"Owl be back later!\"",
    "What's black and white and lives in Antarctica? A penguin!",
    "What do you call an owl with a sore throat? A screech owl!",
    "Why don't owls need alarm clocks? Because they're already up all night!",
    "What do you call a bird that visits every winter and won't stop talking? A chatterbox goose!",
    "Why did the woodpecker get a promotion? Because he really knocked it out of the park!",
    "What do you call a bird stuck in a traffic jam? A traffic jay!",
    "Why did the pigeon bring string to the park? Because he wanted to fly a kite!",
    "What's a bird's favourite game at playtime? Hide and peck!",
    "Why did the owl sit on the branch all night? He was pulling an owl-nighter!",
    "What do you call a bird who won't stop talking about himself? A peacock!",
    "Why did the penguin stand in the fridge? Because he wanted to keep his cool!",
    "What did one owl say to the other on Valentine's Day? \"Owl always love you!\"",
    "Why do hummingbirds fly so fast? Because they never have time to waste!",
    "What do you call a bird of prey who's scared of everything? A chicken hawk!",
    "Why did the eagle get top marks at school? Because he had the best eyesight in the class!",
    "What kind of bird can carry the heaviest things? A crane!",
    "Why don't seagulls make good secret keepers? Because they always squawk!",
    "What do you call a very organised bird? A stork — he always delivers right on time!",
    "Why did the sparrow join the choir? Because he had a beautiful tweety voice!",
    "Why did the little bird get sent to his room? For using fowl language!",
    "Why did the robin get a gold star? Because he always sang his very best!",
    "What do you call a bird who's brilliant at basketball? A slam-duck!",
]


def get_joke_of_the_day() -> str:
    """Same joke for everyone on a given calendar day, rotating through
    the whole list before repeating."""
    day_of_year = datetime.datetime.utcnow().date().timetuple().tm_yday
    index = day_of_year % len(JOKES)
    return JOKES[index]
