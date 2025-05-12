# Examples

## Overview
This directory contains a collection of example Fortran-to-C++ translations that demonstrate various aspects of our evaluation framework. Each example includes the original Fortran code, reference C++ translation, generated translations from selected models, and analysis of key translation patterns.

## Example Categories

### 1. Basic Numerical Algorithms

#### Example: Simple Matrix Multiplication
**Fortran (original.f90):**
```fortran
PROGRAM MatrixMultiplication
  IMPLICIT NONE
  INTEGER, PARAMETER :: N = 3
  REAL, DIMENSION(N,N) :: A, B, C
  INTEGER :: i, j, k

  ! Initialize matrices A and B
  DO i = 1, N
    DO j = 1, N
      A(i,j) = i + j
      B(i,j) = i * j
    END DO
  END DO

  ! Compute matrix multiplication C = A * B
  C = 0.0
  DO i = 1, N
    DO j = 1, N
      DO k = 1, N
        C(i,j) = C(i,j) + A(i,k) * B(k,j)
      END DO
    END DO
  END DO

  ! Print result
  PRINT *, "Result matrix C:"
  DO i = 1, N
    PRINT *, (C(i,j), j=1,N)
  END DO
END PROGRAM MatrixMultiplication
```

**Reference C++ (reference.cpp):**
```cpp
#include <iostream>
#include <vector>

int main() {
    const int N = 3;
    std::vector<std::vector<float>> A(N, std::vector<float>(N));
    std::vector<std::vector<float>> B(N, std::vector<float>(N));
    std::vector<std::vector<float>> C(N, std::vector<float>(N, 0.0f));

    // Initialize matrices A and B
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            A[i][j] = (i + 1) + (j + 1);  // Adjust for 0-based indexing
            B[i][j] = (i + 1) * (j + 1);  // Adjust for 0-based indexing
        }
    }

    // Compute matrix multiplication C = A * B
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            for (int k = 0; k < N; ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }

    // Print result
    std::cout << "Result matrix C:" << std::endl;
    for (int i = 0; i < N; ++i) {
        for (int j = 0; j < N; ++j) {
            std::cout << C[i][j] << " ";
        }
        std::cout << std::endl;
    }

    return 0;
}
```

**Key Translation Patterns:**
- Index adjustment (1-based to 0-based)
- Array declaration and initialization patterns
- I/O formatting differences
- Loop structure preservation

### 2. Scientific Computing Algorithms

#### Example: Trapezoidal Numerical Integration
**Fortran (original.f90):**
```fortran
MODULE integration
  IMPLICIT NONE

CONTAINS
  FUNCTION trapz(f, a, b, n) RESULT(integral)
    INTERFACE
      FUNCTION f(x) RESULT(fx)
        REAL, INTENT(IN) :: x
        REAL :: fx
      END FUNCTION f
    END INTERFACE
    REAL, INTENT(IN) :: a, b
    INTEGER, INTENT(IN) :: n
    REAL :: integral
    
    REAL :: h, x
    INTEGER :: i
    
    h = (b - a) / n
    integral = 0.5 * (f(a) + f(b))
    
    DO i = 1, n-1
      x = a + i * h
      integral = integral + f(x)
    END DO
    
    integral = integral * h
  END FUNCTION trapz
END MODULE integration

PROGRAM test_trapz
  USE integration
  IMPLICIT NONE
  
  REAL :: result
  INTEGER :: num_intervals = 1000
  
  result = trapz(f, 0.0, 1.0, num_intervals)
  PRINT *, "The integral of x^2 from 0 to 1 is:", result
  
CONTAINS
  FUNCTION f(x) RESULT(fx)
    REAL, INTENT(IN) :: x
    REAL :: fx
    fx = x**2
  END FUNCTION f
END PROGRAM test_trapz
```

**Reference C++ (reference.cpp):**
```cpp
#include <iostream>
#include <functional>

namespace integration {
    double trapz(std::function<double(double)> f, double a, double b, int n) {
        double h = (b - a) / n;
        double integral = 0.5 * (f(a) + f(b));
        
        for (int i = 1; i < n; ++i) {
            double x = a + i * h;
            integral += f(x);
        }
        
        return integral * h;
    }
}

double f(double x) {
    return x * x;
}

int main() {
    int num_intervals = 1000;
    double result = integration::trapz(f, 0.0, 1.0, num_intervals);
    
    std::cout << "The integral of x^2 from 0 to 1 is: " << result << std::endl;
    
    return 0;
}
```

