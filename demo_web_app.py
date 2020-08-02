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

from http import HTTPStatus
import json
import subprocess

from flask import Flask, request, Response

from gpt import set_openai_key, Example
from ui_config import UIConfig

CONFIG_VAR = "OPENAI_CONFIG"
KEY_NAME = "OPENAI_KEY"


def demo_web_app(gpt, openai_key, config=UIConfig()):
    """Creates Flask app to serve the React app."""
    app = Flask(__name__)

    set_openai_key(openai_key)

    @app.route("/params", methods=["GET"])
    def get_params():
        # pylint: disable=unused-variable
        response = config.json()
        return response

    def error(err_msg, status_code):
        return Response(json.dumps({"error": err_msg}), status=status_code)

    def get_example(example_id):
        """Gets a single example or all the examples."""
        # return all examples
        if not example_id:
            return json.dumps(gpt.get_all_examples())

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)
        return json.dumps(example.as_dict())

    def post_example():
        """Adds an empty example."""
        new_example = Example("", "")
        gpt.add_example(new_example)
        return json.dumps(gpt.get_all_examples())

    def put_example(args, example_id):
        """Modifies an existing example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)

        if "input" in args:
            example.input = args["input"]
        if "output" in args:
            example.output = args["output"]

        # update the example
        gpt.add_example(example)
        return json.dumps(example.as_dict())

    def delete_example(example_id):
        """Deletes an example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        gpt.delete_example(example_id)
        return json.dumps(gpt.get_all_examples())

    @app.route(
        "/examples",
        methods=["GET", "POST"],
        defaults={"example_id": ""},
    )
    @app.route(
        "/examples/<example_id>",
        methods=["GET", "PUT", "DELETE"],
    )
    def examples(example_id):
        method = request.method
        args = request.json
        if method == "GET":
            return get_example(example_id)
        if method == "POST":
            return post_example()
        if method == "PUT":
            return put_example(args, example_id)
        if method == "DELETE":
            return delete_example(example_id)
        return error("Not implemented", HTTPStatus.NOT_IMPLEMENTED)

    @app.route("/translate", methods=["GET", "POST"])
    def translate():
        # pylint: disable=unused-variable
        prompt = request.json["prompt"]
        response = gpt.submit_request(prompt)
        offset = 0
        if not gpt.append_output_prefix_to_query:
            offset = len(gpt.output_prefix)

        return {'text': response['choices'][0]['text'][offset:]}

    subprocess.Popen(["yarn", "start"])
    app.run()
