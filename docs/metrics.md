# Metrics

## Overview
This document details the evaluation metrics implemented in our framework to assess the quality, accuracy, and functional equivalence of LLM-generated Fortran to C++ code translations. Our approach combines established code similarity metrics with custom evaluations specific to the Fortran-to-C++ translation task.

## CodeBLEU Metrics

### Implementation Details
We implemented the CodeBLEU metric suite as described by Ren et al. (2020), with adaptations specific to Fortran and C++ language pairs. CodeBLEU combines four components:

#### 1. N-gram Match (Weight: 0.25)
- Measures surface-level lexical similarity between generated and reference code
- Implemented using modified n-gram precision calculation
- N-gram ranges: unigrams through 4-grams
- Tokenization: language-specific tokenizer for C++ with handling for identifiers and keywords

#### 2. Weighted Reference Match (Weight: 0.25)
- Evaluates keyword and identifier preservation across languages
- Custom mapping dictionary translating Fortran keywords to C++ equivalents
- Examples: `DO` → `for`, `ALLOCATE` → `new`, `MODULE` → `namespace`
- Identifier preservation metrics tracking variable name consistency

#### 3. Abstract Syntax Tree (AST) Match (Weight: 0.25)
- Evaluates syntactic structure preservation
- Generated using Clang for C++ and Open Fortran Parser for Fortran
- Custom comparator for cross-language AST matching
- Calculates sub-tree similarity between language-specific ASTs

#### 4. Data Flow Match (Weight: 0.25)
- Assesses preservation of data dependencies and control flow
- Control flow graph (CFG) construction for both Fortran and C++
- Custom graph similarity algorithm to compare CFGs
- Emphasis on loop structure, conditional logic, and function call patterns

### Adaptation for Fortran-to-C++ Translation
Standard CodeBLEU was enhanced with:
- Language-specific tokenization rules for Fortran and C++
- Cross-language keyword mapping tables
- Normalization of language-specific idioms (e.g., 1-based vs. 0-based indexing)
- Special handling for Fortran array notation vs. C++ iteration patterns

## Compilation Success Metrics

### Binary Compilation Success
- **Definition**: Whether generated C++ code compiles without errors
- **Implementation**: Automated GCC invocation with standardized flags
- **Scoring**: Binary pass/fail (1.0/0.0)

### Error Severity Classification
- **Minor Errors**: Warnings or non-blocking issues (0.75)
- **Moderate Errors**: Errors that prevent compilation but have clear fixes (0.5)
- **Severe Errors**: Fundamental flaws in language understanding (0.25)
- **Critical Errors**: Complete failure to produce valid C++ syntax (0.0)

### Compiler Feedback Iterations
- **First-pass Success Rate**: Percentage of translations compiling on first attempt
- **Convergence Rate**: Percentage reaching successful compilation within N iterations
- **Average Iterations to Success**: Mean number of feedback cycles to compilation

## Functional Equivalence Metrics

### Output Equivalence Testing
- Input-output comparison between Fortran original and C++ translation
- Standardized test cases with controlled inputs
- Numerical tolerance thresholds for floating-point operations
- Precision and accuracy metrics for scientific computations

### Runtime Performance Ratio
- Relative execution time between original and translated code
- Normalized against hardware configuration
- Sampling-based profiling of hot spots

### Memory Usage Patterns
- Static analysis of memory allocation/deallocation patterns
- Dynamic tracking of memory footprint
- Comparison of peak memory usage

## Translation Quality Metrics

### API Mapping Accuracy
- Correct mapping of Fortran intrinsics to C++ standard library
- Appropriate translation of common scientific libraries
- Preservation of mathematical functions and their semantics

### Idiomaticity Score
- Measures use of C++-specific idioms where appropriate
- Evaluates modernization of legacy patterns
- Rewards use of C++ features like RAII, templates, and STL

### Documentation Quality
- Preservation of original code comments
- Addition of translation-specific explanations
- Documentation of critical mapping decisions

## Visualization Metrics

### Error Heatmaps
- Visualization of error locations in code
- Categorization by error type and severity
- Mapping common error patterns across models

### Translation Consistency
- Variation in translations across models
- Identification of consensus translations
- Detection of outlier approaches

## Composite Scoring

Our final evaluation combined individual metrics into a weighted composite score:
- CodeBLEU Suite: 40%
- Compilation Success: 25%
- Functional Equivalence: 25%
- Translation Quality: 10%

This weighting prioritizes structural correctness and functional equivalence while still rewarding idiomatic C++ translation.

## Statistical Analysis

Statistical significance testing was performed using:
- Paired t-tests for performance comparisons
- Bootstrap resampling for confidence intervals
- Effect size calculations for meaningful differences

All metrics were aggregated across the test suite with 95% confidence intervals reported.

## References

Ren, S., Guo, D., Lu, S., Zhou, L., Liu, S., Tang, D., Sundaresan, N., Zhou, M., Blanco, A., & Ma, S. (2020). CodeBLEU: a Method for Automatic Evaluation of Code Synthesis. arXiv preprint arXiv:2009.10297.
