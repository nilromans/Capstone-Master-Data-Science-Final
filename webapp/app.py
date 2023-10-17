from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import os
import pandas as pd
import xgboost as xgb
import pickle

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 3.5 * 1024 * 1024 * 1024  # 3.5 GB
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ruta donde se guardarán los archivos CSV

def hacer_prediccion(archivo_csv_path):
    app.logger.info('Haciendo prediccion')
    df = pd.read_csv(archivo_csv_path, index_col='ID')
    modelo = pickle.load(open('model.pkl', "rb"))
    preds = modelo.predict(df)
    app.logger.info('Predicción hecha')

    return list(preds), preds.sum()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/ventas')
def ventas():
    return render_template('ventas.html')

@app.route('/productos')
def products():
    return render_template('productos.html')

@app.route('/input')
def input():
    return render_template('input.html')

@app.route('/prediccion', methods=['POST'])
def prediccion():
    if request.method == 'POST' and 'file' in request.files:
        archivo = request.files['file']
        if archivo.filename.endswith('.csv'):
            archivo_csv_path = os.path.join(app.config['UPLOAD_FOLDER'], archivo.filename)
            archivo.save(archivo_csv_path)

            pred, pred_sum = hacer_prediccion(archivo_csv_path)

            # Guardar prediction como un archivo CSV
            df_prediction = pd.DataFrame({'prediction': pred})
            df_prediction.to_csv('prediction.csv', index=False)

            # Preparar la respuesta JSON
            response_data = {'prediction_sum': float(pred_sum)}
            return jsonify(response_data)

    return redirect(url_for('resultado'))

@app.route('/resultado')
def resultado():
    prediction_sum = request.args.get('prediction_sum')

    return render_template('resultado.html', prediction_sum=prediction_sum)    

@app.route('/download', methods=['GET'])
def descargar_prediccion():
    return send_file('prediction.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)







