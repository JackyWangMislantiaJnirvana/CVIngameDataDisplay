from flask import render_template

import server.renderer.renderer as renderer
import server.utils as utils


class RatioBarRenderer(renderer.Renderer):
    @staticmethod
    def render(data_content: dict, layout: dict, is_modal=True):
        try:
            return render_template('dataset/ratio_bar.html',
                                   display_name=layout['display_name'], text=layout['text'].format(**data_content),
                                   width=utils.to_percentage(utils.fill_and_calc(layout['width'], data_content)))
        except SyntaxError:
            raise
