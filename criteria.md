# Acceptance criteria — TakeMeter

Five criteria that say what "working" means for this classifier, written in
unit 5 **before** anything was trained.

**All five are yours this time.** None are given. You've had two projects of
practice.

An acceptance criterion names a number. *"The model is accurate"* is an
opinion. *"Every label has an F1 of at least 0.60 on the held-out set"* is a
criterion.

Under each, write a sentence or two on **why that number**. A reason that says
something about your data or your taxonomy earns credit — *"I picked 0.60 F1
for `reaction` because it's my smallest label and I only have about 50
examples of it"*. A reason that could be attached to any project does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

Not numbers that sound impressive. Three labels means a coin-flip guesser gets
about 33%, so a target of 0.40 is barely a target. Your number should sit
somewhere you'd honestly call useful.

**Cover at least three of these five areas.** They're here as prompts, not as a
form to fill in — a criterion that fits none of them is fine if it names a
number.

| Area | A question it could answer |
|---|---|
| Overall accuracy | How often does it need to be right to be worth using? |
| Per-label performance | Is one label allowed to be much worse than the others? |
| Balance | How lopsided can your label counts get before it's a problem? |
| Consistency | If someone else labelled the same posts, how often should you agree? |
| Confidence | Should a confident prediction be right more often than an unsure one? |

Two things worth knowing before you pick numbers, because both will affect
whether you hit them:

- **Your smallest label will have the jumpiest score.** If a label has 50
  examples, about 8 land in the test split. An F1 computed on 8 examples moves
  a lot between seeds. A target for that label should be looser than one for
  your biggest label, and saying so is a good reason.
- **Unit 6 tests across three seeds, and the target has to hold across all
  three.** A target of 0.65 against results of 0.71, 0.62, 0.68 is a **miss**.
  Pick with that in mind — it is stricter than it first sounds.

---

## 1. Overall accuracy is at least 0.60 on the held-out set, on all three seeds.

**Why this target:**

My biggest label is `claim` and it is about 44% of my file. So a model that
ignores the text completely and always guesses `claim` already gets 0.44. If I
set my target anywhere near that I am not really asking for anything. 0.60 is
far enough above it that the model has to actually be reading the post.

I did not go higher because I only have about 140 posts to train on, and the
difference between `advice` and `experience` is subtle enough that I got it
wrong myself when I stress-tested my own definitions in Milestone 2.

---

## 2. Every label has an F1 of at least 0.45 on the held-out set, on all three seeds.

**Why this target:**

My test split is only 30 posts and `advice` is my smallest label at about 26%
of the file, so about 8 `advice` posts land in test. Getting one of those 8
wrong moves recall by 12.5 points on its own.

A tighter target would just be measuring which seed I got lucky on, especially
since this has to hold across all three. So 0.45 is loose on purpose. It is
still a real target, because a model that gives up on a label and never
predicts it scores 0.

---

## 3. No label is more than 50% of labels.csv, and my smallest label is at least 15%.

**Why this target:**

This is the one I can check before training, straight from the file.

The project only requires that nothing goes over 70%, but 70% would be bad for
me specifically. At 70% my smallest label would have about 4 posts in the test
split, and I cannot honestly measure anything on 4 posts. Holding the biggest
label to 50% keeps my smallest at roughly 8 in test, which is already thin.

`claim` is sitting at about 44% right now, so this is tight, but it should
hold if I keep watching the counts while I collect.

---

## 4. I agree with the staff labels on at least 21 of the 30 posts, which is 70%.

**Why this target:**

data/staff_taxonomy.md says a rate in the 70s is normal and expected, so 70%
is the honest number rather than one I padded to look good.

The reason I care about it is that the staff set uses somebody else's written
rules, not mine. If I cannot apply rules somebody else wrote at 70%, then I
probably did not apply my own rules the same way across all 200 of my posts
either. That would explain a bad model better than the model itself being bad.

---

## 5. The most confident third of predictions is at least 15 points more accurate than the least confident third.

**Why this target:**

The notebook does not report confidence as a threshold. It sorts the test
predictions by how sure the model was, then reports accuracy for the most sure
third and the least sure third separately. With 30 test posts each third is 10
posts, so accuracy there moves in steps of 10 points. 15 points means the
confident third has to get at least 2 more right than the unsure third.

I picked a gap instead of a level because what I actually want to know is
whether the confidence number means anything at all. If both thirds score the
same then the confidence is noise, and I cannot use it to decide which
predictions are worth checking by hand.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 6 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Every label performs acceptably

         The model performs well on all labels.

         **Why this target:** ...

         > **Revised in unit 6:** Every label has an F1 of at least 0.60 on
         > the held-out set.
         >
         > **Why revised:** "performs well" gave me nothing to check. I
         > couldn't produce a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "Overall accuracy of at least 0.65" → "at least 0.55", because
            0.65 turned out to be optimistic for 200 examples.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
