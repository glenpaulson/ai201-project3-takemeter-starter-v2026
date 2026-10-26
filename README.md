# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

TakeMeter sorts comments from r/cscareerquestions into three kinds: `advice`,
`experience`, and `claim`. The idea is to tell apart somebody telling you what
to do, somebody describing their own job or situation, and somebody making a
general statement about the industry.

I picked that sub because it has a lot of long text and people argue constantly,
and I picked those three labels because that is what people in there are
actually doing. The thread titles are mostly questions like "should I take this
offer", so I collected comments instead.

It is a fine-tune of `distilbert-base-uncased` on 208 posts I collected and
labelled myself.

The short version of how it went: it doesn’t work yet. It gets 53% accuracy and
never predicts `advice` at all. Why that happened is written up in The Training
Run.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `advice`

**Definition:** Tells somebody to do something, either the original poster
or people in general.

**Example 1:**
> Switch teams the moment you realize you’re in a dysfunctional environment.
> You can’t change an org as a jr/mid level.

**Example 2:**
> If you’re not getting interviews then that tells you something else -
> rewrite resume if it needs it. Apply to even easier jobs. Maybe adjacent
> roles.

### `experience`

**Definition:** Reports the writer’s own situation, job, or feelings rather
than making a general point.

**Example 1:**
> I received a promotion from 75k to 92k recently after seniors left. So I
> don’t think I’ll be getting much for a while.

**Example 2:**
> I work at Adobe and I’m making around 250k fully remote. The wlb here is
> incredible, we have gotten every 3rd Friday off since COVID started and
> outside of on-call shifts I never work more than 35 hours a week.

### `claim`

**Definition:** States something general about the industry, the market, or
the field.

**Example 1:**
> Their goal is to turn software engineering into a low-wage job with no
> benefits. And to blame anything that goes wrong on humans.

**Example 2:**
> Technology never eases anything it just then requires people to do more,
> slave like a robot. Reduce staff,get current staff to do more.

### The hardest boundary

**Which two labels:** `advice` and `experience`.

These two keep landing on the same post because the normal way people give
advice in this sub is to tell you their own story and let you draw the
conclusion. This one is both at once and I could argue it either way:

> Is moving cities an option? I also came from a mid size city with a rough
> tech scene. My job search would have been 1000x harder if I didn’t have
> geographic flexibility. I ended up moving 3 times my career and eventually
> settled in a large city (nyc)

Most of the words are his own story, but the first line is clearly telling
the poster to consider moving.

**The decision rule I used every time:**

If the post tells somebody to do something, it is `advice`, even if most of
the post is the writer’s own story. The story is the support. The
instruction is the point.

So the post above is `advice`, because of the first line.

Two more rules I needed after I stress-tested the definitions:

- If there is no instruction, and the post is mostly about the writer’s own
  situation or feelings, it is `experience`. Being tired or annoyed counts
  even if nothing actually happened.
- If there is no instruction, and the post tells a personal story and then
  turns it into a general point, I go with whichever one takes up more words.

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:**

r/cscareerquestions. I collected **comments**, not the thread titles. The
titles in that sub are mostly questions like "should I take this offer", and a
question doesn’t have an opinion in it so none of my three labels fit. The
opinions are all down in the replies.

They came from about twelve threads so that one topic wouldn’t take over the
file. The threads were about offshoring, AI replacing developers, leetcode
interviews, work life balance, comp, and a few people asking for career advice.

I copy pasted them into a text file with a blank line between each one, then
ran `make_labels.py` to turn that into labels.csv. The script drops anything
under 60 characters, anything that is only a question, and any duplicates. It
dropped 8 posts out of 216.

**How I labelled them:**

Three different ways, and the `note` column says which for every row.

- **20 rows marked `cold`.** I labelled these myself with no help and no tools,
  before I had seen any AI labels at all. They were picked at random from
  across the whole file, not the first 20, because my first 20 rows are all
  from one offshoring thread and wouldn’t have been representative.
- **6 rows marked `self`.** I labelled these myself too, but I wasn’t being
  careful about it, so I didn’t count them as part of the cold check.
- **182 rows marked `pre-labelled, checked`.** Claude labelled these using my
  definitions and my decision rules. I then read every one of them. I agreed
  with all of them and didn’t change any.

I did the cold 20 first on purpose. If I had seen the AI labels first then my
own 20 wouldn’t really be mine, and next unit’s agreement report is supposed to
measure how consistent **I** am.

**Counts per label:**

| Label | Count | Share |
|---|---|---|
| `claim` | 93 | 44.7% |
| `experience` | 79 | 38.0% |
| `advice` | 36 | 17.3% |
| **Total** | **208** | 100% |

My biggest label is 44.7%, which is under the 70% the project allows and also
under the 50% I set myself in criteria.md.

`advice` being only 17.3% is the thing I am worried about. At a 15% test split
that is about 5 advice posts in test, and getting one of them wrong moves
recall by 20 points. I decided to go with the data I had instead of collecting
more, so I am writing it down now: if my per-label criterion misses next unit,
this is probably why, and it is a problem with my dataset and not with the
model.

**A gap in my taxonomy that I noticed while labelling**

About seven posts are somebody responding directly to another person. Things
like "You communicated fine", or "market’s a mess but you can still get back
in", or someone telling the poster their passion was never real.

They are not instructions, so they are not `advice`. They are not about the
writer, so they are not `experience`. And they are not really about the
industry either, so `claim` doesn’t fit them properly. I put them in `claim`
because I had to put them somewhere, not because the definition covers them.

I am writing this down before I train anything. If `claim` turns out to be my
messiest label next unit, this is my first suspect.

**Three hard cases**

