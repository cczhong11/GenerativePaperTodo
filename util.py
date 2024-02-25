import json
from openai import OpenAI
import base64
from PIL import Image, ImageEnhance
import io

client = OpenAI()


def get_json(data):
    print(data)
    try:

        return json.loads(data)
    except:
        # find first {
        start = data.find("{")
        end = data.rfind("}")
        print(data[start : end + 1])
        return json.loads(data[start : end + 1])


def encode_image(image_path):
    image = Image.open(image_path)
    # turn image to bw
    image = image.convert("L")
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2)
    height, width = image.size
    new_image = image.resize((height // 2, width // 2))
    buffered = io.BytesIO()
    # print(type(new_image))

    new_image.save(buffered, format="JPEG")
    # save the image to the image_path
    new_image.save("process_" + image_path)
    # Encode the image to base64
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def give_me_text_from_graph(filename):
    base64_image = encode_image(filename)
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "give me a json with date and list of tasks from this image. json has two fields: date and tasks. date is a string (MM/DD) and tasks is a list of strings. the image is a bullet journal page. only return actual json. do not return any other text.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    result = response.choices[0].message.content

    return get_json(result)


def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ],
            }
        ],
        max_tokens=300,
    )
    result = response.choices[0].message.content

    return result


def combine_to_json_gpt(old_json, new_json):
    prompt = f"combine the following two jsons into one. {old_json} and {new_json}. if have the same index, update it with the new value. if not, add it to the list. return the combined json."
    response = call_gpt(prompt)
    return get_json(response)


def answer_question(old_json, question):
    prompt = f"Here is the current my todo JSON: {old_json}. please help me answer the following question: {question}."
    response = call_gpt(prompt)
    return response


def combine_to_json(old_json, new_json):
    old_json.update(new_json)
    return old_json


# print(give_me_text_from_graph("myfile.jpg"))
print(get_json('hello world {"a":1}'))
