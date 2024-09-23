I started this project because I wanted to understand Toronto's city councillors when it comes to enacting similar policies and behaving in municipal politics. I went in just wanting to see if councillors would group together at all, and I was pleasantly surprised to see that they do!

## What is this?

The idea behind this graph is that we can group councillors together based on how they vote in council meetings. Each point represents a different councillor. Councillors who vote together are grouped closer to one another. 

It's interesting how some patterns emerge! For example, when limiting the graph to the year 2020, councillors are much closer to each another than in other years.

## How it works

First, I downloaded the past City Council voting records from [Toronto's Open Data Catalogue](https://open.toronto.ca/dataset/members-of-toronto-city-council-voting-record/). These files record how over 90 city councillors have voted on municipal agenda items dating back to 2009. (One of the source files is labelled as dating from 2006, but it isn't complete.)

In the example below, we can see that Alejandra Bravo voted "yes" to agenda item "2023.FM1.8", which carried 25-1:

|_id|Term|First Name|Last Name|Committee|Date/Time|Agenda Item #|Agenda Item Title|Motion Type|Vote|Result|Vote Description|
|--|--|--|--|--|--|--|--|--|--|--|--|
|3|2022-2026|Alejandra|Bravo|City Council||2023.FM1.8|Election of the Speaker and Deputy Speaker|Nomination of a Member|Yes|Carried, 25-1|Majority required - Appoint Councillor Nunziata as Speaker|

I gathered all these rows and reformated them into a new table. The table above has each vote on a separate row, but for my purposes, I needed to concentrate the rows to show how a given councillor voted for **all** agenda items. For example:

|Councillor|2009.IA30.5|2009.RM30.5|2009.EX28.8|(skipping thousands of items)|2024.PB16.9|
|--|--|--|--|--|--|
|Maria Augimeri|No|Absent|Yes|...|N/A|

Then, because algorithms work much better with numerical data, I converted each vote into a number.
- 1 for "Yes"
- 0 for "No"
- -1 for "Absent" or "N/A" *(I tried -2 for N/A and results were very similar)*

This results in a table like the following:

|Councillor|2009.IA30.5|2009.RM30.5|2009.EX28.8|(skipping thousands of items)|2024.PB16.9|
|--|--|--|--|--|--|
|Maria Augimeri|0|-1|1|...|-1|

Now if you remember high school math, you can graph points using x-y coordinates, where x tells you how far to go left and right, and y tells you up or down. Why am I mentioning this?

Well, if we could simplify this table down to just 2 or 3 columns for each councillor, we could graph them! But how in the world can we do that?

Luckily for you, there's a technique called [dimensionality reduction](https://www.ibm.com/topics/dimensionality-reduction)! Imagine that for agenda items #1 and #2, the results were exactly the same, right down to who voted yes or no, and who was absent. In that case, item #2 confirms the councillors' behaviour but it doesn't tell us anything new about them when compared to item #1. So we can safely remove either one of the items because no new information is gained.

What this technique allows us to do is to simplify this table down to just a few columns, which is just what we wanted! After that, we can graph each councillor as a point where the coordinates are the reduced columns. *For this reason, I'm hesitant to label the axes as "Conservative" or "Liberal" because the algorithm doesn't necessarily pick up on that, as it would be a subjective interpretation of the data.*

Next, spend an hour [clustering](https://www.nvidia.com/en-us/glossary/k-means/) and trying out colours based on groupings. Spend weeks to months figuring out how to add some fancy buttons and sliders for a nice UI. Voilà! You've got your interactive graph.