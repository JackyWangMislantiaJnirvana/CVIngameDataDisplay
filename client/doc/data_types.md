# Data Types

- `text` Plain text
```json
{
    "type":"text",
    "value":"Panda played chicken with a train; the train won."
}
```

- `image` Scalar Image（`value` is base64 encoded string of the image）
```json
{
    "type":"image",
    "height":120,
    "weight":120,
    "title":"map",
    "value":"asdasdfasdfasdf..."
}
```

- `boolean`
```json
{
    "type":"boolean",
    "value":true
}
```

- `phyQuantity` Physical Quantity（An integer or a float with unit）（If you don't want a unit，just set `unit` to `null`）（Considering there's little chance for us to use _scientific notation_, so we use normal form to represent physical quantities.）
```json
{
    "type":"phyQuantity",
    "value":200,
    "unit":"EU"
}
```

```json
{
    "type":"phyQuantity",
    "value":213.4,
    "unit":"MJ"
}
```

- `vector`（used to represent any multi-dimensional data, such as coordinates and intervals.）（Considering there's little chance for us to use multi-dimensional physical quantities, every component of `vector` doesn't have a unit.）
```json
{
    "type":"vector",
    "value":[100, 200]
}
```