**1.**
> *The post:* "After 30 yrs in software engineer and web development, I can
> tell you it absolutely is replacing developers and anyone who says otherwise
> simply doesn’t know what they are talking about. Our company shrank our dept
> by just over half and we are doing the same work as before and in less time.
> We no longer hire Jr devs, only senior with loads of experience."
>
> *Could have been:* `claim` or `experience`
>
> *I chose, because:* `experience`, but only just. The general part is 31 words
> and the part about his own company is 35 words, so my word count tie-break
> picked experience by four words. If he had written one less sentence about
> his company it would have flipped. This is the case that made me realise my
> tie-break rule is doing a lot of work and is not really a principled rule,
> it is just a consistent one.

**2.**
> *The post:* "Personally if I’m in your boat, I would start a side hassle
> instead of changing jobs. 2hr per day vs 8+ hrs doesn’t seem comparable."
>
> *Could have been:* `advice` or `experience`
>
> *I chose, because:* `advice`. This one is a gap in my rules rather than a
> hard post. My rule says advice is when the post tells somebody to do
> something, but the subject of this sentence is "I", not "you". Read
> literally my rule doesn’t fire at all. But the whole purpose of the comment
> is to tell the poster what to do, it is just being polite about it. I
> decided that "if I were you I would do X" counts as telling somebody to do
> something, and applied that to every post like it.

**3.**
> *The post:* "Yeah you have to sacrifice something, since landing dev job I
> stopped the side projects etc. I wake up around 5am go for a run/workout,
> clean or take care of things around house, then begin work, then take care
> of business after work (errands, meal prep, etc). Social time comes maybe on
> the weekends."
>
> *Could have been:* `advice` or `experience`
>
> *I chose, because:* `advice`, and I still don’t love it. There are six words
> of instruction at the front and about fifty words of the guy describing his
> own day. It reads like experience. But my rule says an instruction wins even
> when most of the post is the writer’s own story, and I decided breaking my
> own rule on one post I happened to feel strongly about was worse than a
> label I disagree with.

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:** `distilbert-base-uncased`

**Settings:** 3 epochs, learning rate 2e-5, batch size 16, seed 42, and
max_length 128 tokens per post.

**Anything I changed from the defaults, and why:**

Nothing. I left every setting where the notebook had it. My longest post is 557
characters which is roughly 140 tokens, and my median post is about 40 tokens,
so 128 only truncates one or two posts and raising it would have doubled the
time and memory for text I don’t actually have.

**What I trained on:** `cpu`. The notebook printed `cpu (CPU)` and torch
`2.14.1+cpu`, and results.json records it. My machine does have an NVIDIA
Quadro T1000, but the pip default on Windows is the CPU build of torch and the
whole run takes a couple of minutes anyway, so I didn’t go chasing CUDA for it.

**Split sizes:** 208 posts, split 70/15/15, which came out as **train 144 /
val 32 / test 32**.

| Label | Train | Val | Test |
|---|---|---|---|
| `advice` | 24 | 6 | 6 |
| `experience` | 55 | 12 | 12 |
| `claim` | 65 | 14 | 14 |

`advice` has **6 examples in the test split**, which is under the 8 the course
says you need before a per-label number means much. The notebook flagged it on
its own. I had already written this down in The Dataset section before I
trained anything, so it is a thing I predicted rather than a thing that
surprised me.

What I did not predict is how bad it would be. `advice` only got **24 training
examples**, and the model never once predicted `advice` on the test set. Not a
single time. It guessed `claim` for 29 of the 32 test posts and `experience`
for the other 3.

So the real problem turned out to be the training side, not the test side. I
was worried about measuring `advice` on 6 posts. I should have been worried
about teaching it from 24.

I am leaving the numbers where they are. My criteria were committed before this
run and the unit says the score isn’t what’s graded here, so changing anything
now to make the result look better would just hide the finding.

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

I used Claude throughout this project, so rather than pretend it was two small
moments, the two below are the ones where what came back actually changed a
decision I had made.

**Moment 1 — stress testing my label definitions (Milestone 2)**

- *What I asked for:* I gave it my three definitions and asked it to write eight
  posts that would sit right on the boundaries between them, then tried to
  classify those eight myself.
- *What came back:* Eight posts, and I could only cleanly label four of them.
  The four that broke were "anyone in a dead-end team should move" (an
  instruction, but not aimed at one person), "I’m so tired of this industry"
  (about the writer, but nothing actually happened), and two that started
  personal and ended general.
- *What I changed:* I added two rules. Advice covers instructions to people in
  general, not just to the poster. Experience covers feelings and not just
  events. And I took the word-count tie-break from the staff taxonomy for posts
  that start personal and end general. Without this I would have hit all four
  of those cases while labelling 200 posts and decided them differently each
  time.

**Moment 2 — checking my criteria were actually checkable (Milestone 3)**

- *What I asked for:* The milestone says not to let a model write your criteria,
  so instead I asked whether each one could be verified by somebody who
  couldn’t ask me what I meant.
- *What came back:* Four were fine. My confidence criterion wasn’t. I had
  written it as a threshold, something like "predictions the model is over 80%
  sure about should be right 80% of the time", and it turns out the notebook
  doesn’t report confidence that way at all. It sorts the test predictions and
  reports accuracy for the most sure third and the least sure third.
- *What I changed:* I rewrote criterion 5 as a gap between those two thirds
  instead of a threshold. Then I worked out that 32 test posts means about 10
  per third, so accuracy there only moves in steps of 10 points, and set the
  target at 15 points so it needs at least 2 more correct. If I hadn’t checked,
  I would have filed a criterion I had no way of producing a verdict for.

**Pre-labelling disclosure:**

Yes, I pre-labelled. The `note` column in labels.csv says which rows are which.

- **20 rows marked `cold`** — I labelled these myself, no AI, before I had seen
  any machine-generated label. Chosen at random across the whole file.
- **6 rows marked `self`** — also mine, but I wasn’t being careful, so I didn’t
  count them toward the cold check.
- **182 rows marked `pre-labelled, checked`** — Claude labelled these using my
  definitions and my decision rules. I read every one afterwards. I agreed with
  all of them and didn’t change any.

I also used Claude for the write-ups in this README, for a converter script
(`make_labels.py`) that turns my raw collected text into labels.csv, and to set
my labels in the notebook.

