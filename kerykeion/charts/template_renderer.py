from __future__ import annotations

from pathlib import Path
from string import Template

from scour.scour import scourString

from kerykeion.charts.charts_utils import draw_transit_aspect_grid, draw_aspect_grid
from kerykeion.utilities import inline_css_variables_in_svg


class ChartTemplateRenderer:
    """
    Handles SVG template rendering and output for KerykeionChartSVG.
    """

    def __init__(self, chart_svg: "KerykeionChartSVG"):
        self.chart_svg = chart_svg

    def makeTemplate(self, minify: bool = False, remove_css_variables = False) -> str:
        td = self.chart_svg._create_template_dictionary()

        DATA_DIR = Path(__file__).parent
        xml_svg = DATA_DIR / "templates" / "chart.xml"

        with open(xml_svg, "r", encoding="utf-8", errors="ignore") as f:
            template = Template(f.read()).substitute(td)

        if remove_css_variables:
            template = inline_css_variables_in_svg(template)

        if minify:
            template = scourString(template).replace('"', "'").replace("\n", "").replace("\t","").replace("    ", "").replace("  ", "")
        else:
            template = template.replace('"', "'")

        return template

    def makeSVG(self, minify: bool = False, remove_css_variables = False):
        template = self.makeTemplate(minify, remove_css_variables)
        chartname = self.chart_svg.output_directory / f"{self.chart_svg.user.name} - {self.chart_svg.chart_type} Chart.svg"
        with open(chartname, "w", encoding="utf-8", errors="ignore") as output_file:
            output_file.write(template)
        print(f"SVG Generated Correctly in: {chartname}")

    def makeWheelOnlyTemplate(self, minify: bool = False, remove_css_variables = False):
        with open(Path(__file__).parent / "templates" / "wheel_only.xml", "r", encoding="utf-8", errors="ignore") as f:
            template = f.read()

        template_dict = self.chart_svg._create_template_dictionary()
        template = Template(template).substitute(template_dict)

        if remove_css_variables:
            template = inline_css_variables_in_svg(template)

        if minify:
            template = scourString(template).replace('"', "'").replace("\n", "").replace("\t","").replace("    ", "").replace("  ", "")
        else:
            template = template.replace('"', "'")

        return template

    def makeWheelOnlySVG(self, minify: bool = False, remove_css_variables = False):
        template = self.makeWheelOnlyTemplate(minify, remove_css_variables)
        chartname = self.chart_svg.output_directory / f"{self.chart_svg.user.name} - {self.chart_svg.chart_type} Chart - Wheel Only.svg"
        with open(chartname, "w", encoding="utf-8", errors="ignore") as output_file:
            output_file.write(template)
        print(f"SVG Generated Correctly in: {chartname}")

    def makeAspectGridOnlyTemplate(self, minify: bool = False, remove_css_variables = False):
        with open(Path(__file__).parent / "templates" / "aspect_grid_only.xml", "r", encoding="utf-8", errors="ignore") as f:
            template = f.read()

        template_dict = self.chart_svg._create_template_dictionary()

        if self.chart_svg.chart_type in ["Transit", "Synastry"]:
            aspects_grid = draw_transit_aspect_grid(
                self.chart_svg.chart_colors_settings['paper_0'],
                self.chart_svg.available_planets_setting,
                self.chart_svg.aspects_list
            )
        else:
            aspects_grid = draw_aspect_grid(
                self.chart_svg.chart_colors_settings['paper_0'],
                self.chart_svg.available_planets_setting,
                self.chart_svg.aspects_list,
                x_start=50,
                y_start=250
            )

        template = Template(template).substitute({**template_dict, "makeAspectGrid": aspects_grid})

        if remove_css_variables:
            template = inline_css_variables_in_svg(template)

        if minify:
            template = scourString(template).replace('"', "'").replace("\n", "").replace("\t","").replace("    ", "").replace("  ", "")
        else:
            template = template.replace('"', "'")

        return template

    def makeAspectGridOnlySVG(self, minify: bool = False, remove_css_variables = False):
        template = self.makeAspectGridOnlyTemplate(minify, remove_css_variables)
        chartname = self.chart_svg.output_directory / f"{self.chart_svg.user.name} - {self.chart_svg.chart_type} Chart - Aspect Grid Only.svg"
        with open(chartname, "w", encoding="utf-8", errors="ignore") as output_file:
            output_file.write(template)
        print(f"SVG Generated Correctly in: {chartname}")
