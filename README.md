# Bokeh-Dashboard-Debate-Analysis
Project developed in Python 3.5 making use of Bokeh library to display opinion of users from the [Debate](http://www.lavanguardia.com/politica/elecciones/20160613/402479864119/en-directo-13j-debate-a-cuatro.html) of June 13, 2016 among the candidates for the presidency of the Government of Spain.

## Dashboard elements

![Alt text](https://github.com/ARomoH/Bokeh-Dashboard-Debate-Analysis/blob/master/Images/dashboard_image.png)

In the upper left, it can see 3 widget where can be entered the next information:
- **Political**: It can select all tweets where the name of a certain candidate appears.
- **Politic Party**: It can select all tweets where the name of a certain politic party appears.
- **Keywords**: It can select certain keywords that appear during the debate. It can be choosen from the following words **[españ, vota, catal, gana, pais, gobiern, corrup, euro, grecia, europ, cambio, trabaj, venez, mejor, perd, programa, refugiado, perd, independ, finan, violenc, empleo, terror, banc, vergüenza]**. The words have undergone a previous stemmer process for getting maximum number of matches with tweet texts.

Below the widgets, it can see 2 figures where the first one represents the mean of all hashtagg and mentions used in each tweet. And finally, it can see 3 graphs with the information of the number of positive, negative or neutral tweets gather every 5 minutes.

## Execution example
First you must be inside of proyect folder and then:
```
bokeh serve --show .
```
