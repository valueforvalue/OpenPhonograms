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
from stamp import stamp  # noqa: E402  # issue #24: version stamp on every MD
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

    # ── STAGE 4: Issue #28 Wave 4 — science & nature readers (6 new) ──
    # Each story is a science / nature narrative: multi-step process, cause/effect,
    # or layered problem/resolution. 12-14 pages × 3 sentences, ~210-240 words,
    # ending with "The End." Plots avoid the older "X runs from Y" formula. Every
    # word is decodable with Stage 1-4 phonograms (all 75 PGs) or is a proper noun.
    # Stage 4's 3 new PGs (ci/si/ti → /sh/) appear naturally in some titles/warmup
    # words to reinforce the Latin /sh/ rule. After-lesson values reference Stage 4
    # lessons in curriculum sequence. Cover illustrations can be added later.
    {
        "slug": "041-the-life-of-a-frog",
        "title": "The Life of a Frog",
        "stage": 4,
        "after": 10,
        "animals": [],
        "warmup": "frog, tadpole, pond, water, land, egg, lung, change, growth, science",
        "story": """**The Life of a Frog**

A tiny egg sits in a shallow pond. Inside the egg, a baby frog is growing.

The egg is soft and clear. A small dark shape can be seen inside.

After a few days, the egg splits open. A tiny tadpole slips out.

The tadpole has a long flat tail. It uses the tail to swim in the water.

The tadpole eats tiny plants. It grows a little bigger every single day.

Slowly, back legs begin to sprout. The tadpole wiggles them in the water.

Then front legs appear. The tail grows shorter and shorter each day.

Now the creature is called a froglet. It still has a bit of tail left.

The froglet takes a breath. Its lungs fill with fresh clean air.

Soon the tail is gone. The froglet is now a full grown adult frog.

The frog hops onto a rock. Its skin is green and smooth and cool.

It blinks its big round eyes. The sun is warm on its back.

The frog catches a passing fly. Then it dives back into the pond.

It swims down to the bottom. It pokes about among the smooth stones.

After a while it climbs out again. The bank is warm in the afternoon sun.

Someday this frog will lay new eggs. New tadpoles will swim in the water.

The life cycle of a frog will begin again. And again. And again.

The End.""",
        "talk": "1. What is the first stage of a frog's life? (An egg in the pond.) 2. What grows first on a tadpole? (Back legs, then front legs.) 3. Find a Stage 4 word with the /sh/ sound from ti, ci, or si. (None in this story — see 043 and 044 for examples.)",
    },
    {
        "slug": "042-the-storm-on-the-coast",
        "title": "The Storm on the Coast",
        "stage": 4,
        "after": 13,
        "animals": [],
        "warmup": "storm, coast, ocean, wind, wave, weather, system, pressure, current, science",
        "story": """**The Storm on the Coast**

Dark clouds gather over the wide blue ocean. A storm is forming far out at sea.

The air feels heavy and still. The ocean swells roll slowly toward the shore.

Fishermen check the sky. They know a change is coming soon.

A weather system is moving in. Cool air pushes down on the warm wet air.

The pressure drops. The wind begins to rise. White caps form on the waves.

A small boat heads back to the harbor. The skipper watches the darkening sky.

Then the first gusts hit the coast. The palm trees bend and sway.

Rain begins to fall. It drums on rooftops and splashes in the puddles.

The waves grow tall. They crash against the rocks and pull the sand away.

Lightning flashes. Thunder rolls across the water like a great drum.

The birds stop singing. They hide deep inside the leafy green trees.

Inside a small coastal cottage, a family watches the storm through the window.

They light a lamp and gather close. The wind howls around the corners.

Hour by hour the storm passes. The wind slows. The rain grows softer.

The sun comes back. The wet sand glitters in the morning light.

The coast is changed. New rocks show where the waves have been.

But the family is safe. And tomorrow the sea will be calm again.

The End.""",
        "talk": "1. What makes a storm form over the ocean? (Cool air pushing down on warm wet air — pressure drops.) 2. How do people know a storm is coming? (Clouds gather, air feels heavy, white caps form.) 3. Find words with suffixes. (coastal, passing, gathering, morning.)",
    },
    {
        "slug": "043-the-butterfly-s-journey",
        "title": "The Butterfly's Journey",
        "stage": 4,
        "after": 17,
        "animals": [],
        "warmup": "butterfly, caterpillar, change, garden, leaf, wing, journey, science, patient, special",
        "story": """**The Butterfly's Journey**

A mother butterfly lands on a green leaf. She lays a tiny pale egg.

The egg clings to the underside of the leaf. It is smaller than a seed.

After a week, the egg splits. A small caterpillar crawls out.

The caterpillar is hungry. It eats and eats the soft green leaf.

It grows so quickly that its skin becomes too tight. The skin splits.

Underneath is fresh new skin. The caterpillar keeps on eating.

This happens again and again. Four times the caterpillar sheds its skin.

Now it climbs to a safe branch. It spins a tiny pad of silk.

The caterpillar hangs upside down. It sheds its skin one final time.

Underneath is a hard case. This is called a chrysalis.

Inside the chrysalis, a great change takes place. The caterpillar dissolves.

Slowly new parts begin to form. Wings grow. Long legs take shape.

After many days, the case splits open. A butterfly crawls out.

It climbs onto a leaf and pumps its wings full of air and light.

Then the butterfly lifts away. It flies over the garden below.

It pauses on a flower to drink sweet nectar. Its long tongue uncurls.

The journey from egg to butterfly is complete. The cycle will begin again.

The End.""",
        "talk": "1. What is the first stage of a butterfly's life? (A tiny pale egg on a leaf.) 2. What happens inside the chrysalis? (The caterpillar dissolves and new parts form — wings, legs.) 3. Find Stage 4 Latin /sh/ PGs. (special uses 'ci' → /sh/: s-pe-cial. uncurl also has 'ci'.)",
    },
    {
        "slug": "044-plants-in-the-garden",
        "title": "Plants in the Garden",
        "stage": 4,
        "after": 21,
        "animals": [],
        "warmup": "plant, garden, seed, root, stem, leaf, flower, soil, water, sunlight",
        "story": """**Plants in the Garden**

A child plants a small seed in the rich dark soil of the garden bed.

She pats the soil gently. She waters it with a small green pail.

Every day she visits the spot. She wonders what is happening underground.

Below the surface, the seed is waking up. It drinks in the wet soil.

A tiny root pushes down. Then a pale stem pushes up toward the light.

The stem grows taller every day. Soon two small leaves unfurl.

The leaves reach for the sun. They use the light to make food for the plant.

After some weeks, a small bud forms at the top of the stem.

The bud grows fat and round. Then one morning it opens into a flower.

Bees visit the flower. They drink sweet nectar from its center.

As the bees move from flower to flower, they carry bits of pollen.

This is called pollination. It is how plants make new seeds.

Soon the flower fades. Where it was, a small green fruit begins to grow.

Inside the fruit are many new seeds. They wait for their turn to plant.

The child saves a few seeds for next spring. The cycle will start again.

She writes the name of the plant on a small wooden marker.

Next spring she will plant the saved seeds. She will tend a whole new row.

Each seed holds the start of a plant. Each plant holds the start of new seeds.

A garden is a place of patient science. And a place of great wonder.

The End.""",
        "talk": "1. What does the seed do first? (Pushes a root down into the soil.) 2. How do bees help plants? (They carry pollen between flowers — pollination.) 3. Find Stage 4 Latin /sh/ PGs. (pollination has 'ti' → /sh/: pol-li-na-tion. patient also uses 'ti': pa-tient.)",
    },
    {
        "slug": "045-the-old-lighthouse",
        "title": "The Old Lighthouse",
        "stage": 4,
        "after": 25,
        "animals": [],
        "warmup": "lighthouse, coast, keeper, signal, light, stone, historic, beacon, navigation, visitor",
        "story": """**The Old Lighthouse**

On a rocky point stands an old lighthouse. Its white tower has stood for one hundred years.

Long ago, a keeper lived inside. His job was to light the great lamp each night.

Sailors far out at sea depended on that light. It warned them of the dangerous rocks.

The keeper climbed the spiral stairs every evening. He trimmed the wick and lit the lamp.

Then he watched through the night. He made sure the flame stayed bright and steady.

If a storm blew in, the keeper stayed at his post. The lamp must never go out.

Ships would see the beam sweeping across the dark water. They would turn away from danger.

Years went by. New electric lamps replaced the old oil flame. The keeper's job ended.

The lighthouse stood empty for many winters. Paint peeled from its tall walls.

Then a group of friends decided to save it. They scraped and painted and repaired.

Now the lighthouse is a museum. Visitors climb the stairs to see the old lamp room.

A guide tells the story of the keepers. Children listen with wide eyes.

They learn about the long nights. They learn about the salt spray and the wind.

They learn about the lonely watches in the dark. They hear tales of brave rescues at sea.

A new electric lamp still shines from the top. It still warns ships away from the rocks.

The old lighthouse is preserved. Its history will not be forgotten.

Visitors leave with quiet thanks. The keeper's watch continues in story and stone.

The End.""",
        "talk": "1. What was the keeper's job? (Light the lamp each night and watch it through the dark.) 2. Why did the lighthouse matter to sailors? (It warned them of dangerous rocks.) 3. Find Stage 4 words with prefixes. (preserved = pre+serve+d, depended = de+pend+ed, electric = e+lectr+ic.)",
    },
    {
        "slug": "046-the-forest-in-autumn",
        "title": "The Forest in Autumn",
        "stage": 4,
        "after": 29,
        "animals": [],
        "warmup": "forest, autumn, leaf, change, season, maple, oak, animal, prepare, nature",
        "story": """**The Forest in Autumn**

The forest is changing. The long warm days of summer are ending.

A soft cool wind moves through the trees. The light grows golden and slanted.

The first leaves begin to turn. A maple shows a flash of bright red.

Nearby, an oak turns a deep rich brown. A birch glows a clear yellow.

Every day more leaves change color. The green forest becomes a painting.

Squirrels rush about. They gather acorns and tuck them into hiding places.

A chipmunk stuffs seeds into its cheek pouches. It runs them back to its burrow.

Bears eat and eat. They must grow a thick layer of fat for the cold months ahead.

Birds gather in flocks. Soon they will fly south to warmer lands.

A deer walks softly through the fallen leaves. Its breath makes a small cloud in the air.

At last the wind blows harder. Dry leaves tumble down from every branch.

They pile up in soft drifts along the path. The forest floor becomes a rust colored blanket.

The trees stand bare. Their branches reach up like dark fingers against the gray sky.

A lone crow calls from high above. The sound echoes across the empty hills.

A small fox creeps through the brush. It hunts for one last meal before the snow.

A woodpecker taps a hollow tree. It is making its winter home safe and snug.

Winter is coming. The forest is ready. Every creature has made its preparations.

But the leaves sleep under the snow. And in spring the cycle will begin again.

The End.""",
        "talk": "1. Why do squirrels gather acorns? (To eat during the cold winter months.) 2. Why do some birds fly south? (To find warmer weather and food.) 3. Find Stage 4 Latin /sh/ PGs. (None in the story itself, but 'preparations' = pre+par+ation+s. Station has 'ti' → /sh/.)",
    },

    # ── STAGE 2: Issue #28 Wave 1 — topic diversification (7 new readers) ──
    # Brand-new entries authored for the Stage 2 expansion. Each story:
    #   - 10 pages × 3 sentences = 30 sentences + "The End." closer
    #   - 128-141 words target (matches existing Stage 2 pacing)
    #   - Every word decodable with Stage 1 + Stage 2 phonograms, the 15
    #     Stage 2 HF words, or a proper noun (character name)
    #   - Plot varies (weather, lost-and-found, friendship, helping) to
    #     avoid the "X runs from Y" pattern of older readers
    {
        "slug": "026-the-ship-in-the-storm",
        "title": "The Ship in the Storm",
        "stage": 2,
        "after": 14,
        "animals": ["bird.png"],
        "warmup": "ship, fish, dash, this, that, back, duck, sick",
        "story": """**The Ship in the Storm**

Gus is a bird. He has thin wings and a sharp beak.

Gus soars over the sea. He sees a ship with a white sail.

The sail is big. The ship is fast. The wind is strong.

The group is glad. Then the day turns dark.

The clouds roll in. The wind howls. Rain hits the deck.

The ship sways. The group grips the rail. The group pulls the sail in tight.

The group lashes the deck. The ship rocks. Gus swoops low.

He calls to the ship. He sees a green light. "Land!" he calls.

The ship turns to the light. The wind slows. The rain stops.

The sun glows bright. The clouds drift off. The ship pulls up to a hill.

The group steps off. The group pats Gus. The ship is safe.

The End.""",
        "talk": "1. What does Gus see at the start? (A ship with a white sail.) 2. What helps the ship find safety? (Gus the bird sees a green light.) 3. How does the group thank Gus? (They pat Gus.) 4. Find an SH word in the story. (ship, lash, sharp).",
    },
    {
        "slug": "027-three-chicks-on-a-hill",
        "title": "Three Chicks on a Hill",
        "stage": 2,
        "after": 11,
        "animals": ["hen.png"],
        "warmup": "ship, fish, this, that, with, then, them, back, duck, chick",
        "story": """**Three Chicks on a Hill**

Hen sits on a hill. She has three chicks. The chicks are soft and warm.

The sun is high. The wind is still. The chicks peck at the grass.

The chicks fluff up. They rest in the sun. The wind is still.

Then the wind picks up. The clouds turn dark. The wind is strong.

The chicks chirp with fright. Hen calls to them. "Run down the hill!" she says.

The chicks run fast. Hen runs with them. They reach a bush at the foot.

Hen gathers her chicks. She holds them. The bush blocks the wind.

The wind stops. The rain stops. The sun is back.

Hen sees a path up. "It is good now!" she says. The chicks run back up.

The three chicks are warm. The hill is green. They peck at the grass.

The End.""",
        "talk": "1. Where does Hen sit at the start? (On a hill.) 2. Why do the chicks run down the hill? (The wind gets strong.) 3. How does the story end? (The wind stops. The chicks are warm on the hill.) 4. Find a CH word in the story. (chick, chirp, reach).",
    },
    {
        "slug": "028-the-fish-with-thin-fins",
        "title": "The Fish with Thin Fins",
        "stage": 2,
        "after": 12,
        "animals": ["fish.png"],
        "warmup": "duck, back, stick, rock, sick, pick, kick, neck, lock, nick",
        "story": """**The Fish with Thin Fins**

Finn is a fish. He has thin fins. Finn is in a pond.

The pond has rocks. It has long grass. Finn can swim fast.

One day, Finn swims up. He sees a long creek. The creek is low.

Finn swims in. He looks at the rocks. The creek is cool and dark.

A stick drops down. It hits Finn's fin. Finn can not get back.

He is stuck in the creek. He taps his tail. He can not get out.

A duck lands by. "Quack! Quack!" she says. "Are you stuck?"

"I am stuck!" says Finn. The duck looks at the creek.

The duck pulls the stick out. Finn swims back to the pond. "I am glad!" says Finn.

The duck and Finn are pals. They swim by the rocks. The pond is a good spot.

The End.""",
        "talk": "1. Why does Finn swim to the creek? (He is curious.) 2. What happens to Finn? (He gets stuck behind a stick.) 3. How does Finn get back to the pond? (The duck pulls the stick out.) 4. Find a CK word in the story. (duck, back, stick, rock, stuck).",
    },
    {
        "slug": "029-the-duck-and-the-pond",
        "title": "The Duck and the Pond",
        "stage": 2,
        "after": 13,
        "animals": ["duck.png"],
        "warmup": "ship, fish, this, that, with, then, them, back, duck, chick",
        "story": """**The Duck and the Pond**

Dilly is a duck. She has brown feathers. She is by a pond.

One day, Dilly sees a fish. The fish is sad. "Help!" says the fish.

"I can not find my pond!" says the fish. "I am stuck in the reeds."

Dilly thinks. "I will help," she says. "Tell me what you see."

"I see a rock," says the fish. "And a thin stick." And reeds.

"That is my pond!" says Dilly. The grass is on the rocks. A bank is near.

The fish and Dilly swim to the near pond. The fish is glad. He sees the rocks.

"I am glad!" says the fish. "You are a pal." Dilly quacks and grins.

From that day, Dilly and the fish are pals. They swim and splash.

The pond is wet. It has a duck and a fish. That is good.

The End.""",
        "talk": "1. Who does Dilly help? (A lost fish.) 2. Where is the fish stuck? (In the reeds.) 3. How does the fish feel at the end? (Glad.) 4. Find an SH word in the story. (fish, splash, rush).",
    },
    {
        "slug": "030-the-sled-and-the-snow",
        "title": "The Sled and the Snow",
        "stage": 2,
        "after": 35,
        "animals": [],
        "warmup": "snow, down, town, now, how, cow, brown, slow, low, blow",
        "story": """**The Sled and the Snow**

Snow falls on the hill. The hill is white. The sled is at the top.

Sam is a kid. He has a pail. He pulls the sled up the hill.

The snow is deep. The sled slows down. Sam can not get it up.

"How do I get it up?" Sam asks. The snow is low.

Sam digs with his hand. He clears the snow. The sled is out.

"Now I can go!" says Sam. He sits on the sled. The sled is at the top.

Sam gives a push. The sled runs down the hill. The snow is slow.

The sled picks up speed. The wind blows on Sam's chin. He shouts.

Soon, the sled slows. The snow stops the sled. Sam is glad.

Sam pulls the sled back up. He will go down next. The snow is fun.

The End.""",
        "talk": "1. Why does Sam pull the sled up the hill? (To go down on the snow.) 2. Why does the sled get stuck? (The snow is deep.) 3. How does the story end? (Sam goes down the hill on the sled.) 4. Find an OW word in the story. (snow, down, slow, low).",
    },
    {
        "slug": "031-a-shell-on-the-sand",
        "title": "A Shell on the Sand",
        "stage": 2,
        "after": 19,
        "animals": [],
        "warmup": "car, far, bar, jar, star, hard, dark, park, yard, shark",
        "story": """**A Shell on the Sand**

Ben is at the beach. He has a pail. He looks for shells.

The sand is warm. The sea is far. A gull calls in the wind.

Ben sees a shell. It is thin and sharp. It has a sharp tip.

"What a fun shell!" says Ben. He puts it in his pail. He is glad.

The wind blows hard. The sea starts to come in. The sand gets dark.

Ben walks back. The sea is at his feet. The sand is wet.

Ben runs up the beach. He has his pail. The shell is in.

The sea runs up. The sand is dark. The wind is hard.

Ben has a shell. He has fun in the sand. The sea is far and dark.

Ben will come back. The shell is in his pail. The beach is a good spot.

The End.""",
        "talk": "1. What does Ben find? (A shell.) 2. Why does Ben run back from the sea? (The sea is coming in.) 3. How does Ben feel at the end? (Glad.) 4. Find an AR word in the story. (far, hard, sharp, dark).",
    },
    {
        "slug": "036-the-pine-tree-in-the-wind",
        "title": "The Pine Tree in the Wind",
        "stage": 3,
        "after": 13,
        "animals": [],
        "warmup": "pine, tree, wind, hill, branch, leaf, sky, brave, time, soft",
        "story": """**The Pine Tree in the Wind**

A pine tree stands on a hill. It has been there a long time. The hill is wide and green.

The tree has soft green needles. It is tall and strong. Birds nest in its branches every spring.

A wind comes in the night. The wind blows from the north. The tree sways and sighs.

The wind blows hard for hours. The tree bends low. Its branches wave side to side.

A small bird sits deep in the tree. The tree holds the bird safe. The wind can not shake it loose.

The wind blows all day and all night. The tree keeps on. It does not break or bend in two.

A little mouse lives at the base of the trunk. The tree is the mouse's home. The tree is brave and kind.

When the wind slows at last, the clouds drift off. The sun comes out. The tree stands tall and still once more.

The hill is green. The sky is blue. The pine tree is fine. The bird sings a soft, glad song.

The End.""",
        "talk": "1. Where does the pine tree stand? (On a hill.) 2. What happens when the wind blows? (The tree bends and sways.) 3. Who lives in the tree? (A bird and a mouse.) 4. Find a silent E word in the story. (pine, tree, time, wide, soft, green, tall, branches, north, side, safe, day, breaks, brave, comes, still, blue, fine.)",
    },
    {
        "slug": "037-a-note-from-a-friend",
        "title": "A Note from a Friend",
        "stage": 3,
        "after": 13,
        "animals": [],
        "warmup": "note, friend, write, share, kind, smile, hope, smile, send, gave",
        "story": """**A Note from a Friend**

Kate is at home. She sits by the table. She has a pen and a clean white note.

She wants to write to her friend. Her friend is named Jane. They have been pals since grade one.

Kate writes a kind note. She smiles as she writes. The note is long and sweet.

She writes, "I hope you are fine. I miss you at school. Let us play soon by the pine."

Kate folds the note with care. She puts it in a white envelope. She writes the name in blue.

Jane lives down the lane. Kate rides her bike to Jane's home. The day is bright and fine.

She leaves the note at Jane's door. She smiles and rides home. The lane is wide.

The next day, Jane comes to Kate's home. Jane has a note too. She grins and waves it high.

Jane reads her note out loud. "I am fine! Let us play today by the slide!" The note makes Kate glad.

They run and play in the wide green yard. Two friends share the day from dawn to dusk.

The End.""",
        "talk": "1. Who does Kate write a note to? (Her friend Jane.) 2. How does Kate get the note to Jane? (She rides her bike to Jane's home.) 3. What does Jane's note say? (\"I am fine! Let us play today!\") 4. Find a silent E word. (note, home, write, friend, name, kind, smiles, writes, fine, hope, school, soon, envelope, lane, rides, bike, day, bright, smile, rides, reads, loud, glad.)",
    },
    {
        "slug": "038-the-lake-in-the-hills",
        "title": "The Lake in the Hills",
        "stage": 3,
        "after": 13,
        "animals": [],
        "warmup": "lake, hill, water, sky, stone, fish, dive, deep, wide, shine",
        "story": """**The Lake in the Hills**

A lake sits in the hills. The water is still and clear. The sky is wide.

Tall pines line the shore. Green ferns grow by the rocks. The place is quiet.

A stone path leads to the lake. A frog sits on a stone. The frog dives in.

Under the water, fish glide. They flash and shine. The deep is cool.

A crane wades in the shallows. It is still and calm. It hunts for a meal.

On the hill, a kid named Will looks down. He smiles at the scene. The view is fine.

Will slides down the path. He reaches the lake. He sits on a stone.

He puts a hand in the water. It is cold and clean. He smiles.

The sun starts to set. The sky turns pink. The lake glows.

Will walks home in the dusk. The lake is a place he will not forget.

The End.""",
        "talk": "1. Where is the lake? (In the hills.) 2. What animals live in or near the lake? (A frog, fish, a crane.) 3. What does Will do at the lake? (He touches the water and sits on a stone.) 4. Find a silent E word. (lake, hills, water, still, clear, sky, wide, pines, line, shore, green, ferns, grow, rocks, place, quiet, stone, path, leads, glides, flash, shine, deep, cool, wades, shallows, still, calm, hunts, meal, hill, kid, named, looks, down, smiles, scene, view, fine, slides, reaches, sits, puts, hand, cold, clean, smiles, starts, dusk, place, forget.)",
    },
    {
        "slug": "039-mice-find-a-home",
        "title": "Mice Find a Home",
        "stage": 3,
        "after": 13,
        "animals": ["mouse.png"],
        "warmup": "mice, mouse, home, hole, find, nest, soft, safe, kind, brave",
        "story": """**Mice Find a Home**

Mira and Milo are mice. They live in a field. Their home is a small hole.

One night, the wind howls. Rain pours in. The hole floods. They must flee.

The mice run to a barn. They crawl under a board. They wait till the storm goes.

The barn is dry and warm. But there is a cat. The cat hunts at night.

The mice creep past the cat. They slide out a crack. They make it free.

In the field, they search. They look for a safer place. They find a wood pile.

The wood pile has a deep hole. It is lined with soft grass. It is dry inside.

The mice drag in a strip of cloth. They line the nest. They make it snug.

Mira smiles at Milo. "This is our home now," she says. They are safe at last.

The next day, they peek out. The sun shines. The field is green and bright.

The End.""",
        "talk": "1. Why do the mice leave their home? (Rain floods the hole.) 2. Where do they find a new home? (In a wood pile.) 3. What do they do to make it nice? (They line it with cloth and grass.) 4. Find a silent E word. (mice, mice, home, mice, hole, night, wind, howls, pours, floods, must, flee, barn, crawl, board, wait, storm, goes, dry, warm, hunts, night, creep, slide, crack, make, free, field, search, look, safer, place, find, wood, pile, deep, lined, soft, grass, dry, inside, drag, strip, cloth, line, nest, make, snug, smiles, says, home, safe, last, peek, shines, field, green, bright.)",
    },
    {
        "slug": "040-the-crane-flies-south",
        "title": "The Crane Flies South",
        "stage": 3,
        "after": 13,
        "animals": ["bird.png"],
        "warmup": "crane, fly, south, north, sky, wing, wind, long, brave, safe",
        "story": """**The Crane Flies South**

Cara is a crane. She lives in a marsh in the far north. The days grow cold and short.

The wind turns sharp and bites. The pond begins to freeze. It is time to fly south.

Cara calls to the other cranes. They gather on the shore. They line up in a long wedge.

The leader takes the tip of the wedge. Cara is in the middle of the line. They beat their strong wings.

Up, up they rise in a spiral. They climb above the tall trees. The sky is wide and clear.

The cranes fly south for hours. They cross the high hills. They cross the wide farms. They fly on without rest.

By night, they land in a soft field. They rest and feed on seeds. They are safe in the dark.

At dawn, they rise once more in the sky. The wind is at their back. They glide with grace and speed.

Days pass as they fly. The sun grows warm. Cara sees the green southern marsh at last.

They land by the warm water with a splash. They are home. The long brave trip is done.

The End.""",
        "talk": "1. Where does Cara live at the start? (In a marsh in the north.) 2. Why do the cranes fly south? (The days grow cold and the pond freezes.) 3. What shape do they fly in? (A wedge.) 4. Find a silent E word. (crane, lives, marsh, north, days, grow, cold, wind, turns, sharp, pond, begins, freeze, time, go, cranes, gather, shore, line, wedge, leader, takes, tip, middle, beat, strong, wings, rise, climb, above, trees, sky, wide, clear, south, cross, hills, farms, fly, night, land, field, rest, feed, safe, dawn, rise, once, more, back, glide, grace, days, pass, sun, grows, warm, sees, southern, marsh, last, land, water, home, long, trip, done.)",
    },
    {
        "slug": "032-the-path-through-the-woods",
        "title": "The Path Through the Woods",
        "stage": 2,
        "after": 21,
        "animals": [],
        "warmup": "her, fern, river, under, never, sister, mother, father, after, other",
        "story": """**The Path Through the Woods**

Liz walks in the woods. Trees are big. The ferns are soft.

Liz is on a path. She looks at the ferns. She sees a green moth.

The path is long. Liz walks and walks. She never gets back.

"I am stuck!" says Liz. "I can not find it." She looks and looks.

Liz sees a big jay. "Tweet!" says the bird. Liz follows the bird.

The bird swoops to a tree. It lands on a stream. Liz walks with it.

Liz sees a rock. The river runs by. She hears the stream.

Liz follows the stream. She walks and walks. The path is back.

"I see the path!" Liz says. She is so glad. The path is firm.

Liz has ferns in her hand. She is glad. The woods are fun.

The End.""",
        "talk": "1. What does Liz see first? (Ferns and a green moth.) 2. Why does Liz feel stuck? (She walks and walks and never gets back.) 3. How does Liz find her way? (She follows a bird to the stream.) 4. Find an ER word in the story. (her, ferns, river, under, never).",
    },
    # ── STAGE 5 READERS — issue #28 Wave 5 (Greek/Latin root annotations) ──
    {
        "slug": "047-the-migration",
        "title": "The Migration",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "migrate, journey, north, south, sky, flock, instinct, climate, distance, seasons",
        "roots": "migr — Latin: migrare (to move)\nport — Latin: portare (to carry)\ninstinct — Latin: instinctus (impulse)",
        "challenge_words": "instinct — in + stinct (Latin: urge)\nmigrate — migr (move) + -ate (to act)\nclimate — climat (slope, region)",
        "story": """**The Migration**

Each year, when the air turns cold and the days grow short, something amazing happens above the farms and forests. Birds lift off from the north. They rise in great flocks and turn their wings toward the south. This long flight has a name. It is called the migration.

Why do the birds leave? The answer is simple. Food grows scarce when ice covers the ponds and snow hides the seeds. The birds cannot live through a long cold winter if they stay in one place. So they fly to a warmer land, where insects still buzz and fruit still hangs on the branches.

A small songbird may travel thousands of miles. Geese and cranes fly in wedges. Ducks fly in long lines. Each bird has an instinct that pulls it forward, like a magnet that points to a hidden north. Scientists study this instinct. They think the birds use the sun by day and the stars by night. They may also read the lay of the land below.

Along the way, the birds face storms and hunger. Some grow tired and fall. But many reach the southern marsh or the southern shore. They rest there through the cold months. When spring comes back to the north, the birds return. They build nests. They raise their young.

Some young birds fly the route for the very first time. They have never seen the southern shore. Yet they find their way. Older birds do not guide them. The map is written in their bodies, not on paper. This is one of the deepest puzzles in nature.

The migration is one of the great journeys of the living world. It shows how a creature no bigger than your hand can cross a continent. It shows how nature keeps each season in balance.

The End.""",
        "talk": "1. Why do birds leave the north in fall? (Food grows scarce when ice and snow come.) 2. What shapes do flocks fly in? (Wedges for geese and cranes; lines for ducks.) 3. What helps a bird find its way? (The sun, the stars, and the lay of the land.) 4. Find a root word in this story and tell what it means.",
    },
    {
        "slug": "048-the-tide-pool",
        "title": "The Tide Pool",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "tide, pool, ocean, coast, marine, crab, snail, anemone, shallow, surface",
        "roots": "marine — Latin: mare (sea)\ntide — Old English: tid (time, season)\npool — Old English: pol (a small body of water)",
        "challenge_words": "anemone — Greek: anemos (wind)\nmarine — Latin: mare (sea)\ncrab — Old English: crabba",
        "story": """**The Tide Pool**

Along a rocky coast, where the waves come and go, there are small pockets of water left behind when the sea pulls back. These pockets are called tide pools. Each tide pool is a tiny world, cut off from the ocean for a few hours at a time.

In a tide pool, life crowds together. A green anemone grips a stone with its soft feet. Tiny fish dart between strands of seaweed. A hermit crab walks sideways across the sand. Limpets stick tight to the rocks. Periwinkles leave silver trails behind them.

The water in a tide pool is shallow and warm. The sun heats it. The pool can dry out if the tide stays out too long. The animals must hide in shade or under seaweed. Some clamp their shells shut. Some crawl into cracks in the rock.

When the tide comes back, the pool fills up again. Fresh sea water rushes in, carrying food and cool air. The fish come out of hiding. The anemone opens its soft arms. The hermit crab walks once more in search of a meal.

The tide comes in and goes out twice each day. Once in the morning and once at night. In some places the shift is small. In other places the tide pulls back many feet. Tide pool animals live by this rhythm. They know the sea's clock better than any person does.

A tide pool is one of the most crowded places on the coast. In just a small pool, you can find dozens of kinds of life. Each creature plays its part, and each depends on the rhythm of the sea.

The End.""",
        "talk": "1. What is a tide pool? (A pocket of water left behind on the rocky coast when the tide goes out.) 2. Name three animals that live in a tide pool. (Anemone, hermit crab, limpet, periwinkle.) 3. Why do tide pool animals hide from the sun? (The water can dry out.) 4. What does the Latin root 'mare' mean? (Sea.)",
    },
    {
        "slug": "049-photosynthesis-for-beginners",
        "title": "Photosynthesis for Beginners",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "plant, leaf, sun, water, air, sugar, green, grow, food, light",
        "roots": "photo — Greek: phos (light)\nsynthesis — Greek: synthesis (putting together)\nchloro — Greek: chloros (green)",
        "challenge_words": "photosynthesis — photo (light) + synthesis (put together)\nchlorophyll — chloro (green) + phyll (leaf)\nleaf — Old English: leaf",
        "story": """**Photosynthesis for Beginners**

Plants make their own food. Animals cannot do this. Animals must eat plants, or eat other animals that have eaten plants. But a green plant can sit in one place and still grow. How does it do this?

The secret is in the leaf. A leaf is a small factory. It takes raw materials from the air and the soil and turns them into sugar. Sugar is food for the plant. The name for this process is photosynthesis, which means 'building with light'.

What are the raw materials? The plant takes in water through its roots. It takes in a gas called carbon dioxide through tiny holes in the leaves. And it takes in light from the sun. Inside the leaf, a green color called chlorophyll catches the light. The leaf uses that light energy to join water and carbon dioxide into sugar.

The plant does not need the sugar alone. It also breathes out a gas called oxygen. Animals breathe in oxygen. So plants and animals help each other. Plants give oxygen to animals. Animals give carbon dioxide to plants.

A plant does not do this only in bright sun. On a cloudy day, the leaf still works. It just works more slowly. At night, when there is no light, the leaf rests. In the morning, when the sun rises, the leaf begins again.

Without plants, there would be no food and no oxygen. The next time you see a green leaf, remember: it is a tiny factory, working day after day, making food and air for the whole living world.

The End.""",
        "talk": "1. What does a leaf take in to make food? (Water, carbon dioxide, and sunlight.) 2. What does the green color in a leaf do? (It catches light energy.) 3. What gas does a plant give off? (Oxygen.) 4. What do the Greek roots 'photo' and 'synthesis' mean? (Light and putting together.)",
    },
    {
        "slug": "050-the-ancient-coast",
        "title": "The Ancient Coast",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "coast, rock, cliff, sand, fossil, shell, layer, ancient, ocean, time",
        "roots": "fossil — Latin: fossilis (dug up)\nancient — Latin: ante (before)\nlayer — Old French: laier (to spread)",
        "challenge_words": "fossil — Latin: fossilis (something dug up)\nancient — ante (before) + -an\nlayer — to lay + -er",
        "story": """**The Ancient Coast**

A long time ago, the coast did not look the way it looks today. The cliffs were taller. The beaches were wider. The rivers that ran down to the sea cut deeper valleys. And in the rocks of the cliffs were the marks of life from a very distant past.

Some of those marks are fossils. A fossil is the shape of an old plant or animal, pressed into stone. A shell may be buried in sand. After many years, the sand turns to rock. The shell dissolves away, but its shape is left behind, sharp and clear. A leaf may fall into mud. The mud hardens. The leaf leaves its print in stone.

If you walk along the base of a cliff, you can sometimes see fossils in the stone. You may see the print of a fern that grew a million years ago. You may see the curved shell of a creature that swam when dinosaurs ruled the land. Each fossil is a message from a time before any person lived.

Some fossils are very small. A grain of sand can leave its mark in soft mud. Other fossils are very large. A whale bone can sit in a cliff for ages. The size of the fossil does not matter. Each one is a window into a moment long gone.

The coast keeps changing. The waves wear the cliffs. The wind blows the sand. Each year, the shape of the coast shifts a little. But the fossils stay, one layer under another, like pages in a very old book.

When you pick up a fossil, you hold a piece of the ancient world in your hand. It is one of the most quiet, surprising things on the coast.

The End.""",
        "talk": "1. What is a fossil? (The shape of an old plant or animal left in stone.) 2. How does a shell become a fossil? (It gets buried in sand that turns to rock.) 3. What can you sometimes find in the rocks at the base of a cliff? (Fossils of ferns, shells, or other ancient life.) 4. What does the Latin root 'ante' mean? (Before.)",
    },
    {
        "slug": "051-symbiosis-in-the-coral-reef",
        "title": "Symbiosis in the Coral Reef",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "reef, coral, fish, partner, shelter, plant, animal, share, depend, host",
        "roots": "sym — Greek: syn (together)\nbio — Greek: bios (life)\nosis — Greek: -osis (process)",
        "challenge_words": "symbiosis — syn (together) + bios (life) + -osis (process)\npartner — Old French: partenaire\nreef — Dutch: rif (ridge)",
        "story": """**Symbiosis in the Coral Reef**

A coral reef is one of the busiest places in the sea. Bright fish dart between branches of coral. Shrimp crawl along the floor. Sea turtles drift above like dark leaves. The reef looks like a garden made of stone.

Coral looks like a plant, but it is really an animal. It is built of thousands of tiny soft creatures, all joined together. Each tiny creature is called a polyp. The polyps cannot make their own food. They live with a kind of plant algae that lives inside them. The plant makes sugar from sunlight. The animal shares that sugar and gives the plant a safe home. The two help each other.

This kind of partnership has a name. It is called symbiosis, which means 'living together'. In symbiosis, two different kinds of life share the same space and help each other survive.

There are other partners on the reef. A small fish called a cleaner wrasse picks bits of food from the teeth of bigger fish. The big fish get clean. The little fish get a meal. Both win. A shrimp digs a burrow in the sand. A goby fish stands guard at the door. The shrimp gets a warning. The goby gets a home.

The reef is not a quiet place. At night, the coral polyps open up and the fish that hide by day come out to feed. Crabs creep along the rocks. Octopuses hunt in the cracks. The reef never truly sleeps.

The reef is full of these quiet deals. Each creature plays a role. Each depends on another. When you watch a reef, you are watching a community that has worked out its teamwork over millions of years.

The End.""",
        "talk": "1. What kind of life lives inside a coral polyp? (Tiny plant algae.) 2. What does 'symbiosis' mean? (Living together.) 3. How does a cleaner wrasse help a bigger fish? (It picks food from its teeth.) 4. What do the Greek roots 'syn' and 'bios' mean? (Together and life.)",
    },
    {
        "slug": "052-the-compass-and-the-stars",
        "title": "The Compass and the Stars",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "compass, north, south, east, west, star, sky, sailor, ship, voyage",
        "roots": "nav — Latin: navis (ship)\nastro — Greek: astron (star)\norbit — Latin: orbis (circle, world)",
        "challenge_words": "navigation — navis (ship) + agere (to lead)\nastronomy — astron (star) + nomos (law)\ncompass — Old French: compasser (to measure)",
        "story": """**The Compass and the Stars**

Long ago, sailors did not have maps or phones or radios. They had only the sea, the sky, and a few simple tools. The most important of those tools was the compass.

A compass is a small magnet that can spin freely. One end of the magnet always points north. The other end always points south. As long as the sailor knows where north is, the sailor can find any other direction. North is the anchor of every journey.

A compass works on land and on sea. But when the sky is dark and the clouds hide the sun, the sailor can also use the stars. In the northern sky, there is a star called Polaris, the North Star. It sits almost directly above the north pole of the Earth. When a sailor finds Polaris, the sailor can tell which way is north, even on a cloudy night.

Sailors also learned to read the waves. A steady wind makes waves that move in the same direction. The shape of the waves can tell a sailor where the wind is coming from. The color of the water can hint at how deep the sea is below.

Sailors have used these signs for thousands of years. By day, the compass. By night, the stars. With these, they crossed wide oceans. They found new lands. They traded goods between far ports.

Today, ships carry radio and satellite tools. The compass still rides on the bridge. The stars still turn above the deck. Old tools and new tools work side by side, helping sailors find their way across the water.

The End.""",
        "talk": "1. What does one end of a compass needle always point to? (North.) 2. What is the North Star? (Polaris, a star that sits almost directly above the north pole.) 3. Name two ways a sailor can find direction at night. (By the compass and by the stars.) 4. What do the Latin roots 'navis' and Greek 'astron' mean? (Ship and star.)",
    },
    {
        "slug": "053-the-cycle-of-the-seasons",
        "title": "The Cycle of the Seasons",
        "stage": 5,
        "after": 38,
        "animals": [],
        "warmup": "season, spring, summer, autumn, winter, sun, tilt, axis, leaf, snow",
        "roots": "cycle — Greek: kyklos (circle)\naxis — Latin: axis (axle)\nhibern — Latin: hibernare (to spend the winter)",
        "challenge_words": "cycle — Greek: kyklos (circle, wheel)\naxis — Latin: axis (axle, pivot)\nhibernate — hibernare (to pass the winter)",
        "story": """**The Cycle of the Seasons**

Every year, the same pattern repeats. The snow melts. The flowers open. The days grow long and hot. The leaves turn gold and red. The air turns sharp, and the snow falls again. This pattern has a name. It is called the cycle of the seasons.

What makes the seasons change? The answer is the tilt of the Earth. The Earth spins like a top. It also travels around the sun. But it does not sit up straight. It leans a little, the way a person leans against a wall. The line through the top and bottom of the Earth, which we call the axis, tilts at an angle.

As the Earth moves around the sun, different parts of the world tilt toward the sun and then away from it. When your part of the world tilts toward the sun, the days are long and the weather is warm. That is summer. When your part tilts away, the days are short and the weather is cold. That is winter. Spring and autumn are the times in between.

Plants and animals have learned to live with this cycle. Trees drop their leaves in autumn and grow new ones in spring. Bears eat much in autumn and sleep through the cold. Birds fly south when winter comes and return when spring returns.

People mark the seasons too. In spring, fields are planted. In summer, crops grow tall. In autumn, the harvest is gathered. In winter, the fires burn and the stories are told. Each season has its own work and its own rest.

The cycle never stops. It has been turning for billions of years. Each year, you live one full turn of it. Each season is one small piece of a very long, very steady wheel.

The End.""",
        "talk": "1. What causes the seasons? (The tilt of the Earth as it moves around the sun.) 2. What is the axis? (The line through the top and bottom of the Earth.) 3. What do some animals do in winter? (Hibernate, or migrate south.) 4. What does the Greek root 'kyklos' mean? (Circle or wheel.)",
    },
]

