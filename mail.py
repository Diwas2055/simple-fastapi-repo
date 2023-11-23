import os
from fastapi import logger
from fastapi.templating import Jinja2Templates


async def send_email(
    template_name,
    data_obj,
):
    templates = Jinja2Templates(directory="template")
    try:
        if "PYTEST_CURRENT_TEST" in os.environ:
            # Skip sending email during pytest run
            return {"message": "Email not sent during testing."}
        template = templates.get_template(template_name)
        html_body = template.render(data_obj)
        print(html_body)
    except Exception as e:
        print(e)
        return False
