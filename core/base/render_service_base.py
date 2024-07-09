"""
    `base/service/render_service_base.py`
"""

from pygal.style import Style, DefaultStyle

from core.util.logging import notice


class RenderServiceBase:
    def __init__(self) -> None:
        pass

    def _get_style(self, style_name: str) -> Style:
        """ Function: Verify if chart style is valid and returns the style class """
        try:
            exec('from pygal.style import {}'.format(style_name))
            return eval(style_name)
        except (NameError, SyntaxError, ImportError):
            return DefaultStyle

    def _notice_chart_export(self, chart_name: str) -> None:
        """ Function: Notice the export of the chart """
        notice('Chart \'{}\' successfully exported.'.format(chart_name))
