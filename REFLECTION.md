# Reflection — W9 TDD Lab

## 1. How many tests did you write in Part A, and how many lines of production code? What is the ratio?

`test_kitchen.py` ends with 9 test functions, which come to 34 non-blank, non-comment lines. `kitchen.py` has 40 non-blank lines. That is about 0.85 lines of test for every line of production code, or roughly one test per 4–5 lines of code. Along the way I wrote one more test, `test_multiplication_by_two`, and deleted it in A3 once the value-object test covered multiplication by 2. So the number of tests that pushed the design was a bit higher than the final count.

## 2. When was your bar red for the longest time, and what made it last so long?

The longest red was `test_mixed_addition` in A7. It stayed red for four commits: the AttributeError for the missing `add_rate`, the empty `add_rate` that gave `Quantity(201, 'g') != Quantity(228, 'g')`, the step that added the rate table, and the step that changed `reduce` to take the converter. It lasted so long because I followed the order in the handout and ran the tests after each change. The first two changes were only plumbing: the rates were stored and the converter was passed in, but nothing used them yet, so the bar could not turn green until the third change, where `Quantity.reduce` multiplies by the rate. Reading the `201` before changing anything made the cause clear: `Sum.reduce` was adding raw amounts and ignoring units.

## 3. Find one place where you used Fake It, one where you triangulated, and one where you used Obvious Implementation. Was each choice right?

- **Fake It**: in A1, `times` set `self.amount = 600`, and in A6, `plus` returned `grams(500)` while `Converter.reduce` returned its argument. Both were right. Each one proved the test was wired up, and the fake constant was gone within one or two commits. In A6 the fake made the next step (returning a `Sum`) much smaller.
- **Triangulate**: in A2, `test_multiplication_by_two` broke the faked 600 and forced `amount * multiplier`. For something as simple as multiplication this was more ceremony than I needed, but it showed me how a second example removes a constant.
- **Obvious Implementation**: in A8, `Sum.times` was a single line that applies `times` to both operands, and it went green the first time. That was right, because the design from A6 and A7 already made the answer obvious. If I had needed to restructure `plus`, that would have been a sign to slow down.

## 4. Which items are still on your test list? Which would you implement next, and which should you delete because they were speculation?

Only `__hash__` is left. Defining `__eq__` without `__hash__` makes `Quantity` unhashable, but no test or caller has needed a set or dict key yet. Other things occurred to me but are not on the list because no test demanded them: comparing a `Quantity` to a non-`Quantity` (right now `__eq__` would raise AttributeError), a missing conversion rate (raises KeyError), and reducing a `Sum` of two different non-target units. Next I would implement the non-`Quantity` equality case, because an exception from `==` is surprising. I would delete `__hash__` from the list until a real use needs it, because right now it is speculation.

## 5. Look at Quantity.reduce. If you had designed the whole system on paper first, would you have written this method?

Probably not. On paper I would have put the conversion logic in one place, perhaps a function that takes two quantities and a rate. `Quantity.reduce` exists because `Converter.reduce` needed to treat a `Sum` and a single `Quantity` the same way. Once `Sum` had `reduce`, giving `Quantity` the same method was the smallest change that let the converter delegate without checking types. The polymorphism appeared from the tests, not from a design I made up front.

## 6. In Part 0 you wrote the tests after the code, and in Part A before it. How did the two feel different, and which tests shaped your design?

In Part 0 the tests felt like checking someone else's work. I read the docstring, chose inputs from each block and its edges, and looked for places where the code disagreed. That is how the three bugs in `shipping_fee` showed up: weight 0, exactly 1 kg, and the "started kilogram" above 5 kg. The tests did not change the shape of the code, only its correctness. In Part A the tests came first and decided the API. `test_multiplication_returns_a_new_quantity` turned `Quantity` into a value object. `test_equality` added `__eq__` because comparing `.amount` everywhere was clumsy. `test_simple_addition` introduced `Converter` and `Sum`, and `test_mixed_addition` made the converter travel with `reduce`. Writing the test first felt slower step by step, but I never had to debug for long, because each red bar had exactly one cause.
