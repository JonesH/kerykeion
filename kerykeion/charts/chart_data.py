from abc import ABC
from functools import cached_property
from pathlib import Path
from typing import Union, List, Literal, Protocol

from pydantic import BaseModel, computed_field, ConfigDict, field_validator

from kerykeion.settings.config_constants import DEFAULT_ACTIVE_POINTS, DEFAULT_ACTIVE_ASPECTS
from kerykeion.settings.kerykeion_settings import get_settings
from kerykeion.aspects.synastry_aspects import SynastryAspects
from kerykeion.aspects.natal_aspects import NatalAspects
from kerykeion.astrological_subject import AstrologicalSubject
from kerykeion.kr_types import (
    KerykeionException, ChartType, KerykeionPointModel,
    CompositeSubjectModel, AstrologicalSubjectModel,
    ActiveAspect, Planet, AxialCusps
)
from kerykeion.kr_types.settings_models import KerykeionSettingsCelestialPointModel, KerykeionSettingsModel, \
    KerykeionSettingsChartColorsModel, KerykeionSettingsAspectModel, KerykeionLanguageModel, \
    KerykeionGeneralSettingsModel
from kerykeion.kr_types.kr_literals import KerykeionChartTheme, KerykeionChartLanguage


class HasUser(Protocol):
    @property
    def first_obj(self) -> Union[AstrologicalSubject, AstrologicalSubjectModel, CompositeSubjectModel]:
        ...

    @property
    def user(self) -> Union[AstrologicalSubject, AstrologicalSubjectModel, CompositeSubjectModel]:
        return self.first_obj


class HasTUser(Protocol):
    @property
    def t_user(self) -> Union[AstrologicalSubject, AstrologicalSubjectModel, None]:
        ...


class HasOutputDir(Protocol):
    @property
    def new_output_directory(self) -> Union[str, Path, None]: ...

    @property
    def output_directory(self) -> Path:
        if self.new_output_directory:
            return Path(self.new_output_directory)
        return Path.home()


class HasKerykeionSettings(Protocol):
    @property
    def new_settings_file(self) -> Union[Path, KerykeionSettingsModel, dict, None]:
        ...
    @property
    def chart_language(self) -> KerykeionChartLanguage:
        ...
    @property
    def active_aspects(self) -> list[ActiveAspect]:
        ...
    @property
    def active_points(self) -> list[Union[Planet, AxialCusps]]:
        ...

    @cached_property
    def _parsed_settings(self) -> KerykeionSettingsModel:
        return get_settings(self.new_settings_file)

    @property
    def language_settings(self) -> dict:
        return self._parsed_settings["language_settings"][self.chart_language]

    @property
    def chart_colors_settings(self) -> dict:
        return self._parsed_settings["chart_colors"]

    @property
    def planets_settings(self) -> dict:
        return self._parsed_settings["celestial_points"]

    @property
    def aspects_settings(self) -> dict:
        return self._parsed_settings["aspects"]

    @property
    def available_planets_setting(self) -> List[KerykeionSettingsCelestialPointModel]:
        result = []
        for body in self.planets_settings:
            if body["name"] not in self.active_points:
                continue
            body["is_active"] = True
            result.append(body)
        return result


class HasTheme(Protocol):
    @property
    def theme(self) -> Union[KerykeionChartTheme, None]:
        ...

    @property
    def color_style_tag(self) -> str:
        if self.theme is None:
            return ""
        theme_dir = Path(__file__).parent / "themes"
        with open(theme_dir / f"{self.theme}.css", "r") as f:
            return f.read()


