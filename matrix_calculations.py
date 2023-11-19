# Program: The user can choose between two different functions:
# 1. Enter a square matrix and caculate the inverse
# 2. Solve a system of linear equations by entering a square matrix and a vector
# The matrix and vector can have float values

def main():
    # The User can choose which function he wants to use
    program = int(input("Press '1' if you want to inverse a square matrix. Press '2' if you want to solve a system of linear equations. "))
    print("")

    # The functions for the calculations are called
    if program == 1:
        inverse_matrix()
    elif program == 2:
        solve_equations()
    else:
        print("Invalid input")
        exit()


# Full function to calculate the inverse
def inverse_matrix():

    # User is asked which size the matrix should have
    m = int(input("Enter the size of the square matrix: "))
   
    # Call the function to get the matrix from user
    matrix = matrix_input(m)
    print(matrix)

    # Call the function to calculate the determinant
    determinant = check_singularity(matrix)
    print(f"The determinant of the matrix is: {determinant}")

    # If the matrix is singular the program terminates
    if determinant == 0:
        print("The matrix is singular, no inverse exists.")
        exit()

    print("Now we calculate the Inverse of the matrix.")

    # Call the function to calculate the inverse
    inversed_matrix = calculate_inverse(matrix)

    # Print the result in a more user friendly way
    print("The Inverse Matrix is: ")
    for row in inversed_matrix:
        for element in row:
            print(element, end='\t')
        print()

# Full function to solve a system of linear equations
def solve_equations():
    
    print("The input has to be done as follows:")
    print("The left side of the system of equations will be inputted as matrix")
    print("The right side of the system of equations will be inputted as vector")
    print("")
    # User is asked which size the matrix should have
    m = int(input("Enter the size of the square matrix: "))

    # Call the function to get the matrix input from user
    matrix = matrix_input(m)


    determinant = check_singularity(matrix)

    if determinant == 0:
        print("The system has no solutions")
        exit()


    # Call the function to calculate the inverse
    inversed_matrix = calculate_inverse(matrix)

    # Call the function to get the matrix input from user
    vector = vector_input(m)
    # Call the function to calculate the inverse
    solved_system = solve_system(inversed_matrix, vector)

    # Print the result more user-friendly
    variables = [f'x_{i+1}' for i in range(len(solved_system))]
    equations = ', '.join([f'{variables[i]} = {solved_system[i]}' for i in range(len(solved_system))])
    print("The solution is: ")
    print(equations)



# This function is for the input of the matrix
def matrix_input(m):
    
    # The matrix will be stored in a list
    user_matrix = []

    # If the matrix is valid, the user is asked to input the values of the matrix for each row
    if m > 1:
        for i in range(m):
            # A table with the matrix values is created for each row
            row = input(f"Enter values for row {i + 1} separated by spaces: ").split()

            # The program checks if the amount of values in each row is correct
            # If the input is invalid and error message is printed and the program terminates
            if len(row) != m:
                print(f"Invalid input. Each row should have {m} values.")
                exit()

            # Each row is appended to the user_matrix list 
            row = [float(val) for val in row]
            user_matrix.append(row)
        
        # if the input is valid, a list of lists is returned. Each row is stored as a list within the matrix list
        return user_matrix
    
    # Calculations for a 1x1 matrix
    elif m == 1:
        row = float(input(f"Enter value: "))
        # If the value of the matrix is 0, it is not invertible
        if row == 0:
            print("This matrix has no inverse")
            exit()  
        # If the value of the matrix is not 0, the inverse is 1/value
        else:
            inverse_matrix = float(1 / row)
            print(f"The inverse matrix is ({inverse_matrix:.2f})")
            exit()

    # If the matrix size is not valid an error message is printed and the program terminates
    else:
        print("The size of the matrix is invalid")
        exit()


# This function checks if the matrix is not singular, meaning if an Inverse even exists
# To check that, the determinant needs to be calculated
def check_singularity(matrix):

    # Get the length of the matrix
    n = len(matrix)

    # Base case for a 1x1 matrix
    if n == 1:
        return matrix[0][0]

    # Initialize the determinant
    det = 0

    # The determinant is calculated with the recursive formula of the laplace expansion
    for j in range(n):
        # Calculate the submatrix without the current row and column
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        # Calculate the determinant of the submatrix and add it to the result
        det += matrix[0][j] * (-1) ** j * check_singularity(submatrix)
    
    # The function returns the determinant
    return det

# This function calculates the inverse of the matrix
def calculate_inverse(matrix):
    
    # The inverse is calculated with the adjugate matrix and the determinant formula
    determinant = check_singularity(matrix)
    n = len(matrix)
    cofactor_matrix = calculate_cofactor_matrix(matrix)
    # The cofactor matrix needs to be transposed in order to get the adjugate matrix
    adjugate_matrix = transpose_matrix(cofactor_matrix)
    
    inverse_matrix = [[adjugate_matrix[i][j] / determinant for j in range(n)] for i in range(n)]
    
    return inverse_matrix

# Transposes the matrix
def transpose_matrix(matrix):
    
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

# The cofactor matrix is needed for calculating the inverse later
# The subdeterminants are calculated by crossing out the row and column of the element and calculating the 
# determinant of that submatrix. Each element has alternately a positive or negative sign
def calculate_cofactor_matrix(matrix):
    # Calculate the cofactor matrix
    n = len(matrix)
    cofactor_matrix = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            submatrix = [row[:j] + row[j + 1:] for row in (matrix[:i] + matrix[i + 1:])]
            cofactor_matrix[i][j] = ((-1) ** (i + j)) * check_singularity(submatrix)
    
    return cofactor_matrix



# This function is for the input of the vector
def vector_input(m):
    
    # The vector will be stored in a list
    # If the matrix is valid, the user is asked to input the values of the matrix for each row
    user_vector = input(f"Enter the {m} vector values separated by spaces: ").split()
    print("")
    # The program checks if the amount of values in the vector is correct
    # If the input is invalid and error message is printed and the program terminates
    if len(user_vector) != m:
        print(f"Invalid input. The vector should have {m} values.")
        exit()

    try:
        user_vector = [float(value) for value in user_vector]
    except ValueError:
        print("Invalid input. Please enter numerical values.")
        exit()

    # if the input is valid, a list is returned.
    return user_vector



# This function solves the system of linear equations with given inversed matrix and vector
def solve_system(inversed_matrix, vector):

    # The result will be stored in a list
    result = []
    # Multiplying the value of the nth vector value with the corresponding value of each matrix row
    for i in range(len(inversed_matrix)):
        product = sum(inversed_matrix[i][j] * vector[j] for j in range(len(vector)))
        result.append(product)
    return result



main()