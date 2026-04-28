class FakeEntry:
    def __init__(self, value=""):
        self.value = value
        self.fg = None
        self.bindings = {}

    def get(self):
        return self.value

    def delete(self, _start, _end):
        self.value = ""

    def insert(self, _index, value):
        self.value = value

    def config(self, **kwargs):
        if "fg" in kwargs:
            self.fg = kwargs["fg"]

    def bind(self, event, callback):
        self.bindings[event] = callback


class FakeLabel:
    def __init__(self):
        self.props = {}

    def config(self, **kwargs):
        self.props.update(kwargs)


class FakeButton:
    def __init__(self):
        self.state = "normal"

    def config(self, **kwargs):
        if "state" in kwargs:
            self.state = kwargs["state"]


class FakeTreeTable:
    def __init__(self):
        self.rows = {}
        self.counter = 0
        self.headings = {}
        self.columns = {}

    def insert(self, _parent, _index, values=()):
        row_id = str(self.counter)
        self.rows[row_id] = values
        self.counter += 1
        return row_id

    def get_children(self):
        return list(self.rows.keys())

    def delete(self, row_id):
        self.rows.pop(str(row_id), None)

    def heading(self, col, text):
        self.headings[col] = text

    def column(self, col, width, anchor):
        self.columns[col] = {"width": width, "anchor": anchor}

    def configure(self, **_kwargs):
        return None


class FakeWidget:
    def __init__(self):
        self.destroyed = False

    def destroy(self):
        self.destroyed = True


class FakeWindow:
    def __init__(self, children):
        self._children = children

    def winfo_children(self):
        return self._children
