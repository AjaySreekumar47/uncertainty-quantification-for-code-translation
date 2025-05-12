# LLM-Based Fortran to C++ Translation Framework

## Overview
This repository contains a reimplementation of research work I conducted as a Graduate Research Intern in the CCS-3 Division at Los Alamos National Laboratory. This work contributed to the NAACL 2025 conference paper: "LLM-Assisted Translation of Legacy FORTRAN Code to C++: A Cross-Platform Study".

**Important Note:** This is a reimplementation based on my research at Los Alamos. The original code and specific data remain property of the laboratory.

## Project Background
Legacy Fortran code remains prevalent in scientific computing applications, but modern development often favors C++. This project evaluated the capabilities of current Large Language Models (LLMs) to assist in this translation process, potentially accelerating legacy code migration and modernization efforts.

## Research Components

### Evaluation Framework
- Designed and implemented a comprehensive framework to evaluate 12 open-source LLMs (7B-34B parameters)
- Used controlled zero-shot prompting experiments to assess code translation capabilities
- Developed standardized test cases covering various Fortran coding patterns and complexities

### Quantitative Assessment
- Implemented CodeBLEU metrics to evaluate structural similarity between LLM-generated C++ code and ground truth translations
- Created custom evaluation metrics to assess functional equivalence and performance characteristics
- Benchmarked translation accuracy across different model sizes and architectures

### Visualization & Analysis
- Created advanced visualizations to analyze LLM consistency and error patterns
- Identified common failure modes and logical approaches in code translation tasks
- Conducted comparative analysis between zero-shot and session-maintained prompting strategies

### Feedback Mechanism
- Implemented an agentic feedback system with compiler error integration
- Developed methodology to improve code translation accuracy by incorporating compiler feedback
- Tested various feedback loop implementations to maximize improvement

## Publication
This work contributed to the following paper:
Nishath Rajiv Ranasinghe, Shawn M. Jones, Michal Kucer, Ayan Biswas, Daniel O’Malley, Alexander Most, Selma Liliane Wanna, and Ajay Sreekumar. (2025). "LLM-Assisted Translation of Legacy FORTRAN Code to C++: A Cross-Platform Study". North American Chapter of the Association for Computational Linguistics (NAACL 2025).

## Technologies Used
- Python for framework implementation and analysis
- Hugging Face Transformers for model access and inference
- Ollama models as open-source LLMs for prompting experiments
- CodeBLEU and custom metrics for evaluation
- Matplotlib/Seaborn/Plotly for advanced visualizations
- GCC and GFortran compilers for validation and feedback mechanisms

## License
This reimplementation is made available under the MIT License.