The two things it did not do were pick my community and collect my posts, and
label the cold 20. I did those, and I did the cold 20 before seeing any AI
labels on purpose, because next unit’s agreement report is supposed to measure
how consistent I am and it would measure nothing if I had looked first.

### Unit 6 update

**Moment 3 — reading my own confusion matrix**

- *What I asked for:* I gave Claude `results_three_seeds_before.json` and asked
  what the matrix was actually saying, rather than asking whether the numbers
  were good.
- *What came back:* That my errors were entirely one directional. Nine real
  `experience` posts were called `claim` on seed 42 and zero went the other
  way, and the same asymmetry held on the other two seeds.
- *What I changed:* I had been treating `advice` as my only problem because it
  was the label sitting at 0.000. The direction of the `experience` errors
  pointed at a second problem I had not noticed: the one pair in my taxonomy
  with no written decision rule. That became a diagnosis in Verdicts and
  Diagnoses and the second item in What's Still Broken.

**Moment 4 — why my improvement failed**

- *What I asked for:* After the retrain came back worse, I asked for an
  explanation of why eleven more `advice` examples made the model less stable
  rather than better.
- *What came back:* That the eleven posts read as statements about the world,
  and are only `advice` if you know which question they were answering. That
  context lives in the thread and never reaches the model. So I had not added
  eleven `advice` examples, I had added eleven `claim` shaped sentences to
  `advice` while removing nine clean cases from `claim`.
- *What I changed:* My write-up of the result. I had been about to record it as
  "more data did not help", which would have been the wrong lesson. The actual
  lesson is that the examples have to carry the signal the label is defined by,
  and it matters enough that it changed what I would do next: collect posts
  with real directives in them rather than reclassify the ones I have.

**Disclosure for this unit**

Claude labelled the 30 staff posts in `my_staff_labels.csv`. I did not label
them myself. This is disclosed in full at the top of the Agreement Report,
along with what it costs: my agreement rate measures Claude's consistency with
staff rather than mine, so it cannot serve as evidence about whether my own 208
labels were consistent. I diagnosed criterion 2 from the baseline comparison
instead, and said so.

Claude also ran the notebook for me, wrote the prose in this README, and
checked my Milestone 1 and 2 numbers against the JSON files rather than against
what I had typed.

What I did myself in this unit was choose the improvement, and decide each
verdict.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

Both models scored on the same 32 held-out posts, read from `test_split.csv`.
The baseline is `facebook/bart-large-mnli` with no training, prompted with the
three definitions in `label_definitions.txt`.

The two commands I ran, in this order:

```
python baseline.py --trained results.json
python baseline.py --definitions no_definitions_bare_names.txt --out baseline_results_bare_names.json
```

The second one points at a file that does not exist on purpose. That is how
`baseline.py` falls back to bare label names, and it says so when it starts.

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.312 | 0.531 | +0.219 |
| Macro F1 | 0.271 | 0.350 | +0.080 |
| F1 for `advice` | 0.312 | 0.000 | -0.312 |
| F1 for `claim` | 0.500 | 0.651 | +0.151 |
| F1 for `experience` | 0.000 | 0.400 | +0.400 |

**What I predicted before I looked:**
<!-- Milestone 1 asks you to write this BEFORE seeing the trained numbers. A
     prediction made afterwards isn't one. -->

Written before I ran `baseline.py` at all, so I had neither column in front of
me except the 0.53 accuracy my own model already got in unit 5.

I think the baseline will do fine on `claim` and badly on the other two. My
`claim` definition says "states something general about the industry", and that
is the kind of sentence a general model can spot from the words alone. But the
line between `advice` and `experience` in my taxonomy is not in my definitions
at all. It is in the decision rule I wrote underneath them, the one that says an
instruction wins even when most of the post is the writer's own story. The
baseline never sees that rule. It only gets the one line definition.

So my guess is the baseline lands somewhere around 0.40 to 0.45 overall, and my
trained model beats it by about 10 points, with the whole gap coming from
`advice` and `experience` rather than from `claim`.

**What the gap actually means:**
<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

**How my prediction did:** right about `claim`, wrong about almost everything
else. `claim` was indeed the baseline's best label in both runs, 0.500 with
definitions and 0.667 with bare names, so that part held. But I predicted the
baseline would land around 0.40 to 0.45 and that my trained model would beat it
by about 10 points. Neither baseline landed in that range. One came in well
under at 0.312, the other well over at 0.594, and the second one beat my trained
model instead of losing to it. I also said the gap would come from `advice` and
`experience`. `experience` was right. `advice` went the opposite way from what I
said, and by a lot.

The thing I got most wrong was an assumption I did not know I was making: that
writing careful definitions would help a model that reads them. Measured, they
hurt.

**I ran the baseline twice, and the second run changes the answer.** The table
above uses my written definitions as the prompt, which is what `baseline.py`
does by default. I also ran it on purpose with bare label names, no definitions
at all, just the words `advice`, `claim` and `experience`, to measure what my
definitions were worth instead of assuming they were worth something.

| Measure | Baseline, bare names | Baseline, my definitions | Trained |
|---|---|---|---|
| Overall accuracy | **0.594** | 0.312 | 0.531 |
| Macro F1 | **0.512** | 0.271 | 0.350 |
| F1 for `advice` | 0.286 | 0.312 | 0.000 |
| F1 for `claim` | 0.667 | 0.500 | 0.651 |
| F1 for `experience` | 0.583 | 0.000 | 0.400 |

**My definitions made the baseline worse by 28 points of accuracy.** That is the
opposite of what I assumed when I wrote them. With the definitions in the prompt
the model called **26 of the 32 posts `advice`**, at a precision of 0.192, so it
was wrong about five times out of six that it said it. It had collapsed onto one
label.

