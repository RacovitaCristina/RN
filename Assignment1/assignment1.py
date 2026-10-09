import pathlib
import math


#ex 1-Parsing the System of Equations

#extrag coeficientul unui termen
def get_coefficient(term):
    coefficient = term[:-1]   #toate caracterele in afara de ultimul (care este variabila)

    #daca coeficientul este gol, inseamna ca este 1
    if coefficient == "":
        return 1.0

    return float(coefficient)


#citeste sistemul de ecuatii dintr-un fisier si returneaza matricea A si vectorul B
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    A = []
    B = []

    with open(path, "r") as file:
        lines = file.readlines()

    for line in lines:
        tokens = line.split()

        coefficients = []
        sign = 1

        for token in tokens:
            if token == "+":
                sign = 1

            elif token == "-":
                sign = -1

            elif token == "=":
                break

            else:
                coefficient = get_coefficient(token)
                coefficients.append(sign * coefficient)
        #add coef ecuatiei ca o linie in matricea A   
        A.append(coefficients)
        #ultimul element al ecuatiei este termenul liber, care se adauga in vectorul B
        B.append(float(tokens[-1]))

    return A, B


A, B = load_system(pathlib.Path("system.txt"))

print("A =", A)
print("B =", B)




# ex 2 - Matrix and Vector Operations

# 2.1 - Determinant

def determinant(matrix: list[list[float]]) -> float:
    det = (
        matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
        - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
        + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    )

    return det


print(f"{determinant(A)=}")



# 2.2 - Trace
#suma elementelor de pe diagonala principala a unei matrice
def trace(matrix: list[list[float]]) -> float:
    result = 0.0

    for i in range(len(matrix)):
        result += matrix[i][i]

    return result


print(f"{trace(A)=}")


# 2.3 - Vector norm
#norma euclidiana a unui vector, adica radacina patrata a sumei patratelor elementelor vectorului
def norm(vector: list[float]) -> float:
    sum_squares = 0.0

    for value in vector:
        sum_squares += value ** 2

    return math.sqrt(sum_squares)

print("norm([3, 4]) =", norm([3, 4]))
print(f"{norm(B)=}")

# 2.4 - Transpose of a matrix

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    transposed = []

    for j in range(len(matrix[0])):
        new_row = []

        for i in range(len(matrix)):
            new_row.append(matrix[i][j])

        transposed.append(new_row)

    return transposed

print(f"{transpose(A)=}")

# 2.5 - Matrix-vector multiplication

def multiply(
    matrix: list[list[float]],
    vector: list[float]
) -> list[float]:

    result = []

    for row in matrix:
        value = 0.0

        for i in range(len(vector)):
            value += row[i] * vector[i]

        result.append(value)

    return result


print(f"{multiply(A, B)=}")


# ex 3 - Solving using Cramer's Rule

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)

    if det_A == 0:
     raise ValueError("Matricea are determinantul 0, deci nu se poate aplica regula lui Cramer")


    solution = []

    for column in range(len(matrix)):
        # fac o copie a matricei pentru a nu modifica matricea originala
        modified_matrix = [row.copy() for row in matrix]

        # inlocuiesc coloana curenta cu vectorul B
        for row in range(len(matrix)):
            modified_matrix[row][column] = vector[row]

        # aplic regula lui Cramer
        det_modified = determinant(modified_matrix)
        solution.append(det_modified / det_A)

    return solution


print(f"{solve_cramer(A, B)=}")


# ex 4 - Solving using Inversion

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    result = []

    for row in range(len(matrix)):
        if row == i:
            continue   #practic sarim peste linia i si continam

        new_row = []

        for column in range(len(matrix[row])):
            if column == j: #saring peste coloana j si continam
                continue

            new_row.append(matrix[row][column])

        result.append(new_row)

    return result
print(f"{minor(A, 0, 0)=}")


def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    result = []

    for i in range(len(matrix)):
        cofactor_row = []

        for j in range(len(matrix[i])):
            m = minor(matrix, i, j)

            det_minor = m[0][0] * m[1][1] - m[0][1] * m[1][0]

            sign = (-1) ** (i + j)
            cofactor_row.append(sign * det_minor)

        result.append(cofactor_row)

    return result
print(f"{cofactor(A)=}")

#adjuncta e transpusa matricei de cofactori
def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    cofactor_matrix = cofactor(matrix)
    return transpose(cofactor_matrix)


print(f"{adjoint(A)=}")

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    
    if det_A == 0:
     raise ValueError("Matricea nu este inversabila")

    adj_A = adjoint(matrix)

    inverse = []

    for row in adj_A:
        inverse_row = []

        for value in row:
            inverse_row.append(value / det_A)

        inverse.append(inverse_row)

    return multiply(inverse, vector)


print(f"{solve(A, B)=}")