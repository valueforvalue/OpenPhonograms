#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# Copyright (c) 2026 Jeremy Morris. Released under the MIT License (see LICENSE).

"""Generate additional decodable readers for Stages 2-4."""
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "readers"
OUT.mkdir(parents=True, exist_ok=True)

READERS = []

# ── STAGE 2 READERS (after key phonograms) ──

READERS.append({
    "slug": "002-dash-the-fish",
    "title": "Dash the Fish",
    "stage": 2,
    "after_lesson": 14,
    "phonograms": "sh, th, ck + all single-letter",
    "warmup": "ship, fish, dash, this, that, back, duck, sick",
    "story": """**Dash the Fish**

Dash is a small fish. He has thin fins.

Dash lives in a pond. The pond has rocks. The pond has plants.

One day, Dash sits on a rock. He looks up.

A bug! It is on a log. Yum!

Dash swims up. He opens his mouth. ZAP!

Dash has the bug. He has it for his snack.

Then — a duck! A big brown duck.

"QUACK!" says the duck.

Dash swims fast. He hides in the plants.

The duck looks. The duck can not find Dash.

Dash sits still. His fins tick.

The duck goes back. She swims off.

Dash pops up. He is safe.

"Whew!" says Dash. "That was too close."

Dash swims back to his rock. He sits in the sun.

Dash is a smart fish.

The End.""",
    "talk": "1. What did Dash catch for his snack? (A bug.) 2. Why did Dash hide? (A big duck came.) 3. How did Dash stay safe? (He sat still in the plants.) 4. Find a CK word in the story. (duck, back, rock, snack, tick)",
})

READERS.append({
    "slug": "003-the-green-tree",
    "title": "The Green Tree",
    "stage": 2,
    "after_lesson": 18,
    "phonograms": "sh, th, ck, ee + blends",
    "warmup": "tree, green, see, sleep, stop, frog, swim, glad, hand, lamp, nest",
    "story": """**The Green Tree**

Deep in the park, there is a green tree. The tree is big and old.

A frog named Fern lives by the tree. She sits on a log next to the trunk.

"It is good here," says Fern. "The tree keeps me cool."

Up in the tree top, a bird has a nest. The nest has three small eggs.

The bird sings all day long.

Then — strong wind! The wind shakes the tree.

The nest slips! "Help!" sings the bird.

Fern sees the nest fall. She jumps up. She catches it.

The eggs are safe. The bird is glad.

"Thank you, Fern!" sings the bird.

"You are welcome," says Fern.

The wind stops. The sun comes back.

Fern and the bird sit in the green tree. They are pals.

The green tree is the best home.

The End.""",
    "talk": "1. Who lives in the green tree? (A bird with three eggs.) 2. What happens when the wind comes? (The nest falls.) 3. How does Fern help? (She catches the nest.) 4. Find an EE word in the story. (tree, green, see, keep, deep, three, seed)",
})

READERS.append({
    "slug": "004-the-rainy-day",
    "title": "The Rainy Day",
    "stage": 2,
    "after_lesson": 31,
    "phonograms": "oi, oy, ai, ay + all previous",
    "warmup": "rain, day, play, stay, boy, toy, coin, join, paint, train, sail",
    "story": """**The Rainy Day**

Today is a fine day. The sky is blue.

Sam has a red ball. He likes his ball.

"Let's play!" says Sam.

Sam and his pal Roy go out. Roy has a toy train.

They run. They play. They shout.

Then the ball flies up. Up, up!

It lands on the roof. Oh no!

"I want my ball!" cries Sam.

Roy looks up. He thinks. He has an idea.

"I have my train!" says Roy. "Watch!"

Roy throws the train up. It hits the ball.

The ball rolls off. It lands on the grass.

Sam gets his ball. He is so glad.

"Roy, you are a good pal!" says Sam.

They play until the sun sets.

Then they go in for milk.

The End.""",
    "talk": "1. What does Sam have? (A red ball.) 2. Where does the ball land? (On the roof.) 3. How does Roy help? (He throws his train up to knock it down.) 4. Find an OI word in the story. (coin, join, soil)",
})

