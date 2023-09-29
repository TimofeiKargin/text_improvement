# text_improvement
Simple trial task. Performance is not so good, but as a first stage of job interviews - should be fine.

## Objective
Develop a tool that analyses a given text and suggests improvements based on the similarity to a list of "standardised" phrases. These standardised phrases represent the ideal way certain concepts should be articulated, and the tool should recommend changes to align the input text closer to these standards.

## How to use
Script needs two argumnts -- filenames of text sample and list of terms.

For example:

    python improv_text.py sample_text.txt terms.csv 

Output:

in today is meeting, we {discussed a variety -> conduct an analysis} of issues affecting our department. the weather was unusually sunny, a pleasant backdrop to our serious discussions. we came {to the consensus -> conduct an analysis} that we need to do better in terms of performance. sally brought doughnuts, which lightened the mood. {it is important -> conduct an analysis} to {make good use -> implement best practices} of what we have at our disposal. during the coffee break, we talked about the upcoming company picnic. we should aim to be more efficient and look for ways to be more creative in our daily tasks. growth is {essential for our -> implement best practices} future, but equally important is building strong relationships with our team members. as a reminder, the annual staff survey is due next friday. lastly, we agreed that we must take time to look over our plans carefully and consider all angles before moving forward. on a side note, david mentioned that his cat is recovering well from surgery.
