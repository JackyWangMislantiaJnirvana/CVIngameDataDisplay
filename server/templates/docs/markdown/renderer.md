## Renderer

Here lists the usage of special renderers, i.e. the renderers that have a positive `render_type `.

1. Ratio Bar

   ```json
   {
       "display_name": "Storage",
       "render_type": 1,
       "text": "{battery.value} / {capacity.value}",
       "width": "{battery.value} / {capacity.value}"
   }
   ```

   Apart from the first 2 fields, which is a must for every layout item, you must specify `text` and `width` fields.

   - `text` 
     - type: `string`
     - decides the text that will be displayed on the bar
   - `width`
     - type: `string` that contains a real number x (or an expression yielding it), where 0 ≤ x ≤ 1
     - decides the width of the bar
     - **Pay attention: This is a string, not a number!**

   In order to generate the content of a ratio bar from the uploaded data, you can use "Bracket syntax" in Python to fill the string with data, like the example shown above, where `battery` and `capacity` are of `PhyQuantity` type (See "Update" for their definition).