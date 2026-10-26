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

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |  |  |  |
|---|---|---|---|
| **** |  |  |  |
| **** |  |  |  |
| **** |  |  |  |

**My biggest off-diagonal number, and what it means:**
<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->



---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->



---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** ___ / 30 = ___%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**2.**
> *The post:*
>
> *Staff said / I said:*
>
> *My call, and why:*
>
> *Which pile:*

**What the pattern in my disagreements tells me:**



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->



**The gap between what I meant my labels to capture and what the model
learned:**
<!-- Two sentences. Your confusion matrix is the evidence. -->



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