I think I know why, and it is a lesson about prompts rather than about my
taxonomy. `baseline.py` slots each definition into the sentence `This post is
{}.` My `advice` definition is *"tells somebody to do something, either the
original poster or people in general"*, so the model is actually being asked
whether *"This post is tells somebody to do something, either the original
poster or people in general."* That is not a sentence. With bare names it gets
*"This post is advice."*, which is, and the predictions spread out sensibly into
19 `claim`, 12 `experience` and 1 `advice`, against a true split of 14, 12 and 6.

So my definitions are written for a human reading the README, not for a model
reading a prompt. They were never tested as a prompt until just now.

**The headline, and it is not the one I wanted:** against the stronger of the two
baselines, my fine-tuning added nothing. It lost. **0.594 against my trained
model's 0.531 on accuracy, and 0.512 against 0.350 on macro F1**, on exactly the
same 32 posts. A general model that has never seen one of my 208 labelled posts,
given nothing but my three label names, beats the model I spent the last unit
training.

This is the case the milestone warns about, so I am saying it plainly rather
than hiding behind the friendlier definitions column. **I am reporting the bare
names run, 0.594, as my real baseline.** Judging myself against the definitions
run would be picking the opponent I can beat.

**The second thing I did not expect is `advice`.** My trained model scores
**0.000** on it. Both baselines beat that, 0.286 with bare names and 0.312 with
definitions, so on my smallest label the untrained model wins no matter which
prompt it gets.

I went back to the confusion block in `results.json` to check it was not a
rounding artefact. All 6 `advice` posts in the held-out split were predicted
`claim`, and the `advice` column is zero all the way down. My model does not
predict `advice` at all, for any post. It did not learn the label badly. It
learned to stop using it.

That explains where its 0.531 comes from. `advice` is only 36 of my 208 posts,
about 17%, so a model that never predicts it can still reach 83% of the file.
Dropping a label it found hard is cheap in accuracy terms, and the training took
that trade. The bare names baseline did not take it. It still predicted `advice`
once, and when it did, it was right, at a precision of 1.000 on that one guess.

**What this sets up for the rest of the unit.** Two of my criteria already look
to be in trouble on seed 42, and I am writing that here rather than waiting to be
surprised by it:

* **Criterion 1** wants overall accuracy of at least 0.60 on all three seeds.
  Seed 42 gave 0.531, and my baseline gives 0.594 without training at all.
* **Criterion 2** wants every label at F1 0.45 or better on all three seeds.
  `advice` is at 0.000. A label the model refuses to predict cannot miss by a
  small margin.

Milestone 2 runs three seeds, so one unlucky split is not what decides either of
these. Milestone 4 is where I give them verdicts, and the agreement report from
Milestone 3 is the instrument that tells me whether the `advice` collapse is my
labelling or the model.



---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

**The device these numbers came from:** `cpu`, reported as CPU, on torch
2.14.1+cpu. Section 1 prints this and section 6 writes it into every entry of
`results_three_seeds_before.json`. It matters because two people running this
notebook on the same data with the same seed can get different numbers on
different hardware, so the device is part of the result rather than a detail
about my laptop.

All three seeds ran in a single execution of section 6, so these are a
comparable set. Each test split is 32 posts out of 208. Seed 42 reproduced the
accuracy and macro F1 in my committed unit 5 `results.json` exactly, which
tells me the run is repeatable on this machine.

### The three seeds, as section 6 printed them

| Measure | Seed 42 | Seed 7 | Seed 2024 | Spread |
|---|---|---|---|---|
| Overall accuracy | 0.531 | 0.625 | 0.562 | 0.094 |
| Macro F1 | 0.350 | 0.461 | 0.398 | 0.111 |
| F1 for `advice` | 0.000 | 0.000 | 0.000 | 0.000 |
| F1 for `experience` | 0.400 | 0.700 | 0.526 | 0.300 |
| F1 for `claim` | 0.651 | 0.684 | 0.667 | 0.033 |

**What the spread tells me.** Accuracy moved 0.094 across the three seeds. The
notebook's own reading is that this is enough that a criterion landing inside
that band cannot really be called either way. It sits just under the ten point
line, so I am not going to claim my dataset is too small on the strength of
accuracy alone. But macro F1 moved 0.111, which is over the line, and the
reason is visible one row further down.

`experience` swung from 0.400 to 0.700 depending only on which posts landed in
the test split. That is a 30 point swing on a label with 79 examples in the
file and about 12 in each test split. Nothing about the model changed between
those two runs. Only the draw did. So any statement I make about `experience`
from a single split is a statement about luck, and this is exactly what running
three seeds was supposed to expose.

`claim` is the opposite. It moved 0.033 across all three, which is the one
number here I would call stable.

**The row that decides most of this unit.** `advice` scored **0.000 on all
three seeds**. Not low, not jumpy, zero every time. I checked the prediction
totals in `results_three_seeds_before.json` and the model predicted `advice`
**zero times across all three runs**, on 96 test posts in total. This is not a
seed being unkind. The model has dropped the label entirely, and three
different splits all agree on that.

<!-- Verdicts belong to Milestone 4, and criterion 4 needs the agreement check
     from Milestone 3 before it can be filled in. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | at least 0.60 | 0.531 | 0.625 | 0.562 | **MISSED** |
| 2. Every label F1 (worst label shown) | at least 0.45 | 0.000 | 0.000 | 0.000 | **MISSED** |
| 3. Biggest label at most 50%, smallest at least 15% | 50% / 15% | 44.7% / 17.3% | same file | same file | **MET** |
| 4. Agreement with the staff set | at least 21 of 30 | 30/30 | 30/30 | 30/30 | **MET** |
| 5. Confidence gap between thirds | at least 15 points | 10.0 | 50.0 | 10.0 | **MISSED** |

Criteria 3 and 4 do not vary by seed. Criterion 3 is a property of `labels.csv`
and criterion 4 is measured against the staff set, not against a split.

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

Seed 42, printed by section 7 and typed in as text. Rows are the true labels,
columns are what the model guessed.

| true \ predicted | advice | experience | claim |
|---|---|---|---|
| **advice** | 0 | 0 | 6 |
| **experience** | 0 | 3 | 9 |
| **claim** | 0 | 0 | 14 |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

