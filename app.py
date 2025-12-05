import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from agent.index import initialize_agent
from routes.ai_routes import ai_router

app = FastAPI()

allowed_origins = [
    "https://ballin-wear.onrender.com",
    "http://localhost:5173"
]

initialize_agent()
app.include_router(ai_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    try:
        return JSONResponse(content={"response": ""})
    except Exception as e:
        print("Error in /:", str(e))
        return JSONResponse(content={"error": "Internal Server Error"}, status_code=500)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
