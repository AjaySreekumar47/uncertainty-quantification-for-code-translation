# Framework

## Overview
This directory contains a simplified reimplementation of the core components of our Fortran-to-C++ translation evaluation framework. While the original implementation remains at Los Alamos National Laboratory, these files demonstrate the architecture and approach we used to evaluate LLM performance on code translation tasks.

## Components

### 1. Model Interface (`model_interface.py`)

```python
import os
import json
import requests
from typing import Dict, List, Optional, Union

class ModelInterface:
    """Base class for interacting with LLM APIs."""
    
    def __init__(self, model_name: str, api_config: Dict):
        """
        Initialize a model interface.
        
        Args:
            model_name: Name of the model
            api_config: Configuration for API access
        """
        self.model_name = model_name
        self.api_config = api_config
        self.history = []
        
    def translate(self, fortran_code: str, prompt_template: str) -> str:
        """
        Translate Fortran code to C++ using the model.
        
        Args:
            fortran_code: The Fortran code to translate
            prompt_template: Template for the prompt
            
        Returns:
            Translated C++ code
        """
        prompt = prompt_template.format(fortran_code=fortran_code)
        response = self._get_completion(prompt)
        cpp_code = self._extract_code(response)
        self.history.append({"prompt": prompt, "response": response, "extracted": cpp_code})
        return cpp_code
    
    def _get_completion(self, prompt: str) -> str:
        """
        Get completion from the model. To be implemented by subclasses.
        
        Args:
            prompt: Prompt to send to the model
            
        Returns:
            Model's response
        """
        raise NotImplementedError
    
    def _extract_code(self, response: str) -> str:
        """
        Extract code from model response.
        
        Args:
            response: Full model response
            
        Returns:
            Extracted C++ code
        """
        # Simple implementation - in practice, we used more robust extraction
        if "```cpp" in response and "```" in response.split("```cpp", 1)[1]:
            return response.split("```cpp", 1)[1].split("```", 1)[0].strip()
        elif "```c++" in response and "```" in response.split("```c++", 1)[1]:
            return response.split("```c++", 1)[1].split("```", 1)[0].strip()
        elif "```" in response and "```" in response.split("```", 1)[1]:
            return response.split("```", 1)[1].split("```", 1)[0].strip()
        else:
            # Fallback to looking for code-like patterns
            return response.strip()
            
    def apply_feedback(self, compiler_errors: str, previous_translation: str, 
                       fortran_code: str, feedback_template: str) -> str:
        """
        Apply compiler feedback to improve translation.
        
        Args:
            compiler_errors: Compiler error messages
            previous_translation: Previous C++ translation
            fortran_code: Original Fortran code
            feedback_template: Template for feedback prompt
            
        Returns:
            Improved C++ translation
        """
        prompt = feedback_template.format(
            compiler_errors=compiler_errors,
            previous_translation=previous_translation,
            fortran_code=fortran_code
        )
        response = self._get_completion(prompt)
        cpp_code = self._extract_code(response)
        self.history.append({
            "prompt": prompt, 
            "response": response, 
            "extracted": cpp_code,
            "feedback": True
        })
        return cpp_code


class HuggingFaceModelInterface(ModelInterface):
    """Interface for Hugging Face models."""
    
    def _get_completion(self, prompt: str) -> str:
        """
        Get completion from Hugging Face model.
        
        Args:
            prompt: Prompt to send to the model
            
        Returns:
            Model's response
        """
        # In practice, this would use the Hugging Face API or local inference
        # This is a placeholder implementation
        print(f"Would call Hugging Face API for model {self.model_name}")
        return "Placeholder response - would contain C++ code in actual implementation"


class ModelRegistry:
    """Registry for managing multiple models."""
    
    @staticmethod
    def load_models(model_names: List[str], config_path: str = "config/models.json") -> Dict[str, ModelInterface]:
        """
        Load multiple models from configuration.
        
        Args:
            model_names: List of model names to load
            config_path: Path to model configuration file
            
        Returns:
            Dictionary of model interfaces
        """
        # In practice, would load from a configuration file
        # This is a simplified implementation
        models = {}
        for model_name in model_names:
            if "llama" in model_name.lower():
                api_config = {"api_key": "placeholder", "endpoint": "placeholder"}
                models[model_name] = HuggingFaceModelInterface(model_name, api_config)
            elif "mixtral" in model_name.lower():
                api_config = {"api_key": "placeholder", "endpoint": "placeholder"}
                models[model_name] = HuggingFaceModelInterface(model_name, api_config)
            # Add more model types as needed
        return models
```

### 2. Evaluation Framework (`evaluation.py`)

```python
import os
import subprocess
import tempfile
from typing import Dict, List, Tuple, Optional, Union
import re

