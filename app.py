from flask import Flask, send_from_directory, abort, send_file
import os
import zipfile
import io

app = Flask(__name__)
FILE_FOLDER = os.path.join(os.path.dirname(__file__), 'files')

@app.route('/<int:file_id>')
def serve_file(file_id):
    if file_id in range(1, 5):  # Serve .mat files
        filename = f"file{file_id}.txt"
        filepath = os.path.join(FILE_FOLDER, filename)
        if os.path.exists(filepath):
            return send_from_directory(FILE_FOLDER, filename, as_attachment=True)
        else:
            abort(404, description=f"{filename} not found.")

    elif file_id == 5:  # Serve .m and .slx files as a zip
        m_file = os.path.join(FILE_FOLDER, 'file5.txt')
        slx_file = os.path.join(FILE_FOLDER, 'file5.slx')

        if os.path.exists(m_file) and os.path.exists(slx_file):
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w') as zf:
                zf.write(m_file, arcname='file5.m')
                zf.write(slx_file, arcname='file5.slx')
            memory_file.seek(0)
            return send_file(memory_file, download_name='file5_bundle.zip', as_attachment=True)
        else:
            abort(404, description="Required files for /5 not found.")

    else:
        abort(404, description="Invalid endpoint.")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
