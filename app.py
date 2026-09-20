import asyncio
import streamlit as st

from mcp import Client
from mcp_server import mcp


st.set_page_config(
    page_title="MCP Learning Path Generator",
    page_icon="🧠",
    layout="centered",
)


async def call_mcp(tool_name, arguments):
    async with Client(mcp) as client:

        result = await client.call_tool(
            tool_name,
            arguments
        )

        data = result.structured_content

        if isinstance(data, dict) and set(data.keys()) == {"result"}:
            return data["result"]

        return data


st.title("🧠 MCP-Powered AI Learning Path Generator")

st.caption(
    "Generate a personalized learning roadmap using "
    "Model Context Protocol (MCP)."
)


with st.form("learning_form"):

    subject = st.text_input(
        "What do you want to learn?",
        "Python and Machine Learning"
    )

    days = st.slider(
        "Learning Duration",
        min_value=7,
        max_value=60,
        value=30
    )

    level = st.selectbox(
        "Current Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    submitted = st.form_submit_button(
        "🚀 Generate Learning Path"
    )


if submitted:

    try:

        with st.spinner("🔌 Calling MCP tools..."):

            plan = asyncio.run(
                call_mcp(
                    "generate_learning_path",
                    {
                        "subject": subject,
                        "days": days,
                        "level": level
                    }
                )
            )

            resources = asyncio.run(
                call_mcp(
                    "get_learning_resources",
                    {
                        "subject": subject
                    }
                )
            )

            project = asyncio.run(
                call_mcp(
                    "suggest_project",
                    {
                        "subject": subject,
                        "level": level
                    }
                )
            )


        st.success(
            "✅ Learning path generated successfully using MCP!"
        )


        st.subheader("🎯 Learning Goal")

        st.write(plan["goal"])


        st.subheader("📅 Day-by-Day Roadmap")

        for item in plan["roadmap"]:

            with st.expander(
                f"Day {item['day']} — {item['topic']}"
            ):

                st.write(item["task"])


        st.subheader("📚 Learning Resources")

        for resource in resources:

            st.markdown(
                f"- [{resource['title']}]"
                f"({resource['url']}) — "
                f"{resource['purpose']}"
            )


        st.subheader("💡 Suggested Mini Project")

        st.markdown(
            f"### {project['title']}"
        )

        st.write(
            project["description"]
        )


        st.subheader("🔌 MCP Tools Used")

        st.code(
            """
generate_learning_path()
get_learning_resources()
suggest_project()
"""
        )


    except Exception as e:

        st.error(
            f"Something went wrong: {e}"
        )

        st.info(
            "Please check that app.py, mcp_server.py "
            "and requirements.txt are updated."
        )
