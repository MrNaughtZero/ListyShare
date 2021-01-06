from app import app
import jinja2
 
if __name__ == "__main__":
   app.jinja_env.auto_reload = True
   app.config['TEMPLATES_AUTO_RELOAD'] = True
   app.run(debug=True)