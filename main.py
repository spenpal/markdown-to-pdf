import base64
import os
import subprocess
import tempfile
from pathlib import Path

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Markdown to PDF Converter",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Force light theme for better visual consistency
st.markdown(
    """
<style>
    /* Force light theme */
    .stApp {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    
    /* Override dark theme elements */
    .main .block-container {
        background-color: #ffffff !important;
    }
    
    /* Fix code blocks and expanders */
    .stCodeBlock, .stCodeBlock > div, .stCodeBlock pre {
        background-color: #f8f9fa !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
        color: #212529 !important;
    }
    
    .stCodeBlock code, .stCodeBlock pre code {
        color: #212529 !important;
        background-color: #f8f9fa !important;
    }
    
    /* Fix expander content */
    .streamlit-expanderContent, .streamlit-expanderContent div {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e9ecef !important;
        border-radius: 8px !important;
    }
    
    /* Ensure text is readable */
    p, li, span, div, .stMarkdown, .stText {
        color: #262730 !important;
    }
    
    /* Keep certain elements with intended colors */
    .feature-box h4,
    h3,
    .main-header {
        color: #667eea !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Custom CSS for beautiful styling with dark theme support
st.markdown(
    """
<style>
    /* Main header with better dark theme support */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        /* Fallback for browsers that don't support background-clip */
        color: #667eea;
    }
    
    /* Better dark theme support for header */
    [data-theme="dark"] .main-header {
        background: linear-gradient(90deg, #8fa4f3 0%, #9d7cc4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        color: #8fa4f3;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: var(--text-color);
        text-align: center;
        margin-bottom: 2rem;
        line-height: 1.6;
        opacity: 0.8;
    }
    
    /* Enhanced feature boxes for dark theme */
    .feature-box {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        background: rgba(102, 126, 234, 0.15);
        border-color: rgba(102, 126, 234, 0.3);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    }
    
    .feature-box h4 {
        color: #667eea;
        margin-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .feature-box p {
        margin: 0;
        opacity: 0.9;
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #7c8df0 0%, #8a5db8 100%);
    }
    
    /* Enhanced file uploader - fix dark background */
    .stFileUploader, .stFileUploader > div, .stFileUploader > div > div,
    [data-testid="stFileUploader"], [data-testid="stFileUploader"] > div,
    [data-testid="stFileUploader"] > div > div {
        background-color: #ffffff !important;
        border: 2px dashed rgba(102, 126, 234, 0.3) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        color: #262730 !important;
    }
    
    .stFileUploader label, .stFileUploader span, .stFileUploader p,
    [data-testid="stFileUploader"] label, [data-testid="stFileUploader"] span,
    [data-testid="stFileUploader"] p {
        color: #262730 !important;
        background-color: transparent !important;
    }
    
    /* Fix file uploader button */
    .stFileUploader button, [data-testid="stFileUploader"] button {
        background-color: #667eea !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.5rem 1rem !important;
    }
    
    .stFileUploader:hover > div > div, 
    [data-testid="stFileUploader"]:hover > div > div {
        background-color: rgba(102, 126, 234, 0.05) !important;
        border-color: rgba(102, 126, 234, 0.5) !important;
    }
    
    /* Additional code block fixes */
    pre, code {
        background-color: #f8f9fa !important;
        color: #212529 !important;
        border: 1px solid #e9ecef !important;
        border-radius: 4px !important;
        padding: 0.2em 0.4em !important;
    }
    
    /* Fix any remaining dark backgrounds */
    .element-container, .stMarkdown, .stText {
        background-color: transparent !important;
        color: #262730 !important;
    }
    
    /* Success and error messages */
    .success-message {
        background: rgba(40, 167, 69, 0.1);
        color: #28a745;
        border: 1px solid rgba(40, 167, 69, 0.3);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    
    .error-message {
        background: rgba(220, 53, 69, 0.1);
        color: #dc3545;
        border: 1px solid rgba(220, 53, 69, 0.3);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #dc3545;
        margin: 1rem 0;
    }
    
    /* Enhanced info messages */
    .stInfo {
        background: rgba(102, 126, 234, 0.1);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 10px;
    }
    
    /* Better spacing and layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Section headers */
    h3 {
        color: #667eea;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    /* Dividers */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.3), transparent);
    }
    
    /* Comprehensive dark theme override */
    .stApp, .stApp > div, .main, .block-container,
    .streamlit-container, .css-1d391kg, .css-12oz5g7,
    .css-1cpxqw2, .css-1y4p8pa, .css-18e3th9 {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    
    /* Fix Streamlit header/toolbar area */
    header, .stToolbar, [data-testid="stToolbar"],
    .stHeader, [data-testid="stHeader"],
    [data-testid="stDecoration"], .stDecoration {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
    
    /* Fix any remaining containers */
    section, .element-container, .stContainer,
    [data-testid="stVerticalBlock"], [data-testid="stHorizontalBlock"] {
        background-color: transparent !important;
        color: #262730 !important;
    }
    
    /* Force light theme on all text elements */
    * {
        color: #262730 !important;
    }
    
    /* Restore intended colors for specific elements */
    .main-header, .feature-box h4, h3, 
    .stButton > button, .success-message, .error-message {
        color: inherit !important;
    }
    
    /* Additional file uploader fixes */
    .uploadedFile, .uploadedFileName {
        background-color: #ffffff !important;
        color: #262730 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def build_docker_image():
    """Build the Docker image if it doesn't exist"""
    try:
        # Check if image exists
        result = subprocess.run(
            ["docker", "images", "-q", "md2pdf"], capture_output=True, text=True
        )
        if not result.stdout.strip():
            st.info("🔨 Building Docker image (first time only)...")
            build_result = subprocess.run(
                ["docker", "build", "-t", "md2pdf", "."],
                capture_output=True,
                text=True,
                cwd=os.getcwd(),
            )
            if build_result.returncode != 0:
                st.error(f"Failed to build Docker image: {build_result.stderr}")
                return False
            st.success("✅ Docker image built successfully!")
        return True
    except Exception as e:
        st.error(f"Error checking/building Docker image: {str(e)}")
        return False


def convert_markdown_to_pdf(markdown_content, filename):
    """Convert markdown content to PDF using Docker container"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Write markdown content to temporary file
            md_path = os.path.join(temp_dir, f"{filename}.md")
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content)

            # Run Docker container to convert
            docker_cmd = [
                "docker",
                "run",
                "--rm",
                "-v",
                f"{temp_dir}:/data",
                "md2pdf",
                f"{filename}.md",
            ]

            result = subprocess.run(docker_cmd, capture_output=True, text=True)

            if result.returncode != 0:
                return None, f"Conversion failed: {result.stderr}"

            # Read the generated PDF
            pdf_path = os.path.join(temp_dir, f"{filename}.pdf")
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    pdf_content = f.read()
                return pdf_content, None
            else:
                return None, "PDF file was not generated"

    except Exception as e:
        return None, f"Error during conversion: {str(e)}"


def display_pdf(pdf_content):
    """Display PDF in Streamlit using an iframe"""
    base64_pdf = base64.b64encode(pdf_content).decode("utf-8")
    pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" 
            width="100%" height="800" type="application/pdf">
    </iframe>
    """
    st.markdown(pdf_display, unsafe_allow_html=True)


def main():
    # Header
    st.markdown(
        '<h1 class="main-header">📄 Markdown to PDF Converter</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-header">Transform your Markdown files into beautiful PDFs with professional typography and formatting</p>',
        unsafe_allow_html=True,
    )

    # Features section
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
        <div class="feature-box">
            <h4>⚡ Lightning Fast</h4>
            <p>Powered by Tectonic engine for quick compilation</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
        <div class="feature-box">
            <h4>🎨 Beautiful Output</h4>
            <p>Eisvogel template with professional typography</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
        <div class="feature-box">
            <h4>🔧 Zero Config</h4>
            <p>Optimized defaults that just work out of the box</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # File upload section with enhanced styling
    st.markdown("### 📁 Upload Your Markdown File")

    # Create a more prominent upload area
    upload_container = st.container()
    with upload_container:
        uploaded_file = st.file_uploader(
            "Choose a Markdown file",
            type=["md", "markdown"],
            help="Upload a .md or .markdown file to convert to PDF",
            label_visibility="collapsed",
        )

        if not uploaded_file:
            st.markdown(
                """
            <div style="
                text-align: center; 
                padding: 2rem; 
                background: rgba(102, 126, 234, 0.05);
                border: 2px dashed rgba(102, 126, 234, 0.3);
                border-radius: 12px;
                margin: 1rem 0;
            ">
                <h4 style="color: #667eea; margin-bottom: 0.5rem;">📄 Drag and drop your markdown file here</h4>
                <p style="opacity: 0.7; margin: 0;">Supports .md and .markdown files</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

    if uploaded_file is not None:
        # Display file info
        st.success(
            f"✅ File uploaded: **{uploaded_file.name}** ({uploaded_file.size} bytes)"
        )

        # Read the markdown content
        markdown_content = uploaded_file.read().decode("utf-8")

        # Show markdown preview in expandable section
        with st.expander("📖 Preview Markdown Content", expanded=False):
            st.markdown(markdown_content)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Convert to PDF", use_container_width=True):
                # Ensure Docker image is built
                if not build_docker_image():
                    return

                # Show progress
                with st.spinner("Converting your markdown to PDF..."):
                    filename = Path(uploaded_file.name).stem
                    pdf_content, error = convert_markdown_to_pdf(
                        markdown_content, filename
                    )

                if error:
                    st.markdown(
                        f'<div class="error-message">❌ {error}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        '<div class="success-message">🎉 PDF generated successfully!</div>',
                        unsafe_allow_html=True,
                    )

                    # Store PDF in session state for download
                    st.session_state.pdf_content = pdf_content
                    st.session_state.pdf_filename = f"{filename}.pdf"

                    # Create download button
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_content,
                            file_name=f"{filename}.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                        )

                    st.markdown("---")
                    st.markdown("### 👀 PDF Preview")

                    # Display PDF
                    try:
                        display_pdf(pdf_content)
                    except Exception as e:
                        st.warning(f"Could not display PDF preview: {str(e)}")
                        st.info(
                            "You can still download the PDF using the button above."
                        )

    else:
        # Show example when no file is uploaded
        st.markdown(
            """
        <div style="
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
            border: 1px solid rgba(102, 126, 234, 0.2);
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            margin: 2rem 0;
        ">
            <h4 style="color: #667eea; margin-bottom: 0.5rem;">🚀 Ready to convert your markdown?</h4>
            <p style="margin: 0; opacity: 0.8;">Upload a file above to see the magic happen!</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

        with st.expander("📝 Example Markdown", expanded=False):
            example_md = """# Sample Document

## Introduction

This is a **sample markdown** document to demonstrate the conversion process.

### Features

- Beautiful typography
- Professional layout
- Code syntax highlighting
- Mathematical equations

### Code Example

```python
def hello_world():
    print("Hello, World!")
    return "Success"
```

### Math Example

The quadratic formula: $x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$

> This is a blockquote example.

That's it! Your PDF will look amazing."""

            st.code(example_md, language="markdown")


if __name__ == "__main__":
    main()
