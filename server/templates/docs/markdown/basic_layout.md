## Basic Layout

In this article, we assume that you have already configured a dataset and **updated** it at least once. 

### Edit layout

After updating the data, you may notice that there's still nothing in the corresponding card on the dashboard. That's because you haven't edited the layout profile of the dataset.

Expand the dataset, and then click the gears at the top of the "details" page. Then you can edit the layout of the dataset.

### Layout format

The layout is in JSON format, containing a list of JSON dictionaries.

```json
[
    {
        "display_name": "Generating",
        "render_type": 0,
        "data": "gen"
    },
    {
        "display_name": "Map",
        "render_type": 0,
        "data": "map",
    }
]
```

Each dictionary contains 3 fields, if you're using the default renderer.

- `display_name`  is what will be displayed on the dashboard with the data.

- `render_type` decides how the data will be rendered. IDs are below. For default renderers, simply fill in `"render_type": 0` and everything will work just fine.

  | `render_type` | Name      | Description                                          |
  | ------------- | --------- | ---------------------------------------------------- |
  | 0             | Default   | Use the default renderer bundled with the data item. |
  | 1             | Ratio Bar | Render a ratio bar on the card.                      |

  If you're using the default renderer, you must specify the name of the data item (a string) in the `data` field. As for other renderers (well, currently only one), refer to page *Renderer* .