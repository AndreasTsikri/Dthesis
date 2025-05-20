# Dthesis

This is the main repo for my diploma thesis code(2022). The code used for an optimization problem, the workflow is very helpfull as it can be used in general for any optimization problem. There are two parts of the thesis **optimization process** were we use the physical solver together with an optimizer and **machine learning regression** were we use the physical solver results in order to train a machine learnign algorithm and check if we can accurately replace the physical solver in the specified domain!

From an initial airfoil distribution(Xi, Yi points) taken from DTU university(ffas241) we first interpolate the data using the **PARSEC parametarization** technique to get the function definition and to get parsec coefficients. These coefficients are our design variables - variables that controlling the shape of the airfoil

# Problem Description
The noise emissions are considered a main issue in the operation of a Wind Turbine. Noise is coming from the interaction of the wingsof the wind turbine with the moving airflow. A great part of this noise is dependent on the wing's **airfoil shape**, here in this thesis we will **try to find an airfoil shape that minimizes noise emissions**. 

The problem is considered an optimization problem - minimization of an objective function(noise emission) that are dependent on 9 design variables(the shape of the airfoil).In plain text, the question that need to be answered is "what is the shape of the airfoil in each position of the wing in order to have minimum total noise emissions". 

For noise calculation we use a physical solver that has been developed in the National Technical University of Athens inside the Fluid Dynamics department. For the shape of airfoil a function with 4 variables for each airfoil side(up and down) is used.

Optimization is an iterative process, here we use the **Particle Swarm Optimization(PSO)**, a metaheuristic optimization algorithm. For each iteration we use the in-house solver to get the noise emissions. After collecting all the data from all runs we use **machine learning algorithms** to see if we can reduce the time of simulation. Finally, we train 2 linear machine learning models(Lasso and simple linear regressor) and a non-linear Neural Network.  

More detail on the problem can be found on the diploma thesis on [this](https://dspace.lib.ntua.gr/xmlui/handle/123456789/56355?locale-attribute=en) link of the final thesis.

# Optimization Workflow
In order to use an optimization algorithm we want to find a description of the geometry in the form of g(xi), where xi: design variables , g: output geometry shape of airfoil and then connect the geometry g with the produced noise from the wind turbine N, so we finally have N(g(xi)) that has to be minimun, of course we do not have an analytical form of N but we can compute it arithmetical using the in-house solver. The problem is unbound so we will reach solution inside specified limits of the initial geometry that we must optimize.

The algorithmic workflow is :
```
                                         +----------------+  
                                         |  Initialize xᵢ |  
                                         +----------------+  
                                                   |  
                                         +--------------------+  
                                     |-> |  Parameterization  |  
                                     |   +--------------------+  
                                     |             |    
                                     |   +----------------------+  
                                     |   |  Find gᵢ (Geometry)  |  
                                     |   +----------------------+  
                                     |             |  
                                     |   +----------------------+  
                                     |   |  Compute Nᵢ (Noise)  |  
                                     |   +----------------------+  
                                     |             |   
                             (loop)  |   +--------------------------+  
                                     |   |  Update xᵢ(Search Step)  |  
                                     |   +--------------------------+  
                                     |             |             
                                     |   +-------------------------------+  
                                     |   |  Optimization Criterion met?  |  
                                     |   +-------------------------------+  
                                     |             |             |  
                                     |          No |             | Yes                 
                                     |        +----------+    +-----+
                                     |        | (new xi) |    | End |       
                                     |        +----------+    +-----+
                                     |             |              
                                     |_____________|              
```
The **optimization algorithm** that is used in this project is the implementation of **Particle Swarm Optimization (PSO)**, a metaheuristic algorithm. More details of the implementation can be found in [pyswarms](https://pypi.org/project/pyswarms/)

# Machine Learning Workflow
We used 3 regression models in the process, 2 linear regressors(Linear regressor and Lasso) and one non-linear Neural Network. The linear models will tell us 1) can we use a (relative) easy linear relationship between design variables and output and to predict the result 2)What variables play the most crusial role in this process(Lasso example). The NN as it is approved as a general approximator is expected to have better results, and it finally has(over 98%!). 

The workflow is :
```
                                  +-------------------------------------------------+  
                                  | Collect Data from optimizaion Process (xᵢ, Nᵢ)  |
                                  +-------------------------------------------------+  
                                            |  
                                  +----------------------------------------------------------+  
                                  |  Pick model using sklearn library(i.e Linear Regressor)  |  
                                  +----------------------------------------------------------+  
                                            |    
                                  +--------------------------------+  
                                  |  Set up model hyperparameters  |  
                                  +--------------------------------+  
                                            |  
                                  +---------------------------------+  
                                  |  Split to 80/20 train-test set  |  
                                  +---------------------------------+  
                                            |   
                                  +---------------------+  
                                  |  Fit on train Data  |  
                                  +---------------------+  
                                            |   
                                  +--------------------------+  
                                  |  Evaluate on  test Data  |  
                                  +--------------------------+  
```
