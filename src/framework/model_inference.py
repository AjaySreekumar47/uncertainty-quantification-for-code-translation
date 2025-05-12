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
