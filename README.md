![](https://i.ibb.co/wC9LxYw/Neutron-nobg.png)

Create modern cross-platform apps in HTML and CSS with Python

## What is Neutron
Neutron will allow developers to build complex Python apps while using CSS and HTML for the design. Neutron will give full access to the DOM just as it would be in Javascript and will offer an easy scripting method to bind HTML with Python.

For example:
```
import Neutron

win = Neutron.Window("Example", size=(600,100))
NeutronLogo = "https://camo.githubusercontent.com/27afdb9e229abd7fae33de3db681fcc2c30f1e472881ca4c910ad655b38a3831/68747470733a2f2f692e6962622e636f2f7743394c7859772f4e657574726f6e2d6e6f62672e706e67"

def afterResize():
    # Set window to fullscreen once finished loading
    win.toggle_fullscreen()

# The loader covers while all the other elements and css load
win.loader(source=f"<img src={NeutronLogo} style='{Neutron.utils.css.center()}'>", color="#353537", duration=3000, after=afterResize)


def setName():
    name = win.getElementById("inputName").value
    win.getElementById("title").innerHTML = "Hello: " + name


win.display(f"""

<!DOCTYPE html>
<html>
   <head lang="en">
      <meta charset="UTF-8">
   </head>
   <body>
      <h1 id="title">Hello: </h1>
      <input id="inputName">
      <button id="submitName" onclick="{Neutron.event(setName)}">Submit</button>
      <!-- OR-->
      {Neutron.Button(win, content="Submit", onclick=Neutron.event(setName))}
   </body>
</html>
""")
win.show()
```
Neutron is still in it's alpha and phase and many feature are not out yet, but it is important to know that **the examples shown in this repo are always working and updating**.

Another example:
```
import Neutron

win = Neutron.Window("Example", css="def.css")

HeaderObject = Neutron.Header(win, id="title", content="Hello")


def setName():
    HeaderObject.setAttribute("style", "color: red;")
    HeaderObject.innerHTML = "Hello world!"
    win.getElementById("submit").innerHTML = "clicked!"


Neutron.Button(win, id="submit", content="Hi", onclick=Neutron.event(setName))

win.show()
```

### CSS
As stated before Neutron allows developers to integrate CSS. Simply enter the CSS file's path in the Neutron.Window() object and then use CSS as you normally would.

## Contributing
Contributions are welcome and in need! You can easily get started contributing by reading [CONTRIBUTING.md](https://github.com/IanTerzo/Neutron/blob/main/CONTRIBUTING.md)

## Installation
At the moment there is no straight forward installation method. It is always possible to just clone the repo.
