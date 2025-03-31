import logging
from datetime import datetime, timezone

import pytz
import requests
from plugins.base_plugin.base_plugin import BasePlugin

logger = logging.getLogger(__name__)


class F1Standings(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        return template_params

    def generate_image(self, settings, device_config):
        pass
