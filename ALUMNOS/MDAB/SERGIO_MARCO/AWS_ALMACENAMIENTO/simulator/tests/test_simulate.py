import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_NAME", "test")
os.environ.setdefault("DB_USER", "test")
os.environ.setdefault("DB_PASSWORD", "test")

from simulate import distance, interpolate_step, STEP, MIN_DIST

def test_distance_same_point():
    assert distance(40.0, -3.0, 40.0, -3.0) == 0.0

def test_distance_pythagorean():
    assert abs(distance(0, 0, 3, 4) - 5.0) < 1e-9

def test_interpolate_moves_toward_destination():
    new_lat, new_lng = interpolate_step(40.0, -3.0, 41.0, -2.0)
    assert new_lat > 40.0
    assert new_lng > -3.0

def test_interpolate_step_size():
    new_lat, new_lng = interpolate_step(40.0, 0.0, 41.0, 0.0)
    assert abs(new_lat - (40.0 + 1.0 * STEP)) < 1e-9

def test_arrived_condition():
    assert distance(41.0, 2.0, 41.001, 2.001) < MIN_DIST
