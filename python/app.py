
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from analysis import run_fourier_analysis
from gwosc import list_wave_files


app = Flask(
    __name__,
    static_folder=".",
    static_url_path=""
)

CORS(app)

#frontend

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

#list file

@app.route("/api/files")
def files():

    wave_files = list_wave_files()

    return jsonify({
        "files": wave_files
    })
#analyse file

@app.route("/api/analyze")
def analyze():

    filename = request.args.get("file")

    if not filename:

        return jsonify({
            "error":
            "No gravitational-wave file was selected."
        }), 400


    try:

        low_cut = float(
            request.args.get("low", 25)
        )

        high_cut = float(
            request.args.get("high", 220)
        )

    except ValueError:

        return jsonify({
            "error":
            "Cutoff frequencies must be numeric."
        }), 400


    if low_cut >= high_cut:

        return jsonify({
            "error":
            "Low cutoff must be lower than high cutoff."
        }), 400


    try:

        result = run_fourier_analysis(
            filename=filename,
            low_cut=low_cut,
            high_cut=high_cut
        )

        return jsonify(result)


    except FileNotFoundError as error:

        return jsonify({
            "error": str(error)
        }), 404


    except Exception as error:

        print(error)

        return jsonify({
            "error":
            "An error occurred during gravitational-wave analysis."
        }), 500
#Run app

if __name__ == "__main__":

    app.run(
        debug=True,
        port=4092
    )
