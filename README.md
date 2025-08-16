# ClauseWise

**AI-Powered Legal Document Analysis Tool**

ClauseWise is a comprehensive legal document analysis platform that uses artificial intelligence to extract, categorize, and simplify complex legal documents. It helps legal professionals, business owners, and individuals understand contracts and legal agreements through intelligent entity extraction, clause analysis, and natural language processing.

## 🚀 Features

### 📊 Entity Extraction & Analysis
- **Smart Detection**: Automatically identifies and categorizes key document elements
- **Entity Types**: Dates, monetary values, parties, contact information, legal terms, obligations
- **Interactive Exploration**: Click-to-explore modal interface with search and filtering
- **Pattern Analysis**: Identifies duplicates, suspicious entries, and provides recommendations

### 🔍 Document Analysis
- **Multi-Tab Interface**: Organized view of entities, clauses, and raw text
- **Clause Breakdown**: Individual clause analysis with expand/collapse functionality
- **AI Simplification**: Convert complex legal language into plain English
- **Visual Categorization**: Color-coded entity types for easy identification

### 🤖 AI Assistant Integration
- **Contextual Chat**: Ask questions about document content and implications
- **Quick Questions**: Pre-built queries for common legal concerns
- **Real-time Analysis**: Instant responses about risks, obligations, and next steps
- **Legal Guidance**: General legal advice with professional disclaimer

### 📱 User Experience
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Modern Interface**: Clean, intuitive design with smooth animations
- **Accessibility**: Keyboard shortcuts, tooltips, and screen reader support
- **Export Capabilities**: Download entities as CSV, copy to clipboard

## 🛠️ Technology Stack

### Frontend
- **HTML5/CSS3**: Modern semantic markup and responsive styling
- **JavaScript (ES6+)**: Interactive functionality and API communication
- **Font Awesome**: Professional icon library
- **CSS Grid/Flexbox**: Advanced layout management

### Backend Integration
- **RESTful API**: Clean endpoints for document processing
- **AI Processing**: Integration with language models for analysis
- **Real-time Communication**: WebSocket support for chat functionality

### Key Components
```
├── Templates/
│   ├── analysis_results.html    # Main analysis interface
│   └── base.html               # Base template
├── Static/
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript modules
│   └── assets/                # Images and icons
└── API/
    ├── document_processor.py  # Document analysis engine
    ├── entity_extractor.py   # Entity detection logic
    └── ai_chat.py            # Chat assistant backend
```

## 🏗️ Architecture

### Entity Processing Pipeline
1. **Document Upload** → Parse and extract text content
2. **NLP Analysis** → Apply named entity recognition and pattern matching
3. **Categorization** → Sort entities into predefined types
4. **Enrichment** → Add metadata, frequency analysis, and validation
5. **Presentation** → Render in interactive UI components

### Modal System
- **Dynamic Content Generation**: Build modal content based on entity type
- **Search & Filter**: Real-time filtering with performance optimization
- **Export Functions**: Multiple format support (CSV, JSON, plain text)
- **Accessibility**: Keyboard navigation and screen reader support

## 📋 Entity Types

| Type | Icon | Description | Examples |
|------|------|-------------|----------|
| **Dates** | 📅 | Contract dates, deadlines, milestones | `2024-01-15`, `March 31st, 2024` |
| **Monetary Values** | 💰 | Amounts, fees, penalties | `$50,000`, `€25,000`, `₹1,00,000` |
| **Parties** | 👥 | Individuals, companies, organizations | `ABC Corp`, `John Smith` |
| **Contact Info** | 📧 | Email addresses, phone numbers | `legal@company.com`, `+1-555-0123` |
| **Legal Terms** | ⚖️ | Legal concepts, clauses | `Force Majeure`, `Indemnification` |
| **Obligations** | ✅ | Duties, requirements, responsibilities | `Payment due within 30 days` |

## 🎨 UI Components

