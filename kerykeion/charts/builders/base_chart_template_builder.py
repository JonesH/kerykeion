# -*- coding: utf-8 -*-
"""
    This is part of Kerykeion (C) 2025 Giacomo Battaglia
"""

from kerykeion.utilities import get_houses_list
from kerykeion.charts.charts_utils import (
    draw_degree_ring,
    draw_transit_ring,
    draw_transit_ring_degree_steps,
    draw_first_circle,
    draw_second_circle,
    draw_third_circle,
    draw_aspect_grid,
    draw_transit_aspect_grid,
    draw_transit_aspect_list,
    draw_houses_cusps_and_text_number,
    draw_house_grid,
    calculate_moon_phase_chart_params,
)
from kerykeion.charts.draw_planets import draw_planets
from datetime import datetime
import swisseph as swe
from typing import Any, Dict, Optional
from kerykeion.kr_types import ChartTemplateDictionary
from kerykeion.utilities import convert_latitude_coordinate_to_string, convert_longitude_coordinate_to_string


class BaseChartTemplateBuilder:
    """
    Base class for building chart template dictionaries.
    This class handles the construction of the template dictionary for different chart types.
    """

    def __init__(self, chart_svg):
        """
        Initialize the template builder with a reference to the chart SVG object.
        
        Args:
            chart_svg: The KerykeionChartSVG instance containing chart data and settings
        """
        # Store reference to parent chart_svg
        self.chart_svg = chart_svg
        
        # Copy essential properties from chart_svg for easier access
        self.chart_type = chart_svg.chart_type
        self.user = chart_svg.user
        self.second_obj = chart_svg.second_obj if hasattr(chart_svg, "second_obj") else None
        self.t_user = self.second_obj
        self.language_settings = chart_svg.language_settings
        self.chart_colors_settings = chart_svg.chart_colors_settings
        self.planets_settings = chart_svg.planets_settings
        self.aspects_settings = chart_svg.aspects_settings
        self.main_radius = chart_svg.main_radius
        self.first_circle_radius = chart_svg.first_circle_radius
        self.second_circle_radius = chart_svg.second_circle_radius
        self.third_circle_radius = chart_svg.third_circle_radius
        self.double_chart_aspect_grid_type = chart_svg.double_chart_aspect_grid_type
        self.aspects_list = chart_svg.aspects_list
        self.available_planets_setting = chart_svg.available_planets_setting
        self.available_kerykeion_celestial_points = chart_svg.available_kerykeion_celestial_points

        # Copy optional properties that may not be present in all chart types
        if hasattr(chart_svg, "t_available_kerykeion_celestial_points"):
            self.t_available_kerykeion_celestial_points = chart_svg.t_available_kerykeion_celestial_points
        else:
            self.t_available_kerykeion_celestial_points = None
            
        self.location = chart_svg.location
        self.geolat = chart_svg.geolat
        self.geolon = chart_svg.geolon
        self.fire = chart_svg.fire
        self.earth = chart_svg.earth
        self.air = chart_svg.air
        self.water = chart_svg.water
        self.height = chart_svg.height
        self.width = chart_svg.width
        self.color_style_tag = chart_svg.color_style_tag

    def build_template_dictionary(self) -> Dict[str, Any]:
        """
        Build and return the complete template dictionary for chart rendering.
        
        The template dictionary contains all the data needed to render the chart SVG,
        including chart configuration, rings, circles, planets, aspects, etc.
        
        Returns:
            dict: The template dictionary with all chart data and rendering instructions
        """
        template_dict: Dict[str, Any] = {}
        
        self._set_basic_chart_config(template_dict)
        self._set_chart_rings_and_circles(template_dict)
        self._set_chart_title_and_info(template_dict)
        self._set_chart_colors(template_dict)
        self._draw_chart_elements(template_dict)
        self._set_element_percentages(template_dict)
        self._set_date_time_info(template_dict)
        
        return template_dict

    def _set_basic_chart_config(self, template_dict: Dict[str, Any]) -> None:
        """Set basic chart configuration like dimensions and viewbox."""
        template_dict["color_style_tag"] = self.color_style_tag
        template_dict["chart_height"] = self.height
        template_dict["chart_width"] = self.width
        
        # Set viewbox based on chart type
        if self.chart_type in ["Natal", "ExternalNatal", "Composite"]:
            template_dict['viewbox'] = self.chart_svg._BASIC_CHART_VIEWBOX
        elif self.double_chart_aspect_grid_type == "table" and self.chart_type == "Transit":
            template_dict['viewbox'] = self.chart_svg._TRANSIT_CHART_WITH_TABLE_VIWBOX
        else:
            template_dict['viewbox'] = self.chart_svg._WIDE_CHART_VIEWBOX

    def _set_chart_rings_and_circles(self, template_dict: Dict[str, Any]) -> None:
        """Generate rings and circles based on chart type."""
        if self.chart_type in ["Transit", "Synastry"]:
            self._set_transit_synastry_rings_circles(template_dict)
        else:
            self._set_natal_rings_circles(template_dict)

    def _set_transit_synastry_rings_circles(self, template_dict: Dict[str, Any]) -> None:
        """Set rings and circles for Transit or Synastry charts."""
        template_dict["transitRing"] = draw_transit_ring(
            self.main_radius, 
            self.chart_colors_settings["paper_1"], 
            self.chart_colors_settings["zodiac_transit_ring_3"]
        )
        template_dict["degreeRing"] = draw_transit_ring_degree_steps(
            self.main_radius, 
            self.user.seventh_house.abs_pos
        )
        template_dict["first_circle"] = draw_first_circle(
            self.main_radius, 
            self.chart_colors_settings["zodiac_transit_ring_2"], 
            self.chart_type
        )
        template_dict["second_circle"] = draw_second_circle(
            self.main_radius, 
            self.chart_colors_settings['zodiac_transit_ring_1'], 
            self.chart_colors_settings['paper_1'], 
            self.chart_type
        )
        template_dict['third_circle'] = draw_third_circle(
            self.main_radius, 
            self.chart_colors_settings['zodiac_transit_ring_0'], 
            self.chart_colors_settings['paper_1'], 
            self.chart_type, 
            self.third_circle_radius
        )

        # Set aspect grid based on chart type
        self._set_transit_synastry_aspect_grid(template_dict)
        
        template_dict["makeAspects"] = self.chart_svg._draw_all_transit_aspects_lines(
            self.main_radius, 
            self.main_radius - 160
        )

    def _set_natal_rings_circles(self, template_dict: Dict[str, Any]) -> None:
        """Set rings and circles for Natal charts."""
        template_dict["transitRing"] = ""
        template_dict["degreeRing"] = draw_degree_ring(
            self.main_radius, 
            self.first_circle_radius, 
            self.user.seventh_house.abs_pos, 
            self.chart_colors_settings["paper_0"]
        )
        template_dict['first_circle'] = draw_first_circle(
            self.main_radius, 
            self.chart_colors_settings["zodiac_radix_ring_2"], 
            self.chart_type, 
            self.first_circle_radius
        )
        template_dict["second_circle"] = draw_second_circle(
            self.main_radius, 
            self.chart_colors_settings["zodiac_radix_ring_1"], 
            self.chart_colors_settings["paper_1"], 
            self.chart_type, 
            self.second_circle_radius
        )
        template_dict['third_circle'] = draw_third_circle(
            self.main_radius, 
            self.chart_colors_settings["zodiac_radix_ring_0"], 
            self.chart_colors_settings["paper_1"], 
            self.chart_type, 
            self.third_circle_radius
        )
        template_dict["makeAspectGrid"] = draw_aspect_grid(
            self.chart_colors_settings['paper_0'], 
            self.available_planets_setting, 
            self.aspects_list
        )
        template_dict["makeAspects"] = self.chart_svg._draw_all_aspects_lines(
            self.main_radius, 
            self.main_radius - self.third_circle_radius
        )

    def _set_transit_synastry_aspect_grid(self, template_dict: Dict[str, Any]) -> None:
        """Set aspect grid for Transit or Synastry charts."""
        if self.double_chart_aspect_grid_type == "list":
            title = ""
            if self.chart_type == "Synastry":
                title = self.language_settings.get("couple_aspects", "Couple Aspects")
            else:
                title = self.language_settings.get("transit_aspects", "Transit Aspects")

            template_dict["makeAspectGrid"] = draw_transit_aspect_list(
                title, 
                self.aspects_list, 
                self.planets_settings, 
                self.aspects_settings
            )
        else:
            template_dict["makeAspectGrid"] = draw_transit_aspect_grid(
                self.chart_colors_settings['paper_0'], 
                self.available_planets_setting, 
                self.aspects_list, 
                550, 
                450
            )

    def _set_chart_title_and_info(self, template_dict: Dict[str, Any]) -> None:
        """Set chart title and information text."""
        self._set_chart_title(template_dict)
        self._set_zodiac_info(template_dict)
        self._set_bottom_left_info(template_dict)
        self._set_moon_phase_info(template_dict)
        self._set_location_info(template_dict)
        self._set_chart_name(template_dict)
        self._set_additional_chart_info(template_dict)

    def _set_chart_title(self, template_dict: Dict[str, Any]) -> None:
        """Set the main chart title."""
        if self.chart_type == "Synastry":
            template_dict["stringTitle"] = f"{self.user.name} {self.language_settings['and_word']} {self.t_user.name}"
        elif self.chart_type == "Transit":
            template_dict["stringTitle"] = f"{self.language_settings['transits']} {self.t_user.day}/{self.t_user.month}/{self.t_user.year}"
        elif self.chart_type in ["Natal", "ExternalNatal"]:
            template_dict["stringTitle"] = self.user.name
        elif self.chart_type == "Composite":
            template_dict["stringTitle"] = f"{self.user.first_subject.name} {self.language_settings['and_word']} {self.user.second_subject.name}"

    def _set_zodiac_info(self, template_dict: Dict[str, Any]) -> None:
        """Set zodiac system information."""
        if self.user.zodiac_type == 'Tropic':
            zodiac_info = f"{self.language_settings.get('zodiac', 'Zodiac')}: {self.language_settings.get('tropical', 'Tropical')}"
        else:
            mode_const = "SIDM_" + self.user.sidereal_mode # type: ignore
            mode_name = swe.get_ayanamsa_name(getattr(swe, mode_const))
            zodiac_info = f"{self.language_settings.get('ayanamsa', 'Ayanamsa')}: {mode_name}"

        template_dict["bottom_left_0"] = f"{self.language_settings.get('houses_system_' + self.user.houses_system_identifier, self.user.houses_system_name)} {self.language_settings.get('houses', 'Houses')}"
        template_dict["bottom_left_1"] = zodiac_info

    def _set_bottom_left_info(self, template_dict: Dict[str, Any]) -> None:
        """Set bottom-left chart information."""
        if self.chart_type in ["Natal", "ExternalNatal", "Synastry"]:
            template_dict["bottom_left_2"] = f'{self.language_settings.get("lunar_phase", "Lunar Phase")} {self.language_settings.get("day", "Day").lower()}: {self.user.lunar_phase.get("moon_phase", "")}'
            template_dict["bottom_left_3"] = f'{self.language_settings.get("lunar_phase", "Lunar Phase")}: {self.language_settings.get(self.user.lunar_phase.moon_phase_name.lower().replace(" ", "_"), self.user.lunar_phase.moon_phase_name)}'
            template_dict["bottom_left_4"] = f'{self.language_settings.get(self.user.perspective_type.lower().replace(" ", "_"), self.user.perspective_type)}'
        elif self.chart_type == "Transit":
            template_dict["bottom_left_2"] = f'{self.language_settings.get("lunar_phase", "Lunar Phase")}: {self.language_settings.get("day", "Day")} {self.t_user.lunar_phase.get("moon_phase", "")}'
            template_dict["bottom_left_3"] = f'{self.language_settings.get("lunar_phase", "Lunar Phase")}: {self.t_user.lunar_phase.moon_phase_name}'
            template_dict["bottom_left_4"] = f'{self.language_settings.get(self.t_user.perspective_type.lower().replace(" ", "_"), self.t_user.perspective_type)}'
        elif self.chart_type == "Composite":
            template_dict["bottom_left_2"] = f'{self.user.first_subject.perspective_type}'
            template_dict["bottom_left_3"] = f'{self.language_settings.get("composite_chart", "Composite Chart")} - {self.language_settings.get("midpoints", "Midpoints")}'
            template_dict["bottom_left_4"] = ""

    def _set_moon_phase_info(self, template_dict: Dict[str, Any]) -> None:
        """Set moon phase diagram parameters."""
        moon_phase_dict = calculate_moon_phase_chart_params(
            self.user.lunar_phase["degrees_between_s_m"],
            self.geolat
        )

        template_dict["lunar_phase_rotate"] = moon_phase_dict["lunar_phase_rotate"]
        template_dict["lunar_phase_circle_center_x"] = moon_phase_dict["circle_center_x"]
        template_dict["lunar_phase_circle_radius"] = moon_phase_dict["circle_radius"]

    def _set_location_info(self, template_dict: Dict[str, Any]) -> None:
        """Set location information."""
        if self.chart_type == "Composite":
            template_dict["top_left_1"] = f"{datetime.fromisoformat(self.user.first_subject.iso_formatted_local_datetime).strftime('%Y-%m-%d %H:%M')}"
        elif len(self.location) > 35:
            split_location = self.location.split(",")
            if len(split_location) > 1:
                template_dict["top_left_1"] = split_location[0] + ", " + split_location[-1]
                if len(template_dict["top_left_1"]) > 35:
                    template_dict["top_left_1"] = template_dict["top_left_1"][:35] + "..."
            else:
                template_dict["top_left_1"] = self.location[:35] + "..."
        else:
            template_dict["top_left_1"] = self.location

    def _set_chart_name(self, template_dict: Dict[str, Any]) -> None:
        """Set chart name."""
        if self.chart_type in ["Synastry", "Transit"]:
            template_dict["top_left_0"] = f"{self.user.name}:"
        elif self.chart_type in ["Natal", "ExternalNatal"]:
            template_dict["top_left_0"] = f'{self.language_settings["info"]}:'
        elif self.chart_type == "Composite":
            template_dict["top_left_0"] = f'{self.user.first_subject.name}'

    def _set_additional_chart_info(self, template_dict: Dict[str, Any]) -> None:
        """Set additional chart-specific information."""
        if self.chart_type == "Synastry":
            template_dict["top_left_3"] = f"{self.t_user.name}: "
            template_dict["top_left_4"] = self.t_user.city
            template_dict["top_left_5"] = f"{self.t_user.year}-{self.t_user.month}-{self.t_user.day} {self.t_user.hour:02d}:{self.t_user.minute:02d}"
        elif self.chart_type == "Composite":
            template_dict["top_left_3"] = self.user.second_subject.name
            template_dict["top_left_4"] = f"{datetime.fromisoformat(self.user.second_subject.iso_formatted_local_datetime).strftime('%Y-%m-%d %H:%M')}"
            
            latitude_string = convert_latitude_coordinate_to_string(
                self.user.second_subject.lat, 
                self.language_settings['north_letter'], 
                self.language_settings['south_letter']
            )
            longitude_string = convert_longitude_coordinate_to_string(
                self.user.second_subject.lng, 
                self.language_settings['east_letter'], 
                self.language_settings['west_letter']
            )
            template_dict["top_left_5"] = f"{latitude_string} / {longitude_string}"
        else:
            latitude_string = convert_latitude_coordinate_to_string(
                self.geolat, 
                self.language_settings['north'], 
                self.language_settings['south']
            )
            longitude_string = convert_longitude_coordinate_to_string(
                self.geolon, 
                self.language_settings['east'], 
                self.language_settings['west']
            )
            template_dict["top_left_3"] = f"{self.language_settings['latitude']}: {latitude_string}"
            template_dict["top_left_4"] = f"{self.language_settings['longitude']}: {longitude_string}"
            template_dict["top_left_5"] = f"{self.language_settings['type']}: {self.language_settings.get(self.chart_type, self.chart_type)}"

    def _set_chart_colors(self, template_dict: Dict[str, Any]) -> None:
        """Set colors for various chart elements."""
        # Set paper colors
        template_dict["paper_color_0"] = self.chart_colors_settings["paper_0"]
        template_dict["paper_color_1"] = self.chart_colors_settings["paper_1"]

        # Set planet colors
        for planet in self.planets_settings:
            planet_id = planet["id"]
            template_dict[f"planets_color_{planet_id}"] = planet["color"] # type: ignore

        # Set zodiac colors
        for i in range(12):
            template_dict[f"zodiac_color_{i}"] = self.chart_colors_settings[f"zodiac_icon_{i}"] # type: ignore

        # Set orb colors
        for aspect in self.aspects_settings:
            template_dict[f"orb_color_{aspect['degree']}"] = aspect['color'] # type: ignore

    def _draw_chart_elements(self, template_dict: Dict[str, Any]) -> None:
        """Draw zodiac, houses, planets, and other chart elements."""
        # Draw zodiac
        template_dict["makeZodiac"] = self.chart_svg._draw_zodiac_circle_slices(self.main_radius)

        # Draw houses
        self._draw_houses_elements(template_dict)
        
        # Draw planets
        self._draw_planets_elements(template_dict)
        
        # Draw planet grid
        self._draw_planet_grid(template_dict)

    def _draw_houses_elements(self, template_dict: Dict[str, Any]) -> None:
        """Draw houses grid and cusps."""
        first_subject_houses_list = get_houses_list(self.user)

        if self.chart_type in ["Transit", "Synastry"]:
            second_subject_houses_list = get_houses_list(self.t_user)

            template_dict["makeHousesGrid"] = draw_house_grid(
                main_subject_houses_list=first_subject_houses_list,
                secondary_subject_houses_list=second_subject_houses_list,
                chart_type=self.chart_type,
                text_color=self.chart_colors_settings["paper_0"],
                house_cusp_generale_name_label=self.language_settings["cusp"]
            )

            template_dict["makeHouses"] = draw_houses_cusps_and_text_number(
                r=self.main_radius,
                first_subject_houses_list=first_subject_houses_list,
                standard_house_cusp_color=self.chart_colors_settings["houses_radix_line"],
                first_house_color=self.planets_settings[12]["color"],
                tenth_house_color=self.planets_settings[13]["color"],
                seventh_house_color=self.planets_settings[14]["color"],
                fourth_house_color=self.planets_settings[15]["color"],
                c1=self.first_circle_radius,
                c3=self.third_circle_radius,
                chart_type=self.chart_type,
                second_subject_houses_list=second_subject_houses_list,
                transit_house_cusp_color=self.chart_colors_settings["houses_transit_line"],
            )
        else:
            template_dict["makeHousesGrid"] = draw_house_grid(
                main_subject_houses_list=first_subject_houses_list,
                chart_type=self.chart_type,
                text_color=self.chart_colors_settings["paper_0"],
                house_cusp_generale_name_label=self.language_settings["cusp"]
            )

            template_dict["makeHouses"] = draw_houses_cusps_and_text_number(
                r=self.main_radius,
                first_subject_houses_list=first_subject_houses_list,
                standard_house_cusp_color=self.chart_colors_settings["houses_radix_line"],
                first_house_color=self.planets_settings[12]["color"],
                tenth_house_color=self.planets_settings[13]["color"],
                seventh_house_color=self.planets_settings[14]["color"],
                fourth_house_color=self.planets_settings[15]["color"],
                c1=self.first_circle_radius,
                c3=self.third_circle_radius,
                chart_type=self.chart_type,
            )

    def _draw_planets_elements(self, template_dict: Dict[str, Any]) -> None:
        """Draw planets on the chart."""
        if self.chart_type in ["Transit", "Synastry"]:
            template_dict["makePlanets"] = draw_planets(
                available_kerykeion_celestial_points=self.available_kerykeion_celestial_points,
                available_planets_setting=self.available_planets_setting,
                second_subject_available_kerykeion_celestial_points=self.t_available_kerykeion_celestial_points,
                radius=self.main_radius,
                main_subject_first_house_degree_ut=self.user.first_house.abs_pos,
                main_subject_seventh_house_degree_ut=self.user.seventh_house.abs_pos,
                chart_type=self.chart_type,
                third_circle_radius=self.third_circle_radius,
            )
        else:
            template_dict["makePlanets"] = draw_planets(
                available_planets_setting=self.available_planets_setting,
                chart_type=self.chart_type,
                radius=self.main_radius,
                available_kerykeion_celestial_points=self.available_kerykeion_celestial_points,
                third_circle_radius=self.third_circle_radius,
                main_subject_first_house_degree_ut=self.user.first_house.abs_pos,
                main_subject_seventh_house_degree_ut=self.user.seventh_house.abs_pos
            )

    def _draw_planet_grid(self, template_dict: Dict[str, Any]) -> None:
        """Draw planet grid with positions."""
        if self.chart_type in ["Transit", "Synastry"]:
            if self.chart_type == "Transit":
                second_subject_table_name = self.language_settings["transit_name"]
            else:
                second_subject_table_name = self.t_user.name

            template_dict["makePlanetGrid"] = draw_planet_grid(
                planets_and_houses_grid_title=self.language_settings["planets_and_house"],
                subject_name=self.user.name,
                available_kerykeion_celestial_points=self.available_kerykeion_celestial_points,
                chart_type=self.chart_type,
                text_color=self.chart_colors_settings["paper_0"],
                celestial_point_language=self.language_settings["celestial_points"],
                second_subject_name=second_subject_table_name,
                second_subject_available_kerykeion_celestial_points=self.t_available_kerykeion_celestial_points,
            )
        else:
            if self.chart_type == "Composite":
                subject_name = f"{self.user.first_subject.name} {self.language_settings['and_word']} {self.user.second_subject.name}"
            else:
                subject_name = self.user.name

            template_dict["makePlanetGrid"] = draw_planet_grid(
                planets_and_houses_grid_title=self.language_settings["planets_and_house"],
                subject_name=subject_name,
                available_kerykeion_celestial_points=self.available_kerykeion_celestial_points,
                chart_type=self.chart_type,
                text_color=self.chart_colors_settings["paper_0"],
                celestial_point_language=self.language_settings["celestial_points"],
            )

    def _set_element_percentages(self, template_dict: Dict[str, Any]) -> None:
        """Calculate and set element percentages."""
        total = self.fire + self.water + self.earth + self.air

        fire_percentage = int(round(100 * self.fire / total))
        earth_percentage = int(round(100 * self.earth / total))
        air_percentage = int(round(100 * self.air / total))
        water_percentage = int(round(100 * self.water / total))

        template_dict["fire_string"] = f"{self.language_settings['fire']} {fire_percentage}%"
        template_dict["earth_string"] = f"{self.language_settings['earth']} {earth_percentage}%"
        template_dict["air_string"] = f"{self.language_settings['air']} {air_percentage}%"
        template_dict["water_string"] = f"{self.language_settings['water']} {water_percentage}%"

    def _set_date_time_info(self, template_dict: Dict[str, Any]) -> None:
        """Set date and time information."""
        if self.chart_type in ["Composite"]:
            # First Subject Latitude and Longitude
            latitude = convert_latitude_coordinate_to_string(
                self.user.first_subject.lat, 
                self.language_settings["north_letter"], 
                self.language_settings["south_letter"]
            )
            longitude = convert_longitude_coordinate_to_string(
                self.user.first_subject.lng, 
                self.language_settings["east_letter"], 
                self.language_settings["west_letter"]
            )
            template_dict["top_left_2"] = f"{latitude} {longitude}"
        else:
            dt = datetime.fromisoformat(self.user.iso_formatted_local_datetime)
            custom_format = dt.strftime('%Y-%m-%d %H:%M [%z]')
            custom_format = custom_format[:-3] + ':' + custom_format[-3:]
            template_dict["top_left_2"] = f"{custom_format}"