**Nine real `experience` posts were called `claim`, and zero real `claim` posts
went the other way.** That is completely one directional. The model has not
learned a boundary between `experience` and `claim` that it crosses in both
directions. It has learned to walk one way across it.

Reading the whole matrix rather than just the worst cell makes it starker. The
`advice` column is empty and the `experience` column holds 3. Everything else,
29 of the 32 posts, was called `claim`. On the other two seeds the model
predicted `claim` 24 and 25 times out of 32. So on all three splits it is doing
something close to guessing my largest label and occasionally conceding an
`experience`.

My taxonomy says `experience` reports the writer's own situation and `claim`
states something general about the industry. The direction of the errors says
the model treats a post as general unless something forces it not to, and that
nothing in my 208 examples taught it what that forcing thing is. The notebook
flags this pattern as pointing at my labelling rather than at the model, which
I cannot confirm from the matrix alone. That is what the agreement check in
Milestone 3 is for, and I will come back to this in the diagnosis.



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 | Overall accuracy on the held-out set | at least 0.60 | **MISSED** | 0.531, 0.625, 0.562. Only seed 7 clears it. The target had to hold across all three and it held on one. |
| 2 | Every label has an F1 of at least 0.45 | at least 0.45 | **MISSED** | `advice` scored 0.000 on all three seeds. `experience` also failed on seed 42 at 0.400. Only `claim` cleared it every time. |
| 3 | Biggest label at most 50% of labels.csv, smallest at least 15% | 50% / 15% | **MET** | `claim` is 93 of 208 at 44.7%, `advice` is 36 of 208 at 17.3%. Checked from the file, not from a run, so no seed can move it. |
| 4 | Agreement with the staff set | at least 21 of 30 | **MET**, with a caveat that matters | 30 of 30, so the arithmetic is unambiguous. But I did not produce those 30 labels, Claude did, and that is disclosed in the Agreement Report. The number is MET. The evidence is not mine. |
| 5 | Most confident third beats least confident third | at least 15 points | **MISSED** | 10.0, 50.0, 10.0 points. Passed once and failed twice. |

**Diagnoses**

### Criterion 2, and it causes criterion 1

I am taking these together because the second one is the first one's cause.

`advice` has an F1 of **0.000 on all three seeds**. Its precision and recall are
both 0, which does not mean the model guessed badly. It means the model made
**zero `advice` predictions across all 96 held-out posts** in three different
splits. It did not learn the label poorly. It stopped using it.

That one fact also explains criterion 1. The prediction counts per seed are
`claim` 29, 24 and 25 out of 32. A model that ignored every post and always
said `claim` would score 0.4375, and mine averages 0.573. So about 13 points of
my accuracy is real reading and the rest is the majority label.

**The cause is too few examples for the label, and the reason there were too few
is a labelling decision I made on purpose in unit 5.**

Here is the evidence, in the order that convinced me.

**First, the training counts.** The 70/15/15 split gives `advice` 24 training
examples against `claim`'s 65. Dropping a label that only covers 17% of the file
costs very little accuracy, and three independent splits all took that trade.
That is consistent with too few examples, but on its own it is just a
correlation.

**Second, and this is the part that settles it: the untrained baseline does
better.** `baseline.py` with bare label names and no training at all scores
**0.286 on `advice`**. With my definitions it scores **0.312**. Both beat my
fine-tuned model's 0.000.

That rules out the explanation I would otherwise have reached for, which is that
`advice` is simply not separable from text alone. A general model that has never
seen one of my 208 posts can find it. The signal is in the text. My training
data failed to teach a model that was looking right at it.

**Third, the labelling decision.** In unit 5 I had to choose how literally to
read my own rule that `advice` "tells somebody to do something". I chose the
literal reading: there had to be an actual directive, an imperative or a "you
should", and a recommendation stated as a fact about the world went to `claim`
instead. I documented eleven posts that this moved, things like "Embedded is a
good bet" and "tech adjacent fortune 500 is where it's at".

I defended that choice at the time on the grounds that the literal rule is
visible in the text and the broad one depends on thread context the model never
sees. I still think that reasoning was right. But the consequence was that I
took eleven of the clearest `advice` shaped posts out of a label that only had
36 of them, and handed them to the label that already had the most. I made my
thinnest class thinner to keep a rule clean.

**What I cannot claim.** The honest competing explanation is that I applied the
`advice` boundary inconsistently across my own 200, so there was no coherent
pattern to learn. The agreement check is the instrument that separates those
two, and because I did not label the staff set myself, it cannot do that here.
So I am naming too few examples as the cause on the strength of the baseline
comparison and the training counts, and recording that I have no direct evidence
about my own consistency.

### Criterion 2, the `experience` half

`experience` fails only on seed 42, at 0.400 against the 0.45 target, then
recovers to 0.700 and 0.526.

The precision and recall tell a cleaner story than the F1 does.

| Seed | Precision | Recall |
|---|---|---|
| 42 | 1.000 | 0.250 |
| 7 | 0.875 | 0.583 |
| 2024 | 0.714 | 0.417 |

Precision is high and recall is low on every seed. When the model says
`experience` it is almost always right. It just hardly ever says it. The posts
it misses go to `claim`, and they go one way only: on seed 42 the matrix shows
**9 real `experience` posts called `claim` and 0 real `claim` posts called
`experience`**.

**The cause is a boundary I never wrote a rule for.** My unit 5 taxonomy has one
written decision rule and it covers `advice` against `experience`, which I had
correctly identified as my hardest pair. I never wrote one for `experience`
against `claim`, because I did not think that pair was hard. The matrix says it
is the pair the model actually cannot cross.

My own README gives the supporting evidence. I recorded before training that
seven posts landed in `claim` "by elimination, not because the definition covers
them", all of them people responding directly to another person. A label that is
partly a container for leftovers is a label whose edge is soft, and the
direction of these errors says the model treats a post as general unless
something forces it not to.

### Criterion 5

