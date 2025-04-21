# -*- coding: utf-8 -*-
"""
    This is part of Kerykeion (C) 2025 Giacomo Battaglia
"""

from typing import Optional, Any

def create_template_builder(chart_svg: Any):
    """
    Create the appropriate template builder based on chart type.
    
    Args:
        chart_svg: KerykeionChartSVG instance
        
    Returns:
        BaseChartTemplateBuilder: The appropriate template builder instance
    """
    from .base_chart_template_builder import BaseChartTemplateBuilder
    
    # For now, just return the base builder
    # In future versions, specialized builders could be created for each chart type
    return BaseChartTemplateBuilder(chart_svg)
