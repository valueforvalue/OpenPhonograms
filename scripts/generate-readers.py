#!/usr/bin/env python3
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

Dash is a fish. Dash swims in the big pond.

The pond has rocks and plants. Dash likes the plants.

Dash sees a bug on a rock. "Yum!" Dash zips up.

ZAP! Dash gets the bug.

But then Dash sees a big duck! The duck is on the pond.

The duck sees Dash. "Quack!" says the duck.

Dash swims fast! Dash hides in the plants.

The duck can not get Dash. Dash is safe.

"Whew!" says Dash. "That was close!"

The duck swims away. Dash comes out.

Dash is glad. The pond is calm.

The End.""",
    "talk": "1. Where does Dash live? (In a pond.) 2. What does Dash eat? (A bug.) 3. Why does Dash hide? (A duck wants to eat him!) 4. Find a CK word. (duck, back, rock, quick)",
})

READERS.append({
    "slug": "003-the-green-tree",
    "title": "The Green Tree",
    "stage": 2,
    "after_lesson": 18,
    "phonograms": "sh, th, ck, ee + blends",
    "warmup": "tree, green, see, sleep, stop, frog, swim, glad, hand, lamp, nest",
    "story": """**The Green Tree**

There is a big green tree in the park. The tree is old and tall.

A frog sits on a log next to the tree. The frog is green, like the tree.

"I am glad to sit here," says the frog. "The tree keeps me cool."

A bird is in the tree. The bird has a nest. The nest has three eggs.

"I am glad to be here," says the bird. "The tree keeps my nest safe."

A child runs to the tree. The child stops and looks up.

"I see the frog!" says the child. "I see the bird! I see the nest!"

The child sits under the green tree. The frog sings. The bird sings.

The green tree is a good home.

The End.""",
    "talk": "1. Who lives in the tree? (A bird.) 2. Who sits next to the tree? (A frog.) 3. What color is the frog? (Green, like the tree.) 4. Find a word with EE. (tree, green, see, keep, etc.)",
})

READERS.append({
    "slug": "004-the-rainy-day",
    "title": "The Rainy Day",
    "stage": 2,
    "after_lesson": 31,
    "phonograms": "oi, oy, ai, ay + all previous",
    "warmup": "rain, day, play, stay, boy, toy, coin, join, paint, train, sail",
    "story": """**The Rainy Day**

It is a rainy day. Rain falls on the roof. Rain falls on the street.

Sam looks out the window. "I want to play," he says. "But it is too wet."

Sam's mom says, "You can play with your toys."

Sam gets his toy train. The train has ten cars. Sam makes the train go on the floor.

Then Sam gets his coins. He counts the coins. One, two, three, four, five!

Sam's dog, Roy, comes in. Roy has a toy in his mouth. It is a toy boat!

"Good boy, Roy!" says Sam. "Let's play!"

Sam and Roy play all day. The rain stops at night.

"I had fun," says Sam. "Rainy days can be good days."

The End.""",
    "talk": "1. Why can't Sam play outside? (It's raining.) 2. What toys does Sam play with? (Train and coins.) 3. Who is Roy? (Sam's dog.) 4. Find words with OY and AI. (toy, Roy, boy, rainy, train, paint)",
})

READERS.append({
    "slug": "005-the-farm",
    "title": "The Farm",
    "stage": 2,
    "after_lesson": 50,
    "phonograms": "oa, ear + all previous",
    "warmup": "farm, car, horse, corn, goat, boat, road, learn, early, sister, under",
    "story": """**The Farm**

Grandpa has a farm. The farm is far from town.

On the farm, there are many animals. There is a horse named Star. There is a goat named Billy. There are ten hens and one big rooster.

Grandpa grows corn in the field. The corn is tall and green. The goats like to eat the corn!

"Shoo, Billy!" calls Grandpa. "The corn is not for you!"

There is a pond on the farm. Grandpa has a small boat. The boat is red.

In the summer, the children visit the farm. They ride in the red boat. They feed the hens. They help Grandpa pick the corn.

"Farms are the best," says Lily. "I want to live on a farm when I grow up."

Grandpa smiles. "You can visit any time."

The End.""",
    "talk": "1. What animals live on the farm? (Horse, goat, hens, rooster.) 2. What does Grandpa grow? (Corn.) 3. What color is the boat? (Red.) 4. Find words with AR and OR. (farm, far, horse, corn, for, short)",
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

Jake wants to bake a cake. "I will make the best cake!" he says.

Jake gets a big bowl. He gets the flour, eggs, and milk. He mixes them up.

"Time to add the sugar," Jake says. He dumps in a cup of sugar.

Jake puts the cake in the oven. He waits and waits. The cake rises up!

The timer dings. Jake takes the cake out. It is golden and smells so fine!

Jake puts white frosting on top. He adds red berries. The cake looks beautiful.

Jake's sister, Kate, comes home. "What is that?" she asks.

"It is a cake!" says Jake. "I baked it all by myself."

Kate takes a bite. Her eyes get wide. "Jake! This is the best cake I have ever had!"

Jake smiles. "I told you. I make the best cake."

The End.""",
    "talk": "1. What does Jake bake? (A cake.) 2. What does he put on top? (White frosting and red berries.) 3. Who comes home? (His sister Kate.) 4. Find silent E words. (cake, bake, make, time, take, fine, plate, etc.)",
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

"Don't be silly," says Tom. "That bridge has been there since I was a child."

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

"I'm scared," said little Sue.

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

A journalist heard about the invention and wrote a story. Soon, people around the world were talking about the SolarPure. It could help millions of people who didn't have clean water.

"An invention isn't just a clever machine," Dr. Chen said. "An invention is a solution to a problem. And the best inventions help people."

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
        print(f"  readers/{r['slug']}.md")
    print(f"\n{len(READERS)} additional readers generated")

if __name__ == "__main__":
    main()
