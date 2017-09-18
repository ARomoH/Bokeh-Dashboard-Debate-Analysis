# Bokeh-Dashboard-Debate-Analysis
Project developed in Python 3.5 making use of Bokeh library to display opinion of users from the [Debate](http://www.lavanguardia.com/politica/elecciones/20160613/402479864119/en-directo-13j-debate-a-cuatro.html) of June 13, 2016 among the candidates for the presidency of the Government of Spain.

## Dashboard elements
An image of the dashboard is shown below.
![alt text](https://raw.githubusercontent.com/ARomoH/Bokeh-Dashboard-Debate-Analysis/branch/Images/dashboard_image.png)

In the upper left, it can see 3 widget where can be add the next information:
- **Political**: It can select all tweets where the name of a candidate appears.
- **Politic Party**: It can select all tweets where the name of a politic party appears.
- **Keywords**: It can select certain keywords that appear during the debate. It can be choosen from the following **[españ, vota, catal, gana, pais, gobiern, corrup, euro, grecia, europ, cambio, trabaj, venez, mejor, perd, programa, refugiado, perd, independ, finan, violenc, empleo, terror, banc, vergüenza]**. To these words were applied a stemmer process to get maximum number of matches.

## Execution example
First you must be inside of proyect folder and then:
```
bokeh serve --show .
```
