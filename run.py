# -*- coding: utf-8 -*-
import jinja2
from app import create_app

app = create_app()
app.jinja_env.add_extension('jinja2.ext.i18n')
app.jinja_env.install_null_translations(newstyle=True)
if __name__ == '__main__':
    app.run(debug=True)
