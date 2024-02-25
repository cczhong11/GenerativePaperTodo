from io import StringIO
import streamlit as st
import json
from util import combine_to_json_gpt, give_me_text_from_graph
import uuid
import os
import pandas as pd

datafile = "data.json"


def read_file():
    if not os.path.exists(datafile):
        return {}
    with open(datafile, "r") as file:
        data = json.loads(file.read())
    return data


data = read_file()


def write_file(data):
    with open(datafile, "w") as file:
        file.write(data)


# Title of the app
st.title("My To-Do List")

# To-do list items
# tasks = ["Write project", "Design", "Write Code"]
uploaded_file = st.file_uploader("Choose a file")


def create_bullet_journal_container(data):
    # combine df
    final_df = None
    count = 0
    for k, v in data.items():
        tasks = v.get("tasks")
        date = v.get("date")
        df = pd.DataFrame(
            {
                "Date": [date] * len(tasks),
                "Tasks": tasks,
                "image": ["http://127.0.0.1:8000/" + v.get("image")] * len(tasks),
                "Order": range(count + 1, count + len(tasks) + 1),
            }
        )
        count += len(tasks)
        if final_df is None:
            final_df = df
        else:
            final_df = pd.concat([final_df, df], ignore_index=True)
    st.data_editor(
        final_df,
        column_config={"image": st.column_config.ImageColumn()},
        hide_index=True,
        num_rows="dynamic",
    )


def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        # To read file as bytes:

        bytes_data = uploaded_file.getvalue()
        st.write("Uploaded file is now stored as bytes.")

        # Can use any file handling or processing here
        # For example, saving the file
        uiud = uuid.uuid4()
        with open(f"{uiud}.jpeg", "wb") as f:
            f.write(bytes_data)
        st.success("File saved!")
        output = give_me_text_from_graph(f"{uiud}.jpeg")
        print(output)
        output_json = json.loads(output)
        output_json["image"] = f"{uiud}.jpeg"
        date = output_json.get("date")
        old_data = data[date]
        new_data = output_json
        new_data = combine_to_json_gpt(old_data, new_data)
        data[date] = new_data
        write_file(json.dumps(data))
        return data
    return data


new_data = process_uploaded_file(uploaded_file)
if new_data:
    data = new_data  # 如果有新数据，更新data变量
create_bullet_journal_container(data)
