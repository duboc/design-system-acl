import os
import json
import logging
from typing import Dict, List
import re
from .gemini_client import GeminiRegionClient

class ComponentGenerator:
    def __init__(self, gemini_client: GeminiRegionClient):
        """Initialize ComponentGenerator with a GeminiRegionClient instance"""
        self.gemini_client = gemini_client
        self.logger = logging.getLogger(__name__)
        self.load_templates()

    def load_templates(self):
        """Load example components as templates"""
        self.templates = {}
        template_types = ["Button", "List", "Dialog"]
        
        template_dir = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        
        for component_type in template_types:
            component_files = {}
            
            # Load main component file
            tsx_content = self._read_template(f"{component_type}.tsx")
            if tsx_content:
                component_files["tsx"] = tsx_content
            
            # Load CSS file
            css_content = self._read_template(f"{component_type}.css")
            if css_content:
                component_files["css"] = css_content
            
            # Load package.json (shared across all components)
            pkg_content = self._read_template("package.json")
            if pkg_content:
                component_files["package"] = pkg_content
            
            # Only add template if we have the main component file
            if component_files.get("tsx"):
                self.templates[component_type] = component_files
                self.logger.info(f"Loaded template for {component_type}")
            else:
                self.logger.warning(f"Skipping {component_type} template - missing main component file")

    def _read_template(self, filename: str) -> str:
        """Read template file content"""
        template_path = os.path.join(os.path.dirname(__file__), "..", "..", "templates", filename)
        try:
            with open(template_path, "r", encoding='utf-8') as f:
                content = f.read()
                self.logger.info(f"Successfully read template file: {filename}")
                return content
        except FileNotFoundError:
            self.logger.warning(f"Template file not found: {template_path}")
            return ""
        except Exception as e:
            self.logger.error(f"Error reading template file {filename}: {str(e)}")
            return ""

    def _extract_code_content(self, content: str) -> str:
        """Extract clean code content from generated output"""
        # Remove markdown code blocks
        content = re.sub(r'```[a-z]*\n', '', content)
        content = re.sub(r'\n```', '', content)
        
        # Remove backticks
        content = content.replace('`', '')
        
        # Remove instruction comments
        content = re.sub(r"\/\*\*?\s*Example.*?\*\/", "", content, flags=re.DOTALL)
        content = re.sub(r"\/\*\*?\s*Remember.*?\*\/", "", content, flags=re.DOTALL)
        content = re.sub(r"\/\/\s*Example.*?$", "", content, flags=re.MULTILINE)
        content = re.sub(r"\/\/\s*Remember.*?$", "", content, flags=re.MULTILINE)
        
        # Clean whitespace
        lines = [line.rstrip() for line in content.splitlines() if line.strip()]
        return "\n".join(lines)

    def _create_prompt(
        self,
        component_name: str,
        component_type: str,
        variants: List[str],
        sizes: List[str],
        features: List[str],
        custom_requirements: str
    ) -> str:
        """Create the generation prompt"""
        template = self.templates.get(component_type, {})
        
        # Include package.json template structure
        package_template = """{
  "name": "@design-system/component",
  "version": "1.0.0",
  "description": "React component library",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "scripts": {
    "build": "tsc",
    "test": "jest",
    "lint": "eslint ."
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "peerDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "typescript": "^5.0.0"
  }
}"""
        
        prompt = f"""Generate a React component with these specifications:
Component Name: {component_name}
Type: {component_type}
Variants: {', '.join(variants)}
Sizes: {', '.join(sizes)}
Features: {', '.join(features)}
Requirements: {custom_requirements}

IMPORTANT CSS REQUIREMENTS:
1. Use regular CSS imports (import './Component.css') instead of CSS modules
2. Use BEM-style class naming (e.g., component--variant, component--size)
3. Import CSS file directly in the component file

Reference Templates:
TypeScript: {template.get('tsx', '')}
CSS: {template.get('css', '')}
Props: {template.get('props', '')}

Package.json Template (use this structure):
{package_template}

Respond with a JSON object containing these files:
{{"files": {{
    "{component_name}.tsx": "<component code>",
    "{component_name}.css": "<css code>",
    "{component_name}Props.ts": "<props code>",
    "{component_name}Example.tsx": "<example code>",
    "package.json": "<package.json content following the template structure above>"
}}}}

IMPORTANT: 
1. Return ONLY the JSON object
2. The package.json MUST include the dependencies field with at least React dependencies
3. Follow the package.json template structure exactly
4. Use regular CSS imports and BEM-style class names like in the example template"""
        
        return prompt

    def generate_component(self, component_name: str, component_type: str, variants: List[str], sizes: List[str], features: List[str], custom_requirements: str) -> Dict[str, str]:
        """Generate component files using Gemini"""
        try:
            prompt = self._create_prompt(component_name, component_type, variants, sizes, features, custom_requirements)
            response = self.gemini_client.generate_content(prompt, response_mime_type="application/json")
            
            try:
                files = json.loads(response)["files"]
            except (json.JSONDecodeError, KeyError) as e:
                raise ValueError(f"Invalid response format: {str(e)}")
            
            files = {filename: self._extract_code_content(content) for filename, content in files.items()}
            self._validate_files(files, component_name)
            self._validate_component_structure(files, component_name)
            return files
            
        except Exception as e:
            self.logger.error(f"Component generation failed: {str(e)}")
            raise

    def _validate_files(self, files: Dict[str, str], component_name: str):
        """Validate required files and their content"""
        # Check required files
        required_files = [
            f"{component_name}.tsx",
            f"{component_name}.css",
            f"{component_name}Props.ts",
            f"{component_name}Example.tsx",
            "package.json"
        ]
        
        missing_files = [f for f in required_files if f not in files]
        if missing_files:
            raise ValueError(f"Missing required files: {', '.join(missing_files)}")
        
        # Validate file contents
        for filename, content in files.items():
            if not content or not content.strip():
                raise ValueError(f"Empty content for file: {filename}")
            
            # TypeScript file validation
            if filename.endswith('.tsx'):
                if 'import React' not in content:
                    raise ValueError(f"Missing React import in {filename}")
                if 'export' not in content:
                    raise ValueError(f"Missing export in {filename}")
            
            # CSS module validation
            if filename.endswith('.css'):
                if not any(c in content for c in ['.', '#', '@media']):
                    raise ValueError(f"Invalid CSS content in {filename}")
            
            # Props validation
            if filename.endswith('Props.ts'):
                if 'interface' not in content and 'type' not in content:
                    raise ValueError(f"Missing type definitions in {filename}")
            
            # Package.json validation
            if filename == 'package.json':
                try:
                    pkg_data = json.loads(content)
                    required_fields = ['name', 'version', 'dependencies']
                    missing_fields = [f for f in required_fields if f not in pkg_data]
                    if missing_fields:
                        raise ValueError(f"Missing fields in package.json: {', '.join(missing_fields)}")
                except json.JSONDecodeError:
                    raise ValueError("Invalid package.json format")

    def _validate_component_structure(self, files: Dict[str, str], component_name: str):
        """Validate component structure and relationships"""
        main_component = files.get(f"{component_name}.tsx", "")
        props_file = files.get(f"{component_name}Props.ts", "")
        css_file = files.get(f"{component_name}.css", "")
        
        # Check props import - allow different valid import patterns
        valid_props_imports = [
            f"import type {{ {component_name}Props }}", # Direct type import
            f"import {{ {component_name}Props }}", # Regular import
            f"import type * as Types", # Namespace import
            f"import * as Types", # Namespace import
            "import type {", # Grouped imports
            "import {" # Grouped imports
        ]
        
        if not any(pattern in main_component for pattern in valid_props_imports):
            raise ValueError(f"Props not properly imported in {component_name}.tsx")
        
        # Check CSS import - allow both module and regular imports
        valid_css_imports = [
            f"import styles from", # CSS modules
            f"import './{component_name}.css'", # Regular CSS import
        ]
        if not any(pattern in main_component for pattern in valid_css_imports):
            raise ValueError(f"CSS not properly imported in {component_name}.tsx")
        
        # Check CSS classes usage - adapt for both module and regular CSS
        css_classes = re.findall(r'\.([a-zA-Z0-9_-]+)\s*{', css_file)
        
        # For regular CSS, check for class names in string literals
        uses_regular_css = f"import './{component_name}.css'" in main_component
        if uses_regular_css:
            # Look for class names in template literals or string concatenation
            class_usage_patterns = [
                r'className=["`\']([^"`\']+)["`\']',  # className="something"
                r'className=\{[`"\'](.*?)[`"\']\}',   # className={'something'}
                r'className=\{.*?\}',                 # className={dynamic}
            ]
            has_classes = any(
                re.search(pattern, main_component)
                for pattern in class_usage_patterns
            )
            if not has_classes:
                raise ValueError("No CSS classes used in component")
        else:
            # CSS modules validation
            if not any(c in main_component for c in css_classes):
                raise ValueError("CSS classes not used in component")
        
        # Check props interface/type - allow both interface and type
        valid_props_patterns = [
            f"interface {component_name}Props",
            f"type {component_name}Props",
            "export interface",
            "export type"
        ]
        if not any(pattern in props_file for pattern in valid_props_patterns):
            raise ValueError("Props interface/type not properly defined")

    def validate_component(self, files: Dict[str, str]) -> bool:
        """Final validation of the complete component"""
        try:
            # Additional validations could be added here
            return True
        except Exception as e:
            self.logger.error(f"Component validation failed: {str(e)}")
            return False