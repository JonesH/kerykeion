# -*- coding: utf-8 -*-
"""
    This is part of Kerykeion (C) 2025 Giacomo Battaglia
    
    This module provides input classes for chart configuration and generation.
    It helps with proper parameter encapsulation and validation for different chart types.
"""

from typing import Union, List, Optional, Literal, Dict, Any, Type, TypeVar, Generic, ClassVar
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field, field_validator

from kerykeion import AstrologicalSubject
from kerykeion.kr_types import (
    KerykeionChartTheme, 
    KerykeionChartLanguage, 
    KerykeionSettingsModel,
    AstrologicalSubjectModel,
    CompositeSubjectModel,
    Planet, 
    AxialCusps, 
    ActiveAspect,
    ChartType
)
from kerykeion.settings.config_constants import DEFAULT_ACTIVE_POINTS, DEFAULT_ACTIVE_ASPECTS


class ChartConfig(BaseModel):
    """
    Common configuration parameters for all chart types.
    
    This class encapsulates configuration options that are common to all chart types,
    providing default values where appropriate.
    
    Attributes:
        output_directory: Directory where SVG files will be saved (default: user's home directory)
        settings_file: Custom settings for colors, aspects, etc. (optional)
        theme: CSS theme for the chart (default: "classic")
        chart_language: Language for chart labels (default: "EN")
        active_points: List of planets/points to display (default: DEFAULT_ACTIVE_POINTS)
        active_aspects: List of aspects to calculate (default: DEFAULT_ACTIVE_ASPECTS)
        double_chart_aspect_grid_type: Display style for dual-chart aspect grids (default: "list")
    """
    output_directory: Union[str, Path, None] = None
    settings_file: Optional[Union[Path, dict, KerykeionSettingsModel]] = None
    theme: Optional[KerykeionChartTheme] = "classic"
    chart_language: KerykeionChartLanguage = "EN" 
    active_points: List[Union[Planet, AxialCusps]] = DEFAULT_ACTIVE_POINTS
    active_aspects: List[ActiveAspect] = DEFAULT_ACTIVE_ASPECTS
    double_chart_aspect_grid_type: Literal["list", "table"] = "list"
    
    @field_validator('output_directory', mode="before")
    def validate_output_directory(cls, v):
        """Convert string paths to Path objects and default to home directory if None."""
        if v is None:
            return Path.home()
        if isinstance(v, str):
            return Path(v)
        return v


class ChartInput(BaseModel):
    """
    Base class for all chart input types.
    
    This abstract base class provides common structure and validation
    for all specific chart input types.
    
    Attributes:
        config: Common chart configuration options
        chart_type: The type of chart to generate (set by subclasses)
    """
    model_config = ConfigDict(arbitrary_types_allowed=True)
    config: ChartConfig = Field(default_factory=ChartConfig)
    chart_type: ClassVar[ChartType] = ""


class NatalChartInput(ChartInput):
    """
    Input parameters for Natal charts.
    
    A Natal chart requires only a single subject (the birth chart).
    
    Attributes:
        subject: The astrological subject for the chart
    
    Example:
        ```python
        # Create a natal chart for a person
        subject = AstrologicalSubject("John Doe", 1990, 1, 1, 12, 0, "New York")
        
        chart_input = NatalChartInput(subject=subject)
        # Optionally customize configuration
        chart_input.config.theme = "dark"
        chart_input.config.chart_language = "DE"
        ```
    """
    chart_type: ClassVar[ChartType] = "Natal"
    subject: Union[AstrologicalSubject, AstrologicalSubjectModel]


class ExternalNatalChartInput(ChartInput):
    """
    Input parameters for External Natal charts.
    
    An External Natal chart shows a birth chart with an external reference ring.
    
    Attributes:
        primary_subject: The main astrological subject for the chart
        external_subject: The external reference subject
    
    Example:
        ```python
        # Create an external natal chart
        primary = AstrologicalSubject("John Doe", 1990, 1, 1, 12, 0, "New York")
        external = AstrologicalSubject("Jane Doe", 1992, 5, 15, 15, 30, "Boston")
        
        chart_input = ExternalNatalChartInput(
            primary_subject=primary,
            external_subject=external
        )
        ```
    """
    chart_type: ClassVar[ChartType] = "ExternalNatal"
    primary_subject: Union[AstrologicalSubject, AstrologicalSubjectModel]
    external_subject: Union[AstrologicalSubject, AstrologicalSubjectModel]


class SynastryChartInput(ChartInput):
    """
    Input parameters for Synastry charts.
    
    A Synastry chart compares two birth charts to analyze compatibility.
    
    Attributes:
        subject1: The first astrological subject
        subject2: The second astrological subject
    
    Example:
        ```python
        # Create a synastry chart for relationship analysis
        person1 = AstrologicalSubject("John Doe", 1990, 1, 1, 12, 0, "New York")
        person2 = AstrologicalSubject("Jane Doe", 1992, 5, 15, 15, 30, "Boston")
        
        chart_input = SynastryChartInput(
            subject1=person1,
            subject2=person2,
            config=ChartConfig(theme="dark", double_chart_aspect_grid_type="table")
        )
        ```
    """
    chart_type: ClassVar[ChartType] = "Synastry"
    subject1: Union[AstrologicalSubject, AstrologicalSubjectModel]
    subject2: Union[AstrologicalSubject, AstrologicalSubjectModel]


