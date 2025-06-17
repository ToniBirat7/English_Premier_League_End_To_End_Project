### **Viva Tomorrow: A Vision for the Future of Work**

**How Data Drift is Handled**

Refers to changes in the distribution of the input features over time. In our dataset, this could manifest
as changes in typical match statistics. For example, the average number of goals per game might increase or
decrease across seasons due to tactical evolution or changes in team strengths. Similarly, the distribution of
fouls, cards, or the frequency of home wins could shift. Suppose our model was trained on data with a higher
average number of shots per game, and the current match data starts showing a consistently lower average. In
that case, the model might struggle to make accurate predictions.

Threshold is 5%, which means if the distribution of a feature changes by more than 5% compared to the training data, we consider it as drift.

Visualization of the input features and their distributions over time can help identify these drifts. For instance, if the average number of goals per game has shifted significantly, we can visualize this change using a line chart or histogram.

We track all the metrics and log in the MLFlow server. If we detect a drift, we can retrain the model with the new data to ensure it remains accurate.

**ETL Pipeline**

**Read Report**