**Key Translation Patterns:**
- Module to namespace conversion
- Function interfaces to std::function
- Power operator translation
- Function passing between components

### 3. Memory Management Patterns

#### Example: Dynamic Array Allocation and Deallocation
**Fortran (original.f90):**
```fortran
SUBROUTINE process_data(n, result)
  INTEGER, INTENT(IN) :: n
  REAL, INTENT(OUT) :: result
  
  REAL, DIMENSION(:), ALLOCATABLE :: data
  INTEGER :: i, stat
  
  ALLOCATE(data(n), STAT=stat)
  IF (stat /= 0) THEN
    PRINT *, "Error: Could not allocate memory"
    result = -1.0
    RETURN
  END IF
  
  ! Initialize data
  DO i = 1, n
    data(i) = i * 0.5
  END DO
  
  ! Process data
  result = SUM(data) / n
  
  ! Clean up
  DEALLOCATE(data, STAT=stat)
  IF (stat /= 0) THEN
    PRINT *, "Warning: Deallocation failed"
  END IF
END SUBROUTINE process_data

PROGRAM test_allocation
  IMPLICIT NONE
  INTEGER, PARAMETER :: data_size = 1000
  REAL :: avg
  
  CALL process_data(data_size, avg)
  PRINT *, "Average value:", avg
END PROGRAM test_allocation
```

**Reference C++ (reference.cpp):**
```cpp
#include <iostream>
#include <vector>
#include <numeric>
#include <stdexcept>

void process_data(int n, float& result) {
    try {
        std::vector<float> data(n);
        
        // Initialize data
        for (int i = 0; i < n; ++i) {
            data[i] = (i + 1) * 0.5f;
        }
        
        // Process data
        result = std::accumulate(data.begin(), data.end(), 0.0f) / n;
        
        // Vector will automatically deallocate when it goes out of scope
    } catch (const std::bad_alloc& e) {
        std::cerr << "Error: Could not allocate memory" << std::endl;
        result = -1.0f;
        return;
    }
}

int main() {
    const int data_size = 1000;
    float avg;
    
    process_data(data_size, avg);
    std::cout << "Average value: " << avg << std::endl;
    
    return 0;
}
```

**Key Translation Patterns:**
- ALLOCATE/DEALLOCATE to std::vector
- Error handling conversion (STAT to try/catch)
- Resource management (RAII pattern in C++)
- Fortran array functions to C++ algorithms

### 4. Complex Numerical Methods

#### Example: Gauss-Seidel Iterative Solver
**Fortran (original.f90):**
```fortran
MODULE gauss_seidel
  IMPLICIT NONE
  
CONTAINS
  SUBROUTINE solve(A, b, x, max_iter, tol, iter_count, converged)
    REAL, DIMENSION(:,:), INTENT(IN) :: A
    REAL, DIMENSION(:), INTENT(IN) :: b
    REAL, DIMENSION(:), INTENT(INOUT) :: x
    INTEGER, INTENT(IN) :: max_iter
    REAL, INTENT(IN) :: tol
    INTEGER, INTENT(OUT) :: iter_count
    LOGICAL, INTENT(OUT) :: converged
    
    INTEGER :: n, i, j, k
    REAL :: sigma, error, prev
    
    n = SIZE(b)
    converged = .FALSE.
    
    DO k = 1, max_iter
      error = 0.0
      
      DO i = 1, n
        sigma = 0.0
        DO j = 1, n
          IF (j /= i) THEN
            sigma = sigma + A(i,j) * x(j)
          END IF
        END DO
        
        prev = x(i)
        x(i) = (b(i) - sigma) / A(i,i)
        error = MAX(error, ABS(x(i) - prev))
      END DO
      
      IF (error < tol) THEN
        converged = .TRUE.
        iter_count = k
        RETURN
      END IF
    END DO
    
    iter_count = max_iter
  END SUBROUTINE solve
END MODULE gauss_seidel

PROGRAM test_solver
  USE gauss_seidel
  IMPLICIT NONE
  
  INTEGER, PARAMETER :: n = 3
  REAL, DIMENSION(n,n) :: A
  REAL, DIMENSION(n) :: b, x
  INTEGER :: iter
  LOGICAL :: conv
  
  ! Define system Ax = b
  A = RESHAPE([4.0, 1.0, 1.0, 1.0, 3.0, -1.0, 2.0, 1.0, 5.0], [n, n])
  b = [6.0, 3.0, 8.0]
  
  ! Initial guess
  x = 0.0
  
  CALL solve(A, b, x, 100, 1.0E-6, iter, conv)
  
  IF (conv) THEN
    PRINT *, "Solution converged in", iter, "iterations:"
    PRINT *, x
  ELSE
    PRINT *, "No convergence after maximum iterations"
  END IF
END PROGRAM test_solver
```

