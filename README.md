# Price Look Up

A Python script that lets a local AI model look up a product’s price in `prices.json`.

## Run it

Install Python and Ollama, then run these commands from this folder:

```powershell
python -m pip install openai
ollama pull qwen3:1.7b
python main.py
```

## How the tool call works

1. Python loads the product prices from `prices.json`.
2. The script sends Ollama a question about the mug and describes the `get_price` function. The description tells the model that the function takes a product name.
3. The model requests a call to `get_price` with `mug` as the product.
4. Python runs the function and gets `12.5` from the price list.
5. Python sends that result back to Ollama with the ID of the tool call. The model uses the result to write its final answer.