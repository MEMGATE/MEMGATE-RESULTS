# LM-1 labelling guide

**Written:** 23 October 2026, before any LM-1 answer was labelled. The labeller sees one item at a time: a question a chat assistant was asked about its past conversations with a user, the question's date, the reference answer, whether the question is an abstention question, and the assistant's final answer. The labeller does not see which memory arm or which model produced the answer. Items are shuffled.

## Label "right" when
- the answer gives the reference answer, or something that means the same: the same person, place or thing, or the same number in any form ("five", "5", "5 sessions");
- the reference names an alternative as "also acceptable", and the answer gives that alternative;
- for a fact that changed over time, the answer gives the updated value as the current one, even if it also mentions the earlier value;
- for a question about order, the answer gives the same order as the reference, in any wording;
- for a yes or no question, the answer's yes or no matches the reference, whatever else it adds (if it adds a wrong detail that contradicts the reference, label "wrong");
- for an abstention question (the reference says the information was not mentioned), the answer says the information was not mentioned or is not known. Naming what was mentioned instead is fine.

## Label "wrong" when
- the answer gives a different value, person, place, count or date;
- the reference has several parts and the answer misses or gets one wrong;
- the answer hedges between a right and a wrong value without choosing;
- the answer says the information is not available, for a question that is not an abstention question;
- for an abstention question, the answer gives a value instead of saying it was not mentioned.

## Rules
- Judge only the answer against the reference. Do not use outside knowledge, and do not judge the reasoning.
- A number with a different unit counts only if it is the same quantity ("two weeks" and "14 days" are the same; "2 weeks" and "2 days" are not).
- An answer cut off before it gives a value is "wrong".

## Conventions settled on dev (23 October 2026, before any main answer)
The dev labellers met these cases and decided them as follows; main labels follow the same:
- A value with "about", "around" or "close to" that names the reference value is right.
- "At least N" or "N or more" gives a bound, not a value, and is wrong.
- "3 weeks and 1 day" is not "3 weeks": a different quantity, wrong unless the reference allows it.
- A stated count that differs from the reference is wrong, even if a list after it has the right number of items.
- For an order question, the order must match the reference, with no item missing or wrong.
- A yes or no answer that matches the reference, with extra detail that does not contradict it, is right.
