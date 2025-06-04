@Backend_WebApp @Dummy_Datasets @Frontend_WebApp @Models

So, we are trying to build to a complete full fledge football website that is very similar to https://www.sofascore.com/. (SofaScore)

All the design and layour should be very similar to the SofaScore.

Below is the Description about each folder of our project:

Backedn_WebApp: It is the backend for our project, we will use the Django and Django Rest Framework.

Frontend_WebApp: We are using the Next.js project with React, TypeScript and No Tailwind.

Models: Contains the xgboost model that we will be using for the prediction.

Dummy_Datasets: There are two folders inside it. WebScrapping_Matches to simulate the scrapping of the web. It contains the csv file for all the match fixtures of the team for the 2025-26 Premier League Season. Our backend will provide this data to the frontend Next.js application through API.

Another folder is Input_Features_For_EPL_Teams, so these are the dummy input features for our model to predict that match. When the user in the frontend click run prediction for the match, we will take the names of the team and find their input features and then predict the outcome.

Below is the complete project workflow:

We will have frontend with best UI with attractive design especially football, English Premier League.

The frontend should show all the matches that are happening this week, and should provide all the details realted to the match. There should be a predict the match button for each match that the user can click and get the predictions.

Scrapping data should be fetched from the Backend and then Sever to the frontend Next.js.

We need to complete the project in step wise fashion and we will need to push the changes in our repo after implementing each fature.

Before starting the project, first create a Readme file describing our pipeline and plan to complete this project.

Based on the plan we will continue and complete our development.
