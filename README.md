# Book of Shadows - The Crone

A research-grade, ritual-aware Grimoire IDE and conversational assistant for scholars, practitioners, and writers who author, index, annotate, simulate (symbolically) and cite spells, rituals, and associated folkloric texts.

## Overview

Book of Shadows - The Crone is a sophisticated system designed to help users build a persistent, searchable, and citable Book of Shadows (a living grimoire) that can:

- Ingest books and folk sources
- Author new spells/rituals
- Manage ritual components
- Schedule and annotate practice logs
- Present verifiable provenance for all claims

## Core Features

### 🏛️ Scholarly Approach
- **Rigorous Provenance**: Every claim is backed by precise citations to ingested sources
- **Academic Standards**: Distinguishes between verifiable textual claims and unverifiable supernatural claims
- **Cultural Sensitivity**: Validates ethnographic content and respects cultural boundaries

### 📚 Document Ingestion
- **Multi-format Support**: PDF, EPUB, TXT, Markdown, DOCX, HTML
- **OCR Integration**: Process image-only pages with confidence reporting
- **Intelligent Chunking**: 2000-token chunks with 200-token overlap
- **Vector Database**: Semantic search and retrieval using ChromaDB

### ✍️ Grimoire Authoring
- **Structured Entries**: Title, lineage, ingredients, tools, instructions, notes
- **Citation Integration**: Inline citation insertion with chunk IDs
- **Efficacy Claims**: Tagged as HISTORICAL, RITUAL_TRADITIONAL, PERSONAL_ANECDOTAL, or UNVERIFIABLE_SUPERNATURAL
- **Version Control**: Git-style workflows for collaborative editing

### 🔒 Safety & Ethics
- **Harm Prevention**: Refuses operational instructions for dangerous content
- **Cultural Respect**: Flags restricted or sacred material
- **Legal Compliance**: Copyright-aware excerpt policies
- **Medical Disclaimers**: No professional medical advice

### 🔌 Modular Architecture
- **Plugin System**: Extensible capabilities through plugins
- **Core Plugins**: PDF ingestor, OCR, vector DB, citation manager, ingredients manager, ritual simulator, ethnography validator, safety checker, UI bridge, memory store, auth

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup
```bash
# Clone the repository
git clone <repository-url>
cd book-of-shadows

# Install dependencies
pip install -r requirements.txt

# Run basic test
python test_basic.py
```

### Configuration
Edit `config.yaml` to customize:
- Database settings
- Safety parameters
- Ingestion preferences
- UI preferences
- Plugin configuration

## Usage

### Starting the System
```bash
python main.py
```

### Basic Commands

#### Ingest Documents
```
INGEST file="path/to/document.pdf" TAG tag_name
```

#### Create Spell Entry
```
CREATE_ENTRY title="House Blessing" lineage="County Cork tradition" source=@BOOKID
```

#### Search and Synthesize
```
SYNTHESIZE "protection ritual template" FROM tag:folk-magic FORMAT=ritual-draft+timeline
```

#### Export Citations
```
EXPORT_CITATIONS format=bibtex include_chunks=true
```

### Example Workflow

1. **Ingest Source Material**
   ```bash
   INGEST file="County_Cork_Field_Notes.pdf" TAG county-cork
   ```

2. **Create Ritual Entry**
   ```bash
   CREATE_ENTRY title="House Blessing" lineage="County Cork tradition"
   ```

3. **Add Ingredients and Citations**
   - Use the grimoire editor to add ingredients
   - Insert citations using chunk IDs (e.g., @ETHN002::CHUNK089)

4. **Export for Publication**
   ```bash
   EXPORT_CITATIONS format=bibtex include_chunks=true
   ```

## Architecture

### Core Components
- **main.py**: Application entry point
- **core/**: Core system modules (config, app, safety, memory)
- **plugins/**: Plugin system with extensible capabilities
- **ui/**: User interface components
- **data/**: Persistent storage (vector DB, memory, books)

### Plugin System
Each plugin implements:
- `initialize()`: Setup and configuration
- `execute(capability, **kwargs)`: Core functionality
- `cleanup()`: Resource cleanup

### Safety Framework
- **Content Validation**: Checks for prohibited keywords and dangerous procedures
- **Cultural Sensitivity**: Validates ethnographic content
- **Medical Claims**: Prevents unlicensed medical advice
- **Legal Compliance**: Enforces copyright and legal restrictions

## Development

### Project Structure
```
book_of_shadows/
├── main.py                 # Application entry point
├── config.yaml            # Configuration
├── requirements.txt       # Dependencies
├── core/                  # Core system modules
│   ├── config.py         # Configuration management
│   ├── app.py            # Main application
│   ├── safety.py         # Safety and ethics
│   └── memory.py         # Memory and persistence
├── plugins/               # Plugin system
│   ├── manager.py        # Plugin manager
│   ├── pdf_ingestor.py   # PDF processing
│   ├── vector_db.py      # Vector database
│   ├── citation_manager.py # Citation management
│   └── ...               # Other plugins
├── ui/                    # User interface
│   └── grimoire_editor.py # Spell/ritual editor
└── data/                  # Persistent storage
    ├── vector_db/         # ChromaDB storage
    ├── memory/           # Memory persistence
    └── books/            # Ingested documents
```

### Adding New Plugins
1. Create plugin class inheriting from `BasePlugin`
2. Implement required methods (`initialize`, `execute`, `cleanup`)
3. Create manifest file (`plugin_name.manifest.json`)
4. Register in plugin manager

### Testing
```bash
# Run basic functionality test
python test_basic.py

# Run specific component tests
python -m pytest tests/
```

## Safety & Ethics

### Content Safety
- **Prohibited Content**: Weapons, poisons, explosives, illegal activities
- **Medical Claims**: No professional medical advice
- **Cultural Sensitivity**: Respects sacred and restricted material
- **Copyright Compliance**: Limits excerpts to 200 words

### Disclaimers
All ritual simulations and efficacy claims include:
> Simulation/Claim Notice: Outputs that describe ritual effects are historical, symbolic, or subjective reports from sources. They are not guarantees of physical effects. This system does not perform or recommend any real-world actions that are illegal or dangerous.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

## License

[Add appropriate license]

## Support

For questions or issues:
- Check the documentation
- Review the safety guidelines
- Submit issues through the repository

---

**Book of Shadows - The Crone**: A scholarly approach to grimoire authoring and ritual research. 
