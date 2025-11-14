import functions_framework
from agent_8_storyboard_bridge import app

@functions_framework.http
def handler(request):
    return app(request)