# Reading notes (Milestone 1)

## The community I picked

r/cscareerquestions.

I picked it because there is a lot of text there and people
argue a lot. It is public so anyone can read it without an
account. I also already know the topic so I can tell when
someone is saying something real and when they are not, which
I think matters for labelling later.

One thing I noticed early: the main thread titles are mostly
questions, like "should I take this offer" or "am I bad at
communication". Questions don't really have an opinion in them
so I don't think I can label those. The opinions are all in the
comments. So I read comments instead of thread titles.

I read through about 6 or 7 threads. They were about offshoring,
AI taking jobs, leetcode interviews, work life balance, and a
couple of people asking for career advice. I ended up saving 184
comments while I was reading.

## Candidate distinctions

These are the differences I actually noticed while reading. Not
good vs bad, just different things people were doing.

### 1. Telling someone what to do vs just saying something

A lot of comments are advice. They are aimed at the person who
made the post and they usually say "you should" or just give an
order.

> "Switch teams the moment you realize you're in a dysfunctional
> environment. You can't change an org as a jr/mid level."

> "If you're not getting interviews then that tells you something
> else - rewrite resume if it needs it. Apply to even easier jobs.
> Maybe adjacent roles."

This was everywhere. Probably the most common thing in the whole
sub. It feels like its own category because the post is pointed
at a person, not at the world.

### 2. Something that happened to me vs a claim about the industry

Some comments are the person telling their own story. Usually
with real details like a salary or a number of years.

> "I received a promotion from 75k to 92k recently after seniors
> left. So I don't think I'll be getting much for a while."

> "I have had offshore developers near me for about 2 1/2 years
> and It is extremely painful."

Then other comments are about the whole industry and have nothing
personal in them.

> "Their goal is to turn software engineering into a low-wage job
> with no benefits. And to blame anything that goes wrong on
> humans."

> "Technology never eases anything it just then requires people to
> do more, slave like a robot."

These feel very different even though both are opinions. One is
reporting, one is declaring.

### 3. Gave a reason vs did not give a reason

Some people actually back up what they say. Not always with
numbers, sometimes just with a because.

> "Because the other fields with similar payscales have standardised
> exams. Lawyers have their bar, doctors have medical license exams,
> finance has their CFA"

> "Here's a counter argument I saw. If AI is really a 10x productivity
> boost, where are the businesses getting 10 years of work done in one
> year? There should be AI-enabled businesses cleaning up in the market."

And lots of people don't.

> "Yes, the critical thinkers are the most valuable. There are always
> problems to solve, critical thinkers/engineers specialise in problem
> solving."

That last one sounds like a reason but it just says the same thing
twice. I had to read it twice to notice.

### 4. Venting

Some comments are not making a point at all, the person is just
upset or tired.

> "I swear to god I'm going insane. It does not one shot my tickets,
> even after being given all the context I realistically can."

There is a lot of this in the AI threads and the job hunting threads.
Less of it in the advice threads.

## Things I am worried about

**Barely anyone cites a real checkable fact.** The starter file
label_definitions.txt has a label called `analysis` which is about
specific checkable facts like a stat or a date. I went looking and
found maybe 15 or 20 comments like that out of 184. If I use that
label I don't think I will have enough of them, and the project says
no label can be over 70% of the file.

So I probably should not just copy the example labels from the
starter. Those were for a running forum.

**Distinction 1 and 2 overlap.** A lot of advice comments also tell
a personal story, like "I moved cities and it worked, you should
move too". I don't know yet which one wins. That might be my hardest
boundary.

**Venting might be too small.** Lots of comments have a bit of
frustration in them but are still making a point. If I make venting
a label I need a rule for how much frustration is enough.

---

# Designing the labels (Milestone 2)

I went with three labels: `advice`, `experience`, `claim`.

I dropped the venting idea from my candidate list. There is a lot
of venting in the sub but almost none of it is only venting, it is
usually attached to a story or a point. So I folded it into
`experience` instead of making it its own label.

I also did not use `analysis` even though the starter file has it.
Like I said in my reading notes, there are maybe 15 or 20 comments
out of 184 that actually cite a checkable fact. That is not enough
to train on.

## Stress testing the definitions

The milestone says to get an AI to write eight posts that sit on my
boundaries and see if I can classify them. I did that with Claude.

These eight are made up. They are only for testing the definitions.
None of them go in labels.csv.

| # | The test post | What I said | Was it clean? |
|---|---|---|---|
| 1 | Honestly just move. I did it and it worked out. | advice | yes |
| 2 | I moved to Austin in 2021 and my salary went up 40k. | experience | yes |
| 3 | Anyone in a dead-end team should move. The market rewards people who move. | ??? | **no** |
| 4 | The market rewards people who move teams. | claim | yes |
| 5 | I'm so tired of this industry. | ??? | **no** |
| 6 | My manager told me soft skills matter more than code, and he's right, they matter more for everyone. | ??? | **no** |
| 7 | Don't bother with leetcode. | advice | yes |
| 8 | I've been doing this 15 years and the field has gotten worse. | ??? | **no** |

So four out of eight I could not do cleanly. That is worse than I
expected and I am glad I did this before labelling 200 things.

### What was broken

**Post 3.** My first definition of advice said it was aimed at the
person who posted. But "anyone should do X" is still an instruction,
it just isn't aimed at one person. I was going to have to decide this
200 separate times.

Fix: advice is any instruction, to the poster or to people in
general.

**Post 5.** My first definition of experience said it reports
something that happened to the writer. But nothing happens in post 5.
He is just tired. That is clearly not a claim about the industry
though.

Fix: experience also covers the writer's feelings, not just events.

**Posts 6 and 8.** These start personal and end general. Both labels
honestly fit and I went back and forth on both of them.

Fix: I stole the tie-break idea from the staff taxonomy in
data/staff_taxonomy.md. Whichever one takes up more words wins. It
is not a perfect rule but it is a rule, and I can apply it the same
way every time, which is the thing that matters.

### After the fixes

I ran the same eight again with the tightened definitions and got
all eight. Post 3 is advice, post 5 is experience, post 6 is
experience (the manager story is most of it), post 8 is claim (the
15 years is four words, the conclusion is the rest).