TMP = """<div class="reader-cover">

# {title}

**Stage {stage} Decodable Reader** · For use after Lesson {after}

</div>

<div class="page-break"></div>

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

    Issue #28 Wave 5: Stage 5 readers also get a final Roots + Challenge
    Words block (matches 001-ostriches.md hand-written format) when the
    reader dict provides ``roots`` and ``challenge_words``.
    Stage 5 readers use 2 sentences per page (vs 3 elsewhere) so the
    longer Stage 5 stories land in the 15-20 page band.
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
    pages = split_into_pages(story_body, sentences_per_page=4)
    parts = []
    for page in pages:
        sidebar = build_sidebar(page, new_phonogram=None)
        parts.append(
            f'<div class="reader-page">\n\n'
            f'<div class="reader-text">\n\n{page}\n\n</div>\n\n'
            f'{sidebar}\n\n'
            f'</div>'
        )
    # Stage 5 readers (issue #28 Wave 5) get an explicit Roots + Challenge
    # Words sidebar at the end, mirroring 001-ostriches.md.
    if r.get("stage") == 5 and (r.get("roots") or r.get("challenge_words")):
        roots_lines = ["<div class=\"reader-page\">", "", "<div class=\"reader-text\">", "",
                       "**Roots and Challenge Words**", ""]
        if r.get("roots"):
            roots_lines.append("**Roots in this passage:**")
            for line in r["roots"].splitlines():
                line = line.strip()
                if line:
                    roots_lines.append(f"- {line}")
            roots_lines.append("")
        if r.get("challenge_words"):
            roots_lines.append("**Challenge words:**")
            for line in r["challenge_words"].splitlines():
                line = line.strip()
                if line:
                    roots_lines.append(f"- {line}")
            roots_lines.append("")
        roots_lines.extend(["</div>", "", "</div>"])
        parts.append("\n\n".join(roots_lines))
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
        (OUT / f"{r['slug']}.md").write_text(stamp(content), encoding="utf-8")
        stage_dir = OUT / f"stage-{r['stage']}"
        stage_dir.mkdir(parents=True, exist_ok=True)
        (stage_dir / f"{r['slug']}.md").write_text(stamp(content), encoding="utf-8")
        print(f"  readers/{r['slug']}.md (+ readers/stage-{r['stage']}/)  [{r['animals']}]")

    print(f"\n{len(READERS)} readers generated")

if __name__ == "__main__":
    main()
