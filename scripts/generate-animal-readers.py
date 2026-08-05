#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate 19 animal-themed decodable readers for remaining unused images."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# Per-page Spelling Aid sidebar (issues #20, #22) — see framework/reader_sidebar.py
sys.path.insert(0, str(ROOT / "framework"))
from reader_sidebar import build_sidebar, split_into_pages  # noqa: E402
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

Cat sits on the mat. Dog sits on the rug. They are pals.

One day, Cat sees a bug on the mat. The bug has six legs and a hard back.

"Dog! Look!" says Cat.

Dog runs up. He sniffs. The bug zips away.

"It is on the rug now!" says Dog.

Cat and Dog tip-toe to the rug. They get set to run. Cat counts. "One… two…"

But the bug is gone. Up, up, up it goes. Out the window.

"Oh no!" says Cat. "Now we have no bug to run at."

Dog sits. "It is fun to run, even with no bug."

Cat grins. "It is fun to run with you, Dog."

Cat and Dog sit on the rug. The sun is warm. The mat is soft. And being pals is the best fun of all.

The End.""",
        "talk": "1. Where does Cat sit at first? (On the mat.) 2. Where does the bug go? (Out the window.) 3. Find CVC words. (cat, dog, sit, run, big, bug, fun, mat, rug, zip)",
    },
    {
        "slug": "011-the-pig-pen",
        "title": "The Pig Pen",
        "stage": 2,
        "after": 10,
        "animals": ["pig.png"],
        "warmup": "pig, pen, mud, big, dig, fun, run, jump, the",
        "story": """**The Pig Pen**

Pip is a pig. Pip is big and pink. Pip lives in a pen by the farm.

Pip digs in the mud. Pip digs and digs. The mud is wet and cool.

"Digging is fun!" says Pip.

But the mud is not just fun. The mud is hot in the sun. Pip sits in the mud to get cool. The mud keeps Pip from getting too hot.

A hen comes to the pen. "Can I sit in the mud too?" asks the hen. "I am hot."

"Yes!" says Pip. "Sit with me!"

The hen sits. Then a duck comes. Then a small pup.

"This is the best spot on the farm!" says Pip.

The sun goes down. The mud is cool. Pip and the hen and the duck and the pup are all pals.

Being in the pen is fun. Having pals is better.

The End.""",
        "talk": "1. What is the pig's name? (Pip.) 2. Why does Pip sit in the mud? (To get cool.) 3. Who comes to join Pip in the pen? (A hen, a duck, a pup.)",
    },
    {
        "slug": "012-hen-and-duck",
        "title": "Hen and Duck",
        "stage": 2,
        "after": 13,
        "animals": ["hen.png", "duck.png"],
        "warmup": "hen, duck, egg, nest, pond, back, pick, sit, swim, quack",
        "story": """**Hen and Duck**

Hen has a nest in the grass. The nest has six eggs. Hen sits on the eggs to keep them warm and safe.

Duck lives in the pond by the farm. Duck can swim and dive and splash.

"Quack!" says Duck. "Come swim with me, Hen! The water is fun!"

"I cannot swim," says Hen. "I must sit on my eggs."

Duck gets out of the pond. Duck waddles up the bank to the nest.

"I will sit with you," says Duck. "The sun is hot. I will help keep the eggs cool."

Hen and Duck sit by the nest. The wind blows. The grass sways.

Then — CRACK! A small egg has a crack.

A small wet chick pops out. It blinks. It peeps.

"Quack!" says Duck.

"Cluck!" says Hen.

The chick has two pals already.

The End.""",
        "talk": "1. Where does Hen sit? (On her nest with eggs.) 2. Where does Duck live? (In the pond.) 3. What hatches at the end? (A chick.)",
    },
    {
        "slug": "013-the-fox-den",
        "title": "The Fox Den",
        "stage": 2,
        "after": 10,
        "animals": ["fox.png"],
        "warmup": "fox, den, red, run, fast, big, log, sit, the, his",
        "story": """**The Fox Den**

Flick is a red fox. Flick has a den under a big log at the edge of the woods.

Flick is fast. His red fur shines in the sun. His feet are soft on the grass.

One day, Flick is hungry. He sniffs the wind. He smells a hen!

The hen is by the pen. Flick crouches low. He creeps up. He is so still.

Then — SNAP! Flick steps on a twig.

The hen looks up. "Cluck cluck!" She runs fast to the pen. The pen is shut.

Flick stops. "Not today," he says.

Flick goes back to his den. He curls up under the log. He is sad, but he is not cross.

Tomorrow, Flick will try again. Or he will find a bug. A bug is good too.

The sun sets. Flick the fox rests. Being safe in his den is fine.

The End.""",
        "talk": "1. What is the fox's name? (Flick.) 2. Where does Flick live? (In a den under a log.) 3. Why does Flick miss the hen? (He steps on a twig and she runs to the pen.)",
    },
    {
        "slug": "014-the-little-sheep",
        "title": "The Little Sheep",
        "stage": 2,
        "after": 15,
        "animals": ["sheep.png"],
        "warmup": "sheep, little, green, see, keep, sleep, deep, feel, need, tree",
        "story": """**The Little Sheep**

Shep is a little sheep. Shep has soft white wool and four small feet.

Shep lives in a green field. The field has tall green grass and a big green tree.

Shep likes to run. Shep likes to jump. But most of all, Shep likes to sleep in the deep shade of the big green tree.