READERS.append({
    "slug": "005-the-farm",
    "title": "The Farm",
    "stage": 2,
    "after_lesson": 50,
    "phonograms": "oa, ear + all previous",
    "warmup": "farm, car, horse, corn, goat, boat, road, learn, early, sister, under",
    "story": """**The Farm**

It is dawn on the farm. The sky is pink.

A rooster crows. "Cock-a-doodle-doo!"

Grandpa wakes up. He puts on his boots.

Today is barn day. Time to fix the roof.

Grandpa climbs up. He has a hammer. He has nails.

THUD! THUD! The hammer hits the nails.

Then — a sound. A small sound. "Maaaa."

Grandpa looks down. A baby goat!

The baby goat is stuck. She can not get up.

"Hold on!" calls Grandpa.

Grandpa climbs down. He lifts the baby goat.

"There you go!" says Grandpa.

The baby goat runs to her mom.

The mom goat licks her baby. She is so glad.

"Thank you," bleats the mom goat.

Grandpa smiles. Then he climbs back up.

THUD! THUD! The roof is fixed.

The End.""",
    "talk": "1. What does Grandpa fix in the story? (The barn roof.) 2. What sound does Grandpa hear? (A baby goat bleating.) 3. How does Grandpa help? (He lifts the baby goat.) 4. Find an EAR word in the story. (hear, learn, yearn — note 'ear' appears in 'learn' and 'hear')",
})

# ── STAGE 3 READERS ──

READERS.append({
    "slug": "006-the-cake-bake",
    "title": "The Cake Bake",
    "stage": 3,
    "after_lesson": 13,
    "phonograms": "silent E + all previous",
    "warmup": "cake, bake, make, take, time, hope, ride, drove, smile, plate",
    "story": """**The Cake Bake**

Today is Mom's birthday. Jake wants to bake her a cake.

"I will make the best cake ever!" Jake tells his sister Kate.

Jake gets a big bowl. He gets flour, eggs, and milk. He mixes them up.

"Time to add the sugar," Jake says. He dumps in a cup.

He stirs. He tastes. "Hmm, it needs more!"

Jake adds a cup of cocoa. The mix turns brown. Now it is a chocolate cake!

He puts the cake in the oven. He sets the timer. Wait. Wait. Wait.

DING! The cake is done!

Jake takes it out. It is hot. The smell fills the room.

He puts white frosting on top. He adds red berries. The cake looks fine.

Mom comes home. "What is that smell?" she asks.

"It is a cake!" says Jake. "For your birthday!"

Mom's eyes get wide. She takes a bite.

"This is the best cake I have ever had!" Mom smiles.

Jake hugs Mom. "Happy birthday!"

The End.""",
    "talk": "1. Whose birthday is it? (Mom's.) 2. What kind of cake does Jake make? (Chocolate.) 3. How does Mom react? (She says it's the best cake ever.) 4. Find a silent E word in the story. (cake, bake, make, time, take, fine, like, smiles, etc.)",
})

READERS.append({
    "slug": "007-the-bridge",
    "title": "The Bridge",
    "stage": 3,
    "after_lesson": 23,
    "phonograms": "dge, tch, kn, gn, wr + all previous",
    "warmup": "bridge, edge, catch, watch, know, knee, sign, write, wrong, knock",
    "story": """**The Bridge**

There is an old bridge at the edge of town. The bridge goes over a wide river.

"I do not like that bridge," says Meg. "It looks like it will break."

"Do not be silly," says Tom. "That bridge has been there since I was a child."

Meg and Tom need to cross the river. There is no other way to get to the farm where they work.

Tom steps on the bridge. It is firm. "See?" he says. "It is safe."

Meg takes a step. Then another. They walk to the middle of the bridge.

Suddenly, Meg stops. "I see something shiny!"

She kneels down. There, stuck between two boards, is a golden watch!

"Look!" says Meg. "Someone dropped their watch!"

Tom's eyes get wide. "That is a fine watch. We should find who it belongs to."

They take the watch to the farm. An old man is there. "My watch!" he cries. "I lost it on the bridge last week! I thought it was gone forever."

The old man is so happy. He gives Meg and Tom each a coin.

"Sometimes scary things lead to good things," says Meg.

Tom nods. "I knew that bridge was lucky."

The End.""",
    "talk": "1. Where is the bridge? (At the edge of town, over a river.) 2. What do they find on the bridge? (A golden watch.) 3. Who did the watch belong to? (An old man at the farm.) 4. Find words with DGE. (bridge, edge.)",
})

