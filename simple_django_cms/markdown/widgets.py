import re

from django.core.validators import validate_email
from django.template.loader import render_to_string as dj_render_to_string
from django.utils.safestring import mark_safe


class BaseWidget:

    name = None
    patterns = []
    template = ''

    def __init__(self, string):
        self.string = string
        self.previous_widget = None
        self.next_widget = None

    @property
    def render(self):
        return dj_render_to_string(
            self.get_template(),
            context=self.get_context()
        )

    def get_context(self):
        return {}

    def get_template(self):
        return self.template

    def replace_nested_widgets(self, string, widget):
        new_string = str(string)
        for pattern in widget.patterns:
            matches = re.findall(pattern, new_string)
            for match in matches:
                if isinstance(match, tuple) is True:
                    match = match[0]
                new_string = new_string.replace(match, widget(match).render)
        return new_string


#
# Emphasis
#


class Bold(BaseWidget):
    name = 'bold'
    patterns = [r'(\*\*\*([^\*]+)\*\*\*)']
    template = 'simple_django_cms/markdown/widgets/bold.html'

    def get_context(self):
        string = str(self.string)
        string = re.sub('\*\*\*', '', string)
        return {
            'text': string,
        }


#
# Headings
#


class HeadingH1(BaseWidget):
    name = 'heading_h1'
    patterns = [r'^\#\s?[^#]+$']
    template = 'simple_django_cms/markdown/widgets/heading_h1.html'

    def get_context(self):
        return {
            'text': re.sub(r'^\#\s?', '', self.string)
        }


class HeadingH2(BaseWidget):
    name = 'heading_h2'
    patterns = [r'^\#\#\s?[^#]+$']
    template = 'simple_django_cms/markdown/widgets/heading_h2.html'

    def get_context(self):
        return {
            'text': re.sub(r'^\#\#\s?', '', self.string)
        }


class HeadingH3(BaseWidget):
    name = 'heading_h3'
    patterns = [r'^\#\#\#\s?[^#]+$']
    template = 'simple_django_cms/markdown/widgets/heading_h3.html'

    def get_context(self):
        return {
            'text': re.sub(r'^\#\#\#\s?', '', self.string)
        }


class HeadingH4(BaseWidget):
    name = 'heading_h4'
    patterns = [r'^\#\#\#\#\s?[^#]+$']
    template = 'simple_django_cms/markdown/widgets/heading_h4.html'

    def get_context(self):
        return {
            'text': re.sub(r'^\#\#\#\#\s?', '', self.string)
        }


#
# Horizontal rule
#


class HorizontalRule(BaseWidget):
    name = 'horizontal_rule'
    patterns = [r'^\*\*\*$']
    template = 'simple_django_cms/markdown/widgets/horizontal_rule.html'


#
# Image
#

class Image(BaseWidget):
    name = 'link'
    patterns = [r'^\!(\[([^\`\]]+)\]\(([^\)\"]+)\s?(\"([^\"]+)\")?\s?\))$']
    template = 'simple_django_cms/markdown/widgets/image.html'

    def get_context(self):

        string = str(self.string)

        link = ''
        alt = ''
        title = ''

        for pattern in self.patterns:
            matches = re.findall(pattern, string)
            if len(matches) == 1:
                alt = matches[0][1]
                link = matches[0][2]
                if len(matches) >= 4:
                    title = matches[0][4]

        return {
            'alt': alt,
            'link': link,
            'title': title
        }


#
# Links
#

class SimpleLink(BaseWidget):
    name = 'simple_link'
    patterns = [r'\<[^\<\>]+\>']

    def get_context(self):
        string = str(self.string)
        string = re.sub('^\<\s*?', '', string)
        string = re.sub('\s*?\>$', '', string)
        return {
            'link': string
        }

    @property
    def render(self):
        contex = self.get_context()
        return f'[{contex["link"]}]({contex["link"]})'


