from dijkstra import Graph
import ipywidgets as widgets
from IPython.display import display

class Node(widgets.Button):
    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.name = kwargs["name"]
        self.type = kwargs.get("type", "default")

class App(widgets.VBox):
    def __init__(self, *args, **kwargs):
        # Define UI components
        self.rows = kwargs.get("rows", 9)
        self.cols = kwargs.get("cols", 16)

        # Create a grid of buttons 16 x 9
        self.nodes = []
        for i in range(self.rows):
            cols = []
            for j in range(self.cols):
                btn = Node(
                    name=(i, j),
                    layout=dict(width="50px", height="50px"),
                    style=dict(font_size="11px", button_color="DodgerBlue"),
                )
                btn.on_click(self.on_btn_click)
                cols.append(btn)
            self.nodes.append(cols)

        # Clear path button
        self.clear_path_btn = widgets.Button(description="Clear Path")
        self.clear_path_btn.style.button_color = "LightYellow"
        self.clear_path_btn.on_click(self.on_clear_path_btn_click)
        self.clear_path_btn.layout.width = "100px"

        # Clear board button
        self.clear_board_btn = widgets.Button(description="Clear")
        self.clear_board_btn.style.button_color = "LightCoral"
        self.clear_board_btn.on_click(self.on_clear_board_btn_click)
        self.clear_board_btn.layout.width = "100px"

        # Go button
        self.go_btn = widgets.Button(description="Go!")
        self.go_btn.style.button_color = "DarkSeaGreen"
        self.go_btn.on_click(self.on_go_btn_click)
        self.go_btn.layout.width = "100px"

        # Output widget for displaying error messages
        self.output = widgets.Output()

        # Render UI components in a VBox
        super(App, self).__init__(
            children=[
                widgets.VBox([widgets.HBox(node) for node in self.nodes]),
                widgets.HBox([self.clear_path_btn, self.go_btn, self.clear_board_btn]),
                self.output
            ]
        )

    def show_error_message(self, message):
        with self.output:
            self.output.clear_output()
            error_message = widgets.HTML(
                value=f'<div style="text-align: center; color: red; font-size: 20px;">Error</div>'
                      f'<div style="text-align: center; color: gray;">{message}</div>'
            )
            ok_button = widgets.Button(
                description='OK',
                button_style='info',
                layout=widgets.Layout(width='100px', margin='0 auto', display='block')
            )
            ok_button.on_click(self.clear_error_message)
            display(widgets.VBox([error_message, ok_button]))

    def clear_error_message(self, b=None):
        with self.output:
            self.output.clear_output()

    def on_clear_path_btn_click(self, *args):
        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.nodes[i][j]
                if btn.style.button_color == "Gainsboro":
                    btn.style.button_color = "DodgerBlue"
                    btn.type = "default"
                    btn.description = " "
                    btn.icon = " "

    def on_clear_board_btn_click(self, *args):
        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.nodes[i][j]
                btn.style.button_color = "DodgerBlue"
                btn.type = "default"
                btn.description = " "
                btn.icon = " "

    def on_btn_click(self, node):
        if node.type == "default":
            node.type = "start"
            node.description = "Start"
            node.style.button_color = "MediumSeaGreen"
        elif node.type == "start":
            node.type = "block"
            node.description = "Block"
            node.style.button_color = "OrangeRed"
        elif node.type == "block":
            node.type = "end"
            node.description = "End"
            node.style.button_color = "White"
        else:
            node.type = "default"
            node.description = " "
            node.style.button_color = "DodgerBlue"

    def on_go_btn_click(self, *args):
        tups = []
        points = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        start = None
        end = None

        for i in range(self.rows):
            for j in range(self.cols):
                btn = self.nodes[i][j]

                for dx, dy in points:
                    x, y = i + dx, j + dy
                    if 0 <= x < self.rows and 0 <= y < self.cols:
                        if btn.type == "block":
                            tups.append(((i, j), (x, y), float("inf")))
                        else:
                            tups.append(((i, j), (x, y), 1))

                        if btn.type == "start":
                            start = (i, j)

                        if btn.type == "end":
                            end = (i, j)

        if start is None or end is None:
            self.show_error_message("Please select both start and end nodes to proceed.")
            return

        graph = Graph(tups)
        shortest_path = graph.dijkstra(start, end)

        if not shortest_path:
            self.show_error_message("No path found.")
            return

        for i in range(len(shortest_path) - 1):
            if i != 0 and i != len(shortest_path) - 1:
                y, x = shortest_path[i]
                a, b = shortest_path[i + 1]

                btn = self.nodes[y][x]
                btn.style.button_color = "Gainsboro"
                btn.description = " "

                if b == x + 1:
                    btn.icon = "arrow-right"
                elif b == x - 1:
                    btn.icon = "arrow-left"
                elif a == y + 1:
                    btn.icon = "arrow-down"
                elif a == y - 1:
                    btn.icon = "arrow-up"