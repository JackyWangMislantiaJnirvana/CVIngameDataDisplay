from server.renderer.renderer import Renderer
from server.renderer.ratio_bar_renderer import RatioBarRenderer

MAX_RENDERER_NUM = 128


class RendererRegistry:
    def __init__(self):
        self._renderer_mapping = [Renderer for i in range(MAX_RENDERER_NUM)]

    def register_renderer(self, idx, cls):
        self._renderer_mapping[idx] = cls

    def get_renderer(self, idx):
        try:
            return self._renderer_mapping[idx]
        except IndexError:
            raise

    def register_renderer_list(self):
        self.register_renderer(0, Renderer)
        self.register_renderer(1, RatioBarRenderer)


registry = RendererRegistry()