class KerykeionChartSettingsMixin:

    _DEFAULT_HEIGHT: int = 550
    _DEFAULT_FULL_WIDTH: int = 1200
    _DEFAULT_NATAL_WIDTH: int = 820
    _DEFAULT_FULL_WIDTH_WITH_TABLE: int = 960
    _PLANET_IN_ZODIAC_EXTRA_POINTS: int = 10
    _TRANSIT_CHART_WITH_TABLE_VIWBOX = "0 0 960 546.0"
    _WIDE_CHART_VIEWBOX = "0 0 1200 546.0"
    _BASIC_CHART_VIEWBOX = "0 0 820 550.0"

    active_aspects: List[ActiveAspect] = DEFAULT_ACTIVE_ASPECTS
    active_points: List[Union[Planet, AxialCusps]] = DEFAULT_ACTIVE_POINTS

    chart_language: KerykeionChartLanguage = "DE"
    theme: Union[KerykeionChartTheme, None] = "classic"
    new_output_directory: Union[str, Path, None] = None
    double_chart_aspect_grid_type: Literal["list", "table"] = "list"
    new_settings_file: Union[Path, None, KerykeionSettingsModel, dict] = None

    main_radius: int = 240

    first_circle_radius: int = 56
    second_circle_radius: int = 92
    third_circle_radius: int = 112


class KerykeionChartInputBase(BaseModel, KerykeionChartSettingsMixin):
    first_obj: Union[AstrologicalSubject, AstrologicalSubjectModel, CompositeSubjectModel]


class HasKerykeionCelestialPoints(HasUser, HasKerykeionSettings, Protocol):
    @property
    def available_kerykeion_celestial_points(self: HasUser & HasKerykeionSettings) -> List[KerykeionPointModel]:
        available_names = [body["name"].lower() for body in self.available_planets_setting]
        return [self.user.get(body) for body in available_names]

class THasKerykeionCelestialPoints(HasTUser, HasKerykeionSettings, Protocol):
    @property
    def t_available_kerykeion_celestial_points(self) -> List[KerykeionPointModel] | None:
        if self.t_user:
            available_names = [body["name"].lower() for body in self.available_planets_setting]
            return [self.t_user.get(body) for body in available_names]
        return None

    @computed_field
    @property
    def height(self) -> int:
        return self._DEFAULT_HEIGHT

    @computed_field
    @property
    def width(self) -> int:
        if self.chart_type in ["Synastry", "Transit"]:
            return self._DEFAULT_FULL_WIDTH
        elif self.double_chart_aspect_grid_type == "table" and self.chart_type == "Transit":
            return self._DEFAULT_FULL_WIDTH_WITH_TABLE
        return self._DEFAULT_NATAL_WIDTH


class ElementalPointsMixin(KerykeionChartSettingsMixin):

    @cached_property
    def element_points(self: HasKerykeionCelestialPoints) -> dict[str, float]:
        fire, earth, air, water = 0.0, 0.0, 0.0, 0.0

        ZODIAC = (
            {"name": "Ari", "element": "fire"},
            {"name": "Tau", "element": "earth"},
            {"name": "Gem", "element": "air"},
            {"name": "Can", "element": "water"},
            {"name": "Leo", "element": "fire"},
            {"name": "Vir", "element": "earth"},
            {"name": "Lib", "element": "air"},
            {"name": "Sco", "element": "water"},
            {"name": "Sag", "element": "fire"},
            {"name": "Cap", "element": "earth"},
            {"name": "Aqu", "element": "air"},
            {"name": "Pis", "element": "water"},
        )

        available_celestial_points_names = [body["name"].lower() for body in self.available_planets_setting]
        points_sign = [self.user.get(planet).sign_num for planet in available_celestial_points_names]

        for i, planet in enumerate(self.available_planets_setting):
            related_zodiac_signs = planet["related_zodiac_signs"]
            cz = points_sign[i]
            extra_points = 0

            if related_zodiac_signs and any(int(sign) == int(cz) for sign in related_zodiac_signs):
                extra_points = self._PLANET_IN_ZODIAC_EXTRA_POINTS

            ele = ZODIAC[points_sign[i]]["element"]
            element_values = {
                "fire": fire,
                "earth": earth,
                "air": air,
                "water": water
            }
            element_values[ele] += planet["element_points"] + extra_points

            fire, earth, air, water = element_values["fire"], element_values["earth"], element_values["air"], \
                element_values["water"]

        return {"fire": fire, "earth": earth, "air": air, "water": water}

    @computed_field
    @property
    def fire(self) -> float:
        return self.element_points["fire"]

    @computed_field
    @property
    def earth(self) -> float:
        return self.element_points["earth"]

    @computed_field
    @property
    def air(self) -> float:
        return self.element_points["air"]

    @computed_field
    @property
    def water(self) -> float:
        return self.element_points["water"]


