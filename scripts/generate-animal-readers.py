#!/usr/bin/env python3
"""Generate 19 animal-themed decodable readers for remaining unused images."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "readers"

READERS = [
    # ── STAGE 2: CVC + early multi-letter ──
    {
        "slug": "010-cat-and-dog",
        "title": "Cat and Dog",
        "stage": 2,
        "after": 10,
        "animals": ["cat.png", "dog.png"],
        "warmup": "cat, dog, sit, run, big, fun, the, and, see",
        "story": """**Cat and Dog**

Cat is big. Dog is big too.

Cat sits on the mat. Dog sits on the rug.

Cat sees a bug. Dog sees the bug too.

Cat runs at the bug. Dog runs at the bug.

The bug is fast! The bug zips up.

Cat and Dog stop. No bug.

Cat looks at Dog. Dog looks at Cat.

"It is fun to run," says Cat.

"It is fun to run with you," says Dog.

Cat and Dog are pals.

The End.""",
        "talk": "1. Where does Cat sit? (On the mat.) 2. What do Cat and Dog chase? (A bug.) 3. Find CVC words. (cat, dog, sit, run, big, bug, fun, mat, rug, zip)",
    },
    {
        "slug": "011-the-pig-pen",
        "title": "The Pig Pen",
        "stage": 2,
        "after": 10,
        "animals": ["pig.png"],
        "warmup": "pig, pen, mud, big, dig, fun, run, jump, the",
        "story": """**The Pig Pen**

Pip is a pig. Pip is big and pink.

Pip lives in a pen. The pen has mud.

Pip digs in the mud. Pip digs and digs.

"Digging is fun!" says Pip.

A hen comes to the pen. "Can I dig in the mud too?" asks the hen.

"Yes!" says Pip. "Dig with me!"

The hen digs in the mud. Pip digs in the mud.

The pen is a big mud pit! Pip and the hen have fun.

At the end of the day, Pip is a happy pig. Mud is the best!

The End.""",
        "talk": "1. What is the pig's name? (Pip.) 2. What does Pip like to do? (Dig in mud.) 3. Who comes to join Pip? (A hen.)",
    },
    {
        "slug": "012-hen-and-duck",
        "title": "Hen and Duck",
        "stage": 2,
        "after": 13,
        "animals": ["hen.png", "duck.png"],
        "warmup": "hen, duck, egg, nest, pond, back, pick, sit, swim, quack",
        "story": """**Hen and Duck**

Hen has a nest. The nest has six eggs.

Hen sits on the eggs to keep them warm.

Duck lives in the pond. Duck can swim.

"Quack!" says Duck. "Come swim with me, Hen!"

"I cannot swim," says Hen. "I must sit on my eggs."

Duck gets out of the pond. Duck waddles to the nest.

"I will sit with you," says Duck.

Hen and Duck sit by the nest. The sun is warm.

"Thank you, Duck," says Hen. "You are a good pal."

"Quack!" says Duck.

The End.""",
        "talk": "1. Where does Hen sit? (On her nest with eggs.) 2. Where does Duck live? (In the pond.) 3. What does Duck do for Hen? (Sits with her.)",
    },
    {
        "slug": "013-the-fox-den",
        "title": "The Fox Den",
        "stage": 2,
        "after": 10,
        "animals": ["fox.png"],
        "warmup": "fox, den, red, run, fast, big, log, sit, the, his",
        "story": """**The Fox Den**

Flick is a red fox. Flick is fast.

Flick lives in a den. The den is under a big log.

Flick runs and runs. His red fur shines in the sun.

Flick sees a hen. The hen is by the pen.

"Can I get the hen?" Flick thinks.

But the hen is fast too! The hen runs to the pen.

Flick stops. "Not today," he says.

Flick goes back to his den. He sits on the log.

The sun sets. Flick the fox rests. Tomorrow is a new day.

