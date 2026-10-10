# Reflection — W9 TDD Lab

## 1. How many tests did you write in Part A, and how many lines of production code? What is the ratio?

`test_kitchen.py` ends with 9 test functions, which come to 34 non-blank, non-comment lines. `kitchen.py` has 40 non-blank lines. That is about 0.85 lines of test for every line of production code, or roughly one test per 4–5 lines of code. Along the way I wrote one more test, `test_multiplication_by_two`, and deleted it in A3 once the value-object test covered multiplication by 2. So the number of tests that pushed the design was a bit higher than the final count.

## 2. When was your bar red for the longest time, and what made it last so long?

The longest red was `test_mixed_addition` in A7. It stayed red for four commits: the AttributeError for the missing `add_rate`, the empty `add_rate` that gave `Quantity(201, 'g') != Quantity(228, 'g')`, the step that added the rate table, and the step that changed `reduce` to take the converter. It lasted so long because I followed the order in the handout and ran the tests after each change. The first two changes were only plumbing: the rates were stored and the converter was passed in, but nothing used them yet, so the bar could not turn green until the third change, where `Quantity.reduce` multiplies by the rate. Reading the `201` before changing anything made the cause clear: `Sum.reduce` was adding raw amounts and ignoring units.

## 3. Find one place where you used Fake It, one where you triangulated, and one where you used Obvious Implementation. Was each choice right?

**Fake It.** I used it twice: in A1 (`self.amount = 600`) and in A6 (`plus` returns `grams(500)`, `reduce` just hands back whatever it gets). The A1 one honestly felt pointless. I knew the formula, so typing 600 felt like pretending. A6 was different. I didn't really know yet how `plus`, `Sum` and `Converter` should fit together, and faking the whole thing first meant I only had to replace one piece at a time instead of designing all three in my head at once. So I'd say both were the right call, but A6 is the one where I actually felt the benefit.

**Triangulate.** A2, where `times(2)` should give 400. It killed the 600 straight away, and with two examples pulling different ways the real formula was the only thing that worked. For plain multiplication this was more steps than I needed (I could see the answer from the start), so in a real project I'd probably skip it here. I think it's more of a habit for when I *can't* see the rule yet.

**Obvious Implementation.** A8, `Sum.times`. One line, scale both sides, green on the first run. That was the right choice because by then A6 and A7 had already set up the design. It almost felt like the code had been waiting for that method. If it had gone red in a way I didn't expect, I'd have gone back to smaller steps.

## 4. Which items are still on your test list? Which would you implement next, and which should you delete because they were speculation?

Only `__hash__` is left. Defining `__eq__` without `__hash__` makes `Quantity` unhashable, but no test or caller has needed a set or dict key yet. Other things occurred to me but are not on the list because no test demanded them: comparing a `Quantity` to a non-`Quantity` (right now `__eq__` would raise AttributeError), a missing conversion rate (raises KeyError), and reducing a `Sum` of two different non-target units. Next I would implement the non-`Quantity` equality case, because an exception from `==` is surprising. I would delete `__hash__` from the list until a real use needs it, because right now it is speculation.

## 5. Look at Quantity.reduce. If you had designed the whole system on paper first, would you have written this method?

Probably not. On paper I would have put the conversion logic in one place, perhaps a function that takes two quantities and a rate. `Quantity.reduce` exists because `Converter.reduce` needed to treat a `Sum` and a single `Quantity` the same way. Once `Sum` had `reduce`, giving `Quantity` the same method was the smallest change that let the converter delegate without checking types. The polymorphism appeared from the tests, not from a design I made up front.

## 6. In Part 0 you wrote the tests after the code, and in Part A before it. How did the two feel different, and which tests shaped your design?

Part 0 felt like marking someone else's homework. The code was already there, so I just read the docstring, picked weights from each block and right on the edges, and waited to see what broke. That's how all three bugs in `shipping_fee` turned up: 0 kg wasn't rejected, exactly 1 kg cost 60 instead of 40, and 5.2 kg cost 60 instead of 70 because the extra weight got rounded down. The edges were where everything went wrong, which is basically what we learned in Weeks 3 and 5. But none of those tests changed what the code looked like. They only told me whether it was right.

Part A was the opposite. I was writing tests for code that didn't exist yet, so the tests were the first thing that ever *used* `Quantity`, and that's where the design came from. `test_multiplication_returns_a_new_quantity` is the one that surprised me most. `times()` was changing the object in place, the test called it twice, and suddenly `Quantity` had to become a value object. Nobody told me to make it immutable, a failing test did. After that, `test_equality` gave me `__eq__` (comparing `.amount` everywhere was getting annoying), `test_simple_addition` gave me `Sum` and `Converter`, and `test_mixed_addition` is why the converter gets passed into `reduce`.

Test-first felt slower while I was doing it, especially running tests I already knew would fail. But looking back, I never got stuck debugging, because every time the bar went red there was only one thing that could have caused it.
