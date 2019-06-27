class Renderer:
    @staticmethod
    def render(data_content, layout, is_modal=True):
        try:
            return data_content[layout['data']].render(layout['display_name'], is_modal)
        except KeyError:
            raise
