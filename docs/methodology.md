# Methodology

## Experimental Design

### Overview
This document outlines the Uncertainty Quantification methodology used to evaluate the capabilities of Large Language Models (LLMs) in translating legacy Fortran code to modern C++. The evaluation framework was designed to provide quantitative assessments of translation quality, accuracy, and consistency across multiple models.

### Model Selection
We evaluated 12 open-source LLMs with parameter counts ranging from 7B to 34B. Models were selected based on:
- Reported performance on code-related tasks in existing benchmarks
- Diversity of training data and architecture
- Accessibility and open-source availability
- Parameter efficiency and computational requirements

### Dataset Preparation
Our evaluation utilized a diverse set of Fortran code samples, including:
- Academic computational code
- Numerical methods implementations
- Scientific simulation components
- Standard mathematical operations
- I/O handling routines

For each Fortran code sample, we created ground truth C++ translations manually verified by domain experts to ensure functional equivalence and adherence to modern C++ best practices.

Any open source code samples used were sourced from: 
https://rosettacode.org/wiki/Category:Fortran

## Prompting Strategy

### Zero-Shot Approach
Our primary evaluation used zero-shot prompting where models were given:
1. A clear instruction to translate Fortran code to C++
2. The complete Fortran code snippet
3. Guidelines for maintaining functional equivalence
4. Request for clean, well-documented C++ output

Example prompt template:
```
Translate the following Fortran code to modern C++ (C++17 or newer). 
Maintain functional equivalence while using C++ idioms where appropriate.
Return only the translated C++ code with brief comments explaining key translation decisions.

Fortran code:
[FORTRAN CODE HERE]
```

### Session-Maintained Approach
For comparative analysis, we also evaluated models using session-maintained prompting where:
1. Models were provided with the initial translation task
2. Compiler errors were fed back into the conversation
3. Models were asked to refine translations based on error feedback
4. The process continued until successful compilation or a maximum iteration count was reached

## Evaluation Metrics

### CodeBLEU
We implemented the CodeBLEU metric suite to evaluate structural similarity between generated and ground truth translations, which includes:
- N-gram match (measuring surface-level similarity)
- Weighted reference match (accounting for code structure)
- Abstract Syntax Tree (AST) match (evaluating syntactic correctness)
- Data flow match (assessing logical equivalence)

### Compilation Success
We measured the rate at which generated translations successfully compiled without errors using GCC, both:
- Initially (zero-shot success)
- After feedback iterations (with our agentic feedback mechanism)

### Functional Equivalence
We developed test cases to evaluate whether translated code produced functionally equivalent results:
1. Input-output testing with standardized test cases
2. Performance comparison on targeted computational kernels
3. Memory usage analysis
4. Error handling assessment

### Error Classification
We categorized translation errors into distinct classes:
- Syntax errors (fundamental language constructs)
- Semantic errors (logic preservation issues)
- Library/API mapping errors (Fortran to C++ library equivalents)
- Memory management errors (allocation/deallocation patterns)
- Type conversion errors (Fortran to C++ type systems)

## Feedback Mechanism Implementation

### Compiler Integration
Our agentic feedback mechanism incorporated:
1. Automated compilation using GCC with standardized flags
2. Error message parsing and classification
3. Prompt reformulation based on error type and severity
4. Targeted guidance for common error patterns

### Improvement Measurement
We tracked several metrics to measure the impact of our feedback mechanism:
- Error reduction rate across iterations
- Compilation success rate improvement
- Code quality changes (measured via static analysis)
- Convergence speed (iterations required to reach successful compilation)

## Analysis Methods

### Comparative Analysis
We performed detailed comparative analysis between:
- Different model sizes (7B vs. 13B vs. 34B parameters)
- Different model architectures and training approaches
- Zero-shot vs. session-maintained prompting strategies
- With and without compiler feedback integration

### Visualization Techniques
Advanced visualizations were created to analyze:
1. Error distribution patterns across models
2. Consistency of translation approaches
3. Improvement trajectories with feedback iterations
4. Correlation between model size and translation quality
5. Performance across different Fortran code complexity levels

## Limitations and Considerations

- Our evaluation focused on specific scientific computing domains and may not generalize to all Fortran code
- Ground truth translations represent one of many possible correct translations
- Performance assessments were conducted on standard hardware configurations
- Real-world code bases may present additional complexities not covered in this controlled evaluation
