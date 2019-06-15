- `text` 纯文本
```json
{
    "type":"text",
    "value":"Panda played chicken with a train; the train won."
}
```

- `image` 标量图（`value`字段是图片的Base64串）
```json
{
    "type":"image",
    "height":120,
    "weight":120,
    "title":"map",
    "value":"asdasdfasdfasdf..."
}
```

- `boolean` 布尔值
```json
{
    "type":"boolean",
    "value":true
}
```

- `phyQuantity` 物理量（带单位的整数或者小数）（科学计数法在MC语境下应用不多，于是不额外增加复杂度）（如果不需要单位，可将`unit`复制为`null`）
```json
{
    "type":"phyQuantity",
    "value":200,
    "unit":"eu"
}
```

- `vector` 矢量（用来传递各种多元数据，如位置坐标、列车运行区间）（考虑到多元物理量应该用不上，于是`vector`的每个维都是无单位数量）
```json
{
    "type":"vector",
    "value":[100, 200]
}
```