READERS.append({
    "slug": "008-the-storm",
    "title": "The Storm",
    "stage": 3,
    "after_lesson": 35,
    "phonograms": "ough, augh, ew, ui, eu + all previous",
    "warmup": "through, though, caught, taught, few, new, fruit, suit, cause",
    "story": """**The Storm**

The sky grew dark. "A storm is coming," said Mom.

The wind blew through the trees. Rain began to fall. It was not just rain — it was a downpour!

Dad brought the dog inside. "We should stay in until this passes."

The family sat in the living room. They could hear the wind howl outside. The lights flickered.

"I am scared," said little Sue.

"It's okay," said Mom. "We are safe. The storm will pass."

To take Sue's mind off the storm, Dad told a story. It was a story about a brave sailor who sailed through many storms. The sailor was never afraid, because he knew his boat was strong.

Though the storm raged, the family stayed warm inside. They ate fruit and played games.

After an hour, the rain stopped. The sun came out. A rainbow stretched across the sky.

"Look!" said Sue. "It's beautiful!"

"Storms always end," said Mom. "And sometimes they leave something beautiful behind."

The End.""",
    "talk": "1. What did the family do during the storm? (Stayed inside, told stories, ate fruit, played games.) 2. What appeared after the storm? (A rainbow.) 3. Find words with OUGH. (through, though.) 4. Find words with EW. (few, blew, new.)",
})

# ── STAGE 4 READER ──

READERS.append({
    "slug": "009-the-invention",
    "title": "The Invention",
    "stage": 4,
    "after_lesson": 33,
    "phonograms": "all + morphology focus",
    "warmup": "invention, transportation, submarine, telescope, automatic, construction, destruction",
    "story": """**The Invention**

Dr. Chen was a scientist who loved to invent things. Her laboratory was full of strange machines and half-finished projects.

One day, Dr. Chen had an incredible idea. "What if I could build a machine that turns ocean water into clean drinking water using only sunlight?"

She called it the SolarPure. The SolarPure would use solar panels to heat ocean water. The steam would rise, leaving the salt behind. The steam would then cool into pure, fresh water.

Dr. Chen worked for months. She constructed and reconstructed. Some days, nothing worked. "Every failure is a lesson," she said.

Finally, the day came. Dr. Chen took the SolarPure to the beach. She poured in ocean water. She waited.

The sun shone down. The machine hummed. Steam rose. And then — drip, drip, drip — fresh water came out the other side!

Dr. Chen tasted it. "It works!" she shouted. "It really works!"

A journalist heard about the invention and wrote a story. Soon, people around the world were talking about the SolarPure. It could help millions of people who did not have clean water.

"An invention is not just a clever machine," Dr. Chen said. "An invention is a solution to a problem. And the best inventions help people."

The End.""",
    "talk": "1. What problem does the SolarPure solve? (Turns ocean water into drinking water.) 2. What does Dr. Chen say about failure? (Every failure is a lesson.) 3. Find words with Latin prefixes. (invention, transportation, constructed, reconstructed.)",
})

# ── WRITE ───────────────────────────────────────────────────────────

TMP = """# {title}

**Stage {stage}** · Decodable Reader · After Lesson {after_lesson}

---

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
        content = TMP.format(**r)
        (OUT / f"{r['slug']}.md").write_text(content, encoding="utf-8")
        stage_dir = OUT / f"stage-{r['stage']}"
        stage_dir.mkdir(parents=True, exist_ok=True)
        (stage_dir / f"{r['slug']}.md").write_text(content, encoding="utf-8")
        print(f"  readers/{r['slug']}.md (+ readers/stage-{r['stage']}/)")
    print(f"\n{len(READERS)} additional readers generated")

if __name__ == "__main__":
    main()
