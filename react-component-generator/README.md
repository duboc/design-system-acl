# React Component Generator 🧩

A powerful AI-powered tool that generates production-ready React components using Google's Gemini AI. This application helps developers quickly create customizable, production-ready React components following modern best practices and design patterns.

![React Component Generator](./assets/preview.png)

## ✨ Features

### Component Types
- 🔘 **Buttons** - Customizable buttons with various styles and states
- 📋 **Lists** - Flexible list components with different layouts
- 🪟 **Dialogs** - Modal dialogs with customizable headers and actions
- 🎴 **Cards** - Content containers with various layouts
- ⌨️ **Inputs** - Form input elements with validation
- 📝 **Forms** - Complete form components with validation
- 🎨 **Custom** - Create your own custom component types

### Customization Options
- 🎭 **Multiple Variants** - Primary, secondary, outline, success, warning, error, info
- 📏 **Size Options** - Small, medium, large, custom
- 🛠️ **Advanced Features**:
  - Animations and transitions
  - Responsive design
  - Dark mode support
  - Accessibility (ARIA) compliance
  - Custom styling options
  - State management integration
  - Form validation
  - Asynchronous operations

### Developer Experience
- 👁️ **Real-time Preview** - See your component as you configure it
- 📦 **Complete Package** - Get all necessary files in one download
- 🔍 **Template Explorer** - Learn from example components
- 📋 **Generation Logs** - Track the generation process
- 💅 **Modern Styling** - CSS with BEM methodology
- 📱 **Responsive Design** - Works on all screen sizes

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Node.js and npm (for running generated components)
- Google Cloud Project with Gemini API enabled

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/react-component-generator.git
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

4. Set up environment variables:
```bash
export GCP_PROJECT="your-project-id"  # On Windows: set GCP_PROJECT=your-project-id
```

### Running the Application

1. Start the Streamlit server:
```bash
streamlit run src/app.py
```

2. Open your browser and navigate to:
```
http://localhost:8501
```

## 🎯 Usage

1. **Select Component Type**
   - Choose from predefined components or create a custom one
   - Enter a name for custom components

2. **Configure Options**
   - Select desired variants (primary, secondary, etc.)
   - Choose size options
   - Enable additional features

3. **Add Custom Requirements**
   - Specify any additional requirements or specifications
   - Add custom styling needs

4. **Generate Component**
   - Click "Generate Component" to create your component
   - Review the generated files
   - Download the component package

## 📦 Generated Files

Each component generation creates:
- `ComponentName.tsx` - Main component file with TypeScript
- `ComponentName.css` - Styles using BEM methodology
- `ComponentNameProps.ts` - TypeScript interfaces/types
- `ComponentNameExample.tsx` - Usage examples
- `package.json` - Dependencies and configuration

## 🔧 Configuration

The application supports various configuration options:
- Component templates customization
- Styling preferences
- Output directory structure
- Generation settings

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the component generation
- Streamlit for the web interface
- React community for inspiration and best practices

## 📞 Support

If you have any questions or need help:
- Open an issue
- Check our [documentation](docs/README.md)
- Contact the maintainers

---

Made with ❤️ by [Your Name/Organization] 