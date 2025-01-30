# Design System ACL 🎨

This repository contains a comprehensive solution for creating and generating React components for a design system. It consists of two main parts:

1. A React application (`react-app/`) that serves as a showcase and testing ground for design system components
2. A React Component Generator (`react-component-generator/`) that uses AI to generate new components based on examples

## Project Structure 📁

```
.
├── react-app/                 # React application with example components
│   ├── src/                  # Source code for the React app
│   ├── package.json          # Dependencies and scripts
│   └── ...                   # Other React app files
│
└── react-component-generator/ # AI-powered component generator
    ├── src/                  # Source code for the generator
    ├── templates/            # Component templates
    ├── generated_components/ # Output directory for generated components
    └── docs/                 # Documentation files
```

## React Application (react-app/) 🚀

The React application serves as:
- A living showcase of the design system components
- A testing ground for component development
- A source of examples for the AI component generator

### Technical Stack
- React 18
- TypeScript
- Modern React patterns and best practices
- Component-first architecture

### Getting Started with the React App

1. Navigate to the React app directory:
```bash
cd react-app
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

## React Component Generator (react-component-generator/) 🤖

An AI-powered tool that generates production-ready React components using Google's Gemini AI. This application helps developers quickly create customizable components by learning from existing examples in the design system.

### Features
- 🎯 Generates TypeScript React components
- 🎨 Creates matching CSS files with BEM methodology
- 📚 Produces usage examples and documentation
- ✨ Supports various component types (Buttons, Lists, Dialogs, etc.)
- 🔍 Learns from existing components to maintain consistency

### Technical Stack
- Python with Streamlit
- Google Gemini AI
- Modern component generation patterns
- Intelligent template system

### Getting Started with the Generator

1. Navigate to the generator directory:
```bash
cd react-component-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your Google Cloud Project and Gemini API key

5. Start the Streamlit application:
```bash
streamlit run src/app.py
```

## Workflow 🔄

1. **Component Development**
   - Create initial components in the React app
   - Test and refine the components
   - Document component patterns and usage

2. **Component Generation**
   - Use the generator to create new components
   - The generator learns from existing components
   - Generated components maintain consistency with the design system

3. **Integration**
   - Move generated components to the React app
   - Test and validate the components
   - Iterate and refine as needed

## Contributing 🤝

We welcome contributions to both the React application and the component generator. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

Built with ❤️ for better component development 