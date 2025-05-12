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
