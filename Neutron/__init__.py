import webview
from bs4 import BeautifulSoup
from . import utils
import inspect
import sys

html = """
<!DOCTYPE html>
<html>
<head lang="en">
<meta charset="UTF-8">
</head>
<body>
<!-- <div id="cover" style="position: fixed; height: 100%; width: 100%; top:0; left: 0; background: #000; z-index:9999;"></div> -->
<script>
    function bridge(func) {
        pywebview.api.bridge(func)
    }
</script>
</body>
</html>
"""

global api_functions
api_functions = {}


class Api:
    def __init__(self):
        pass

    def bridge(self, func):
        if api_functions[func]:
            api_functions[func]()


def event(function):
    if not str(function) in api_functions:
        api_functions.update({str(function): function})
    return f"bridge('{str(function)}')"


# ELEMENTS #

def Button(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('button', id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Input(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('input', id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Header(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('h' + str(type), id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Paragraph(window, content="", id=None, type=1, **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")
    elem = soup.new_tag('p' + str(type), id=id, attrs=args)
    elem.string = content
    if id:
        elem.id = id
    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


def Div(window, id=None, children=[], **args):
    soup = BeautifulSoup(window.webview.html, features="lxml")

    # Remove children from body
    for child in children:
        soup = str(soup).replace(str(child), "")

    soup = BeautifulSoup(soup, features="lxml")
    elem = soup.new_tag('div', id=id, attrs=args)
    elem.id = id
    for child in children:
        elem.append(child)

    soup.body.append(elem)
    window.setHtml(soup)
    return HTMlelement(window, id, elem)


class HTMlelement:
    def __init__(self, window, id, elementHTML=None):
        self.window = window
        self.elementHTML = elementHTML
        self.id = id

    def __str__(self):
        # elementHTML will be set to None if class is called on runtime
        if self.elementHTML is not None:
            return str(self.elementHTML)
        else:
            return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").outerHTML;"""))

    def getAttributes(self):
        if self.window.running:
            return self.window.webview.get_elements(f'#{self.id}')[0]
        else:
            return self.elementHTML.attrs

    def setAttribute(self, attribute, value):
        self.window.webview.evaluate_js(
            f""" '' + document.getElementById("{self.id}").setAttribute("{attribute}", "{value}");""")

    def innerHTML_get(self):
        return str(self.window.webview.evaluate_js(f""" '' + document.getElementById("{self.id}").innerHTML;"""))

    def innerHTML_set(self, val):
        self.window.webview.evaluate_js(f"""document.getElementById("{self.id}").innerHTML = "{val}";""")

    innerHTML = property(innerHTML_get, innerHTML_set)

    def value_get(self):
        return self.getAttributes()['value']

    def value_set(self, val):
        self.setAttribute("value", val)

    value = property(value_get, value_set)


class Window:
    def __init__(self, title, css="def.css", min_size=(300, 300), size=(900, 600), fullscreen=False):
        api = Api()
        self.webview = webview.create_window(title, html=html, js_api=api, min_size=min_size, width=size[0],
                                             height=size[1], fullscreen=fullscreen)
        self.css = css
        self.running = False

    def load_handler(self, win):
        css_src = open(self.css, "r").read()
        win.load_css(css_src)

    def display(self, html=None, file=None):
        frame = inspect.currentframe()
        locals = frame.f_back.f_locals

        if file:
            # convert file content to f-string
            content = str(open(file, "r").read())
            oneLine = content.replace("\n", "")
            soupSrc = eval(f"f'{oneLine}'", locals)
            
        elif html:
            soupSrc = html
        
        soup = BeautifulSoup(soupSrc, features="lxml")
        elem = soup.new_tag('script')
        elem.string = "function bridge(func) {pywebview.api.bridge(func)}"
        soup.body.append(elem)
        self.webview.html = str(soup)

    def setHtml(self, html):

        self.webview.html = str(html)

    def show(self):
        self.running = True
        webview.start(self.load_handler, self.webview)

    def appendChild(self, html):
        if self.running:
            self.webview.evaluate_js(f"""document.body.innerHTML += '{html}';""")
        else:
            raise Exception(""""Window.append" can only be called while the window is running!""")

    def getElementById(self, id):
        if self.running:
            elem = str(self.webview.evaluate_js(f""" '' + document.getElementById("{id}");"""))

            if elem != "null":
                return HTMlelement(self, id)
            else:
                return None

        else:
            raise Exception(""""Window.getElementById" can only be called while the window is running!""")

    def getElementById(self, id):
        if self.running:
            elem = str(self.webview.evaluate_js(f""" '' + document.getElementById("{id}");"""))

            if elem != "null":
                return HTMlelement(self, id)
            else:
                return None

        else:
            raise Exception(""""Window.getElementById" can only be called while the window is running!""")