class CompilationTester:
    """Tests compilation of C++ translations."""
    
    def __init__(self, compiler_path: str = "g++", flags: List[str] = None):
        """
        Initialize compilation tester.
        
        Args:
            compiler_path: Path to C++ compiler
            flags: Compiler flags
        """
        self.compiler_path = compiler_path
        self.flags = flags or ["-std=c++17", "-Wall", "-Werror"]
        
    def test_compilation(self, cpp_code: str) -> Tuple[bool, str]:
        """
        Test if C++ code compiles.
        
        Args:
            cpp_code: C++ code to test
            
        Returns:
            Tuple of (success, error_message)
        """
        with tempfile.NamedTemporaryFile(suffix=".cpp", delete=False) as f:
            f.write(cpp_code.encode('utf-8'))
            temp_path = f.name
            
        try:
            output_path = temp_path.replace(".cpp", ".out")
            cmd = [self.compiler_path] + self.flags + ["-o", output_path, temp_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return True, ""
            else:
                return False, result.stderr
        finally:
            # Clean up temporary files
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            if os.path.exists(output_path):
                os.unlink(output_path)


class CodeBleuCalculator:
    """Calculates CodeBLEU metric for translations."""
    
    def calculate(self, reference_code: str, generated_code: str) -> float:
        """
        Calculate CodeBLEU score.
        
        Args:
            reference_code: Reference C++ code
            generated_code: Generated C++ code
            
        Returns:
            CodeBLEU score (0-1)
        """
        # This is a placeholder - in practice, we implemented the full CodeBLEU algorithm
        # including AST matching, dataflow analysis, etc.
        # Return a random score for demonstration
        import random
        return random.uniform(0.7, 0.95)


class ErrorAnalyzer:
    """Analyzes compiler errors to provide structured feedback."""
    
    def analyze(self, error_message: str) -> Dict:
        """
        Analyze compiler error message.
        
        Args:
            error_message: Compiler error message
            
        Returns:
            Structured analysis of errors
        """
        errors = []
        
        # In practice, we had sophisticated error pattern matching
        # This is a simplified example
        error_patterns = [
            (r"error: '([^']+)' was not declared", "undeclared_identifier"),
            (r"error: expected ';' before", "missing_semicolon"),
            (r"error: invalid types '([^']+)'", "type_mismatch"),
            (r"error: no matching function for call to '([^']+)'", "function_mismatch")
        ]
        
        for pattern, error_type in error_patterns:
            matches = re.finditer(pattern, error_message)
            for match in matches:
                errors.append({
                    "type": error_type,
                    "message": match.group(0),
                    "entity": match.group(1) if match.groups() else None
                })
        
        return {
            "error_count": len(errors),
            "errors": errors,
            "categories": {error_type: sum(1 for e in errors if e["type"] == error_type) 
                           for error_type in set(e["type"] for e in errors)}
        }


class TranslationFramework:
    """Main framework for evaluating Fortran-to-C++ translations."""
    
    def __init__(self, models: Dict, metrics: List[str] = None, feedback_enabled: bool = True):
        """
        Initialize translation framework.
        
        Args:
            models: Dictionary of model interfaces
            metrics: List of metrics to calculate
            feedback_enabled: Whether to enable feedback loop
        """
        self.models = models
        self.metrics = metrics or ["codebleu", "compilation_success"]
        self.feedback_enabled = feedback_enabled
        
        self.compiler = CompilationTester()
        self.codebleu = CodeBleuCalculator()
        self.error_analyzer = ErrorAnalyzer()
        
        # Templates - in practice, these would be loaded from files
        self.prompt_template = """
        Translate the following Fortran code to modern C++ (C++17 or newer).
        Maintain functional equivalence while using C++ idioms where appropriate.
        Return only the translated C++ code with brief comments explaining key translation decisions.
        
        Fortran code:
        ```fortran
        {fortran_code}
        ```
        """
        
        self.feedback_template = """
        I've attempted to compile your Fortran to C++ translation, but encountered the following errors:
        
        {compiler_errors}
        
        Please revise your translation to address these issues. Pay special attention to type conversions, 
        array indexing (remember C++ uses 0-based indexing), and memory management.
        
        Here's your previous translation attempt:
        ```cpp
        {previous_translation}
        ```
        
        Original Fortran code for reference:
        ```fortran
        {fortran_code}
        ```
        """
    
    def evaluate_translation(self, model_name: str, fortran_code: str, 
                            reference_cpp: str = None, max_iterations: int = 3) -> Dict:
        """
        Evaluate translation from a specific model.
        
        Args:
            model_name: Name of model to use
            fortran_code: Fortran code to translate
            reference_cpp: Reference C++ translation (optional)
            max_iterations: Maximum feedback iterations
            
        Returns:
            Evaluation results
        """
        model = self.models[model_name]
        
        # Initial translation
        cpp_code = model.translate(fortran_code, self.prompt_template)
        
        # Test compilation
        compiles, error_message = self.compiler.test_compilation(cpp_code)
        
        iterations = []
        current_translation = cpp_code
        
        # Store initial results
        iteration_result = {
            "iteration": 0,
            "compiles": compiles,
            "cpp_code": cpp_code
        }
        
        if reference_cpp and "codebleu" in self.metrics:
            iteration_result["codebleu"] = self.codebleu.calculate(reference_cpp, cpp_code)
            
        if not compiles:
            iteration_result["error_message"] = error_message
            iteration_result["error_analysis"] = self.error_analyzer.analyze(error_message)
        
        iterations.append(iteration_result)
        
        # Feedback loop
        if self.feedback_enabled and not compiles:
            for i in range(max_iterations):
                # Apply feedback
                improved_cpp = model.apply_feedback(
                    error_message, current_translation, fortran_code, self.feedback_template
                )
                
                # Test compilation again
                compiles, error_message = self.compiler.test_compilation(improved_cpp)
                
                # Store iteration results
                iteration_result = {
                    "iteration": i + 1,
                    "compiles": compiles,
                    "cpp_code": improved_cpp
                }
                
                if reference_cpp and "codebleu" in self.metrics:
                    iteration_result["codebleu"] = self.codebleu.calculate(reference_cpp, improved_cpp)
                    
                if not compiles:
                    iteration_result["error_message"] = error_message
                    iteration_result["error_analysis"] = self.error_analyzer.analyze(error_message)
                
                iterations.append(iteration_result)
                current_translation = improved_cpp
                
                # If compilation succeeds, break the loop
                if compiles:
                    break
        
        # Final results
        final_iteration = iterations[-1]
        results = {
            "model_name": model_name,
            "compiles": final_iteration["compiles"],
            "iterations_required": len(iterations) - 1,
            "iterations": iterations,
            "final_translation": final_iteration["cpp_code"]
        }
        
        if reference_cpp and "codebleu" in self.metrics:
            results["final_codebleu"] = final_iteration.get("codebleu")
            results["codebleu_improvement"] = (final_iteration.get("codebleu", 0) - 
                                            iterations[0].get("codebleu", 0))
        
        return results
    
    def evaluate_test_suite(self, test_suite_name: str) -> Dict:
        """
        Evaluate all models on a test suite.
        
        Args:
            test_suite_name: Name of test suite
            
        Returns:
            Evaluation results for all models
        """
        # In practice, would load test cases from files
        # This is a simplified placeholder
        print(f"Would evaluate all models on test suite: {test_suite_name}")
        return {"status": "not_implemented_in_example"}
    
    def analyze_results(self, results: Dict) -> Dict:
        """
        Analyze evaluation results.
        
        Args:
            results: Evaluation results
            
        Returns:
            Analysis of results
        """
        # In practice, would perform statistical analysis
        # This is a simplified placeholder
        print("Would analyze results")
        return {"status": "not_implemented_in_example"}
    
    def generate_visualizations(self, analysis: Dict) -> Dict:
        """
        Generate visualizations from analysis.
        
        Args:
            analysis: Analysis results
            
        Returns:
            Generated visualizations
        """
        # In practice, would generate various visualizations
        # This is a simplified placeholder
        print("Would generate visualizations")
        return {"status": "not_implemented_in_example"}
```

### 3. Framework Initialization (`__init__.py`)

```python
from .model_interface import ModelInterface, HuggingFaceModelInterface, ModelRegistry
from .evaluation import TranslationFramework, CompilationTester, CodeBleuCalculator, ErrorAnalyzer

__all__ = [
    'ModelInterface',
    'HuggingFaceModelInterface',
    'ModelRegistry',
    'TranslationFramework',
    'CompilationTester',
    'CodeBleuCalculator',
    'ErrorAnalyzer'
]
```

## Usage Example

Below is a conceptual example of how the framework would be used:

```python
from framework import TranslationFramework, ModelRegistry

# Initialize models
models = ModelRegistry.load_models(['codellama', 'mixtral', 'deepseek-coder:7b'])

# Initialize framework
framework = TranslationFramework(
    models=models,
    metrics=['codebleu', 'compilation_success'],
    feedback_enabled=True
)

# Example Fortran code
fortran_code = """
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
"""

# Reference C++ translation
reference_cpp = """
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
"""

# Evaluate translation for a specific model
results = framework.evaluate_translation(
    model_name='codellama',
    fortran_code=fortran_code,
    reference_cpp=reference_cpp,
    max_iterations=3
)

# Print results
print(f"Model: {results['model_name']}")
print(f"Compiles: {results['compiles']}")
print(f"Iterations required: {results['iterations_required']}")
if 'final_codebleu' in results:
    print(f"Final CodeBLEU: {results['final_codebleu']:.3f}")
    print(f"CodeBLEU improvement: {results['codebleu_improvement']:.3f}")
```

## Notes

This is a simplified reimplementation that demonstrates the architecture and approach of our framework. The actual implementation at Los Alamos National Laboratory included more sophisticated components, error handling, and extensive test suites.
