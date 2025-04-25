import asyncio
import logging
import os
import sys
from typing import List, Optional

from omni.isaac.kit import SimulationApp

from core_runner_utils import (
    get_app_settings,
    get_extension_manager,
    get_headless_app_settings,
    get_log_level,
    get_log_path,
    get_stage_path,
    get_usd_context,
    is_headless,
    load_extension,
    set_log_level,
    set_log_path,
)


class CoreRunner:
    def __init__(
        self,
        headless: Optional[bool] = None,
        app_settings: Optional[dict] = None,
        log_level: Optional[str] = None,
        log_path: Optional[str] = None,
        stage_path: Optional[str] = None,
        extensions: Optional[List[str]] = None,
    ):
        self._headless = headless if headless is not None else is_headless()
        self._app_settings = app_settings if app_settings is not None else get_app_settings()
        self._log_level = log_level if log_level is not None else get_log_level()
        self._log_path = log_path if log_path is not None else get_log_path()
        self._stage_path = stage_path if stage_path is not None else get_stage_path()
        self._extensions = extensions if extensions is not None else []
        self._simulation_app = None
        self._usd_context = None
        self._extension_manager = None

    def start(self):
        if self._headless:
            self._app_settings = get_headless_app_settings(self._app_settings)
        self._simulation_app = SimulationApp(self._app_settings)
        self._usd_context = get_usd_context()
        self._extension_manager = get_extension_manager()
        set_log_level(self._log_level)
        set_log_path(self._log_path)
        for extension in self._extensions:
            load_extension(extension)
        if self