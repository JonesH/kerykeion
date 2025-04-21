# -*- coding: utf-8 -*-
"""
    This is part of Kerykeion (C) 2025 Giacomo Battaglia
    
    This module provides an adapter between the new input structure and the existing KerykeionChartSVG class.
    It allows using the new input classes while maintaining compatibility with the existing implementation.
"""

from typing import Union, Dict, Any, Optional
from pathlib import Path

# Import the input classes
from kerykeion.charts.charts_inputs import (
    ChartInput, 
    NatalChartInput,
    ExternalNatalChartInput,
    SynastryChartInput, 
    TransitChartInput,
    CompositeChartInput
)
from kerykeion.charts.kerykeion_chart_svg import KerykeionChartSVG


class ChartAdapter:
    """
    Adapter class between the new input structure and KerykeionChartSVG.
    
    This class bridges the gap between the new input classes and the existing
    KerykeionChartSVG implementation, allowing for a gradual transition.
    """
    
    @staticmethod
    def create_chart(chart_input: ChartInput) -> KerykeionChartSVG:
        """
        Create a KerykeionChartSVG instance from a ChartInput object.
        
        Args:
            chart_input: A ChartInput instance of the appropriate type
            
        Returns:
            A configured KerykeionChartSVG instance
            
        Raises:
            ValueError: If an unknown chart input type is provided
        """
        # Extract configuration
        config = chart_input.config
        config_dict = config.model_dump(exclude_unset=True)
        
        # Rename fields to match KerykeionChartSVG parameters
        if 'output_directory' in config_dict:
            config_dict['new_output_directory'] = config_dict.pop('output_directory')
            
        if 'settings_file' in config_dict:
            config_dict['new_settings_file'] = config_dict.pop('settings_file')
        
        # Handle different chart types
        if isinstance(chart_input, NatalChartInput):
            return KerykeionChartSVG(
                first_obj=chart_input.subject,
                chart_type="Natal",
                **config_dict
            )
            
        elif isinstance(chart_input, ExternalNatalChartInput):
            return KerykeionChartSVG(
                first_obj=chart_input.primary_subject,
                chart_type="ExternalNatal",
                second_obj=chart_input.external_subject,
                **config_dict
            )
            
        elif isinstance(chart_input, SynastryChartInput):
            return KerykeionChartSVG(
                first_obj=chart_input.subject1,
                chart_type="Synastry",
                second_obj=chart_input.subject2,
                **config_dict
            )
            
        elif isinstance(chart_input, TransitChartInput):
            return KerykeionChartSVG(
                first_obj=chart_input.radix_subject,
                chart_type="Transit",
                second_obj=chart_input.transit_subject,
                **config_dict
            )
            
        elif isinstance(chart_input, CompositeChartInput):
            return KerykeionChartSVG(
                first_obj=chart_input.composite_subject,
                chart_type="Composite",
                **config_dict
            )
            
        else:
            raise ValueError(f"Unknown chart input type: {type(chart_input)}")


# Convenience functions for creating charts
def create_chart_from_input(chart_input: ChartInput) -> KerykeionChartSVG:
    """Create a chart from a ChartInput instance."""
    return ChartAdapter.create_chart(chart_input)

def create_natal_chart(subject, **config_kwargs) -> KerykeionChartSVG:
    """Create a natal chart."""
    from kerykeion.charts.charts_inputs import ChartInputFactory
    chart_input = ChartInputFactory.create_natal_chart(subject, **config_kwargs)
    return create_chart_from_input(chart_input)

def create_synastry_chart(subject1, subject2, **config_kwargs) -> KerykeionChartSVG:
    """Create a synastry chart."""
    from kerykeion.charts.charts_inputs import ChartInputFactory
    chart_input = ChartInputFactory.create_synastry_chart(subject1, subject2, **config_kwargs)
    return create_chart_from_input(chart_input)

def create_transit_chart(radix_subject, transit_subject, **config_kwargs) -> KerykeionChartSVG:
    """Create a transit chart."""
    from kerykeion.charts.charts_inputs import ChartInputFactory
    chart_input = ChartInputFactory.create_transit_chart(radix_subject, transit_subject, **config_kwargs)
    return create_chart_from_input(chart_input)

def create_composite_chart(composite_subject, **config_kwargs) -> KerykeionChartSVG:
    """Create a composite chart."""
    from kerykeion.charts.charts_inputs import ChartInputFactory
    chart_input = ChartInputFactory.create_composite_chart(composite_subject, **config_kwargs)
    return create_chart_from_input(chart_input)
