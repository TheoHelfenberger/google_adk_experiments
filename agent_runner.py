import asyncio
from multi_tool_agent.agent import root_agent  # This is the same agent that `adk run my_agent` loads
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

async def main():
    app_name = "my_agent"
    user_id = "local_user"
    session_id = "session_1"

    # Create in-memory session store
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    while True:
        user_in = "Waht is the weather in Bern?" # input()
        # Build the user message
        new_message = types.UserContent(user_in)

        # new_message = types.Content(
        #     parts=[types.Part.from_text(text="What is the weather in London?")]
        # )

        # Create runner (new API requires app_name + agent)
        runner = Runner(
            app_name=app_name,
            agent=root_agent,
            session_service=session_service
        )

        # Run (always streaming now)
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=new_message
        ):
            if event.content:
                for p in event.content.parts or []:
                    if getattr(p, "text", None):
                        print(p.text, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())