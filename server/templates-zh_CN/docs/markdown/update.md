## 更新数据

我们假定你已经注册了一个账号。

### 仪表板

*仪表板* 是显示所有游戏内数据的地方，每个用户分配一个。数据以 *数据集* 的形式排布于仪表板上的卡片中，一个数据集对应游戏内的一个机器。如果你使用  [CVDD Client](https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/blob/client/client/doc/CVDDClient用户指南.md) ，那么一个数据集就对应一个 MCU。

**我们提供了适用于 OpenComputers 的 [CVDD Client](https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/blob/client/client/doc/CVDDClient用户指南.md)，与本网站完全兼容，若需了解具体使用方法，请点击[链接](https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/blob/client/client/doc/CVDDClient用户指南.md)查看其文档。**

<hr/>

如果你不想使用 CVDD Client，可以自己实现一个。

以下为 API 技术细节，没有需求的话可以无视。

#### 更新数据集
- 更新 API 如下

  `/users/<username>/update`

  HTTP 方法: POST
  
  **MIME Type**: `application/json`
  
  必须设置正确的 MIME Type，服务端才能处理请求。
  
  ##### 请求 body 示例:
  
  ```json
  {
      	"api_secret": "3face281-1942-6ce1-97bc-9a2ec6fa32e5",
      	"payload": {
              "6bfac483": {
                  "gen": {
                  "type": "PhyQuantity",
                  "unit": "EU/t",
                  "value": 1024
                  },
                  "battery": {
                  "type": "PhyQuantity",
                  "unit": "EU",
                  "value": 5000
                  },
                  "capacity": {
                  "type": "PhyQuantity",
                  "unit": "EU",
                  "value": 32768
                  },
                  "map": {
                  "type": "Image",
                  "value": "data:image/gif;base64,R..."
                  }
              }
          }
  }
  
  ```
  
  - `api_secret` 可以在用户设置页面找到。
  
  - `payload` 为一个字典，把数据集 hash （一个八位 hex 串）映射到具体的机器数据集。数据集 hash 是仪表板上数据集的唯一标识，可以在每个数据集的详情中查看。只需要点击每个数据集卡片下方倒三角即可打开数据集详情。而具体的机器数据需要由 Client 提供。
  
  - 在机器数据集中，可以包含以下的 5 种数据。
  
    - `PhyQuantity` 描述一个游戏内物理量。
  
    ```json
    {
        "type": "PhyQuantity",
        "unit": "EU/t",
        "value": 1024
    }
    ```
  
    - `Text` 表示一个字符串。
  
    ```json
    {
    	"type": "Text",
    	"value": "I'm a grout!"
    }
    ```
  
    - `Boolean` 为布尔类型。
  
    ```json
    {
    	"type": "Boolean",
    	"value": true
    }
    ```
  
    - `Vector` 为数据的列表，可以理解为数组。
  
    ```json
    {
    	"type": "Vector",
    	"value": [1, 2, 3, 4, 5]
    }
    ```
  
    - `Image` 保存一个任何格式的图片。
  
    ```json
    {
    	"type": "Image",
    	"value": "https://example.com/logo.png"
    }
    ```
  
    ​	`value` 亦可为 [Data URL](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Basics_of_HTTP/Data_URIs) 图片，便于传输游戏内图像。

