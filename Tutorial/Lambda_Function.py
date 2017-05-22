
Lambda Function:

Lambda is a un-named function in Python:
The syntax for Lambda is 

<lambda parameters: expression>
Lambda expression cannot contain loops or branches but can contain conditional operators.

eg: testfunction = lambda x: x**2 if x == 2 else 10
>>> testfunction  = lambda x: x**2 if x == 2 else 10
>>> type(testfunction)
<class 'function'>
>>> testfunction(2)
4
>>> testfunction(3)
10
>>>


Lambda returns a function that is assigned to testfunction in this specific case. 
The first position  x is the positional variables that are being passed to the function lambda that is defined after the : . 


Another example of creating a function to calculate area of a rectangle:

>>> AreaRectangle = lambda length, breadth: length*breadth
>>> AreaRectangle(10,5)
50

Same function can be written in traditional function defination form as below:

>>> def AreaRectangle(length, breadth):
...     return length * breadth
...
>>> AreaRectangle(10,5)
50