class CallToActionLink(BaseWidget):
    name = 'call_to_action_link'
    patterns = [
        r'(\[cta\s([^\|\]]+)\s*?\|\s*?([^\|\]]+)\s*?\])',
        '[`cta` read more](https://xxxx)',
    ]
    template = 'simple_django_cms/markdown/widgets/call_to_action_link.html'

    def get_context(self):

        string = str(self.string)

        link = ''
        text = ''

        for pattern in self.patterns:
            matches = re.findall(pattern, string)
            if len(matches) == 1:
                text = matches[0][1]
                link = matches[0][2]

        # Link is telephone?
        if link.startswith('+') is True or link.startswith('00') is True:
            link = 'tel:' + link

        # Link is email?
        else:
            try:
                validate_email(link)
                link = 'mailto:' + link
            except Exception:
                pass

        return {
            'text': text,
            'link': link
        }


class Link(BaseWidget):
    name = 'link'
    patterns = [r'(\[([^\`\]]+)\]\(([^\)]+)\))']
    template = 'simple_django_cms/markdown/widgets/link.html'

    def get_context(self):

        string = str(self.string)

        link = ''
        text = ''

        for pattern in self.patterns:
            matches = re.findall(pattern, string)
            if len(matches) == 1:
                text = matches[0][1]
                link = matches[0][2]

        # Link is telephone?
        if link.startswith('+') is True or link.startswith('00') is True:
            link = 'tel:' + link

        # Link is email?
        else:
            try:
                validate_email(link)
                link = 'mailto:' + link
            except Exception:
                pass

        return {
            'text': text,
            'link': link
        }


#
# Lists
#


class OrderedListElement(BaseWidget):
    name = 'ordered_list_element'
    patterns = [r'^[\d]+\.\s?.+$']
    template = 'simple_django_cms/markdown/widgets/list_element.html'

    def get_context(self):
        string = re.sub(r'^\*\s*', '', self.string)
        string = self.replace_nested_widgets(string, SimpleLink)
        string = self.replace_nested_widgets(string, Link)
        string = self.replace_nested_widgets(string, Bold)
        return {
            'first': False,
            'last': False,
            'ordered': True,
            'text': re.sub(r'^[\d]+\.\s?', '', string),
        }

    @property
    def render(self):

        context = self.get_context()

        if self.previous_widget is not None:
            if self.previous_widget.name != self.name:
                context['first'] = True

        if self.next_widget is not None:
            if self.next_widget.name != self.name:
                context['last'] = True

        return dj_render_to_string(
            self.get_template(),
            context=context
        )


class UnorderedListElement(BaseWidget):
    name = 'unordered_list_element'
    patterns = [r'^\*((\s.+)|((?!\*).+))$']
    template = 'simple_django_cms/markdown/widgets/list_element.html'

    def get_context(self):
        string = re.sub(r'^\*\s*?', '', self.string)
        string = self.replace_nested_widgets(string, SimpleLink)
        string = self.replace_nested_widgets(string, Link)
        string = self.replace_nested_widgets(string, Bold)
        return {
            'first': False,
            'last': False,
            'ordered': False,
            'text': string,
        }

    @property
    def render(self):

        context = self.get_context()

        if self.previous_widget is not None:
            if self.previous_widget.name != self.name:
                context['first'] = True

        if self.next_widget is not None:
            if self.next_widget.name != self.name:
                context['last'] = True

        return dj_render_to_string(
            self.get_template(),
            context=context
        )

#
# Paragraph
#


class Paragraph(BaseWidget):
    name = 'paragraph'
    patterns = [r'^.*$']
    template = 'simple_django_cms/markdown/widgets/paragraph.html'

    def get_context(self):
        string = str(self.string)
        string = self.replace_nested_widgets(string, SimpleLink)
        string = self.replace_nested_widgets(string, Link)
        string = self.replace_nested_widgets(string, Bold)
        string = self.replace_nested_widgets(string, CallToActionLink)
        return {
            'text': string
        }
