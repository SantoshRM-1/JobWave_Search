from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from backend.services.stream_manager import stream_manager

router = APIRouter()

@router.get("/agent-stream/{session_id}")
async def get_agent_stream(session_id: str):
    """
    Subscribes to the live execution thoughts of the LangChain agents.
    Yields Server-Sent Events (SSE).
    """
    return StreamingResponse(
        stream_manager.stream_generator(session_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )
