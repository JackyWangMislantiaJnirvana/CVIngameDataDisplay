from server.renderer.renderer import Renderer
from server.renderer.ratio_bar_renderer import RatioBarRenderer


class RendererRegistry:
    def __init__(self):
        self._renderer_mapping = []

    def register_renderer(self, cls):
        self._renderer_mapping.append(cls)

    def get_renderer(self, idx):
        return self._renderer_mapping[idx]

    def register_renderer_list(self):
        self.register_renderer(Renderer)  # 0
        self.register_renderer(RatioBarRenderer)  # 1


registry = RendererRegistry()
