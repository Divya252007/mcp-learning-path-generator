import asyncio
import json
import streamlit as st

from mcp import Client
from mcp_server import mcp


st.set_page_config(
    page_title="MCP Learning Path Generator",
    page_icon="🧠",
    layout="centered"
)


async def call_mcp(tool_name, arguments):

    async with Client(mcp) as client:

        result = await client.call_tool(
            tool_name,
            arguments
        )

        # MCP tool error
        if result.is_error:

            error_text = "MCP tool failed."

            if result.content:
                first = result.content[0]

                if hasattr(first, "text"):
                    error_text = first.text

            raise RuntimeError(error_text)

        # Preferred structured result
        if result.structured_content is not None:

            data = result.structured_content

            # Primitive results are wrapped by MCP as {"result": ...}
            if (
                isinstance(data, dict)
                and set(data.keys()) == {"result"}
            ):
                return data["result"]

            return data

        # Fallback: read JSON from text content
        if result.content:

            first = result.content[0]

            if hasattr(first, "text"):

                try:
                    return json.loads(first.text)
                except json.JSONDecodeError:
                    return first.text

        raise RuntimeError(
            "MCP returned an empty result."
        )


st.title("🧠 MCP-Powered AI Learning Path Generator")

st.write(
    "Generate a personalized learning roadmap "
    "using Model Context Protocol (MCP)."
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

        with st.spinner(
            "🔌 Calling MCP tools..."
        ):

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


        # -------------------------
        # LEARNING GOAL
        # -------------------------

        st.subheader("🎯 Learning Goal")

        st.write(
            plan["goal"]
        )


        # -------------------------
        # ROADMAP
        # -------------------------

        st.subheader("📅 Day-by-Day Roadmap")

        for item in plan["roadmap"]:

            with st.expander(
                f"Day {item['day']} — {item['topic']}"
            ):

                st.write(
                    item["task"]
                )


        # -------------------------
        # RESOURCES
        # -------------------------

        st.subheader("📚 Learning Resources")

        for resource in resources:

            st.markdown(
                f"### 📖 {resource['title']}"
            )

            st.write(
                resource["purpose"]
            )

            st.link_button(
                "Open Resource",
                resource["url"]
            )


        # -------------------------
        # PROJECT
        # -------------------------

        st.subheader("💡 Suggested Mini Project")

        st.markdown(
            f"### {project['title']}"
        )

        st.write(
            project["description"]
        )


        # -------------------------
        # MCP TOOLS
        # -------------------------

        st.subheader("🔌 MCP Tools Used")

        st.code(
            """
MCP Server
│
├── generate_learning_path()
├── get_learning_resources()
└── suggest_project()
            """
        )


    except Exception as e:

        st.error(
            f"❌ MCP Error: {e}"
        )

        st.info(
            "The application is running, but an MCP "
            "tool returned an error. The detailed message "
            "above can be used to diagnose the tool."
        )
