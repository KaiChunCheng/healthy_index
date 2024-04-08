from flask import Flask, request, jsonify

app = Flask(__name__)

raw_data = {} 
test_data = {'tool_list': [{'project_id': '123', 'tool_id': 'CHS', 'chamber': '0311', 'data_time': '2024-04-01 11:48:36', 'data': {'datetime': ['2024-04-01 11:47:00'], 'column_names': ['Unbalance', 'Bent_Shaft', 'Misalignment', 'Looseness', 'Oil_Whirl', 'Oil_Whip', 'Bearing_Faults_Inner_Race', 'Bearing_Faults_Outer_Race', 'Bearing_Faults_Roller', 'Air_Gap_Eccentricity', 'Broken_Rotor_Bar', 'Phasing_Fault', 'Gear_Eccentricity', 'Gear_Misalignment', 'Broken_Gear_Tooth', 'Gear_Tooth_Wear', 'Gear_Bent_Shaft', 'Confidence_Value', 'DryPumpCV', 'SpindleEnergy', 'BearingEnergy', 'GearEnergy', 'LowBandEnergy', 'Diagnosis_Spindle_Unbalance', 'Diagnosis_Spindle_Bending', 'Diagnosis_Spindle_Misalignment', 'Diagnosis_Spindle_Loose', 'Sensor_Temperature', 'sensor_id'], 'value': [[-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, 0.0033774153557142484, 0.0015449113250335133, 0.005538649518022771, 0.0014992750022366477, 0.0035943408797534503, 0.001754005638927465, 0.00038826622825449285, 0.00031800367276832106, 0.00029747928078365914, 25.765625, 3.0]]}}]}
fe_data = test_data

def trans_data(data):
    original_data = data['tool_list'][0]
    new_data = {
        'chamber': original_data['chamber'],
        'tool_id': original_data['tool_id'],
        'date_time': original_data['data_time'],
        'column_names': ['Unbalance', 'Bent_Shaft', 'Misalignment', 'Looseness', \
                         'Confidence_Value', 'Sensor_Temperature', 'sensor_id'],  # Including additional column names
        'values': original_data['data']['value'][0][:4] + \
            [original_data['data']['value'][0][17], original_data['data']['value'][0][27], \
             original_data['data']['value'][0][28]]   # Selecting the first 4 values
    }

    return new_data

@app.route('/')
def root_index():
    return 'Local API on.'

@app.route('/feature', methods=['POST', 'GET'])
def handle_fe_data():
    global fe_data
    if request.method == 'POST':
        fe_data = request.get_json()
        print("data coming: ", fe_data)
        return 'Data received successfully'
    elif request.method == 'GET':
        return jsonify(trans_data(fe_data))
    else:
        return 'Method not allowed'
    
@app.route('/segment', methods=['POST', 'GET'])
def handle_raw_data():
    global raw_data
    if request.method == 'POST':
        raw_data = request.get_json()
        return 'Data received successfully'
    elif request.method == 'GET':
        return jsonify(raw_data)
    else:
        return 'Method not allowed'

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8083)
    app.run()