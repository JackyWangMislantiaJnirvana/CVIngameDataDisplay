## Design

#### Navbar

Ingame DataType Display | 	Home  	| Login

Carousel -- OpenComputers

==Title==

Lorem epsum dolor ...

#### /users/

List of accounts & data

#### /login

WordPress style

*verify code

#### /register

username; pw; invite code: 12chars, A-Za-z0-9; *verify code

#### /users/user_name/dashboard/

3*4 grids

Latest push

size adjustable

click: model dialog showing detail

gadgets

- Customize(Hidden if not logged in)

  +Add DataType/Static Text/Static Image

  ⚙Customize: id, name

#### /users/user_name/settings

general:

- API secret
- Edit password

accounts:

- list of accounts
- invite code generation

statistics:

- graphs

## APIs

#### /users/user_name/update

Method: POST

Example:

```
{
    	"api_secret": "3bfde100-1937-4fa2-95bf-0cb452d5500d",
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



### Details of dashboard

1. Database

   - create a table for each user (suppose UID of "panda_2134" is 1)

   - `id` is a 32-bit integer in hex notation, i.e. '6bfac483'

     ```sql
       CREATE TABLE dashboard_1 (
           id INTEGER PRIMARY KEY, 
           title TEXT, 
           data TEXT, 
           layout TEXT,
           last_update INTEGER)
     ```

   - `title` is the title for the dataset
   - `data` contains the payload in JSON, the format listed above
   - `layout` contains the layout settings of the web UI, in JSON
   - `last_update` is the UNIX time of the last update
   - *functions for dashboard-related database queries*

2. Web UI

   - Render work -> js

   - Syntax

     - **NOTE: Every dynamically-rendered value should be a string, in order to be formatted in-place with `.format()`**
   
     ```javascript
      [
         {
             "display_name": "Generating",
             "render_type": DEFAULT,
             "data": "gen"
         },
         {
             "display_name": "Map",
             "render_type": DEFAULT,
             "data": "map",
         },
         {
        		"display_name": "Storage",
             "render_type": RATIO_BAR,
        		"text": "{battery.value} / {capacity.value}",
             "width": "{battery.value} / {capacity.value}"
         }
     ]
   ```
     - As is known, the width of a progress bar should be a percentage, or BS4 will fail
   
     - provide a helper function in python code:
     
       ```python
       def to_percentage(x):
           return str(x * 100) + '%'
       
       ```
     
     - provide highlight

