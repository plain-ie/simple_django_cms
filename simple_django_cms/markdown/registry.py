import re


class MarkdownWidgetRegistry:

    widgets = {}

    def register(self, extension):
        for pattern in extension.patterns:
            self.widgets[str(pattern)] = extension

    def is_match(self, pattern, string):
        return re.match(pattern, string)

    def parse_row(self, string, previous_widget=None, next_widget=None):
        for pattern in self.widgets.keys():
            widget = self.widgets[pattern]
            if self.is_match(pattern, string) is not None:
                return widget(string)

    def parse(self, text):

        rows = text.split('\n')
        elements = []

        for row in rows:

            row = re.sub(r'^\s*', '', row)
            row = re.sub(r'\s*$', '', row)

            if row != '':

                previous_widget = None
                if len(elements) > 0:
                    previous_widget = elements[-1]

                widget = self.parse_row(row)
                if widget is not None:
                    elements.append(widget)

        for index, element in enumerate(elements, start=0):

            if index == 0:
                previous_widget = None
            else:
                previous_widget = elements[index-1]

            if index + 1 == len(elements):
                next_widget = None
            else:
                next_widget = elements[index+1]

            elements[index].previous_widget = previous_widget
            elements[index].next_widget = next_widget

        return elements
