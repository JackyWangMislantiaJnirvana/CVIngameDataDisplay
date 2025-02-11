## 基本布局

在这篇文档中，我们假设你已经配置好了数据集，并且至少进行了一次**更新**。

### 编辑布局

在使用客户端上传数据后，你会注意到：在仪表板上，数据集对应的卡片仍然空空如也。这是因为你尚未编辑这个数据集的布局设定。

点击数据集卡片下方的倒三角，然后在弹出的页面中点击右上的”设定“按钮，就可以打开”编辑布局“界面。

### 布局格式

布局以 JSON 格式写成，具体而言，包含一个列表，列表中含有多个 JSON 字典。

[（什么？你不会 JSON ？）](https://baike.baidu.com/item/JSON)

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
        "data": "map"
    }
]
```

如果你使用默认渲染器的话，列表中每个字典项都含有 3 个键值对

- `display_name` 描述了这个数据在仪表板的显示名称

- `render_type` 定义了渲染类型，不同渲染类型如下表所示。 对于默认渲染类型只需简单地填入 `"render_type": 0` 即可

  | `render_type` | 名称   | 描述                         |
  | ------------- | ------ | ---------------------------- |
  | 0             | 默认   | 使用与数据变量绑定的渲染器。 |
  | 1             | 比例条 | 渲染一个比例条。             |

- `data` 

  如果你使用默认渲染类型，你必须在 `data` 键指定要渲染的数据变量名称（一个字符串）。对于其他的渲染类型，转到页面 *渲染器*  以了解更多。

