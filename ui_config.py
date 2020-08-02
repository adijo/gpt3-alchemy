"""
MIT License

Copyright (c) 2020 Shreya Shankar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class UIConfig:
    """Stores customized UI parameters."""

    def __init__(self, description='Description',
                 button_text='Submit',
                 placeholder='Default placeholder',
                 show_example_form=False):
        self.description = description
        self.button_text = button_text
        self.placeholder = placeholder
        self.show_example_form = show_example_form

    def get_description(self):
        """Returns the input of the example."""
        return self.description

    def get_button_text(self):
        """Returns the intended output of the example."""
        return self.button_text

    def get_placeholder(self):
        """Returns the intended output of the example."""
        return self.placeholder

    def get_show_example_form(self):
        """Returns whether editable example form is shown."""
        return self.show_example_form

    def json(self):
        """Used to send the parameter values to the API."""
        return {"description": self.description,
                "button_text": self.button_text,
                "placeholder": self.placeholder,
                "show_example_form": self.show_example_form}
