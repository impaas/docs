from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
from flask_uploads import UploadSet, configure_uploads, ALL
from flask_wtf import FlaskForm
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret-key"
app.config["UPLOADED_FILES_DEST"] = "/uploads"
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25MB

files = UploadSet("files", ALL)
configure_uploads(app, files)


class UploadForm(FlaskForm):
    submit = SubmitField("Upload")


@app.route("/", methods=["GET", "POST"])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOADED_FILES_DEST"], filename))
        return redirect(url_for("upload"))
    file_list = os.listdir(app.config["UPLOADED_FILES_DEST"])
    return render_template("upload.html", form=form, file_list=file_list)


@app.route("/files/<filename>")
def files(filename):
    return send_from_directory(app.config["UPLOADED_FILES_DEST"], filename)


@app.route("/delete/<filename>")
def delete(filename):
    os.remove(os.path.join(app.config["UPLOADED_FILES_DEST"], filename))
    return redirect(url_for("upload"))


@app.route("/rename/<filename>", methods=["POST"])
def rename(filename):
    new_name = secure_filename(request.form["new_name"])
    os.rename(
        os.path.join(app.config["UPLOADED_FILES_DEST"], filename),
        os.path.join(app.config["UPLOADED_FILES_DEST"], new_name),
    )
    return redirect(url_for("upload"))


if __name__ == "__main__":
    app.run(debug=True, port=os.environ.get("PORT", 5000), host="0.0.0.0")
