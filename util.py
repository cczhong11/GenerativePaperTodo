from openai import OpenAI
import base64

client = OpenAI()


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


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
                        "text": "give me a json with date and list of tasks from this image. json has two fields: date and tasks. date is a string and tasks is a list of strings. the image is a bullet journal page. only return actual json. do not return any other text.",
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
    result = result.replace("```json", "")
    result = result.replace("```", "")
    return result


# print(give_me_text_from_graph("myfile.jpg"))
