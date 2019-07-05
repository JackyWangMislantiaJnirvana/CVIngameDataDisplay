## 渲染器

此处列出了所有的特殊渲染器，也就是那些 `render_type ` 为正的渲染器。

1. 比例条

   ```json
   {
       "display_name": "Storage",
       "render_type": 1,
       "text": "{battery.value} / {capacity.value}",
       "width": "{battery.value} / {capacity.value}"
   }
   ```

   除开所有布局条目都有的前 2 个键值对，你还必须指定 `text` 和 `width` 的值。

   - `text` 
     - 类型： `string`
     - 对应显示在比例条上方的文本
   - `width`
     - 类型：含有一个实数 x 的字符串（也可为值为实数的表达式），且满足 0 ≤ x ≤ 1
     - 决定比例条宽度
     - **注意，此项的值为一个含有数字的字符串，而非数字**

   在大多数情况下，我们需要利用上传的变量算出比例条的宽度等参数。可以利用 Python 填充字符串的括号语法。如上例所示， `battery` 和 `capacity` 就是上传的 `PhyQuantity` 类型的变量（定义可参考“更新数据”页面的示例）。