The gaps were 10.0, 50.0 and 10.0 points against a target of 15.

**The cause is partly the model and partly a flaw in how I wrote the
criterion.**

The model half: a classifier that answers `claim` for 24 to 29 of 32 posts is
not varying its confidence in any meaningful way, so there is not much for the
thirds to separate.

The criterion half is my own fault and I would rather say it than let it pass.
With 32 test posts each third holds 10, so accuracy within a third moves in
steps of 10 points and the achievable gaps are 0, 10, 20 and so on. A target of
"at least 15 points" cannot be hit exactly. It silently means "at least 20". I
worked out the 10 post granularity when I wrote the criterion and still chose a
number that falls between two achievable values.

**That is not grounds for revising it.** The rule is that a criterion can be
revised only if it could not be measured, and this one measured fine. It
produced three clean numbers and a clear verdict. It was badly chosen, not
unmeasurable, so it stays at 15 and stays MISSED.

### Criterion 4, and why a MET is worth flagging

The arithmetic is 30 of 30 against a target of 21, so MET is the correct verdict
and I am not going to pretend otherwise.

But the point of that criterion, written in unit 5, was this: *"if I cannot
apply rules somebody else wrote at 70%, then I probably did not apply my own
rules the same way across my 200 either."* It was never really about the number.
It was the one measurement that could tell a labelling problem from a model
problem.

Claude produced those 30 labels, not me, which is disclosed in the Agreement
Report. So the criterion is MET and its purpose is unserved. That is the single
most expensive thing about this unit for me, because criterion 2 is exactly the
question it was built to answer, and I had to diagnose that miss from the
baseline comparison instead.

### What the misses have in common

Three of my five criteria missed, and two of the three come back to the same
root. `advice` at 36 posts was too thin to survive a 70/15/15 split, and I made
it thinner with a labelling rule I chose for clean reasons. Criterion 1 misses
because criterion 2 misses. Criterion 5 misses partly because a model that has
collapsed onto one label has no confidence structure left to measure.

That points at one fix rather than four, which is what milestone 5 asks for.

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

> **Disclosure: these 30 labels were produced by Claude, not by me.**
>
> I gave Claude the three staff definitions and the four decision rules from
> `data/staff_taxonomy.md` and had it label all 30 posts. I did not label them
> myself first.
>
> This matters for how the rate below should be read. The exercise is meant to
> measure whether **I** can apply a written rule I did not write, which is the
> only direct evidence available about whether my own 208 labels were
> consistent. Because I did not do it, the rate measures Claude’s consistency
> with staff and says nothing about mine. So where my diagnosis in Verdicts and
> Diagnoses would normally lean on the agreement check to separate a labelling
> problem from a model problem, it cannot, and I have said so there rather than
> borrowing evidence this number does not carry.
>
> The adjudication of each disagreement below is mine.

**Agreement rate:** 30 / 30 = **100%**

`agreement.py` found zero disagreements, so `agreement_results.json` holds an
empty disagreements list.

**Disagreements**

There are none. That is not a boast. It is the reason this section is worth
less than it should be, and I would rather say that than pad it.

The graded part of this milestone is adjudicating disagreements, and a run with
no disagreements produces no adjudication. Combined with the disclosure at the
top of this section, that means the one instrument in this unit that can tell a
labelling problem from a model problem produced nothing I can use.

**Was the set easy, or is the rule genuinely tight?**

`agreement.py` asks this when the rate comes back at 100%, so here is the
answer: neither, really.

The set was not easy. Staff marked 7 of the 30 as borderline in their own key,
with notes saying so:

| Post | Staff label | Why staff called it hard |
|---|---|---|
| sp_005 | `analysis` | Reads like a hot take for one clause, then two comparable numbers do the work |
| sp_010 | `analysis` | Hedged conclusion, tiny sample, but the observation is what the claim rests on |
| sp_014 | `hot_take` | The canonical rule 1 case. "so obviously" does the work, not the 3% |
| sp_019 | `hot_take` | Reads reflective, almost `reaction`, but it is a general claim about everyone |
| sp_020 | `hot_take` | Sounds observational and checkable in principle, but no count is given |
| sp_028 | `reaction` | "Third this year" is countable, but nothing is argued from it |
| sp_029 | `reaction` | Could be read as a wry take on shoe discourse, but it reports the writer’s own realisation |

What the rate reflects is that `data/staff_taxonomy.md` is an unusually tight
rule set. It gives three definitions, four ordered decision rules, and two
worked examples. sp_014 is almost word for word the example printed under rule
1. A rule set that specific leaves little room to drift, which is the opposite
of the problem I have in my own taxonomy.

**What the pattern in my disagreements tells me:**

With no disagreements there is no pattern in them. But there is a pattern in
where the difficulty was **predicted** versus where staff actually found it,
and it is worth recording.

Before the staff key was opened, nine posts were flagged as the hard ones:
5, 10, 14, 17, 18, 21, 23, 27 and 29. Staff flagged seven: 5, 10, 14, 19, 20,
28 and 29.

| | Posts |
|---|---|
| Both agreed were hard | 5, 10, 14, 29 |
| Staff found hard, I did not | 19, 20, 28 |
| I found hard, staff did not | 17, 18, 21, 23, 27 |

Every post in my own list came from one question: is this number load-bearing?
17 has a year in it, 18 has a pace, 21 has four minutes, 23 has eight weeks, 27
has twenty degrees. All of those sit on the `analysis` against `hot_take`
boundary, which is rule 1.

Staff’s extra three sit somewhere else entirely. 19 and 28 are the `reaction`
against `hot_take` boundary, which is rule 2. 20 is a different distinction
again: a claim that could be checked in principle but where no count is
actually given, so the writer is asserting rather than showing.

So the difficulty was looked for in one place and it was really in two. Rule 1
is loud and easy to remember, so it got applied everywhere, including to posts
it settles cleanly. Rule 2 is quieter and that is where the genuine ambiguity
sat.

