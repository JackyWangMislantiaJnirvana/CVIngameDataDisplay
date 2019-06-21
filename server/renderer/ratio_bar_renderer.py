from flask import render_template

import server.renderer.renderer as renderer
import server.utils as utils


class RatioBarRenderer(renderer.Renderer):
    @staticmethod
    def render(data_content, layout):
        return render_template('dataset/ratio_bar.html',
                               display_name=layout['display_name'], text=layout['text'],
                               width=utils.to_percentage(layout['width']))