class TransitChartInput(ChartInput):
    """
    Input parameters for Transit charts.
    
    A Transit chart shows current or future planetary positions relative to a birth chart.
    
    Attributes:
        radix_subject: The natal chart subject
        transit_subject: The transit chart subject (current or future time)
    
    Example:
        ```python
        # Create a transit chart
        from datetime import datetime
        
        # Birth chart
        person = AstrologicalSubject("John Doe", 1990, 1, 1, 12, 0, "New York")
        
        # Current transits
        now = datetime.now()
        transit = AstrologicalSubject("Transit", now.year, now.month, now.day, 
                                     now.hour, now.minute, "New York")
        
        chart_input = TransitChartInput(
            radix_subject=person,
            transit_subject=transit
        )
        ```
    """
    chart_type: ClassVar[ChartType] = "Transit"
    radix_subject: Union[AstrologicalSubject, AstrologicalSubjectModel]
    transit_subject: Union[AstrologicalSubject, AstrologicalSubjectModel]


class CompositeChartInput(ChartInput):
    """
    Input parameters for Composite charts.
    
    A Composite chart shows a combined chart for two individuals.
    The composite subject must be created through CompositeSubjectFactory.
    
    Attributes:
        composite_subject: The composite subject model
    
    Example:
        ```python
        # Create a composite chart
        from kerykeion.composite_subject_factory import CompositeSubjectFactory
        
        person1 = AstrologicalSubject("John Doe", 1990, 1, 1, 12, 0, "New York")
        person2 = AstrologicalSubject("Jane Doe", 1992, 5, 15, 15, 30, "Boston")
        
        factory = CompositeSubjectFactory(person1, person2)
        composite = factory.get_midpoint_composite_subject_model()
        
        chart_input = CompositeChartInput(composite_subject=composite)
        ```
    """
    chart_type: ClassVar[ChartType] = "Composite"
    composite_subject: CompositeSubjectModel


class ChartInputFactory:
    """
    Factory for creating chart inputs from astrological subjects.
    
    This factory provides convenience methods to create different
    types of chart inputs without directly instantiating the classes.
    """
    
    @staticmethod
    def create_natal_chart(subject, **config_kwargs):
        """Create a natal chart input."""
        config = ChartConfig(**config_kwargs)
        return NatalChartInput(subject=subject, config=config)
        
    @staticmethod
    def create_external_natal_chart(primary_subject, external_subject, **config_kwargs):
        """Create an external natal chart input."""
        config = ChartConfig(**config_kwargs)
        return ExternalNatalChartInput(
            primary_subject=primary_subject,
            external_subject=external_subject,
            config=config
        )
        
    @staticmethod
    def create_synastry_chart(subject1, subject2, **config_kwargs):
        """Create a synastry chart input."""
        config = ChartConfig(**config_kwargs)
        return SynastryChartInput(subject1=subject1, subject2=subject2, config=config)
        
    @staticmethod
    def create_transit_chart(radix_subject, transit_subject, **config_kwargs):
        """Create a transit chart input."""
        config = ChartConfig(**config_kwargs)
        return TransitChartInput(
            radix_subject=radix_subject,
            transit_subject=transit_subject,
            config=config
        )
        
    @staticmethod
    def create_composite_chart(composite_subject, **config_kwargs):
        """Create a composite chart input."""
        config = ChartConfig(**config_kwargs)
        return CompositeChartInput(composite_subject=composite_subject, config=config)
        
    @classmethod
    def from_subjects(cls, subject1, subject2=None, chart_type="Natal", **config_kwargs):
        """
        Create a chart input from subjects based on the specified chart type.
        
        Args:
            subject1: The first (or only) astrological subject
            subject2: The second astrological subject (required for certain chart types)
            chart_type: The type of chart to create
            **config_kwargs: Additional configuration options
            
        Returns:
            An appropriate ChartInput instance for the specified chart type
            
        Raises:
            ValueError: If required subjects are missing for the specified chart type
        """
        if chart_type == "Natal":
            return cls.create_natal_chart(subject1, **config_kwargs)
        elif chart_type == "ExternalNatal":
            if subject2 is None:
                raise ValueError("External natal chart requires two subjects")
            return cls.create_external_natal_chart(subject1, subject2, **config_kwargs)
        elif chart_type == "Synastry":
            if subject2 is None:
                raise ValueError("Synastry chart requires two subjects")
            return cls.create_synastry_chart(subject1, subject2, **config_kwargs)
        elif chart_type == "Transit":
            if subject2 is None:
                raise ValueError("Transit chart requires two subjects")
            return cls.create_transit_chart(subject1, subject2, **config_kwargs)
        elif chart_type == "Composite":
            # For composite charts, subject1 should already be a CompositeSubjectModel
            if not isinstance(subject1, CompositeSubjectModel):
                raise ValueError("Composite chart requires a CompositeSubjectModel")
            return cls.create_composite_chart(subject1, **config_kwargs)
        else:
            raise ValueError(f"Unknown chart type: {chart_type}")