**Reference C++ (reference.cpp):**
```cpp
#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>

namespace gauss_seidel {
    void solve(const std::vector<std::vector<double>>& A, 
               const std::vector<double>& b,
               std::vector<double>& x,
               int max_iter, 
               double tol,
               int& iter_count,
               bool& converged) {
        
        int n = b.size();
        converged = false;
        
        for (int k = 0; k < max_iter; ++k) {
            double error = 0.0;
            
            for (int i = 0; i < n; ++i) {
                double sigma = 0.0;
                for (int j = 0; j < n; ++j) {
                    if (j != i) {
                        sigma += A[i][j] * x[j];
                    }
                }
                
                double prev = x[i];
                x[i] = (b[i] - sigma) / A[i][i];
                error = std::max(error, std::abs(x[i] - prev));
            }
            
            if (error < tol) {
                converged = true;
                iter_count = k + 1;
                return;
            }
        }
        
        iter_count = max_iter;
    }
}

int main() {
    const int n = 3;
    std::vector<std::vector<double>> A(n, std::vector<double>(n));
    std::vector<double> b(n);
    std::vector<double> x(n, 0.0);
    
    // Define system Ax = b
    A[0][0] = 4.0; A[0][1] = 1.0; A[0][2] = 1.0;
    A[1][0] = 1.0; A[1][1] = 3.0; A[1][2] = -1.0;
    A[2][0] = 2.0; A[2][1] = 1.0; A[2][2] = 5.0;
    
    b[0] = 6.0; b[1] = 3.0; b[2] = 8.0;
    
    int iter = 0;
    bool conv = false;
    
    gauss_seidel::solve(A, b, x, 100, 1.0e-6, iter, conv);
    
    if (conv) {
        std::cout << "Solution converged in " << iter << " iterations:" << std::endl;
        for (int i = 0; i < n; ++i) {
            std::cout << x[i] << " ";
        }
        std::cout << std::endl;
    } else {
        std::cout << "No convergence after maximum iterations" << std::endl;
    }
    
    return 0;
}
```

**Key Translation Patterns:**
- RESHAPE to direct initialization
- Mathematical intrinsics to C++ equivalents
- Multi-dimensional array handling
- Parameter passing conventions

## Example Analysis

Each example demonstrates specific challenges in Fortran-to-C++ translation:

1. **Index Conversion**: All examples show the critical 1-based to 0-based indexing adjustment
2. **Array Handling**: Various approaches to translating Fortran's native array operations
3. **Memory Management**: Different strategies for resource management
4. **Module Translation**: Conversion of Fortran modules to C++ namespaces
5. **Mathematical Functions**: Mapping of intrinsic functions to C++ equivalents
6. **Input/Output**: Transformation of Fortran's formatted I/O to C++ streams

## Model-Specific Observations

Each example directory includes translations from different models, highlighting:
- Varying approaches to the same translation challenges
- Quality differences across model families
- Impact of model size on translation sophistication
- Error patterns specific to certain models

## Using These Examples

These examples can be used to:
1. Understand common Fortran-to-C++ translation patterns
2. Identify potential challenges in your own code migration
3. Compare translation approaches between different models
4. Evaluate the effectiveness of our feedback mechanism
5. Serve as templates for similar translation tasks

Note: The translations shown here are representative selections from our larger test suite and demonstrate both strengths and limitations of current LLM-based translation approaches.
