# Translation Examples

This directory contains example Fortran code samples and their C++ translations, demonstrating various aspects of the translation process and challenges. These examples illustrate the capabilities and limitations of current LLM-based translation approaches.

## Example Categories

### Basic Numerical Algorithms
Simple numerical computation examples that demonstrate fundamental translation patterns like array handling, loop conversion, and type mapping.

### Scientific Computing Algorithms
More complex scientific algorithms showing translation of numerical methods, function interfaces, and module structures.

### Memory Management Patterns
Examples focusing on memory allocation/deallocation patterns and their C++ equivalents using RAII and smart pointers.

### Complex Numerical Methods
Advanced examples demonstrating translation of iterative solvers, scientific libraries, and complex data structures.

## Example Format

Each example includes:
- `original.f90`: Original Fortran code
- `reference.cpp`: Reference C++ translation (human-created)
- `model_translations/`: Directory containing translations from different models
- `analysis.md`: Discussion of key translation challenges and model performance

## Using These Examples

These examples can serve as:
1. Reference for common Fortran-to-C++ translation patterns
2. Illustrations of typical challenges in legacy code migration
3. Benchmarks for evaluating other translation approaches
4. Teaching resources for understanding cross-language migration

## Note on Implementations

The examples provided are representative selections from the larger test suite used in our research. They have been selected to demonstrate both common patterns and challenging edge cases in Fortran-to-C++ translation.
