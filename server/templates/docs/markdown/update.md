## Update

We assume that you've created an account on this site.

### Dashboard

The *dashboard* is where all in-game data will be displayed. Every user has his/her own dashboard. The data are organized in the form of *datasets* , and generally one dataset represents attributes of an in-game machine.

#### Update an dataset

- **To avoid re-inventing the wheels, please have a look at our [CVDD Client(Chinese)](https://github.com/JackyWangMislantiaJnirvana/CVIngameDataDisplay/blob/master/README.md).**

- The update API are provided here for your information.

  `/users/<username>/update`

  Method: POST
  
  ##### Example of the request body:
  
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
  
  - `api_secret` can be found in the setting page.
  
  - `payload` is a dictionary mapping dataset hash code (can be found in the detail window of each dataset) to machine-specific data.
  
  - There're 5 types of datum, listed below.
  
    - `PhyQuantity` describes a physical quantity in game, e. g. temperature.
  
    ```json
    {
        "type": "PhyQuantity",
        "unit": "EU/t",
        "value": 1024
    }
    ```
  
    - `Text` represent an ordinary string.
  
    ```json
    {
    	"type": "Text",
    	"value": "I'm a grout!"
    }
    ```
  
    - `Boolean` can only have 0 / 1 values
  
    ```json
    {
    	"type": "Boolean",
    	"value": true
    }
    ```
  
    - `Vector` contains an sequence of numbers
  
    ```json
    {
    	"type": "Vector",
    	"value": [1, 2, 3, 4, 5]
    }
    ```
  
    - `Image` stores an image in any format.
  
    ```json
    {
    	"type": "Image",
    	"value": "https://example.com/logo.png"
    }
    ```
  
    ​	`value` can also be an [Data URL](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs) image, making it possible to upload in-game images.