The End.""",
        "talk": "1. What is the fox's name? (Flick.) 2. Where does Flick live? (In a den under a log.) 3. What color is Flick? (Red.)",
    },
    {
        "slug": "014-the-little-sheep",
        "title": "The Little Sheep",
        "stage": 2,
        "after": 15,
        "animals": ["sheep.png"],
        "warmup": "sheep, little, green, see, keep, sleep, deep, feel, need, tree",
        "story": """**The Little Sheep**

Shep is a little sheep. Shep is white and soft.

Shep lives in a green field. The field has tall grass and a big tree.

Shep likes to run. Shep likes to jump. But most of all, Shep likes to sleep under the big green tree.

One day, Shep cannot sleep. "I need a friend," Shep says.

Shep looks and looks. Shep sees a little bird in the tree.

"Will you be my friend?" asks Shep.

"Tweet! Yes!" says the bird.

Now Shep has a friend. Shep and the bird sleep under the big green tree.

The End.""",
        "talk": "1. What is the sheep's name? (Shep.) 2. Where does Shep sleep? (Under the big green tree.) 3. Who becomes Shep's friend? (A little bird.)",
    },
    {
        "slug": "015-the-snail-trail",
        "title": "The Snail Trail",
        "stage": 2,
        "after": 29,
        "animals": ["snail.png"],
        "warmup": "snail, trail, rain, sail, wait, slow, day, stay, play, way",
        "story": """**The Snail Trail**

Snappy is a snail. Snappy is very slow.

Snappy leaves a trail as he goes. The trail shines in the sun.

"Where are you going, Snappy?" asks a bug.

"I am going to the garden," says Snappy. "It is a long way."

"I can fly there!" says the bug. "It is fast!"

"I cannot fly," says Snappy. "But I can wait. Slow and steady, that is my way."

Snappy goes and goes. The sun is hot. The rain comes. Snappy keeps going.

At last, Snappy gets to the garden. The garden has big green plants and red flowers.

"It was a long trail," says Snappy. "But I made it!"

The End.""",
        "talk": "1. What is the snail's name? (Snappy.) 2. Where is Snappy going? (To the garden.) 3. What does Snappy say about being slow? (Slow and steady is his way.)",
    },
    {
        "slug": "016-the-shy-goat",
        "title": "The Shy Goat",
        "stage": 2,
        "after": 50,
        "animals": ["goat.png"],
        "warmup": "goat, shy, boat, float, road, soap, coat, toad, farm, barn",
        "story": """**The Shy Goat**

Greta is a goat. Greta lives on a farm.

Greta is shy. She does not play with the other goats. She stays by the old red barn.

One day, a storm comes. Rain falls and falls. The road turns to mud.

A little toad gets stuck in the mud! "Help!" cries the toad.

Greta sees the toad. She is shy, but she wants to help.

Greta steps into the mud. She puts her head down. The toad climbs onto Greta's back.

"Hold on!" says Greta. She walks out of the mud.

"Thank you, Greta!" says the toad. "You are so brave!"

The other goats see what Greta did. They cheer for her.

Greta is not so shy after that. She made a friend!

The End.""",
        "talk": "1. What is the goat's name? (Greta.) 2. Why doesn't Greta play with others? (She is shy.) 3. How does Greta help the toad? (She carries it out of the mud.)",
    },

    # ── STAGE 3: Silent E + vowel teams ──
    {
        "slug": "017-the-brave-mouse",
        "title": "The Brave Mouse",
        "stage": 3,
        "after": 13,
        "animals": ["mouse.png"],
        "warmup": "mouse, house, brave, cake, make, take, time, ride, home, safe",
        "story": """**The Brave Mouse**

Milo is a little mouse. He lives in a hole in the wall of a big house.

Milo is brave. He is not scared of the cat. He is not scared of the dog. But there is one thing Milo is scared of — the dark.

One night, the moon is hiding. The house is black. Milo hears a sound.

"Help! I am stuck!" It is a baby mouse, trapped in a box.

Milo takes a deep breath. "I can be brave," he says. "I must help."

Milo steps into the dark. He cannot see, but he can hear. He follows the sound.

Milo finds the box. He chews a hole in the side. The baby mouse slips out.

"Thank you!" says the baby mouse. "You saved me!"

