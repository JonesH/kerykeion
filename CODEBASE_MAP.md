# Kerykeion Codebase Map

## Project Structure Overview
```
kerykeion/
├── aspects/          # Aspect calculation modules
├── charts/           # Chart generation and SVG rendering
├── composite_subject_factory.py  # Factory for composite charts
├── kr_types/         # Type definitions and models
├── relationship_score/  # Compatibility scoring system
├── settings/         # Configuration and settings management
├── sweph/           # Swiss Ephemeris data files
└── utilities.py     # Common utilities and helpers
```

## Core Components

### 1. Astrological Subject
Entry point for creating astrological subjects with chart data.

**File:** `kerykeion/astrological_subject.py`
- `class AstrologicalSubject`: Main class for subject calculations
  - Birth data processing
  - Astronomical calculations
  - House and planet positions
  - JSON/model conversion

### 2. Chart Generation
SVG chart rendering system.

**File:** `kerykeion/charts/kerykeion_chart_svg.py`
- `class KerykeionChartSVG`: SVG chart generation
  - Multiple chart types support
  - Customizable themes
  - Template-based SVG generation

**Supporting Files:**
- `charts/charts_utils.py`: Drawing utilities
- `charts/draw_planets.py`: Planet rendering
- `charts/templates/*.xml`: SVG templates
- `charts/themes/*.css`: Chart themes

### 3. Aspect Calculation

**Files:**
- `aspects/natal_aspects.py`: Natal chart aspects
- `aspects/synastry_aspects.py`: Synastry aspects
  - `class SynastryAspects`: Aspect calculations between subjects
- `aspects/aspects_utils.py`: Aspect calculation utilities
- `aspects/transits_time_range.py`: Transit aspects over time

### 4. Type System

**Directory:** `kerykeion/kr_types/`
- `kr_models.py`: Pydantic models for data structures
  - `AstrologicalSubjectModel`, `KerykeionPointModel`, etc.
- `kr_literals.py`: Literal types for type safety
- `settings_models.py`: Settings and configuration models
- `kerykeion_exception.py`: Custom exception types

### 5. Relationship Analysis

**Directory:** `kerykeion/relationship_score/`
- `relationship_score.py`: Core scoring logic
  - `class RelationshipScore`: Compatibility calculations
- `relationship_score_factory.py`: Factory pattern implementation

### 6. Settings System

**Directory:** `kerykeion/settings/`
- `kerykeion_settings.py`: Settings management
  - Settings loading and merging
  - Default configuration handling
- `config_constants.py`: Configuration constants
- `kr.config.json`: Default configuration file

### 7. Additional Features

- **Ephemeris Data Factory:** `ephemeris_data.py`
  - Generation of astronomical data for date ranges
- **Geonames Integration:** `fetch_geonames.py`
  - Geolocation data fetching and timezone handling
- **Report Generation:** `report.py`
  - Formatted chart reports
- **Composite Charts:** `composite_subject_factory.py`
  - Midpoint calculation for composite charts

## Testing Structure

```
tests/
├── aspects/         # Aspect calculation tests
├── charts/          # Chart generation tests
│   └── svg/        # Baseline SVG files for testing
├── settings/        # Settings system tests
└── Test modules for each component
```

## External Dependencies
- Swiss Ephemeris (pyswisseph)
- Pydantic for data validation
- Scour for SVG optimization
- Standard Python modules for math and datetime operations

## Key Features
1. Supports multiple house systems and zodiac types
2. Comprehensive aspect calculations
3. SVG-based chart generation with themes
4. Relationship compatibility scoring
5. Timezone-aware calculations
6. Multiple language support
7. Type-safe data models

## Development Notes
- Type hints throughout codebase
- Poetry-based dependency management
- Comprehensive test coverage
- SVG template system for charts
- Modular architecture for extensibility

Last updated: April 2025