That is the one transferable thing this exercise produced, and it points
straight at my own taxonomy. My hardest boundary is `advice` against
`experience`, and my written decision rule covers exactly that pair. The
boundary I never wrote a rule for is `claim` against everything else, which is
where seven posts ended up by elimination, and which my confusion matrix says
is absorbing nine `experience` posts in one direction with none coming back.

## The Improvement

**What I changed:**

I relabelled one boundary. Eleven posts moved from `claim` or `experience` to
`advice`. Nothing else changed: same 208 posts, same three labels, same five
criteria, same model, same hyperparameters, same three seeds.

The eleven are tagged `relabelled unit 6` in the `note` column of
`labels.csv`, so the change is auditable row by row.

| | Before | After |
|---|---|---|
| `claim` | 93 (44.7%) | 84 (40.4%) |
| `experience` | 79 (38.0%) | 77 (37.0%) |
| `advice` | **36 (17.3%)** | **47 (22.6%)** |

Criterion 3 still holds after the change: biggest label 40.4% against my 50%
cap, smallest 22.6% against my 15% floor.

**The boundary, and what I changed about it.** In unit 5 my rule said `advice`
"tells somebody to do something". I read that literally: there had to be a real
directive, an imperative or a "you should". A recommendation phrased as a fact
about the world went to `claim`. So these went to `claim`:

> "Embedded is a good bet, AI still struggles hard with low-level code..."

> "Trust me tech adjacent non faang fortune 500 is where it's at."

> "Any large non-tech company. Banks, insurance companies, big retail..."

Every one of them is answering somebody who asked what to do. Under the broader
reading they are all `advice`. I have now applied the broader reading, and I
applied it to all eleven rather than to the ones I liked.

**Which diagnosis pointed at it:**

Criterion 2. `advice` scored F1 0.000 on all three seeds, which meant zero
`advice` predictions across 96 held-out posts. My diagnosis named too few
examples as the cause and named the mechanism: a labelling decision I made on
purpose that moved eleven of the clearest `advice` shaped posts into the label
that already had the most. I wrote then that I had made my thinnest class
thinner to keep a rule clean. This undoes exactly that.

The baseline is what made this the fix worth trying rather than a guess. An
untrained model scores 0.286 on `advice` with bare label names and 0.312 with
my definitions. Both beat my fine-tuned 0.000. The signal is in the text, so
the problem is what I taught, not what can be learned.

**What I expect to happen, written before I ran it**

I do not expect this to fix the collapse, and I am recording that now so the
result is a measurement rather than a hope.

Eleven posts takes `advice` from 36 to 47. After a 70/15/15 split that is about
**33 training examples instead of 24**. That is a 37% increase on a number that
was already far too small. `claim` still has roughly 59 after the change. The
imbalance that made dropping `advice` a cheap trade for the model is reduced,
not removed.

So my prediction is:

1. `advice` F1 will still be **0.000 on at least one seed**, and I would not be
   surprised by all three.
2. Overall accuracy will move very little, within about 3 points either way,
   because `claim` is still the majority label and the model's easiest strategy
   has not changed much.
3. If anything moves, it will be `claim` precision, because `claim` lost nine
   of the posts it was absorbing.

What this run actually measures is **how far relabelling alone can carry this
problem**. If `advice` stays at 0.000 with 33 examples, then the honest reading
is that the boundary was never the main constraint and the label simply needs
more data, which is the one fix a relabelling cannot provide. That is a useful
thing to establish, and it is the thing I would act on first next time.

### Run Log — After

Same three seeds, same model, same settings. The only change is the eleven
relabelled rows. Written by section 6 with `RUN_LABEL = "after"` into
`results_three_seeds_after.json`.

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | at least 0.60 | 0.562 | 0.656 | 0.406 | **MISSED** |
| 2. Every label F1 (worst label shown) | at least 0.45 | 0.000 | 0.000 | 0.000 | **MISSED** |
| 3. Biggest label at most 50%, smallest at least 15% | 50% / 15% | 40.4% / 22.6% | same file | same file | **MET** |
| 4. Agreement with the staff set | at least 21 of 30 | 30/30 | 30/30 | 30/30 | **MET** |
| 5. Confidence gap between thirds | at least 15 points | 50.0 | 70.0 | 40.0 | **MET** |

### The two run logs side by side

| Measure | Before | After | Change |
|---|---|---|---|
| Accuracy, seed 42 | 0.531 | 0.562 | +0.031 |
| Accuracy, seed 7 | 0.625 | 0.656 | +0.031 |
| Accuracy, seed 2024 | 0.562 | **0.406** | **-0.156** |
| Mean accuracy | 0.573 | 0.542 | **-0.031** |
| Mean macro F1 | 0.403 | 0.370 | **-0.033** |
| Accuracy spread across seeds | 0.094 | **0.250** | **+0.156** |
| F1 `advice`, all three seeds | 0.000 | 0.000 | no change |
| F1 `experience`, seed 2024 | 0.526 | **0.000** | **-0.526** |
| Criteria MET | 2 of 5 | 3 of 5 | +1 |

**Did it help, and how do I know:**

**No. It made the model worse on average and much less stable, and it did not
move the label it was aimed at.**

Taking the three claims I committed before the run, in order:

**Prediction 1 was right.** I said `advice` would still be 0.000 on at least one
seed and possibly all three. It is 0.000 on all three, again, with zero `advice`
predictions across 96 held-out posts. Going from 24 training examples to 33 did
not get the label off the floor.

**Prediction 2 was wrong, and interestingly wrong.** I said accuracy would move
less than about 3 points either way. On seeds 42 and 7 it moved exactly that,
+0.031 on both. On seed 2024 it fell **15.6 points**, five times my stated
bound. I was right about the typical case and had no idea the worst case was
available.

**Prediction 3 was wrong.** I said any real movement would show up in `claim`
precision. `claim` barely moved. The label that moved was `experience`, up
0.232 on seed 42 and up 0.086 on seed 7, then straight to **0.000 on seed
2024**.