Milo smiles. "I was scared too. But helping you made me brave."

From that night on, Milo is not scared of the dark. He knows he can be brave when it counts.

The End.""",
        "talk": "1. What is the mouse afraid of? (The dark.) 2. Who does Milo save? (A baby mouse.) 3. What makes Milo brave? (Helping someone in need.) Find silent E words.",
    },
    {
        "slug": "018-the-wise-snake",
        "title": "The Wise Snake",
        "stage": 3,
        "after": 13,
        "animals": ["snake.png"],
        "warmup": "snake, wise, make, take, time, slide, hide, safe, home, stone",
        "story": """**The Wise Snake**

Silas is a snake. Silas is old and wise. He lives under a flat stone by the lake.

The other animals come to Silas when they have a problem.

"Silas, the rain made my home wet!" cries a rabbit.

"Find a dry spot under the big oak tree," says Silas. "It is safe there."

"Silas, I cannot find food!" says a frog.

"Hop to the far side of the lake," says Silas. "There are bugs there."

One day, a fire comes to the grass. All the animals panic.

"Be calm," says Silas. "Slide to the lake. The water will keep us safe."

All the animals follow Silas to the lake. The fire stops at the water's edge.

"You saved us!" the animals cry.

"Wisdom is knowing what to do when things are hard," says Silas. "And you all knew to help each other."

The End.""",
        "talk": "1. Where does Silas live? (Under a flat stone by the lake.) 2. What problem faces all the animals? (A fire.) 3. How does Silas save everyone? (Leads them to the lake.)",
    },
    {
        "slug": "019-the-turtle-tale",
        "title": "The Turtle Tale",
        "stage": 3,
        "after": 47,
        "animals": ["turtle.png"],
        "warmup": "turtle, little, purple, circle, simple, gentle, start, far, farm, hard",
        "story": """**The Turtle Tale**

Tully is a turtle. Tully is old — very old. His shell is purple and green with circles all over.

Tully lives by a still pond. Every morning, he sits on his favorite rock and watches the world wake up.

The young turtles race around the pond. "Come race with us, Tully!" they call.

"I am too slow for racing," says Tully. "But I can tell you a story."

The young turtles gather around Tully's rock.

"Long ago," Tully begins, "this pond was just a little puddle. I was the first turtle here. I watched the pond grow. I watched the trees grow. I watched your parents grow up."

"Tell us more!" the young turtles beg.

Tully tells them about the great storm. About the time the pond froze solid. About the family of ducks that visits every spring.

When the tale ends, the sun is setting. The young turtles are quiet.

"Thank you, Tully," they whisper. "Your stories are better than any race."

Tully smiles and tucks into his shell. "Stories live longer than speed," he says.

The End.""",
        "talk": "1. How old is Tully? (Very old — he was the first turtle at the pond.) 2. What does Tully do instead of racing? (Tells stories.) 3. Find consonant+LE words. (turtle, little, purple, circle, simple, gentle, puddle)",
    },
    {
        "slug": "020-the-fast-horse",
        "title": "The Fast Horse",
        "stage": 3,
        "after": 13,
        "animals": ["horse.png"],
        "warmup": "horse, fast, race, more, before, ride, time, make, take, came",
        "story": """**The Fast Horse**

Storm is a black horse. Storm is the fastest horse on the farm.

Storm loves to run. When he runs, his mane flies in the wind. His hooves pound the ground like thunder.

One day, a man comes to the farm. "I need a fast horse," the man says. "There is a race. The winner gets a golden cup."

"Take Storm," says the farmer. "He is the fastest."

The day of the race comes. Storm stands at the starting line. Five other horses stand with him.

The horn sounds! They are off!

Storm runs and runs. The wind rushes past his ears. One horse pulls ahead. Then another.

But Storm does not give up. He runs with all his heart. Faster and faster.

At the finish line, Storm is not first. He is third.

The farmer pats Storm's neck. "You ran well," he says. "You did not give up."

Storm nickers. He did not win the golden cup. But he ran his best race. And that is enough.

