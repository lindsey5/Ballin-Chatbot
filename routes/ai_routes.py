import re
import uuid
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from agent.index import get_chat_bot_agent

ai_router = APIRouter()

@ai_router.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        thread_id = body.get("thread_id") or str(uuid.uuid4())
        user_message = body.get("message")

        if not user_message:
            return JSONResponse(
                content={"error": "Message is required."},
                status_code=400
            )

        input_message = {"role": "user", "content": user_message}
        config = {"configurable": {"thread_id": thread_id}}

        agent = get_chat_bot_agent()
        if agent is None:
            return JSONResponse(
                content={"error": "Chat agent not initialized."},
                status_code=500
            )

        result = ""
        for step, metadata in agent.stream(
            {"messages": [input_message]},
            config=config,
            stream_mode="messages"
        ):
            # Use .text property instead of deprecated .text() method
            if metadata.get("langgraph_node") == "agent" and (text := step.text):
                result += text

        # Clean markdown-style code blocks
        cleaned = re.sub(r"```[a-zA-Z]*\n?", "", result).replace("```", "")

        return JSONResponse(
            content={"response": cleaned.strip(), "success": True, "thread_id": thread_id}
        )

    except Exception as e:
        print("Error in /api/chat:", str(e))
        return JSONResponse(
            content={"error": "Internal Server Error"},
            status_code=500
        )