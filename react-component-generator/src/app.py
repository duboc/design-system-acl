import streamlit as st
import os
import tempfile
import json
import logging
from pathlib import Path
import zipfile
import io
from datetime import datetime
import streamlit.components.v1 as components

from utils.gemini_client import GeminiRegionClient
from utils.component_generator import ComponentGenerator
from utils.file_utils import save_component_files

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a StringIO object to capture logs
log_stream = io.StringIO()
stream_handler = logging.StreamHandler(log_stream)
stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(stream_handler)

# Page configuration
st.set_page_config(
    page_title="React Component Generator",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main > div {
        padding: 2rem;
    }
    .stTabs > div > div {
        gap: 1rem;
    }
    .stMarkdown h1 {
        color: #1E88E5;
        padding-bottom: 1rem;
        border-bottom: 2px solid #E3F2FD;
    }
    .stMarkdown h2 {
        color: #424242;
        margin-top: 2rem;
    }
    .stMarkdown h3 {
        color: #616161;
    }
    .stButton > button {
        width: 100%;
    }
    .stTextArea > div > textarea {
        min-height: 150px;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E8F5E9;
        border: 1px solid #81C784;
        color: #2E7D32;
    }
    .info-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #E3F2FD;
        border: 1px solid #64B5F6;
        color: #1565C0;
    }
    .warning-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FFF3E0;
        border: 1px solid #FFB74D;
        color: #EF6C00;
    }
    .error-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #FFEBEE;
        border: 1px solid #E57373;
        color: #C62828;
    }
    .component-preview {
        background-color: #FAFAFA;
        border: 1px solid #EEEEEE;
        border-radius: 0.5rem;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .code-preview {
        background-color: #263238;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
        color: #EEFFFF;
    }
    .stSelectbox > div > div {
        background-color: white;
    }
    .stMultiSelect > div > div {
        background-color: white;
    }
</style>
""", unsafe_allow_html=True)

def init_session_state():
    """Initialize session state variables"""
    if 'generated_component' not in st.session_state:
        st.session_state.generated_component = None
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    if 'error' not in st.session_state:
        st.session_state.error = None
    if 'templates' not in st.session_state:
        st.session_state.templates = None
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "generator"

def add_log(message: str):
    """Add a timestamped log message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.logs.append(f"[{timestamp}] {message}")
    logger.info(message)

def save_generation_logs(component_name: str, logs: list):
    """Save generation logs to file"""
    output_dir = os.path.join('generated_components', component_name.lower())
    os.makedirs(output_dir, exist_ok=True)
    
    log_file = os.path.join(output_dir, f"{component_name}_generation.log")
    with open(log_file, 'w') as f:
        f.write('\n'.join(logs))
    add_log(f"Saved generation logs to {log_file}")

def create_component_preview(component_files: dict, component_name: str) -> str:
    """Create an HTML preview of the component"""
    # Implementation of preview generation
    pass

def display_component_files(files: dict, component_name: str):
    """Display component files in tabs"""
    tabs = st.tabs(["Component", "CSS", "Props", "Example", "Package"])
    
    with tabs[0]:
        st.markdown("### Component Code")
        st.code(files.get(f"{component_name}.tsx", ""), language="typescript")
    with tabs[1]:
        st.markdown("### Styles")
        st.code(files.get(f"{component_name}.css", ""), language="css")
    with tabs[2]:
        st.markdown("### Props Interface")
        st.code(files.get(f"{component_name}Props.ts", ""), language="typescript")
    with tabs[3]:
        st.markdown("### Usage Example")
        st.code(files.get(f"{component_name}Example.tsx", ""), language="typescript")
    with tabs[4]:
        st.markdown("### Package Configuration")
        st.code(files.get("package.json", ""), language="json")

def create_download_zip(files: dict, component_name: str) -> bytes:
    """Create a zip file containing all component files"""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_name, content in files.items():
            zip_file.writestr(f"{component_name}/{file_name}", content)
    return zip_buffer.getvalue()

def display_template_files(templates: dict, component_type: str):
    """Display template files in tabs"""
    if not templates or not templates.get(component_type):
        st.info("No template files available for this component type.")
        return
        
    template = templates[component_type]
    
    # Create tabs only for available files
    available_files = []
    if template.get("tsx"): available_files.append("Component")
    if template.get("css"): available_files.append("CSS")
    if template.get("package"): available_files.append("Package")
    
    if not available_files:
        st.warning("No template files found for this component.")
        return
    
    tabs = st.tabs(available_files)
    
    # Display files in their respective tabs
    for tab_idx, tab_name in enumerate(available_files):
        with tabs[tab_idx]:
            st.markdown(f"### {tab_name} Template")
            if tab_name == "Component":
                st.code(template.get("tsx", ""), language="typescript")
            elif tab_name == "CSS":
                st.code(template.get("css", ""), language="css")
            elif tab_name == "Package":
                st.code(template.get("package", ""), language="json")

def main():
    init_session_state()
    
    # Header section
    st.title("🧩 React Component Generator")
    st.markdown("""
    <div class="info-message">
        Generate production-ready React components using AI. Configure your component using the sidebar options.
    </div>
    """, unsafe_allow_html=True)

    # Initialize clients
    try:
        gemini_client = GeminiRegionClient(logger=logger)
        component_generator = ComponentGenerator(gemini_client)
        # Store templates in session state for reuse
        if st.session_state.templates is None:
            st.session_state.templates = component_generator.templates
    except Exception as e:
        st.error(f"Failed to initialize AI client: {str(e)}")
        return

    # Main navigation
    tabs = st.tabs(["🎨 Component Generator", "📚 Template Explorer", "📋 Generation Logs"])

    # Generator Tab
    with tabs[0]:
        # Sidebar configuration
        with st.sidebar:
            st.markdown("## ⚙️ Component Configuration")
            
            component_type = st.selectbox(
                "Component Type",
                ["Button", "List", "Dialog", "Card", "Input", "Form", "Custom"],
                help="Select the type of component you want to generate"
            )

            if component_type == "Custom":
                component_name = st.text_input(
                    "Component Name",
                    "CustomComponent",
                    help="Enter a name for your custom component"
                )
            else:
                component_name = component_type

            variants = st.multiselect(
                "Variants",
                ["primary", "secondary", "outline", "success", "warning", "error", "info"],
                default=["primary", "secondary"],
                help="Select the variants your component should support"
            )

            sizes = st.multiselect(
                "Sizes",
                ["small", "medium", "large", "custom"],
                default=["small", "medium", "large"],
                help="Select the sizes your component should support"
            )

            features = st.multiselect(
                "Features",
                ["animations", "responsive", "dark mode", "accessibility", "custom styles", 
                 "state management", "form validation", "async operations"],
                default=["responsive", "accessibility"],
                help="Select additional features for your component"
            )

            st.markdown("### 📝 Custom Requirements")
            custom_requirements = st.text_area(
                "Additional specifications or requirements",
                "Add any specific requirements or descriptions...",
                help="Add any additional requirements or specifications for your component"
            )

            st.markdown("---")
            
            if st.button("🚀 Generate Component", type="primary", use_container_width=True):
                try:
                    with st.spinner("🔄 Generating component..."):
                        # Clear previous logs
                        st.session_state.logs = []
                        st.session_state.error = None
                        
                        # Log generation start
                        add_log(f"Generating component: {component_name}")
                        add_log(f"Type: {component_type}")
                        add_log(f"Variants: {variants}")
                        add_log(f"Sizes: {sizes}")
                        add_log(f"Features: {features}")
                        
                        # Generate component
                        component_files = component_generator.generate_component(
                            component_name=component_name,
                            component_type=component_type,
                            variants=variants,
                            sizes=sizes,
                            features=features,
                            custom_requirements=custom_requirements
                        )
                        
                        # Save files
                        output_dir = os.path.join('generated_components', component_name.lower())
                        save_component_files(component_files, output_dir)
                        
                        # Save logs
                        save_generation_logs(component_name, st.session_state.logs)
                        
                        # Store in session state
                        st.session_state.generated_component = {
                            'name': component_name,
                            'files': component_files,
                            'directory': output_dir
                        }
                        
                        st.markdown("""
                        <div class="success-message">
                            ✨ Component generated successfully!
                        </div>
                        """, unsafe_allow_html=True)

                except Exception as e:
                    st.session_state.error = str(e)
                    st.markdown(f"""
                    <div class="error-message">
                        ❌ Failed to generate component: {str(e)}
                    </div>
                    """, unsafe_allow_html=True)
                    add_log(f"Error: {str(e)}")

        # Display generated component
        if st.session_state.generated_component:
            st.markdown("## 📦 Generated Component")
            st.markdown(f"""
            <div class="info-message">
                📁 Files saved to: {st.session_state.generated_component['directory']}
            </div>
            """, unsafe_allow_html=True)
            
            display_component_files(
                st.session_state.generated_component['files'],
                st.session_state.generated_component['name']
            )
            
            # Download section
            st.markdown("### 📥 Download")
            zip_data = create_download_zip(
                st.session_state.generated_component['files'],
                st.session_state.generated_component['name']
            )
            st.download_button(
                label="📦 Download Component",
                data=zip_data,
                file_name=f"{st.session_state.generated_component['name']}_component.zip",
                mime="application/zip",
                use_container_width=True
            )

    # Template Explorer Tab
    with tabs[1]:
        st.markdown("## 📚 Template Explorer")
        st.markdown("""
        <div class="info-message">
            Explore example components to understand the structure and patterns used in the generated components.
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.templates:
            template_type = st.selectbox(
                "Select a component template",
                list(st.session_state.templates.keys()),
                key="template_explorer"
            )
            
            if template_type:
                st.markdown(f"### 📁 {template_type} Template")
                st.markdown(f"""
                <div class="component-preview">
                    This is an example implementation of a {template_type} component following best practices.
                </div>
                """, unsafe_allow_html=True)
                display_template_files(st.session_state.templates, template_type)

    # Logs Tab
    with tabs[2]:
        st.markdown("## 📋 Generation Logs")
        if st.session_state.logs:
            for log in reversed(st.session_state.logs):
                st.text(log)
        else:
            st.info("No generation logs available. Generate a component to see the logs.")

    # Display errors if any
    if st.session_state.error:
        st.markdown(f"""
        <div class="error-message">
            ❌ Error: {st.session_state.error}
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()