### Entity Cards
```html
<div class="entity-card" onclick="showEntityModal('dates', entityList)">
    <div class="entity-header">
        <div class="entity-icon"><i class="fas fa-calendar-alt"></i></div>
        <div class="entity-count">3</div>
        <div class="entity-label">Dates</div>
    </div>
    <div class="entity-body">
        <div class="entity-list"><!-- Entity items --></div>
        <div class="entity-badge">Click to explore</div>
    </div>
</div>
```

### Modal Interface
- **Enhanced Search**: Real-time filtering with result counters
- **Statistical Overview**: Total count, unique items, type-specific metrics
- **Action Buttons**: Copy, export, generate reports
- **Keyboard Support**: Escape to close, tab navigation

### Chat Interface
- **Message History**: Persistent conversation context
- **Typing Indicators**: Visual feedback during AI processing
- **Quick Questions**: One-click common queries
- **Error Handling**: Graceful degradation and retry mechanisms

## 🔧 Configuration

### Settings Object
```javascript
const settings = {
    api_endpoint: '/api/v1/',
    max_entities: 100,
    chat_history_limit: 10,
    export_formats: ['csv', 'json', 'txt'],
    ai_model: 'gpt-3.5-turbo',
    entity_confidence_threshold: 0.8
};
```

### Customization Options
- **Theme Variables**: CSS custom properties for easy theming
- **Entity Types**: Configurable entity categories and detection patterns
- **AI Prompts**: Customizable system prompts for different document types
- **Export Templates**: Configurable output formats and layouts

## 📱 Responsive Design

### Breakpoints
- **Desktop**: `> 1200px` - Full two-column layout
- **Tablet**: `768px - 1200px` - Stacked layout with collapsible sidebar
- **Mobile**: `< 768px` - Single column with optimized touch targets

### Mobile Optimizations
- **Touch-Friendly**: Larger tap targets and swipe gestures
- **Performance**: Lazy loading and optimized animations
- **Offline Support**: Service worker for basic functionality

## ⚡ Performance Features

### Optimization Strategies
- **Lazy Loading**: Load modal content on demand
- **Debounced Search**: Optimized filtering with 300ms delay
- **Virtual Scrolling**: Handle large entity lists efficiently
- **Caching**: Store processed results in memory

### Error Handling
- **Graceful Degradation**: Fallback UI states for API failures
- **User Feedback**: Toast notifications for all user actions
- **Recovery Options**: Retry mechanisms and alternative workflows

## 🔒 Security Considerations

### Data Protection
- **No Persistent Storage**: All data handled in memory during session
- **Sanitized Inputs**: XSS prevention for user-generated content
- **API Security**: Token-based authentication for backend communication
- **Privacy**: No data logging or external tracking

## 🚦 Browser Support

### Supported Browsers
- **Chrome**: Version 80+ (recommended)
- **Firefox**: Version 75+
- **Safari**: Version 13+
- **Edge**: Version 80+

### Required Features
- ES6+ JavaScript support
- CSS Grid and Flexbox
- Fetch API
- Local Storage (optional)

## 🎯 Usage Examples

### Basic Document Analysis
1. Upload document through the main interface
2. Review extracted entities in the grid view
3. Click entity cards to explore detailed breakdowns
4. Use the AI chat for specific questions

### Advanced Entity Exploration
1. Open entity modal from the grid
2. Use search to filter specific items
3. Export entities in preferred format
4. Generate AI-powered analysis reports

### AI-Assisted Review
1. Ask contextual questions about document content
2. Request clause simplification
3. Get risk assessments and recommendations
4. Explore legal implications with guided prompts

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines for:
- Code style and formatting standards
- Testing requirements and procedures
- Documentation standards
- Pull request process

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- **Documentation**: Check the inline code comments and this README
- **Issues**: Report bugs via GitHub Issues
- **Feature Requests**: Submit enhancement proposals
- **Community**: Join our Discord server for discussions

---

**Built with ❤️ for the legal community** - Making legal documents accessible to everyone.