One day, Shep cannot sleep. He feels sad.

"I need a friend," Shep says. "Sheep should not be alone."

Shep looks and looks. Then he sees a small bird up in the tree.

"Will you be my friend?" Shep calls up.

The bird flies down. "Tweet! Yes! I will keep you company."

Shep and the bird sleep in the deep grass under the tree.

Now Shep feels glad. Friends are what he did need.

The End.""",
        "talk": "1. What is the sheep's name? (Shep.) 2. Why does Shep feel sad? (He has no friend.) 3. Who becomes Shep's friend? (A little bird.)",
    },
    {
        "slug": "015-the-snail-trail",
        "title": "The Snail Trail",
        "stage": 2,
        "after": 29,
        "animals": ["snail.png"],
        "warmup": "snail, trail, rain, sail, wait, slow, day, stay, play, way",
        "story": """**The Snail Trail**

Snappy is a snail. Snappy is very slow. But Snappy is not sad about that.

Snappy leaves a thin trail as he goes. The trail shines in the sun like a small silver way.

"Where are you going, Snappy?" asks a bug on a leaf.

"I am going to the garden," says Snappy. "It is a long way."

"I can fly there in a day!" says the bug.

"I cannot fly," says Snappy. "But I can wait. Slow and steady, that is my way."

The bug flies off. Snappy starts on his way. Day by day, Snappy goes on. The sun is hot. The rain comes down. Snappy keeps on.

He does not stay in one spot. He does not wait too long. He just goes, slow and steady, every day.

At last, Snappy gets to the garden. The garden has big green plants and red flowers and a cool pond to stay by.

"It was a long trail," says Snappy. "But I made it. Slow and steady wins the day."

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

Greta is a goat. Greta lives on a farm with a red barn, a long road, and a small blue pond.

Greta is shy. She stays by the old barn. She does not play with the other goats on the green hill.

One day, a storm comes. Rain falls and falls. The road turns to mud.

A little toad hops down the road. His foot sticks in the mud! He can not get out!

"Help!" cries the toad. "I can not get loose!"

Greta sees the toad. She is shy, but she wants to help.

Greta walks down the road. She steps in the mud. She puts her head low.

"Jump on!" says Greta.

The toad jumps on Greta's back. Greta walks out of the mud.

"Thank you, Greta!" says the toad. "You are so brave!"

Greta walks the toad to the pond. The toad hops in, glad and clean.

The other goats on the hill see Greta. They come down. "Greta, you are brave! Come play with us!"

Greta smiles. Being brave makes pals.

The End.""",
        "talk": "1. What is the goat's name? (Greta.) 2. Why does Greta not play with others at first? (She is shy.) 3. How does Greta help the toad? (She carries it out of the mud on her back.)",
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

Because of her secret, the other animals keep their distance. "Do not get too close to Stella!" they whisper.

Stella is lonely. She just wants to explore the garden like everyone else.

One evening, Stella notices something terrible. A fox is sneaking toward the rabbit den! The mama rabbit and her babies are in danger.

Stella does not hesitate. She runs toward the fox and raises her tail. The fox catches the warning and bolts away.

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

{story_pages}

---

## Think About It

{talk}

---

**Phonograms used:** {phonograms}
"""

def _build_story_pages(r: dict) -> str:
    """Wrap the story in per-page <div class="reader-page"> blocks with sidebars.

    Issue #20 + #22: every page gets a Spelling Aid sidebar listing the
    phonograms + rules used on that page. Animal readers don't have a
    specific 'new' phonogram, so the sidebar is auto-detected per page.
    """
    story = r["story"]
    # Strip the "**Title**" header (it's redundant with the H1)
    lines = story.splitlines()
    if lines and lines[0].startswith("**") and lines[0].endswith("**"):
        lines = lines[1:]
    # Drop "The End." line (always last)
    story_body = "\n".join(lines).strip()
    if story_body.endswith("The End."):
        story_body = story_body[:-len("The End.")].strip()
    pages = split_into_pages(story_body, sentences_per_page=3)
    parts = []
    for page in pages:
        sidebar = build_sidebar(page, new_phonogram=None)
        parts.append(
            f'<div class="reader-page">\n\n'
            f'<div class="reader-text">\n\n{page}\n\n</div>\n\n'
            f'{sidebar}\n\n'
            f'</div>'
        )
    return "\n\n".join(parts)


def main():
    for r in READERS:
        imgs = r["animals"]
        img_lines = "\n\n".join(
            f"![{a.replace('.png','').replace('-',' ').title()}](images/animals/{a})"
            for a in imgs
        )
        # Build per-page story with sidebars
        r_with_pages = dict(r)
        r_with_pages["story_pages"] = _build_story_pages(r)
        r_with_pages["images"] = img_lines
        r_with_pages["phonograms"] = r["warmup"].replace(",", "")
        content = TMP.format(**r_with_pages)
        (OUT / f"{r['slug']}.md").write_text(content, encoding="utf-8")
        stage_dir = OUT / f"stage-{r['stage']}"
        stage_dir.mkdir(parents=True, exist_ok=True)
        (stage_dir / f"{r['slug']}.md").write_text(content, encoding="utf-8")
        print(f"  readers/{r['slug']}.md (+ readers/stage-{r['stage']}/)  [{r['animals']}]")

    print(f"\n{len(READERS)} readers generated")

if __name__ == "__main__":
    main()
