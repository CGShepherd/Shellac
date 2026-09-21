from simulation.scripts.shellac_spice import parse_measurements

def test_ltspice26_expression_measurements_and_ignore_settings():
    log="tnom = 27\ntemp = 27\nvout_avg: AVG(V(OUT) )=5.00552415848 FROM 0.02 TO 0.03\nvout_min: MIN(V(OUT) )=5.00552415848 FROM 0.02 TO 0.03\nvout_max: MAX(V(OUT) )=5.00552415848 FROM 0.02 TO 0.03\n"
    assert parse_measurements(log)=={"VOUT_AVG":5.00552415848,"VOUT_MIN":5.00552415848,"VOUT_MAX":5.00552415848}

def test_direct_colon_measurement():
    assert parse_measurements("gain: -1.25e-3\n")=={"GAIN":-1.25e-3}

def test_known_ltspice_numeric_settings_are_not_measurements():
    assert parse_measurements("tnom = 27\ntemp = 27\n")=={}

def test_scalar_equals_measurements_are_accepted():
    assert parse_measurements("CORR_MATRIX_EQUAL = 1.0\nRUN00_VMINUS18 = -1.8e1\n")=={
        "CORR_MATRIX_EQUAL":1.0,
        "RUN00_VMINUS18":-18.0,
    }

def test_nonnumeric_equals_settings_are_ignored():
    assert parse_measurements("solver = Normal\n")=={}
