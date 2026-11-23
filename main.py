import json
from pathlib import Path
prices_file = Path(__file__).with_name("prices.json")
prices = json.loads(prices_file.read_text(encoding="utf-8"))
def get_price(product):
    return prices.get(product)
price_tool = {
    "type": "function",
    "function": {
        "name": "get_price",
        "description": "Look up the price of a product.",
        "parameters": {
            "type": "object",
            "properties": {"product": {"type": "string"}},
            "required": ["product"],
        },
    },
}
from openai import OpenAI

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
model = "qwen3:1.7b"
messages = [
    {"role": "user", "content": "Use the get_price tool to look up the mug. /no_think"}
]

reply = client.chat.completions.create(
    model=model, messages=messages, tools=[price_tool]
).choices[0].message

if not reply.tool_calls:
    raise SystemExit("The model did not request a price lookup. Try running it again.")

messages.append(reply.model_dump(exclude_none=True))

for call in reply.tool_calls:
    product = json.loads(call.function.arguments)["product"]
    price = get_price(product)
    print(f"Tool looked up {product}: {price}")
    messages.append({
        "role": "tool",
        "tool_call_id": call.id,
        "content": json.dumps({"product": product, "price": price}),
    })

answer = client.chat.completions.create(model=model, messages=messages)
print(answer.choices[0].message.content)