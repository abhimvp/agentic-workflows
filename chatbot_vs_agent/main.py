import asyncio
import json
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()
client = AsyncOpenAI()  # reads OPENAI_API_KEY from env


# 1. A chatbot only generates text responses based on context inputs.
async def run_chatbot(user_message):
    resp = await client.chat.completions.create(
        model="gpt-5.4-nano", messages=[{"role": "user", "content": user_message}]
    )
    return resp.choices[0].message.content


# 2. Local tool implementation
def get_shipping_date(order_id):
    if order_id == 982:
        return "May 30th via FedEx (tracking: FX-99281)"
    return "Order not found"


# 3. An agent uses tools to fetch data and generate a final response.
async def run_agent(user_message):
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_shipping_date",
                "description": "Get the shipping date for a given order ID.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "integer",
                            "description": "The order ID to lookup",
                        }
                    },
                    "required": ["order_id"],
                },
            },
        }
    ]

    messages = [{"role": "user", "content": user_message}]

    resp = await client.chat.completions.create(
        model="gpt-5.4-nano", messages=messages, tools=tools
    )
    msg = resp.choices[0].message
    messages.append(msg)

    if msg.tool_calls:
        call = msg.tool_calls[0]
        tool_name = call.function.name
        args = json.loads(call.function.arguments)

        print(
            f"  [AGENT SYSTEM] Model requested: {tool_name}(order_id={args.get('order_id')})"
        )

        if tool_name == "get_shipping_date":
            outcome = get_shipping_date(args.get("order_id"))
        else:
            outcome = "Unknown tool"

        print(f"  [AGENT SYSTEM] Tool result: {outcome}")

        messages.append({"role": "tool", "tool_call_id": call.id, "content": outcome})

        resp2 = await client.chat.completions.create(
            model="gpt-5.4-nano", messages=messages
        )
        return resp2.choices[0].message.content

    return msg.content


async def main():
    query = "When will order 982 ship?"
    print(f"User Query: '{query}'\n")

    chatbot_reply = await run_chatbot(query)
    print("--- Chatbot Output ---")
    print(chatbot_reply)
    print()

    agent_reply = await run_agent(query)
    print("--- Agent Output ---")
    print(agent_reply)


if __name__ == "__main__":
    asyncio.run(main())
