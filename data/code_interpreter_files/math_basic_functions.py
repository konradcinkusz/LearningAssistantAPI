# Import necessary libraries
import numpy as np

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error: Division by zero is not allowed."
    return a / b

def solve_linear_equation(a, b, c):
    """
    Solves a linear equation of the form ax + b = c.
    """
    if a == 0:
        return "Error: 'a' cannot be zero in a linear equation."
    return (c - b) / a

def calculate_area_of_circle(radius):
    return np.pi * (radius ** 2)

def calculate_roots_of_quadratic_equation(a, b, c):
    """
    Calculates the roots of a quadratic equation of the form ax^2 + bx + c = 0.
    """
    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return "The equation has no real roots."
    elif discriminant == 0:
        return -b / (2*a)
    else:
        root1 = (-b + np.sqrt(discriminant)) / (2*a)
        root2 = (-b - np.sqrt(discriminant)) / (2*a)
        return root1, root2