The End.""",
        "talk": "1. What is the horse's name? (Storm.) 2. What place does Storm come in? (Third.) 3. What lesson does Storm learn? (Running your best is what matters.)",
    },
    {
        "slug": "021-the-white-whale",
        "title": "The White Whale",
        "stage": 3,
        "after": 35,
        "animals": ["whale.png"],
        "warmup": "whale, white, when, whole, while, deep, sea, great, shine, bright",
        "story": """**The White Whale**

Far out in the deep blue sea, there lives a white whale named Winter.

Winter is not like the other whales. While they are gray and black, Winter is pure white. She shines like a star in the dark water.

The other whales stare at Winter. "Why are you different?" they ask.

"I do not know," says Winter. "I was born this way."

Some whales are kind. Some are not. "You do not belong with us," a gray whale says.

Winter swims away. She feels sad and alone.

Then one day, a great storm comes. The water turns dark and rough. The whales cannot see where to go.

But they CAN see Winter! Her white body glows in the dark water like a light.

"Follow Winter!" the whales call. "She will lead us to safety!"

Winter leads the whole pod through the storm to calm water.

"You saved us!" the whales cry. "Your difference is your gift!"

Winter smiles. She was never meant to blend in. She was meant to shine.

The End.""",
        "talk": "1. Why is Winter different? (She is pure white, while other whales are gray/black.) 2. How does Winter save the pod? (Her white body glows in dark water, leading them.) 3. Find WH words. (whale, white, when, while, whole)",
    },
    {
        "slug": "022-the-eager-rabbit",
        "title": "The Eager Rabbit",
        "stage": 3,
        "after": 13,
        "animals": ["rabbit.png"],
        "warmup": "rabbit, eager, garden, carrot, hopping, running, waiting, happy, little, better",
        "story": """**The Eager Rabbit**

Ruby is a rabbit. Ruby is eager — she wants everything RIGHT NOW.

"Hurry up, sun! I want to play!" Ruby shouts at dawn.

"Hurry up, carrot! I want to eat!" Ruby shouts at the garden.

"Hurry up, friends! I want to race!" Ruby shouts at the other rabbits.

But the sun takes its time. The carrot grows slowly. And her friends are not as fast as Ruby.

One day, Ruby's mom says, "Ruby, sit with me. Watch the garden."

"But I want to run!" says Ruby.

"Just for a moment," says Mom. "Be still."

Ruby sits. At first, she is bored. But then she notices things she never saw before. A butterfly on a flower. A worm in the soil. The way the carrot tops wave in the breeze.

"This is nice," Ruby whispers.

"Some things are better when you wait," says Mom. "Even eager rabbits can learn to be patient."

The End.""",
        "talk": "1. What does Ruby want all the time? (Everything RIGHT NOW.) 2. What does Ruby notice when she sits still? (A butterfly, a worm, carrot tops waving.) 3. What lesson does Ruby learn? (Patience — some things are better when you wait.)",
    },

    # ── STAGE 4: Multi-syllable + morphology ──
    {
        "slug": "023-the-beaver-dam",
        "title": "The Beaver Dam",
        "stage": 4,
        "after": 10,
        "animals": ["beaver.png"],
        "warmup": "beaver, river, construction, building, family, together, stronger, underwater, amazing, protection",
        "story": """**The Beaver Dam**

Benny is a beaver. Benny lives by a rushing river with his family.

Every day, the beaver family works on their dam. They carry branches and mud. They stack logs with careful precision.

"Why do we build the dam?" asks Benny's little sister, Bella.

"To make a pond," says Benny. "The pond protects our home. Underwater, no wolf or bear can reach our lodge."

The construction is hard work. Benny's teeth are strong — perfect for cutting wood. He drags a heavy branch to the water's edge.

"Together!" calls Father Beaver. The whole family pushes the branch into place.

Day by day, the dam grows. The rushing river becomes a still, deep pond. Fish swim in the new water. Ducks land on the surface.

"Look what we built!" says Benny. "Working together, we transformed a river into a home."

The beaver family rests on their dam, proud of their creation.

