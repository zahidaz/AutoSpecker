#!/usr/bin/env python3
import json
import os
import platform
import subprocess
import pymongo
from bson import ObjectId, json_util
import pyperclip
import flet as ft


class SpeckApp:
    def __init__(self, page: ft.Page):
        self.history = []
        self.history_pointer = -1

        self.mongo_uri = ""
        with open("mongodb.secrete", "r") as f:
            self.mongo_uri = f.read()
        #self.query = {"manual_validation": {"$exists": False}}
        self.sort = [("rule", 1)]
        self.query = {
            "manual_validation": {"$exists": False},
            "apk": "/mydata/apks/com.alibaba.aliexpresshd"
        }
        self.cursor = None

        self.current_doc = None
        self.collection = None
        self.initialize_page(page)

    def initialize_page(self, page):
        self.page = page
        self.page.title = "Speck - App"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.scroll = "auto"

        self.initialize_buttons()
        self.initialize_views()

    def initialize_views(self):
        hint = "MongoDB URI here..."
        self.mongo_uri_input = ft.TextField(
            value=self.mongo_uri,
            hint_text=hint,
            text_size=10,
            height=20,
            content_padding=3,
            expand=True,
        )
        self.connect_db_button = ft.ElevatedButton(
            "Connect to DB", height=20, on_click=self.on_connect
        )
        self.console_view = ft.Text(
            "Console... Status Appears Here", bgcolor="#fffbbb", max_lines=5
        )
        self.comment_txt_in = ft.TextField(hint_text="Comment...", width=600)
        self.rule = ft.Markdown("", selectable=True)

        json_code = """```json

```"""
        self.json_view = ft.Markdown(
            json_code,
            selectable=True,
            extension_set="gitHubWeb",
            code_theme="atom-one-dark",
            code_style=ft.TextStyle(font_family="Roboto Mono"),
        )

        self.code_view = ft.Markdown(
            json_code,
            selectable=True,
            extension_set="gitHubWeb",
            code_theme="atom-one-dark",
            code_style=ft.TextStyle(font_family="Roboto Mono"),
        )

    def initialize_buttons(self):
        self.prev_button = ft.ElevatedButton("Prev", on_click=self.on_prev)
        self.false_button = ft.ElevatedButton("False & Next", on_click=self.on_false)
        self.true_button = ft.ElevatedButton("True & Next", on_click=self.on_true)
        self.next_button = ft.ElevatedButton("Next", on_click=self.on_next)
        self.open_file_button = ft.ElevatedButton(
            "Show In Editor", on_click=self.open_file
        )
        self.cp_id_to_clipboard_button = ft.ElevatedButton(
            "Copy ID", on_click=self.cp_id_to_clipboard
        )

    def set_console(self, msg, error=False):
        if error:
            self.console_view.bgcolor = "#ffbbbb"
        else:
            self.console_view.bgcolor = "#fffbbb"

        self.console_view.value = msg
        if error:
            print("[!] ", msg)
        self.console_view.update()

    def on_connect(self, event):
        uri = self.mongo_uri_input.value
        if not uri:
            self.set_console("Empty URI")
            print("Empty URI")
            return

        try:
            self.set_console("Connecting...")
            client = pymongo.MongoClient(self.mongo_uri)
            client.admin.command("ismaster")
            db = client["speck"]
            self.collection = db["s2"]
            self.cursor = self.collection.find(self.query).sort(self.sort)
            self.set_console("Connected to MongoDB")
            # call next to setup the empty views
            self.on_next(event)
        except Exception as e:
            self.set_console(str(e), error=True)

    def on_true(self, event):
        self.update_doc(validated=True)
        self.on_next(event=event)

    def on_false(self, event):
        self.update_doc(validated=False)
        self.on_next(event=event)

    def update_doc(self, validated: bool):
        doc = self.current_doc or Exception("No document found")
        comment = self.comment_txt_in.value or ""
        doc["manual_validation"] = validated
        doc["comment"] = comment
        try:
            print("Updating document...")
            update_operation = {
                "$set": {"manual_validation": validated, "comment": comment}
            }
            doc_id = doc["_id"]["$oid"]
            doc_id = ObjectId(doc_id)  # Convert the doc_id to ObjectId
            query = {"_id": doc_id}
            self.collection.update_one(query, update_operation)
            self.log_doc_update(doc)
        except Exception as e:
            self.set_console(str(e), error=True)

    def next_document(self):
        if self.cursor is None:
            print("[!] Error: Cursor is None")
            self.set_console(
                "[!] Cursor is None. Are you connected to the database?", True
            )
            return
        try:
            if (
                not self.history
                or self.history_pointer is None
                or self.history_pointer == len(self.history) - 1
            ):
                # If there's no history or the pointer is at the end of the history
                try:
                    bson = next(self.cursor)
                except pymongo.errors.CursorNotFound:
                    self.set_console("Cursor Not Found", error=True)
                    self.on_connect(None)
                    bson = next(self.cursor)
                    
                json_string = json.dumps(bson, default=json_util.default)
                doc = json.loads(json_string)
                self.history.append(doc)
                self.history_pointer = (
                    len(self.history) - 1
                )  # Update the history pointer

            else:  # If there's a next document in the history
                self.history_pointer += 1
                doc = self.history[self.history_pointer]

            self.current_doc = doc
            return doc

        except StopIteration:
            return None

    def get_prev_document(self):
        if self.history_pointer == 0:
            print("[!] Error: No previous document")
            self.set_console(
                "[!] No previous document. Are you at the beginning?", True
            )
        else:
            try:
                self.history_pointer -= 1
                doc = self.history[self.history_pointer]
                self.current_doc = doc
                return doc
            except StopIteration:
                self.set_console("No previous document found.", error=True)
                return None

    def on_new_doc(self, doc, msg):
        print(msg)
        file_path = "." + doc["file"]
        self.set_console(msg)
        if doc is not None:
            json_code = json.dumps(doc, indent=4)
            self.json_view.value = f"```json\n{json_code}\n```"
            self.set_console("")
            self.json_view.update()

            if doc and "comment" in doc:
                comment = doc["comment"]
            else:
                comment = ""
            self.comment_txt_in.value = comment
            self.comment_txt_in.update()

            rule_number = doc["rule"]
            rule_file_path = f"./rules/{rule_number}.md"
            with open(rule_file_path, "r") as f:
                lines = f.readlines()
                rule = "".join(lines[:2])
                self.rule.value = rule
                self.rule.update()

        # check if the file exists
        if not os.path.exists(file_path):
            self.set_console("File does not exist", error=True)
            self.code_view.value = f"```java\nFile Does NOT exists\n```"
            self.code_view.update()
        else:
            code_context = self.read_code_context(file_path)
            self.code_view.value = f"```java\n{code_context}\n```"
            self.code_view.update()

    def on_next(self, event):
        msg = "Getting Next Document..."
        doc = self.next_document()
        if doc is None:
            return
        self.on_new_doc(doc, msg)

    def on_prev(self, event):
        msg = "Getting Previous Document..."
        doc = self.get_prev_document()
        if doc is None:
            msg = "No previous document found."
            doc = self.current_doc
        self.on_new_doc(doc, msg)

    def open_file(self, event):
        file_path = "." + self.current_doc["file"]
        line_number = self.current_doc["lineNumber"]

        # check if the file exists
        if not os.path.exists(file_path):
            self.set_console("File does not exist", error=True)
            return
        
        # open the file in vscode
        if self.open_in_vscode(file_path, line_number): 
            return # if the file is opened in vscode, return
        # if vscode is not installed, open the file in the default editor
        try: # open the file in the default editor
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", file_path])
            elif platform.system() == "Linux":
                subprocess.Popen(["xdg-open", file_path])
            else:
                self.set_console("Unsupported platform", error=True)
        except Exception as e:
            self.set_console(str(e), error=True)


    def open_in_vscode(self, file_path, line_number):
        help = """VSCode: Open the Command Palette (Cmd+Shift+P) and type 'shell command' to find the Shell Command:
                    Install 'code' command in PATH command."""

        try:
            if platform.system() == "Windows":
                subprocess.Popen(["code", "--goto", f"{file_path}:{line_number}", "-r"])
            elif platform.system() == "Darwin":
                subprocess.Popen(["code", "--goto", f"{file_path}:{line_number}", "-r"])
            elif platform.system() == "Linux":
                subprocess.Popen(["code", "--goto", f"{file_path}:{line_number}", "-r"])
            else:
                self.set_console("Unsupported platform", error=True)

            return True
        except Exception as e:
            self.set_console(help, error=True)
            # self.set_console(str(e), error=True)
        
        return False


    

    def read_code_context(self, file_path):
        # read 3 lines before and after the line number
        line_number = self.current_doc["lineNumber"]
        context_size = 6
        with open(file_path, "r") as f:
            lines = f.readlines()
            start = max(0, line_number - context_size)
            end = min(len(lines), line_number + context_size)
            code_context = "".join(lines[start:end])
            return code_context

    def cp_id_to_clipboard(self, event):
        if self.current_doc is None:
            self.set_console("No document found", error=True)
            return
        document_id = self.current_doc["_id"]["$oid"]
        pyperclip.copy(document_id)

    def run(self):
        info_section = ft.Column(
            [
                ft.Row(
                    [
                        self.console_view,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [self.mongo_uri_input, self.connect_db_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.json_view,
                self.code_view,
                self.rule,
            ],
            scroll=ft.ScrollMode.ALWAYS,
        )

        btns = [
            self.prev_button,
            ft.VerticalDivider(),
            self.false_button,
            self.true_button,
            ft.VerticalDivider(),
            self.next_button,
        ]

        control_section = ft.Column(
            [
                ft.Row(
                    [self.open_file_button, self.cp_id_to_clipboard_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.comment_txt_in,
                ft.Row(btns, alignment=ft.MainAxisAlignment.CENTER),
            ]
        )
        control_section.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        self.page.add(
            ft.Column(
                [
                    info_section,
                    control_section,
                ]
            )
        )

    def log_doc_update(self, doc):
        with open("logs.csv", "a") as f:
            f.write(f"{doc['_id']},{doc['manual_validation']},{doc['comment']}\n")


def main(page):
    SpeckApp(page=page).run()


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")


# Example Document
# {
#   "_id": {
#     "$oid": "64c116eabdce5c8f237673c7"
#   },
#   "severity": "critical",
#   "apk": "/mydata/apks/com.airbnb.android",
#   "kind": "[EXTERNAL]",
#   "file": "/mydata/apks/com.airbnb.android/sources/h43/m.java",
#   "lineNumber": 133,
#   "rule": 1,
#   "errorMsg": "implicit intent(s) (don't) use an app chooser",
#   "eMsg": null,
#   "comment": "Depending on a condition, either the class name or the package name is set for the intent. This indicates that the intent is explicitly targeting a specific component",
#   "manual_validation": false
# }
