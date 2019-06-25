# Client Side Communication Mechanism

## Terms

- `CVDD` is the shortened form of the project.


- `client`: all programs running on `Opencomputers` platform.

  - `MCU`: computers acting as real-time controllers, where data is collected.
  - `central`: a dedicated computer built to collect data.
- `server`: all programs related to CVDD project running on a dedicated web server.
  - `CGI`: Flask CGI program and its database.
  - `front-end`: dynamically-generated HTML pages.
- `data`: information collected from MCUs and processed by CVDD systems.
  - `dataObject`: their structure is defined in `data_types.md`
  - `dataGroup`: map<`nameOfDataobject`, `dataObject`>
  - `dataPost`: map<`nameOfDataGroup`, `dataGroup`>

## Mechanism

Using a safety notification text as a example, let's talk about how data is processed from MCU to server.

MCU submit data by its type (defined in `data_types.md`) through `DataProvider` API.

```lua
dataProvider.submitText(
    "SaftyNotification",
    "Please wear proper protection suit when playing with a locomotive."
)
```

Then this data will be stored as a `dataObject`. All `dataObject` will be stored as a `dataGroup` with their name as their keys. `dataGroup` is buffered in the memory of MCU.

``` lua
-- example of a dataObject
{
    type = "text",
    value = "Please wear proper protection suit when playing with a locomotive."
}
```

```lua
-- example of a dataGroup
{
    -- ...other stuff...
    SaftyNotification = {
        type = "text",
        value = "Please wear proper protection suit when playing with a locomotive."
    }
    -- ...other stuff...
}
```

There's a event handler previously registered on MCU's OS by` DataProvider` API. When receiving a request from central, it will submit the _whole_ `dataGroup` to central through any network available.

Name and network address of a MCU should be registered on central, allowing central to poll all MCUs for data. Let's name our MCU as `BulletinBoard`.

```lua
ProviderMangager.registerRemoteProvider(
    "BulletinBoard",
    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" -- physical address of net modem
)
```

All `dataGroups` collected by central will be stored as a `dataPost`.

```lua
-- example of a dataPost
{
    BulletinBoard = {
        SaftyNotification = {
            type = "text",
            value = "Please wear proper protection suit when playing with a locomotive."
        }
        -- ...other dataObjects...
    }
    -- ...other dataGroups...
}
```

`dataPost` will be encoded into a JSON string for HTTP transmission...

```json
{
    "BulletinBoard":{
        "SaftyNotification":{
            "type":"text",
            "value":"Please wear proper protection suit when playing with a locomotive."
        }
        // ...other dataObjects...
    }
    // ...other dataGroups...
}
```

...and then stuffed into a HTTP POST under the key `payload` with other cargos like `api_secret`:

``` http
POST / HTTP/1.1
User-Agent: cvdd-client
Content-Type: application/x-www-form-urlencoded
...other headers...

api_secret=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx&payload=
{
    "BulletinBoard":{
        "SaftyNotification":{
            "type":"text",
            "value":"Please wear proper protection suit when playing with a locomotive."
        }
        // ...other dataObjects...
    }
    // ...other dataGroups...
}
```