The End.""",
        "talk": "1. Why do beavers build dams? (To create a pond that protects their home.) 2. How do they build it? (Together — carrying branches, mud, stacking logs.) 3. Find words with Latin roots. (construction, protection, family, creation)",
    },
    {
        "slug": "024-the-eagle-flight",
        "title": "The Eagle Flight",
        "stage": 4,
        "after": 10,
        "animals": ["eagle.png"],
        "warmup": "eagle, mountain, majestic, soaring, freedom, silence, magnificent, distance, vision, courage",
        "story": """**The Eagle Flight**

High above the mountain peaks, an eagle named Ember soars on the wind.

Ember has the most magnificent view in the world. From her height, she can see the curve of the earth. She can spot a mouse in the grass from a mile away.

Today is Ember's first solo flight. She has practiced with her mother for weeks. But now she is alone.

The wind is strong. Ember's wings tremble. "I can do this," she tells herself. "I was born to fly."

She spreads her wings wide. The wind lifts her. Higher and higher she climbs.

The world below becomes small. The river is a silver ribbon. The forest is a green carpet. The mountains are ancient guardians.

Ember lets out a cry — a wild, free sound that echoes across the valley.

This is freedom. This is flight. This is what she was made for.

When Ember returns to her nest at sunset, her mother nods with pride. "You are an eagle now."

The End.""",
        "talk": "1. What can Ember see from her height? (The curve of the earth, a mouse from a mile away.) 2. How does Ember feel on her first solo flight? (Nervous, then free.) 3. Find words with silent letters or advanced phonograms. (majestic=soft G, magnificent=soft C, guardians=AR→/er/)",
    },
    {
        "slug": "025-the-skunk-garden",
        "title": "The Skunk Garden",
        "stage": 4,
        "after": 30,
        "animals": ["skunk.png"],
        "warmup": "skunk, garden, protection, powerful, dangerous, respect, distance, nature, creature, understand",
        "story": """**The Skunk Garden**

Stella is a skunk. She has beautiful black and white fur and a fluffy tail. She also has a powerful secret — a scent that no animal wants to encounter.

Because of her secret, the other animals keep their distance. "Don't get too close to Stella!" they whisper.

Stella is lonely. She just wants to explore the garden like everyone else.

One evening, Stella notices something terrible. A fox is sneaking toward the rabbit den! The mama rabbit and her babies are in danger.

Stella doesn't hesitate. She runs toward the fox and raises her tail. The fox catches the warning and bolts away.

The mama rabbit comes out of her den. "You saved my babies," she says. "Thank you, Stella."

Word spreads through the garden. Stella is not dangerous — she is a protector!

From that night on, Stella tends the garden. She patrols at dusk, keeping the smaller creatures safe. Her secret power, once a source of loneliness, is now a gift she shares with everyone.

The End.""",
        "talk": "1. Why do animals avoid Stella? (Her powerful scent.) 2. How does Stella save the rabbits? (She scares away a fox.) 3. Find words with suffixes. (protection, powerful, dangerous, loneliness)",
    },
]

TMP = """# {title}

**Stage {stage}** · Decodable Reader · After Lesson {after}

{images}

## Warm-Up Words — Read These First

> {warmup}

---

## Story

{story}

---

## Think About It

{talk}

---

**Phonograms used:** {phonograms}
"""

def main():
    for r in READERS:
        imgs = r["animals"]
        img_lines = "\n\n".join(
            f"![{a.replace('.png','').replace('-',' ').title()}](images/animals/{a})"
            for a in imgs
        )
        content = TMP.format(
            title=r["title"], stage=r["stage"], after=r["after"],
            images=img_lines, warmup=r["warmup"],
            story=r["story"], talk=r["talk"],
            phonograms=r["warmup"].replace(",", ""),
        )
        (OUT / f"{r['slug']}.md").write_text(content, encoding="utf-8")
        print(f"  readers/{r['slug']}.md  [{r['animals']}]")

    print(f"\n{len(READERS)} readers generated")

if __name__ == "__main__":
    main()