**The headline number is the spread.** Accuracy moved 0.094 across seeds before
and **0.250** after. The notebook flags anything over 0.10 as meaning the
dataset is too small or too lopsided for a stable measure. Before the change I
sat just under that line. After it I am at two and a half times it. One change
of eleven rows, and the same model on the same data now returns anything from
0.406 to 0.656 depending only on the draw.

Seed 2024 shows what that looks like from the inside. The model predicted
`claim` for **31 of 32** posts, `experience` once, `advice` never. Macro F1
0.197. That is a near total collapse onto one label, and before the change that
same seed was my middle result.

### Why I think it failed

The eleven posts I moved are, read as sentences, statements about the world:

> "Embedded is a good bet, AI still struggles hard with low-level code..."

> "Any large non-tech company. Banks, insurance companies, big retail..."

They are only `advice` if you know they were answering somebody who asked what
to do. That context is in the thread. It is not in the text, and the text is
all the model gets.

So I did not add eleven `advice` examples. I added eleven `claim` shaped
sentences to `advice`, and removed nine of the cleanest `claim` examples from
`claim`. `advice` already had an identifiable surface pattern in its imperatives
and its "you should", and I diluted it. The donor label lost clean cases at the
same time, which is the part I did not think about at all.

That is consistent with everything the run produced: `advice` did not improve
because the new examples do not look like `advice`, `claim` got slightly worse
on two seeds out of three, and the whole thing became unstable because two of
my three classes now have blurrier edges than they did.

**The uncomfortable part is that this is an argument I already made and then
overruled.** In unit 5 I chose the literal reading specifically because, in my
own words, it "is visible in the text" while the broad one "depends on thread
context the model never sees". In unit 6 I reversed that choice to get more
examples. The experiment says the unit 5 reasoning was correct and the unit 6
decision was not. I would rather have found that out by measuring it than kept
believing it.

### The one thing that did improve, and I do not fully trust it

Criterion 5 flipped from MISSED to MET. The confidence gap went from 10, 50, 10
to **50, 70, 40**, clearing my 15 point target on all three seeds for the first
time.

I am counting it as MET because that is what the numbers say. But I would not
call it a win from the improvement. The model on seed 2024 answers `claim` for
31 of 32 posts and still shows a 40 point gap between its most and least
confident thirds, which tells me the criterion is measuring how well calibrated
the confidence is **given** the predictions, not whether the predictions are any
good. A model can be reliably confident about a bad answer.

That is a flaw in my criterion rather than a success of my model, and it is the
second thing this unit has taught me about criterion 5, after the 10 point
granularity problem. It still stands as written and it is still MET.

## What's Still Broken

Two criteria are still missed after the improvement, and they are the same two
that were missed before it.

### Criterion 2, every label at F1 0.45 or better

Still missed, and in one respect worse. `advice` is at 0.000 on all three seeds
after the change, exactly as it was before. `experience` now fails too, falling
to 0.000 on seed 2024 where it had been 0.526.

**What I would do.** Two things, in this order.

First, collect 40 to 50 more `advice` posts, and be fussy about which ones.
This unit taught me what kind. The eleven I relabelled were recommendations
phrased as statements about the world, and adding them did nothing because the
thing that makes them `advice` is not in the text. What I need is more posts
that carry the signal `advice` actually has: an imperative, a "you should", a
"don't". They exist in quantity in threads where somebody asks for help, and I
know that because the 36 I already have came from there.

Second, write a decision rule for `experience` against `claim`. My taxonomy has
exactly one written rule and it covers `advice` against `experience`, which I
had identified as my hardest pair. My confusion matrix says the pair the model
cannot cross is the one I never wrote a rule for. I would write that rule first
and then relabel against it, because relabelling without a rule is how I got
the seven posts that landed in `claim` by elimination.

**Why I stopped.** The unit allows one change and I spent it. I picked the
relabel over collecting more posts because my diagnosis named the labelling
decision as the mechanism, and because it cost no collection time. The run says
that was the wrong trade: the diagnosis correctly identified that `advice` was
starved, and I chose the fix that fed it the wrong food.

### Criterion 1, overall accuracy of at least 0.60

Still missed, at 0.562, 0.656 and 0.406.

**What I would do.** Nothing directly. This one is downstream of criterion 2
and I do not think it is worth attacking on its own. A model that never
predicts one of three labels has a ceiling set by the other two, and mine is
sitting near it. Fix `advice` and this moves without being targeted.

**Why I stopped.** Same single change rule, and because chasing accuracy
directly would most likely mean changing a training setting, which my diagnosis
never pointed at.

### Not missed, but not sound either

Criterion 5 is MET after the change, at gaps of 50, 70 and 40 points. I am not
listing it as broken because it passed. I am listing it here because I no
longer believe it measures what I wrote it to measure. A model that answers
`claim` for 31 of 32 posts should not be able to clear a calibration target,
and mine does. The criterion tests whether confidence tracks correctness given
the predictions, not whether the predictions are worth having.

I have left it exactly as written, because the rule is that a criterion may be
revised only when it could not be measured, and this one measured fine twice.
It was badly designed, not unmeasurable.

### The thing that worries me most, which no criterion covers

My accuracy spread across seeds went from 0.094 to 0.250. Nothing in my five
criteria tests stability, so this does not show up as a miss anywhere, and it
is the number I would most want to fix. At a 0.250 spread, any single result I
report is close to meaningless on its own. If I were writing criteria again I
would spend one of the five on it.

**The gap between what I meant my labels to capture and what the model
learned:**

I meant the three labels to capture what a comment is **doing**, so that
`advice` instructs, `experience` reports, and `claim` asserts, which is a
distinction about the writer's purpose rather than their subject matter. What
the model learned is that comments assert: across six training runs and 192
held-out posts it predicted `advice` **zero times**, and my confusion matrix
shows the remaining errors running one direction only, with nine real
`experience` posts called `claim` on seed 42 and none coming back the other
way, which says it never found a reason to treat a post as anything but general
unless the wording forced it.

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
