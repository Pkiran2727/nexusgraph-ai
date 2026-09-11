import sys
import os
from pathlib import Path
import gradio as gr

# Ensure backend directory is in Python module search path
root_dir = Path(__file__).resolve().parent
backend_dir = root_dir / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from main import app as fastapi_app

# ZeroGPU Compatibility Check
try:
    import spaces
    @spaces.GPU(duration=1)
    def zero_gpu_init():
        return True
except Exception:
    pass


# Read frontend files
frontend_dir = root_dir / "frontend"
index_html_path = frontend_dir / "index.html"
css_path = frontend_dir / "css" / "styles.css"
js_app_path = frontend_dir / "js" / "app.js"
js_graph_path = frontend_dir / "js" / "graph_viz.js"
js_role_path = frontend_dir / "js" / "role_analyzer.js"

html_content = index_html_path.read_text(encoding="utf-8")
css_content = css_path.read_text(encoding="utf-8")
js_app_content = js_app_path.read_text(encoding="utf-8")
js_graph_content = js_graph_path.read_text(encoding="utf-8")
js_role_content = js_role_path.read_text(encoding="utf-8")

# Embed CSS and JS directly for Gradio static serving compatibility
inlined_html = html_content.replace(
    '<link rel="stylesheet" href="/static/css/styles.css">',
    f'<style>\n{css_content}\n</style>'
).replace(
    '<script src="/static/js/graph_viz.js"></script>',
    f'<script>\n{js_graph_content}\n</script>'
).replace(
    '<script src="/static/js/role_analyzer.js"></script>',
    f'<script>\n{js_role_content}\n</script>'
).replace(
    '<script src="/static/js/app.js"></script>',
    f'<script>\n{js_app_content}\n</script>'
)

with gr.Blocks(title="NexusGraph AI — Intelligence Engine") as demo:
    gr.HTML(inlined_html)

app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(fastapi_app, host="0.0.0.0", port=port)