class ExternalNatalSettingsMixin(KerykeionChartSettingsMixin):
    first_circle_radius = 0
    second_circle_radius = 36
    third_circle_radius = 120


class ChartInputBase(BaseModel, ABC):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    first_obj: Union[AstrologicalSubject, AstrologicalSubjectModel, CompositeSubjectModel]
    chart_type: ChartType


class NatalChartInput(ChartInputBase, KerykeionChartSettingsMixin):
    second_obj: Union[AstrologicalSubject, AstrologicalSubjectModel, None] = None
    chart_type: ChartType = "Natal"

    @classmethod
    @field_validator("first_obj", mode="before")
    def validate_first_obj(cls, first_obj: Union[AstrologicalSubject, AstrologicalSubjectModel, CompositeSubjectModel]):
        if isinstance(first_obj, AstrologicalSubject):
            return first_obj.model()
        return first_obj

    @computed_field
    @property
    def t_user(self) -> Union[AstrologicalSubject, AstrologicalSubjectModel, None]:
        if self.chart_type in ["Transit", "Synastry"]:
            if not self.second_obj:
                raise KerykeionException("Second object is required for Transit or Synastry charts.")
            return self.second_obj
        return None

    @computed_field
    @property
    def geolon(self) -> float:
        if self.chart_type in ["Natal", "ExternalNatal", "Synastry"]:
            return self.user.lng
        elif self.chart_type == "Composite":
            return (self.user.first_subject.lng + self.user.second_subject.lng) / 2
        elif self.chart_type == "Transit":
            return self.t_user.lng
        raise KerykeionException(f"Invalid chart type: {self.chart_type}")

    @computed_field
    @property
    def geolat(self) -> float:
        if self.chart_type in ["Natal", "ExternalNatal", "Synastry"]:
            return self.user.lat
        elif self.chart_type == "Composite":
            return (self.user.first_subject.lat + self.user.second_subject.lat) / 2
        elif self.chart_type == "Transit":
            return self.t_user.lat
        raise KerykeionException(f"Invalid chart type: {self.chart_type}")

    @computed_field
    @property
    def location(self) -> str:
        if self.chart_type in ["Natal", "ExternalNatal", "Synastry"]:
            return self.user.city
        elif self.chart_type == "Composite":
            return ""
        elif self.chart_type == "Transit":
            return self.t_user.city
        raise KerykeionException(f"Invalid chart type: {self.chart_type}")

    @computed_field
    @property
    def aspects_list(self) -> List[dict]:
        if self.chart_type in ["Natal", "ExternalNatal", "Composite"]:
            natal_aspects = NatalAspects(
                self.user,
                new_settings_file=self.new_settings_file,
                active_points=self.active_points,
                active_aspects=self.active_aspects,
            )
            return natal_aspects.relevant_aspects
        elif self.chart_type in ["Transit", "Synastry"]:
            if not self.second_obj:
                raise KerykeionException("Second object is required for Transit or Synastry charts.")
            if self.chart_type == "Transit":
                synastry_aspects = SynastryAspects(
                    self.t_user,
                    self.user,
                    new_settings_file=self.new_settings_file,
                    active_points=self.active_points,
                    active_aspects=self.active_aspects,
                )
            else:
                synastry_aspects = SynastryAspects(
                    self.user,
                    self.t_user,
                    new_settings_file=self.new_settings_file,
                    active_points=self.active_points,
                    active_aspects=self.active_aspects,
                )
            return synastry_aspects.relevant_aspects
        return []

    @computed_field
    @property
    def user(self) -> Union[AstrologicalSubject, AstrologicalSubjectModel, CompositeSubjectModel]:
        return self.first_obj
