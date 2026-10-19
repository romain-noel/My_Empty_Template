import os
import shutil

REMOVE_PATHS = [
    {% if cookiecutter.type == "article" %} 'parts/avancement.tex', {% endif %}
    {% if cookiecutter.type == "article" %} 'presentation.tex', {% endif %}
    {% if cookiecutter.type == "article" %} 'report.tex', {% endif %}
    # {% if cookiecutter.type == "logbook" %} 'main.tex', {% endif %}
    {% if cookiecutter.type == "logbook" %} 'covers_rebuttals', {% endif %}
]

for path in REMOVE_PATHS:
    path = path.strip()
    if path and os.path.exists(path):
        if os.path.isdir(path):
            # os.rmdir(path)
            shutil.rmtree(path)
        else:
            os.unlink(path)
    print("in post gen hooks, remove:", path, ".")
# end for