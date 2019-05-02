# **Talk to your data**

This project aims to provide a responsive Web-UI linked to a custom _**Amazon Alexa Skill**_.  
The `master` branch aims to be stable, but will need minor adjustements if run on another system.
* [Overview](#overview)
* [UI](#ui)
* [BlockChain](#blockchain)
    * [Blocks](#blocks)
* [Handling Socket Messages](#handling-socket-messages)
    * [Server-Side](#server-side)
    * [Client-Side](#client-side)
    * [Protocol](#protocol)
* [Alexa Integration](#alexa-integration)
* [Custom Block Integration](#custom-block-integration)
***

### Getting started

The current UI features responsive material design provided by _**Material Design Lite**_ and is appropriate for use on devices >= small tablets such as an iPad mini. Best usability is achieved with a horizontal resolution _>1025_ as all UI-elements are permanently unfolded for bigger screens.

The backend is provided by a linux server stack and was tested on Ubuntu Server 16.04. :  

* **nginx**: very basic URL handling and SSL
* **django**: server doing most of the work (SQL/HTTP/Serving Content)  
* **django-alexa**: plugin handling Alexa Requests/Responses for Amazon  
* **django-channels**: plugin handling WebSockets and connected Clients  
* **redis-server**: communication between WebSocket workers
* _memcached_ : memory caching server (optional instead of database caching)

***

A `requirements.txt` for `pip` is included and should install most packages into a virtual environment.  

`redis-server` has to be running and listening (default on `:6379`).

Server deployment is done by running `nginx` with the `alexa.conf` file. This is redirecting traffic coming in for the URL to the django server listening on `localhost:8000` by default.

Caching of the current session can either be done in the database (very slow, but ok with server crashes_) or with `memcached` in-memory caching (`fast, uses RAM, unsaved changes lost when server crashes`). This solution could save to disk periodically to be less susceptible to server outages. Which caching solution is preferred can be set in `settings.py` under `CACHES`.

Amazon is currently pointed towards `https://yourURL.com/alexa/ask/` to send all Alexa requests.
If a new Alexa Skill is created, it is important to change the _APP_ID_ in `AlexaInterface/setttings.py` to the appropriate Skill ID for Skill mapping, as one django server could handle multiple Skills. (_Note: This only works reliably on Linux machines, as it is using `os.environ`_).  

If another URL should be used, a valid SSL certificate for the URL has to be either obtained from a CA or generated locally (_check Alexa SSL guidelines_) and uploaded to the Alexa Dev Portal as well as changed in the `/keys` folder for `nginx` to use. The current server only accepts traffic on `:443` and redirects `:80` requests accordingly (Also, the current machine is only recheable by the outside on `:443` anyway).  

Running Django is either done via the development server `python manage.py runserver` or in a deployment environment as
```sh 
python manage.py runworker --threads 4 &
daphne -b 127.0.0.1 -p 8000 AlexaHandler.asgi:channel_layer
``` 
If a server running on `localhost:8000` is used for local dev, set `ENV = "LOCAL"` in `settings.py`. This will set URLs in `live.html` and the `CACHE_URL` environment variable to the localhost. Further, the directories for `import`, `export` and `cache` folder must be individually set there.

If run on a headless machine (_Ubuntu Server_), make sure all plotting modules like `matplotlib` are set to work without a display.  

Updated intent schemes for the old JSON intent interface in the Alexa Dev Portal can be obtained automatically by running ```shell
python manage.py alexa AlexaHandler > intents.txt``` (See Alexa Integration for further details)


# Overview
[Top &uarr;](#talk-to-your-data)

![Server Diagram](https://github.com/kruegener/Alexa_Server/raw/master/wiki/Server_UML.jpg)
_Rudimentary communication chart of the different components in the stack_  

The complete sequence of components involved in this project tends to be rather cumbersome to visualize. To simplify things, this overview will focus on the components that differ from the standard _Django_ chain and are custom to this project.  
Namely, these are the _Alexa_ components on the left and the _WebSockets_ integration. Mandatory SSL support for _Alexa_ requests is provided by _nginx_.  

An **initial _http_** request for the Site will trigger the server to serve the `live.html` template and -once a _WebSocket_ is established from the client- to check the current Session and serve relevant content/Blocks via _JSON_ files afterwards. Major media is stored in a _cache_ directory and the client pointed towards the serving URL to retrieve the media via _http_.

There are two possible triggers for events in the server and for the connected users to occur. Either, the _Django_ Server is called by _Amazon_ to process an _Alexa_ intent or one of the connected client browser sessions is sending an event (say a button click) over _WebSockets_. 

**Intent** requests will be processed by the suitable intent-function in one of the `Alexa.py` files. On server startup, these are auto-discovered and all incoming requests from Amazon are mapped to the appropriate functions automatically by _django-alexa_. These functions might trigger an UI-event such as enlarging an image or are focused on the Block system. 

**Client** requests are received via _WebSockets_ and processed by `consumers.py`. These actions again can trigger both UI- as well as Block-events.

All **Events** -_whether triggered by Amazon or Clients_- are processed internally and relayed to the clients via _WebSocket_ commands. If the trigger was coming from _Amazon_, an appropriate response message and further action prompts are generated and send to the _Echo_ for playback.

**UI** changes and events such as new Blocks are all received via the socket and then processed by _JavaScript/jQuery_.

# UI
[Top &uarr;](#talk-to-your-data)

![Empty_interface](https://github.com/kruegener/Alexa_Server/raw/master/wiki/Basic_interface.JPG)

### Main view

The user interface consists of three main elements. Taking up most of the screen is the active are where blocks and content are placed. To the left of the screen is the list of available files (found in the `/import` folder) and the current variables in use by any given block.  
Nearly every element has a number assigned to it, as Amazon is not encouraging free-form user input. It is relying on a set of Slots, which can be a custom list of inputs or a type of `Amazon.Field` for example a number. If predefined Slot types are used, recognition is significantly better, so the easiest and most reliable method of input was to assign elements a unique number they can be called by, as well as action **keywords** pointing toward a specific **intent-function**:

> “ _show_ Block **2** ”

> “ Block **1** _do a PCA_ ”  

> “ _load_ File **0** ”

The import folder is watched by the `watchdog` module and auto updated if names or files change. Variables are typeless and connected to blocks only. There are no variables independent from blocks. Their data is conserved inside of the blocks and can be accessed by the `.getData()` function available for blocks who have variables.  
On top of the screen is a toolbar, mainly used for resets and debugging purposes at the moment. Additionally, the bar pulsates when an Alexa Session is active to let the user know the service is listening without having to look at the Echo itself.

The active area itself is populated with blocks either by User input in the browser window or Alexa requests. It is auto scrolling to move to the latest change, i.e. a new block.
On small screens (lower than 1024px wide) the left toolbar is retracted to a drawer menu icon and can be accessed that way. This threshold is embedded into the `mdl` framework and therefore not easily changeable. Arguably, this service shouldn't be used by such small devices anyway.
Files can be selected and loaded through this interface as well.

### Blocks in UI

Each block has a content `div` to store either text or an image and a button-group `div`. Disabled buttons function as the block counter (orange). Every block has a delete button, that can be pressed and deletes the block from the BlockChain.  
Grey buttons show `options` that are stored in the blocks as a list of strings. Functionality for these buttons can be implemented on an individual basis, but is discouraged as the main point of interaction of the UI should be voice. Basically, these buttons are used to prompt the user with available actions to perform on the Block.
Some functionality is common for a basic-type of block. A basic `show` options should be implemented with every block containing an image to enlarge said image. Blocks extending the `ImageBlock.py` base class already inherit this funcionality.  
More complex functionality such as multiple options for a Block can be achieved with the `passOption` intent:

> “ _option_ **word** Block **X** ”    
> “ Block **X** _option_ **word** ”

The _word_ is then passed to the `getOption()` function of the specific block as a string and can be dealt with by the block itself. This is effectively by-passing the need to create a need intent for every new functionality and redirecting it to the option intent.  
This should be used for minor functions that are very specific for one type of block. Functionalities that are shared between multiple types of blocks like `delete` are implemented as their own intent without the need to speak the word `option` as it increases accesability.


# BlockChain
[Top &uarr;](#talk-to-your-data)

![BlockChain Diagram](https://github.com/kruegener/Alexa_Server/raw/master/wiki/BlockChain.jpg)
_BlockChain Diagram_  

If a user connects to the server (this means a _WebSocket_ is calling the `consumers.py` after `live.html` has been loaded by the browser), the relevant session is looked up from the cache pickles or created if it doesn't existed. It is also registered as an object in the Django Model database. This could be used to make certain sessions accessible only to certain Users.  
The `BlockChain` class holds all relevant information for a session and is auto-saved (`.Chain_pickle()`) as a python pickle in the `cache` directory for individual sessions. It provides access to individual Blocks and is the only valid to delete a Block so it is properly removed from the session and it's cache cleaned. If the session needs to be deleted completely, call the Model Instance in Djangos database.  
When first loaded, the `BlockList` is iterated and each `Block` called to provide relevant data as a `JSON` file that can be send to the client via the socket for display. As said before, images are not send via the socket. Instead, the media URL is send to the client and then loaded via `https`.

```python
class BlockChain:
    def __init__ (self, name="", session=""):
        ''' initial save '''
    ...
    def addBlock (self, Block):
        ''' add Block to BlockList, add Vars from Block to VarList, add Connections '''
    def getBlock (self, index)
    def getBlockList (self)
    def getBlockListLength (self)
    def delBlockByIndex (self, index)
    def delBlockByElement (self, Block):
        ''' del associated elements in VarList... -> call Block.delBlock() for cleanup of cache data '''
    def getBlockId (self, Block)
    def delBlocksAll(self):
        ''' reset everything but keep Session alive '''
    ...
    def Chain_pickle (self):
        ''' pickle self in cache folder '''
    def __str__(self):
        ''' provide summary of status '''
```

## Blocks
[Top &uarr;](#talk-to-your-data)

Every Block extends the `BaseBlock` class, while especially the `__init__` and `GetNode` functions might have to be overwritten for custom blocks. During `init`, the type (`IO` , `image`, `rich_image`, `message` etc.). The type determines how the UI handles the new block, i.e. tries to load a cached image or set a specific size for the block. Custom types must be implemented in the `live.html` as-well.  
The `IO_Block` is the preferred way of importing outside data from `/import`, as it loads numeric data (matrices) or images and can pass the processed information to other blocks, so not every block needs to be able to handle IO.  
Any Block `__init__` needs to set following instance variables:
```python
def __init__ (self):
    self.name = name
    self.type = "Type"
    self.session = "session string" # default: "alexa"
    self.options = ["Opt1", "Opt2"] # displayed as grey buttons in the UI
    self.vars = ["Variable Names for vars associated with this block"] # displayed on the left in the UI
    self.block_num = "" # to be filled with number in BlockChain for updates
    # optional
    # if media such as images is stored they have to be stored 
    # in the cache_dir to be servable by the server via the cache_url
    self.cache_path = settings.CACHE_DIR + "/" + self.session + "/" + self.file_name 
    self.call_path = settings.CACHE_URL + "/" + self.session + "/" + self.file_name
    # optional for updatable blocks, initially always false
    self.update = "false"
```
***
Media has to be served via the `cache` folder as it is the only servable Folder. The rest of the file structure is not available from the outside. Additionally, the blocks may not store media within their class instance as it makes them non-pickleable as part of the `BlockChain`. Abstract data such as numpy arrays or similar are however allowed and pickleable.  
The `GetNode` function provides all necessary information to the browser client to fully render the next Block with the JavaScript provided by `live.html`. Depending on the block-type, this may include a `call_path` entry to load media. The basic `ImageBlock` is a good example of the basic structure:  

```python
# inside ImageBlock class (extending BaseBlock)
def GetNode(self):
    # create JSON
    data = {"type": self.type,
            "block_type": self.type,
            "content_type": "image",
            "options": self.options,
            "vars": self.vars,
            # extra-bit required for image retrieval
            "call_path": self.call_path,
            # optional update parameter
            "update": self.update,
             "block_num": self.block_num,
            }
    return data
```
***
If a Block accepts to be called with options via the _passOption_ intent, it has to provide a `getOption` function that deals with the incoming option string. In this case, blocks may themselves create more blocks and add them to the BlockChain or update the existing block.  
If a new block is created, the current BlockChain has to be obtained via the imported `consumers.getSessChain()` function. After adding a Block, it is necessary to distribute the new display information to all clients via a _WebSocket_. To this, the current message Queue has to be provided with the new Block's JSON. This might look like this:
```python
def getOption(self, opt):
    # handle the option and if valid option create new Block or modify existing block
    newBlock = AnyBlock(name, session=self.session, *args, **kwargs)
    # get current BlockChain for session
    chain = consumers.getSessChain()
    # add (wait with save after transmission for performance increase)
    chain.addBlock(newBlock)
    # broadcast to session group
    Group[self.session].send({
        "text": newBlock.GetNode()
    })
    # save
    chain.Chain_pickle()

```
***
If the content a block displays in the UI should not be static once it's loaded and the existing block updated, the `update` keyword and the value `self.update` needs to be present in the `JSON` and `__init__` respectively. When the block first is created, it should be set to `false`. If the state of the block changes and the UI is to be refreshed, `update` is set to `true` and the block re-broadcast:
```python
# stuff has happened that makes the block want to be refreshed in the UI
# change all new vars i.e. :
self.cache_path = "new path"
self.type = "new type"
# etc.
self.update = "true"
self.block_num = #number in the BlockChain
# send updated block
Group(self.session).send({
    "text": self.GetNode()
})
# done updating: IMPORTANT
self.update = "false"
```
This will trigger the `javascript` in `live.html` to empty the block with the provided `self.block_num` and fill it with the updated contents. This way, a message block can turn into an image block or vice versa, or just an updated image. The content of the block is loaded as if it was a new block. Options and variables can also be changed by changing `self.options` and `self.vars`.  
This might be useful when the _Alexa_ command "_option **word** block **number**_" is used to alter a block, but not necessarily create a new one. If the creation of a new block or the update of an already existing one is appropriate depends on the specific workflow. An implementation of both versions can be found in the `SandFilterBlock` in `getOption`.  
The implementation of a "revert change" option in an updated block might be useful.
***
Depending on the `block_type`, different extra parameters are expected, such as `msg` for a block of type `message`. These are matched on the receiving side at `live.html` and processed. It is desired to keep the number of special cases to a minimum. So if a Block for linear Regression is created, the type should not be custom `linear_reg`, but rather of `rich_image` as that type is fully sufficient to show an image with additional text.  
Classes with images should always include a `showBlock` function, which can easily be achieved by extending the `ImageBlock` class or slightly modifying it's function and copying it.  

***
Blocks with the ability to serve data to other blocks need to provide a `getData` function and serve the data as a `dict`:
```python
def getData(self):
    data = {"name": self.data_name, "type": self.data_type, "data": self.data}
    return data
```
***
Media handling blocks also have a responsibility to clean up after themselves if they are deleted. They need to override the `delBlock` function of the `BaseBlock` by something like this:
```python
def delBlock(self):
    # remove any saved media from the cache folder
    try:
        os.remove(self.image_path)
    except:
        # red std print
        print("\033[93m couldnt cache", sys.exc_info(), "\033[0m")
    del self
```

# Handling Socket Messages
[Top &uarr;](#talk-to-your-data)
![Simple Communication Diagram](https://github.com/kruegener/Alexa_Server/raw/master/wiki/Socket_Messages.jpg)
_Simple communication diagram_

All dynamic communication between the server and client browsers happens over _WebSockets_ carrying `JSON` files. Communication between Amazon and the server is done via `https` requests, again handling `JSON`.

## Server-Side
[Top &uarr;](#talk-to-your-data)  

Handling of incoming socket messages happens mainly in the `consumers.py`. All incoming _WebSocket_ traffic is routed by `routing.py` to the three functions `ws_add`, `ws_message` and `ws_disconnect`. As the names imply, they get called on client connection events and incomming messages. The `ws_add` is just accepting the conneciton and adding the `reply_channel` of the client to the current `Group` aka the "mailing list" for all changes. After that, it iterates through all blocks and sends relevant data to the client.  
`ws_message` has to handle most of the messages, mainly it handles UI input directly from a client browser coming in as a `JSON` and manipulating the `BlockChain` accordingly. In general, any function anywhere on the server can broadcast to the `Group` channel and distribute messages, so `consumers.py` is only really important for new clients and incoming UI traffic.  
If a message should be sent from anywhere, import the `Group`:
```python
from channels import Group
# data has to be a JSON file adhering to the protocol
# raw JSON
Group("alexa").send({
    "text": json.dumps(data)
})
# block data
Group("alexa").send({
                "text": block.GetNode()
})
```

## Client-Side
[Top &uarr;](#talk-to-your-data)  
Upon load of `live.html`, the browser opens a `ReconnectingWebSocket` aimed at the Django server over `wss`. Upon succesful connection, it receives a `ready` command  (_type_ `cmd`) from the server and in return asks for the inital configuration of blocks.  
They are delivered sequentially in individual socket messages (_type_ `block`). All incoming socket traffic is handled by the `socket.onmessage` function and routed to functions such as `new_grid_block(data)` for further processing.
```javascript
socket.onmessage = function(e){
    data = JSON.parse(e.data);
    // routing
    if(data.type == "cmd")
        // route commands
        if(data.cmd == "ready")
            socket.send(JSON.stringify({"type": "cmd", "cmd": "init"}))
        else if (data.cmd == "file_list")
            // handling the UI fileList
        else if (data.cmd == "reset")
            // reset UI
        else if (data.cmd == "del_block")
            // delete block from UI
        else if (data.cmd == "show")
            // animate block image zoom
        else if (data.cmd == "listening")
            // indicate active Alexa session
        // etc.
    else if(data.type == "block")
        new_grid_block(data);
}
```
New UI elements are handled by `JavaScript` and `jQuery`. If for example a new block carries the `var` keyword in it's `JSON`, everything in the list is added appropriately to the left-hand varList. Same goes for all `opt` entries, that are generated as grey buttons for any incoming block.  
Clicks on option blocks are send with the block number and button label (that are saved in `jQuery` data for the DOM element) to the server for handling. Although it is not intended to implement functionality for these blocks. Rather, they are used as visual cues for the user what the possible voice inputs are. Some distinction between general options (with their own intent) and options only accesible through `passOption` has to be defined for further clarification.  
***
Block `div` id's follow the naming scheme `grid_block`+`block_number` with class `content`, `mdl-cell` and it's `mdl` options. The div can be filled with the content such as `<img>` tags or `<p>`. Paragraphs should get the `Info` css-class for unified display style. Width of the block can be influenced by the `mdl-cell--X-col` option replacing `X` with a number between 1-12.  
Below this, the `button-group` `div` is rendered automatically.
```html
<div id="grid_block0"> class="content mdl-cell mdl-cell--middle mdl-shadow--6dp mdl-cell--5-col">
    <img src="cache_url">
    <p class="Info mdl-shadow--6dp">
    Info text
    </p>
    <div id="button_group" class="button_group">...
    </div>
</div>
```
Please refrain from building these DOM elements by writing the `html` code as a string and appending it to the `div`. Rather create Elements by `document.createElement("div")` and append them as a child to the active parent-div variable. Block creation is done via javascript only:
```javascript
function new_grid_block(data){
    // ABBREVIATED AND SIMPLIFIED function, see source
    // get parent and create new block div
    var parent = document.getElementById("grid");
    /* 
    update happens in this function as well
     a couple of things have to be handled differently in the full functions
     mainly emptying the div and substituting block_num for grid_count
     might be better as a seperated function for clarity, but it works
    */ 
    if(data.update != "true"){
        name = "grid_block" + grid_count;
        var div = document.createElement("div");
        div.id = name;
    }
    else{
        name = "grid_block" + grid_count;
        var div = document.getElementById(name);
        div.innerHTML = "";
    }
    div.className = "content mdl-cell mdl-cell--middle mdl-shadow--6dp";
    
    // add variables to list and jquery Data
    if(data.hasOwnProperty("vars")){
            new_Var(data.vars, grid_count);
            jQuery.data( div, "vars", {
               vars: data.vars
            });
            
    // specific block_type
    if(data.block_type == "rich_image"){
        var img = document.createElement("img");
        img.src = data.call_path;
        var p = document.createElement("p");
        p.className = "Info mdl-shadow--6dp";
        p.appendChild(document.createTextNode("Info: " + data.add_data));
        div.appendChild(img);
        div.appendChild(p);
        div.className += " " + "mdl-cell--5-col"
    }
    // else if other types
    // ...
    
    // automatic button-group creation
    // ...
    div.appendChild(but_group);
    if (data.update != "true"){
        grid_count +=1;
        $(parent).append(div);
    }
    // add full block to grid
    // screen size and loading handling here
    // ...
}
```

## Protocol
[Top &uarr;](#talk-to-your-data)  
The transfer of display information via _WebSockets_ relies on a consistent `JSON` structure. All these instruction files are written similarly with two major sub-classes. `block`-type and `cmd`-type instructions.  
`block` instructions handle the creation of new blocks and have to carry all information needed for display including text and media URLs.  
`cmd` instructions are more custom and usually include a `block_number` that has to be altered or interacted with.  
`block`-type `JSON` as returned by `GetNode()` of each block:
```
data = {"type": "block",
        "block_type": "i.e. rich_image",
        "content_type": "image",
        "options": ["list of options"],
        "vars": ["list of variables"],
        // extra bits for media blocks
        "call_path": "url to direct to cache folder",
        // optional if block content should be dynamic
        // false at all times except for the message where the actual update happens
        // must be set false at all other times to prevent accidental block doubling in UI
        "update": "true/false"
        "block_num": block_num to update}
```
`cmd`-type `JSON` usually carry a `block_num` parameter if the command is only aimed at a specific block. Other than that, theres always a `cmd` keyword.
```
data = {"type": "cmd", 
        "cmd": "del_block",
        "block_num": 2}
```
The current set of available **commands** is:  
  
`ready` : signals ready state of server to client-side (S2C)  
`init` : send to server to request block config (C2S)  
`init_done` : end of init transmission (S2C)  
`show` (_block_num_) : zooms image embedded in _block_num_ (S2C/C2S)  
`file_list` (_file_list_) : transmit fileList to show on the left UI (S2C)  
`file_list_update` (_file_list_) : update existing fileList UI (S2C)  
`del_block` (_block_number_) : delete Block and it's variables (S2C/C2S)  
`minimize` : return from zoomed state (S2C/C2S)  
`listening` : Alexa Session is active, trigger pulse effect (S2C) (C2S(_debug only_))  
`stopped_listening` : Alexa Session ended, stop pulse (S2C) (C2S(_debug only_))  
`load` (_file_) : trigger the server to load a specific file into `IO_Block` (C2S)  
`click` (_num_, _opt_) : option on block _num_ has been clicked (C2S)  
`reset` : reset BlockChain and empty the active are (S2C/C2S)

Some of these are only valid _server->client_ **(S2C)**, _client->server_ **(C2S)** or both. 
Generally, these are send by the server to all clients via:
```python
# from raw JSON
Group("alexa").send({
                "text": json.dumps(data)
            })
# or for a new block
Group("alexa").send({
                "text": newBlock.GetNode()
            })
```
Or the client to the server at _wss://yourURL.com/alexa/_ (or _ws://localhost:8000/alexa/_):
```javascript
// example of a button click. block number and option are embedded in the caller's jQuery data storage from button creation
socket.send(JSON.stringify({"type" : "cmd",
                    "cmd" : "click",
                    "num" : jQuery.data( this, "call" ).num,
                    "opt" : jQuery.data( this, "call" ).opt
                }));
```

# Alexa-Integration
[Top &uarr;](#talk-to-your-data)

The main part of this UI is the integration of the _Amazon Alexa_ Service (tested with the _Echo_ device). To use the Alexa speech recognition with our service, the server needs to have a static URL (_https://<i></i>yourURL.com/alexa/ask_) that has a valid CA SSL-certificate or a locally generated one uploaded to the Amazon Dev Portal.  
This section is not meant as a general introduction to custom _Alexa_ skills, but only how to implement the custom Skill into this particular setup. Refer to the _Alexa_ documentation for information about _Intents_, _Slots_ and custom Skills.  
To start this particular Skill, the (changeable) invocation is:
> Alexa, open _live session_
***
_Intents_ can lead to the creation/deletion/alteration of blocks or to a change in UI. Usually, any intent will interact with one or more blocks. I.e. The _loadFile_ intent is used to specify a file and load it into an _IO_Block_. The command (_since the live session is already active_) would be:
> load file _zero_

This intent is then matched by the intent scheme in the _Alexa Dev Console_ by the sample utterances to the _loadIntent_ and provides the Slot _num_ to the intent function inside `Alexa.py`. The appropriate function is automatically routed to by the `django-alexa` backend. Specifically, the function is marked by the `@intent` decorator and is passed the slot values defined in its slots class:
```python
# define slots
class Num(fields.AmazonSlots):
    num = fields.AmazonNumber()
    
# load File intent
@intent(slots=Num, app="AlexaHandler")
def loadFile(session, num=0):
    """
        DESCRIPTION: loading file with number {num} / UTTERANCES below
        ---
        read file {num}
        read {num}
        {num} read
        load file {num}
        load {num}
        {num} load
        file {num}
        {num} file  
    """
    # get list of files in /import
    FileList = consumers.getFileList()
    # check validity of slot value
    if type(num) is int:
        if num < len(FileList):
            try:
                # get current BlockChain and add (any) new block
                SessChain = consumers.getSessChain()
                IO = IO_Block(file_name=FileList[num], session="alexa")
                SessChain.addBlock(IO)
                # broadcast new block
                Group("alexa").send({
                    "text": IO.GetNode()
                })
                # save config (optional)
                SessChain.Chain_pickle()
                # Alexa response
                msg = "File " + str(num) + " successfully loaded"
            except:
                print("\033[93mUnexpected error:", sys.exc_info(), "\033[0m")
                msg = "error loading file  " + str(num)
        else:
            msg = "File with number " + str(num) + " does not exist. Maximum File number is " + str(len(FileList) - 1)
    else:
        print("\033[94m Amazon provided None type \033[0m")
        msg = "Please provide a number"
    # return Alexa response
    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)
```
Any Block type that is to be created by an Alexa Skill needs to be imported into the respective `Alexa.py`. There can be mutliple of these files (case-insensitive) around the project. They will be autodetected and automatically routed to.  
The intent scheme, custom slots and sample utterances for all intents can be automatically saved to file with:
```sh
python manage.py alexa AlexaHandler > intent.txt
```
This intent scheme and all sample utterances can then be copy-pasted into the Dev Console. This relies on all intent functions properly defining their slots and utterances. Slots are defined as classes and can expect multiple values, even custom slots. One example is the `passOption` function that expects custom slot values:
```python
# custom values
OPTIONS = ["sand", "glass", "void", "etc"]

# slots
class OPT(fields.AmazonSlots):
    alexa_option = fields.AmazonCustom(label="OPTIONS", choices=OPTIONS)
    number = fields.AmazonNumber()

# function
@intent(slots=OPT, app="AlexaHandler")
def passOption(session, number=-1, alexa_option=""):
    """
        simple function description with UTTERANCES below
        ---
        pass option {alexa_option} to block {number}
        option {alexa_option} block {number}
        block {number} option {alexa_option}
    """
    # SIMPLIFIED without value check or try error handling (see source)
    SessChain.getBlock(num).getOption(alexa_option, num)
    msg = "processed"
    return ResponseBuilder.create_response(message=msg,
                                           reprompt="",
                                           end_session=False,
                                           launched=True)
```
Sample utterances are provided with slot names in curly brackets as placeholders. It is important to allow different ways a user might say a certain command. I.e., the user might say:
> block _{num}_ delete  

or  
> delete block _{num}_  

In both cases, the `delete` intent function will receive the number 4, but the user is not tied to a specific way of saying the command. This makes the commands more "natural" as it is closer to spontanous, normal speech than learning a command by heart before you can use it. Sample utterances should also include shorter variants for users who do not wish to use full sentences.  
Easy to learn or "natural" input:  
> pass option _{alexa_option}_ to block _{num}_
  
Fast command structure:
> option _{alexa_option}_  block _{num}_  
> _{num}_ option _{alexa_option}_


# Custom Block Integration
[Top &uarr;](#talk-to-your-data)


How hard building a new block is depends on a few factors. This will also determine if you only need to use `python` in 1/2 files or require `javascript` and `html` as well. These are a few cases:
- **Easy** (i.e. `IO_Block`):  
The new block can utilize one of the existing UI classes (i.e. `message` or `rich_image`). It lives as a stand-alone block and uses standard intents like `show`/`delete`.
    - Create a new `YourBlock.py` in the `/Block` directory.
    - Create an intent for your block in `AlexaHandler/Block/Alexa.py` and update the scheme @Dev Portal
    
- **Medium** (i.e. `SandFilterBlock`):  
All of the above plus the block should be updatable and/or accept options from the exisiting `passOption` intent.
    - `self.update` needs to be handled and the block needs to be able to change it's content/media.  
    - It handles the passed Options with a `getOptions()` function.  
    - New options are added to the `OPT` custom slot class.

- **Medium++** (i.e. `SandFilterBlock/PCA_Block`):  
All of the above plus the block's option buttons should be clickable and it shares/receives data with other blocks/creates new blocks.
    - If the block is created as the result of an option of another block, the old block needs to import the new class and create the new block.
    - If one of the block's options creates a new block, it needs to handle the creation of a new block.
    - The clicks on buttons are send as `cmd`'s with block number and label to `AlexaHandler/consumers.py` by default and need to be handled there.  
    
- **Hard**:  
All of the above plus the block should read/write from Djangos `SQL` database. 
    - Use the `AlexaHandler/models.py` to define the database objects/structure.

- **Harder** (_the full stack_):  
All of the above plus the block needs a new UI class (more than `rich_image`) / needs to implement multi-step dialogue.
    - Block-UI is handled as `javascript` in the `new_grid_block()` found in `AlexaHandler/templates/AlexaHandler/live.html`. Edit as needed.
    - Multi-step dialogue can be implemented with the (_as of this writing brand-new_) Skill Builder in the Alexa Dev Portal.
