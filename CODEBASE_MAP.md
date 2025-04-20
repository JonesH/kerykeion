# Kerykeion Codebase Map

## Project Overview
- **Name**: Kerykeion
- **Version**: 4.26.1
- **Purpose**: Python library for astrological calculations and chart generation

## Key Modules and Components

### Core Modules
- `astrological_subject.py`: Primary class for creating astrological subjects
- `charts/kerykeion_chart_svg.py`: SVG chart generation
- `aspects/`: Aspect calculation modules
- `relationship_score/`: Relationship compatibility evaluation

### Key Classes
1. `AstrologicalSubject`
   - Instantiates astrological subjects
   - Calculates planetary and house positions
   - Supports various astrological modes

2. `KerykeionChartSVG`
   - Generates SVG charts
   - Supports multiple chart types (natal, synastry, transit, composite)
   - Offers theme and language customization

3. `SynastryAspects`
   - Calculates aspects between two astrological subjects

4. `CompositeSubjectFactory`
   - Creates composite chart models

### Test Coverage
- Extensive test suite covering:
  - Astrological calculations
  - Chart generation
  - Aspect detection
  - Relationship scoring

## Technical Specifications
- **Python Version**: 3.9+
- **Key Dependencies**:
  - pyswisseph
  - pydantic
  - requests
  - pytz

## Development Tools
- Package Management: Poetry
- Testing: pytest
- Code Quality: mypy, black
- Documentation: pdoc

## Supported Features
- Multiple zodiac types (Tropical, Sidereal)
- Various house systems
- Multilingual chart generation
- Customizable chart themes
- Astrological aspect detection
- Relationship compatibility scoring

## Extensibility Points
- Configurable celestial points
- Customizable chart generation
- Supports different astrological perspectives

## Licensing
- AGPL-3.0 License
- Encourages open-source contributions
