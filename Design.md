## Design

#### Navbar

Ingame Data Display | 	Home  	| Login

Carousel -- OpenComputers

==Title==

Lorem epsum dolor ...

#### /users/

List of accounts & data

#### /login

Wordpress style

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

  +Add Data/Static Text/Static Image

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
/users/user_name/update?api_secret=uuid&payload=
    {
    	"6bfac483": {
    		"name": "MFE",
    		"data": {
                "Battery": {
                    "type": "ratio",
                    "value": {
                        "text": "524288/1048576",
                        "ratio": "75%"
                    }
                }
                "Current generating": {
                	"type": "text",
                	"value": "50 eu/t"
           		},
            	"Map": {
                	"type": "image",
                	"height": 240,
                	"width": 320,
                	"value": "data:image/gif;base64,R..." //base64 of png image
            	}
            }
        }
    }

```

