# Data Types

- `Text` Plain text
```json
{
    "type":"Text",
    "value":"Panda played chicken with a train; the train won."
}
```

- `Image` Scalar Image（`value` is base64 encoded string of the image）
```json
{
    "type":"Image",
    "height":120,
    "weight":120,
    "title":"map",
    "value":"asdasdfasdfasdf..."
}
```

- `Boolean`
```json
{
    "type":"Boolean",
    "value":true
}
```

- `PhyQuantity` Physical Quantity（An integer or a float with unit）（If you don't want a unit，just set `unit` to empty string）（Considering there's little chance for us to use _scientific notation_, so we use normal form to represent physical quantities.）
```json
{
    "type":"PhyQuantity",
    "value":200,
    "unit":"EU"
}
```

```json
{
    "type":"PhyQuantity",
    "value":600.0,
    "unit":"MJ"
}
```

- `Vector`（used to represent any multi-dimensional data, such as coordinates and intervals.）（Considering there's little chance for us to use multi-dimensional physical quantities, every component of `Vector` doesn't have a unit.）
```json
{
    "type":"Vector",
    "value":[100, 200]
}
```

