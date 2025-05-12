# Models Evaluated

## Overview
This document details the open-source Large Language Models (LLMs) evaluated in our research on Fortran to C++ code translation. Models were selected to represent diverse architectures, parameter scales, and training approaches, providing a comprehensive view of the current state-of-the-art in code translation capabilities.

## Model Selection Criteria
Models were chosen based on:
- Demonstrated performance on programming tasks
- Parameter efficiency and computational requirements
- Diversity in training data and pre-training objectives
- Open-source availability and licensing
- Community adoption and active development

## Models Included in Evaluation

### Base Models

#### Llama3
- **Architecture**: Latest iteration of Meta's Llama architecture
- **Training**: Broad training corpus with improved code representation
- **Key features**: Enhanced instruction following and reasoning
- **Strengths**: Strong general capabilities with good code understanding
- **Limitations**: Not specifically optimized for Fortran translation

#### CodeLlama
- **Architecture**: Llama architecture optimized for code
- **Training**: Fine-tuned on code-specific data
- **Key features**: Specialized for code generation and understanding
- **Strengths**: Strong performance on programming tasks
- **Limitations**: Less exposure to scientific computing languages

#### Mistral
- **Architecture**: Sliding Window Attention (SWA) architecture
- **Training**: General-purpose with code components
- **Key features**: Efficient context handling
- **Strengths**: Strong reasoning capabilities
- **Limitations**: Not specifically optimized for Fortran

#### DeepSeek-Coder:7B
- **Architecture**: Specialized coding architecture
- **Training**: Focused on code from multiple sources
- **Key features**: Optimized for code generation tasks
- **Strengths**: Efficient performance at 7B parameter scale
- **Limitations**: Smaller model size compared to some competitors

#### CodeBooga
- **Architecture**: Decoder-only transformer
- **Training**: Specialized on code repositories
- **Key features**: Optimized for code completion and translation
- **Strengths**: Good performance on cross-language tasks
- **Limitations**: Less established than some other models

#### Mixtral
- **Architecture**: Mixture of Experts (MoE) architecture
- **Training**: Diverse pretraining including code
- **Key features**: 8 expert networks with sparse activation
- **Strengths**: Efficient parameter utilization
- **Limitations**: Complex routing mechanism

#### StarCoder
- **Architecture**: Decoder-only transformer
- **Training**: 80+ programming languages from GitHub
- **Key features**: Trained on 1T tokens of code
- **Strengths**: Wide language coverage including Fortran
- **Limitations**: Limited scientific domain knowledge

#### WizardCoder
- **Architecture**: Instruction-tuned language model
- **Training**: Specialized training for code tasks
- **Key features**: Optimized for following coding instructions
- **Strengths**: Strong performance on instruction-based tasks
- **Limitations**: Varies by base model size

#### CodeUp
- **Architecture**: Transformer-based model
- **Training**: Focused on code improvement and refactoring
- **Key features**: Specialized for code enhancement
- **Strengths**: Strong performance on code modification tasks
- **Limitations**: Less established in research literature

## Evaluation Configuration

All models were evaluated using the following configuration:
- **Temperature**: Default at first, then 0.2 for controlled variance
- **Top-p**: 0.95
- **Max new tokens**: 2048
- **Context window**: Up to model maximum (truncated as needed)
- **Hardware**: NVIDIA A100 GPUs
- **Quantization**: None (full precision evaluation)

## Performance Summary

While detailed performance metrics are presented in the results section, notable high-level findings include:
- Larger parameter models consistently outperformed smaller variants
- CodeLlama showed strong performance on structural translation fidelity
- Mixtral's MoE architecture demonstrated efficiency advantages
- StarCoder excelled in correctly mapping Fortran libraries to C++ equivalents
- WizardCoder showed strongest improvement with feedback iteration
- DeepSeek-Coder demonstrated impressive performance despite smaller parameter count

## Model Access

All models evaluated are available through the Hugging Face Hub with appropriate licenses for research reproduction.
