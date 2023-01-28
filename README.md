# print

	printf("Hello World") # C+ style

	print("Hello World") # Python style

# Operations + - * / % **

	print(1 + 1) # 2
	print(1 - 1) # 0
	print(1 * 1) # 1
	print(1 / 2) # 0.5
	print(8 % 3) # 2
	print(2 ** 3) # 8
	
# Variables in python

	# Variables are used to store data values.
	# Variables do not need to be declared with any particular type, and can even change type after they have been set.
	# Python has no command for declaring a variable.
	# A variable is created the moment you first assign a value to it.
	# Variables are case-sensitive.
	# Variables can be of any length.
	# Variables can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ ).
	# Variables names cannot start with a number.
	# Variable names are case-sensitive (age, Age and AGE are three different variables).
	
	# Assigning values to variables
	# Python has no command for declaring a variable.
	# A variable is created the moment you first assign a value to it.

	foo, bar, baz = 1, 2, 3
	x = 5
	y = "John"
	print(x)
	print(y)
	
	# Assign Value to Multiple Variables
	x, y, z = "Orange", "Banana", "Cherry"
	print(x)
	print(y)
	print(z)
	
	# Assign the same value to multiple variables in one line
	x = y = z = "Orange"
	print(x)
	print(y)
	print(z)
	
	# Output Variables
	# The Python print statement is often used to output variables.
	# To combine both text and a variable, Python uses the + character:
	x = "awesome"
	print("Python is " + x)
	
	# You can also use the + character to add a variable to another variable:
	x = "Python is "
	y = "awesome"
	z =  x + y
	print(z)
	
	# For numbers, the + character works as a mathematical operator:
	x = 5
	y = 10
	print(x + y)
	
	# If you try to combine a string and a number, Python will give you an error:
	x = 5
	y = "John"
	print(x + y)
	
	# Global Variables
	# Variables that are created outside of a function (as in all of the examples above) are known as global variables.
	# Global variables can be used by everyone, both inside of functions and outside.
	
	# Create a variable outside of a function, and use it inside the function
	x = "awesome"
	
	def myfunc():
	  print("Python is " + x)
	
	myfunc()
	
	# If you create a variable with the same name inside a function, this variable will be local, and can only be used inside the function.
	# The global variable with the same name will remain as it was, global and with the original value.

	x = "awesome"
	
	example: Шартнома 600 бетли ва Jakhongir 250 марта берилган

	HW 
	foo = 5
	print(foo+3)
	

# Grouping of  func

    # print hull year
    # show all days and mounth in one year

    # do not repeat code

    mounth()
        print(1)
        print(2)
        print(3)
        print(4)
        print(5)
        ...
        print(28)

    mounth_short()
        print(29)
        print(30)
    
    mounth_long()
        mounth_short()
        print(31)


    mounth_short()
        mounth()
        print(29)
        print(30)

# Params

    # params is a variable
    # params is a value

    foo(bar)
        print(bar + 1)

    # params can be many
    hello(first_name, surname, age)
        print('Hello', first_name, surname + '!')
        print('You are', age, 'years old')

## HW 
    # Hello World!
    foo(bar)
        ...

    foo("Hello")


    mounth(name)
        print(name)
        print(1)
        print(2)
        ...

    short_mounth(name)
        mounth(name)
        print(29)
        print(30)

    long_mounth(name)
        short_mounth(name)
        print(31)

## if else

    # if else
    # if elif else
    # if elif elif else

    # if
    if condition:
        print('Hello')

    # if else
    if condition:
        print('Hello')
    else:
        print('World')

    # if elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    else:
        print('!')

    # if elif elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    elif condition:
        print('!')
    else:
        print('Goodbye')

    # if elif elif elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    elif condition:
        print('!')
    elif condition:
        print('Goodbye')
    else:
        print('Goodbye')

    # if elif elif elif elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    elif condition:
        print('!')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    else:
        print('Goodbye')

    # if elif elif elif elif elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    elif condition:
        print('!')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    else:
        print('Goodbye')

    # if elif elif elif elif elif elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    elif condition:
        print('!')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    else:
        print('Goodbye')

    # if elif elif elif elif elif elif elif else
    if condition:
        print('Hello')
    elif condition:
        print('World')
    elif condition:
        print('!')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    elif condition:
        print('Goodbye')
    else:
        print('Good

## HW
