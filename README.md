# Toronto City Council Clustering
Cluster Toronto city councillors by how they vote on municipal items.

Data obtained from City of Toronto's [Open Data](https://open.toronto.ca/dataset/members-of-toroxnto-city-council-voting-record/).

![Toronto City Councillors by Voting Records](notebooks/output/city-councillors-3.png "Toronto City Councillors by Voting Records")

**Deployed at https://toronto.klogg.blog/.**

## Ideas
- Add search/dropdown by name
- Click on point to go to their website?
- Make legend easier to parse
- Highlight by person (dropdown?)
- Filter by agenda topic (policing etc) (hard?)
- Add social icons
- Review explanation
- Add 'yes', 'no' and 'absent' votes to hover text
- Use hovertemplate and annotations to customize hover text? https://github.com/plotly/dash-sample-apps/blob/main/apps/dash-clinical-analytics/app.py#L180
- Figure out how to make legend not hide points in 2D
- Try making N/A votes the average of a given councillor's other non-N/A votes
