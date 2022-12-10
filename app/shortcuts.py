from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings


settings = get_settings()
templates = Jinja2Templates(directory=str(settings.templates_dir))


def render(request, template_name, context, status_code: int = 200):
    context = context.copy()
    context.update({"request": request})

    template = templates.get_template(template_name)
    html = template.render(context)

    response = HTMLResponse(html, status_code=status_code)
    return response
    # return templates.TemplateResponse(template_name, context, status_code=status_code)
