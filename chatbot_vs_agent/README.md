# chatbot vs agent

- Create a `.env` file in the project root & Add OpenAI API Key from  <https://platform.openai.com/api-keys>

- `uv init .`
- `uv add openai python-dotenv`
- `uv init` creates a `pyproject.toml`, a `.venv`, and a starter `main.py`. `uv add` installs the packages into that `venv` and records them in `pyproject.toml`.
- `uv run` automatically checks `pyproject.toml`, syncs any missing dependencies into `.venv`, and executes the script - you don't need to source .venv/bin/activate first (though you still can, if you want the venv active for other tools).
  - `msg` (a `ChatCompletionMessage` object) is appended directly to messages — that works with the `openai SDK` since it serializes properly, but if you ever hit a serialization error, swap it for `msg.model_dump()`.

```bash
******System******/agentic-workflows/chatbot_vs_agent (main)
$ uv run main.py
User Query: 'When will order 982 ship?'

--- Chatbot Output ---
I can help, but I’ll need a bit more info.

- What store/carrier is **order 982** from?
- Can you share the **order status/tracking link** (or the latest updateyou see in your order page/email)?

Once I have that, I can tell you when it’s expected to ship.

  [AGENT SYSTEM] Model requested: get_shipping_date(order_id=982)
  [AGENT SYSTEM] Tool result: May 30th via FedEx (tracking: FX-99281)
--- Agent Output ---
Order **982** will ship on **May 30th**, via **FedEx** (tracking: **FX-99281**).
```

- The `chatbot` cannot retrieve the order status and returns generic customer service advice.
- The `agent` identifies the order ID, requests a tool call to retrieve the shipping date, executes the function, and uses the resulting shipment data to formulate a precise answer.
